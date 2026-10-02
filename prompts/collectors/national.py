"""p044-p063: national teams, tournaments, squads.

Historical-state policy (applied consistently across the country prompts):
  * West Germany is merged into Germany (same enwiki team article).
  * Zaire / Congo-Kinshasa -> DR Congo, United Arab Republic -> Egypt, Dutch East Indies -> Indonesia
    (Wikipedia keeps a single team article for each, so they cannot be separate answers).
  * Soviet Union, Yugoslavia, Czechoslovakia, Serbia and Montenegro (incl. FR Yugoslavia) and the CIS
    have their own team articles and are separate answers; their records are NOT credited to
    Russia / Serbia / Czech Republic / Slovakia (Wikipedia's tables do credit successors, we undo that).
"""
import re

from bs4 import BeautifulSoup

from ballion.registry import prompt
from ballion.tables import _link_title, rows, wikitables
from ballion.wiki import api, page_html

def _hdr(t):
    return next(rows(t))[0]


def _table(title, starts):
    """First wikitable on `title` whose header row starts with the given column names."""
    return next(t for t in wikitables(title) if _hdr(t)[:len(starts)] == starts)


def _clean(s):
    return re.sub(r"\s*\[.*?\]|\s+\d+$", "", s).strip()


def _apps(n):
    return f"{n} app" + ("" if int(n) == 1 else "s")


def _split_tables(title):
    """'Team (yyyy–yyyy)' predecessor/successor breakdown tables -> {link: [(label, parts, first_year)]}."""
    out = {}
    for t in wikitables(title):
        h = _hdr(t)
        if h[:2] not in (["Team", "Part"], ["Team", "Part."]):
            continue
        for tx, ln in list(rows(t))[1:]:
            m = re.match(r"(.+?)\s*\((\d{4})", tx[0])
            if m and ln[0]:
                out.setdefault(ln[0][-1], []).append((m.group(1), int(tx[1]), int(m.group(2))))
    return out


# --------------------------------------------------------------------------------------------- p044
WC_APPS = "National team appearances in the FIFA World Cup"


@prompt("p044", "Name a country that has played at a men's FIFA World Cup finals tournament (1930–2026)",
        f"en:{WC_APPS} — appearances table + predecessor/successor breakdown tables")
def wc_teams():
    split = _split_tables(WC_APPS)
    out = {}
    for tx, ln in list(rows(_table(WC_APPS, ["Team", "Appearances"])))[1:]:
        if not ln[0] or not tx[1].isdigit():
            continue
        out[ln[0][-1]] = {"answer": tx[0], "enwiki": ln[0][-1],
                          "detail": f"{_apps(tx[1])} (debut {tx[4]}, last {tx[5]})"}
    for link, parts in split.items():  # replace successor-inclusive counts with own-identity counts
        n = sum(p[1] for p in parts)
        first = min(p[2] for p in parts)
        name = out[link]["answer"] if link in out else parts[-1][0]
        last = re.search(r"last \d{4}", out[link]["detail"]).group(0) if link in out else ""
        names = sorted({p[0] for p in parts} - {name})
        extra = f"; incl. as {', '.join(names)}" if names else ""
        out[link] = {"answer": name, "enwiki": link,
                     "detail": f"{_apps(n)} (debut {first}{', ' + last if last else ''}){extra}"}
    return list(out.values())


# --------------------------------------------------------------------------------------------- p045
@prompt("p045", "Name a country that has hosted or co-hosted a men's FIFA World Cup (1930–2026; future hosts excluded)",
        "en:List of FIFA World Cup hosts — results of host nations table")
def wc_hosts():
    t = _table("List of FIFA World Cup hosts", ["Year", "Team", "Result"])
    out = {}
    for tx, ln in list(rows(t))[1:]:
        if not tx[0].isdigit() or int(tx[0]) > 2026 or not ln[1]:
            continue
        name = "Germany" if tx[1] == "West Germany" else tx[1]
        rec = out.setdefault(ln[1][-1], {"answer": name, "enwiki": ln[1][-1], "detail": []})
        rec["detail"].append(tx[0] + (" (as West Germany)" if tx[1] == "West Germany" else ""))
    for r in out.values():
        r["detail"] = "hosted " + ", ".join(r["detail"])
    return list(out.values())


# --------------------------------------------------------------------------------------------- p046
EURO = "UEFA European Championship records and statistics"
EURO_SUCC = {  # successor team -> predecessors whose appearances Wikipedia folds into it
    "Russia national football team": ["Soviet Union national football team", "CIS national football team"],
    "Czech Republic national football team": ["Czechoslovakia national football team"],
    "Slovakia national football team": ["Czechoslovakia national football team"],
    "Serbia national football team": ["Yugoslavia national football team",
                                      "Serbia and Montenegro national football team"],
}


@prompt("p046", "Name a country that has played at a men's UEFA European Championship finals tournament (1960–2024)",
        f"en:{EURO} — appearances table + predecessor tables")
def euro_teams():
    split = _split_tables(EURO)
    out = {}
    for tx, ln in list(rows(_table(EURO, ["Team", "Appearances"])))[1:]:
        if ln[0] and tx[1].isdigit():
            out[ln[0][-1]] = {"answer": tx[0], "enwiki": ln[0][-1], "n": int(tx[1]),
                              "detail": f"{_apps(tx[1])} (debut {tx[2]}, last {tx[3]})"}
    for link, preds in EURO_SUCC.items():
        own = out[link]["n"] - sum(p[1] for pr in preds for p in split.get(pr, []))
        out[link]["detail"] = f"{_apps(own)} as {out[link]['answer']} (last {out[link]['detail'].split('last ')[1]}"
    for link, parts in split.items():
        if link == "Germany national football team":
            out[link]["detail"] += "; incl. as West Germany"
            continue
        out[link] = {"answer": re.sub(r"^FR Yugoslavia/", "", parts[0][0]), "enwiki": link,
                     "detail": f"{_apps(sum(p[1] for p in parts))} (debut {parts[0][2]})"}
    return [{k: r[k] for k in ("answer", "enwiki", "detail")} for r in out.values()]


# --------------------------------------------------------------------------------------------- p047
AFCON = "Africa Cup of Nations records and statistics"


@prompt("p047", "Name a country that has played at an Africa Cup of Nations finals tournament (1957–2025)",
        f"en:{AFCON} — all-time ranking table")
def afcon_teams():
    t = _table(AFCON, ["Rank", "Team", "Part"])
    out = []
    for tx, ln in list(rows(t))[1:]:
        if ln[1] and tx[2].isdigit():
            d = _apps(tx[2])
            if tx[1] == "DR Congo":
                d += " (incl. as Zaire / Congo-Kinshasa)"
            if tx[1] == "Egypt":
                d += " (incl. as United Arab Republic)"
            out.append({"answer": tx[1], "enwiki": ln[1][-1], "detail": d})
    return out


# --------------------------------------------------------------------------------------------- p048
TOP4_PRED = {"Czech Republic": ("Czechoslovakia", "Czechoslovakia national football team"),
             "Slovakia": ("Czechoslovakia", "Czechoslovakia national football team"),
             "Serbia": ("Yugoslavia", "Yugoslavia national football team"),
             "Russia": ("Soviet Union", "Soviet Union national football team")}


@prompt("p048", "Name a country that has finished in the top four (reached the semi-finals) of a men's FIFA World Cup",
        "en:FIFA World Cup records and statistics — teams reaching the top four (1950 final-group top four included)")
def wc_top4():
    t = _table("FIFA World Cup records and statistics", ["Team", "Titles", "Runners-up", "Third place"])
    out = {}
    labels = ["W", "RU", "3rd", "4th"]
    for tx, ln in list(rows(t))[1:]:
        if not ln[0]:
            continue
        name = re.sub(r"\s+\d+$", "", tx[0])
        link = ln[0][-1]
        if name in TOP4_PRED:  # Wikipedia credits the successor; credit the historical team instead
            name, link = TOP4_PRED[name]
        parts = []
        for lab, cell in zip(labels, tx[1:5]):
            yrs = re.findall(r"\d{4}", cell)
            if yrs:
                parts.append(f"{lab} {', '.join(yrs)}")
        out[link] = {"answer": name, "enwiki": link, "detail": "; ".join(parts)}
    return list(out.values())


# --------------------------------------------------------------------------------------------- p049
def _winners(title, starts, col, year_col=0):
    t = _table(title, starts)
    for tx, ln in list(rows(t))[1:]:
        m = re.match(r"\d{4}", tx[year_col])
        if m and ln[col] and "national" in ln[col][-1] and "team" in ln[col][-1]:
            yield ln[col][-1], m.group(0), re.sub(r"\s*\(\d+\)$", "", tx[col])


@prompt("p049", "Name a country that has won a men's continental championship (European Championship, Copa América, "
        "Africa Cup of Nations, AFC Asian Cup, CONCACAF Championship/Gold Cup, OFC Nations Cup)",
        "en: winners tables of UEFA Euro / Copa América / AFCON / Asian Cup records articles, "
        "CONCACAF Championship (1963–89), CONCACAF Gold Cup (1991–), OFC Men's Nations Cup")
def continental_winners():
    srcs = [
        ("UEFA European Championship records and statistics", ["Year", "Hosts", "Champions"], 2, "Euro", 0),
        ("Copa América records and statistics", ["Year", "Hosts", "Champions"], 2, "Copa América", 0),
        ("Africa Cup of Nations records and statistics", ["Year", "Hosts", "Champions (titles)"], 2, "AFCON", 0),
        ("AFC Asian Cup records and statistics", ["Year", "Host(s)", "Winners"], 2, "Asian Cup", 0),
        ("CONCACAF Championship", ["Ed.", "Year", "Hosts", "Champions"], 3, "CONCACAF Ch.", 1),
        ("CONCACAF Gold Cup", ["Ed.", "Year", "Hosts"], 4, "Gold Cup", 1),
        ("OFC Men's Nations Cup", ["Ed.", "Year", "Host"], 4, "OFC Nations Cup", 1),
    ]
    out = {}
    for title, starts, col, comp, yc in srcs:
        for link, year, name in _winners(title, starts, col, yc):
            c = comp
            if name in ("West Germany",):
                name = "Germany"
            if name in ("United Arab Republic",):
                name = "Egypt"
            if name.startswith("Congo-Kinshasa") or name == "Zaire":
                name = "DR Congo"
            rec = out.setdefault(link, {"answer": name, "enwiki": link, "d": {}})
            rec["d"].setdefault(c, []).append(year)
    return [{"answer": r["answer"], "enwiki": r["enwiki"],
             "detail": "; ".join(f"{c} {', '.join(dict.fromkeys(y))}" for c, y in r["d"].items())}
            for r in out.values()]


# --------------------------------------------------------------------------------------------- p050
WC_YEARS = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994,
            1998, 2002, 2006, 2010, 2014, 2018, 2022, 2026]


def _wc_winning_players():
    """{player article: (display, team, [years])} from List of FIFA World Cup winning players."""
    t = wikitables("List of FIFA World Cup winning players")[0]
    out = {}
    for tx, ln in list(rows(t))[2:]:
        if ln[0]:
            out[ln[0][-1]] = (tx[0], tx[1], re.findall(r"\d{4}", tx[3]))
    return out


@prompt("p050", "Name a player who captained a men's World Cup-winning team in the final (1930–2026)",
        "en:'YYYY FIFA World Cup final' articles (1950: decisive match) — (c) in line-ups, matched to the winners list")
def wc_captains():
    winners = _wc_winning_players()
    out = {}
    for y in WC_YEARS:
        title = f"{y} FIFA World Cup final" if y != 1950 else "Uruguay v Brazil (1950 FIFA World Cup)"
        soup = BeautifulSoup(page_html(title), "lxml")
        for tr in soup.find_all("tr"):
            txt = tr.get_text(" ", strip=True)
            if not re.search(r"\(\s*c\s*\)", txt) or len(txt) > 80:
                continue
            ls = [x for x in (_link_title(a) for a in tr.find_all("a")) if x and not x.startswith("Captain")]
            if ls and ls[0] in winners and str(y) in winners[ls[0]][2]:
                rec = out.setdefault(ls[0], {"answer": winners[ls[0]][0], "enwiki": ls[0], "y": []})
                if y not in rec["y"]:
                    rec["y"].append(y)
    team = {p: v[1] for p, v in winners.items()}
    return [{"answer": r["answer"], "enwiki": r["enwiki"],
             "detail": f"{team[r['enwiki']]} captain in final {', '.join(map(str, r['y']))}"} for r in out.values()]


# --------------------------------------------------------------------------------------------- p051
def _category(cat):
    out, cont = [], {}
    while True:
        d = api(action="query", list="categorymembers", cmtitle=cat, cmlimit="max", cmnamespace=0, **cont)
        out += [m["title"] for m in d["query"]["categorymembers"]]
        if "continue" not in d:
            return out
        cont = d["continue"]


UCL_FINALS = "List of European Cup and UEFA Champions League finals"


def _ucl_final_winners():
    """{player article: [years]} for the winning side's line-up (XI + substitutes) in every final article."""
    t = _table(UCL_FINALS, ["Season", "Country", "Winners"])
    out = {}
    for tx, ln in list(rows(t))[1:]:
        if not ln[3] or not re.match(r"\d{4}", tx[0]):
            continue
        year = str(int(tx[0][:4]) + 1)
        soup = BeautifulSoup(page_html(ln[3][0]), "lxml")
        ev = [e for e in soup.select("table.fevent") if e.select_one(".fhome")]
        home = ev[0].select_one(".fhome").get_text(" ", strip=True)
        side = 0 if home == tx[2] else 1
        for outer in soup.find_all("table"):
            first = outer.find("tr")
            if not first or not re.match(r"^GK\b", first.get_text(" ", strip=True)):
                continue
            inner = outer.find_all("table")
            if len(inner) < 2:
                continue
            for tr in inner[side].find_all("tr"):
                cells = tr.find_all(["td", "th"])
                if not cells or not re.fullmatch(r"[A-Z]{2,3}", cells[0].get_text(strip=True)):
                    continue
                ls = [x for x in (_link_title(a) for a in tr.find_all("a") if not a.find_parent(class_="flagicon"))
                      if x and not x.startswith("Captain")]
                if ls:
                    out.setdefault(ls[0], [])
                    if year not in out[ls[0]]:
                        out[ls[0]].append(year)
    return out


@prompt("p051", "Name a player who has won both the men's FIFA World Cup and the European Cup / UEFA Champions League "
        "(as a squad member)",
        "en:List of FIFA World Cup winning players ∩ (Category:UEFA Champions League–winning players ∪ winning "
        "line-ups in every European Cup/UCL final article)")
def wc_and_ucl():
    winners = _wc_winning_players()
    ucl = set(_category("Category:UEFA Champions League–winning players"))
    finals = _ucl_final_winners()
    out = []
    for p, v in winners.items():
        if p in ucl or p in finals:
            ec = f"; EC/UCL final {', '.join(finals[p])}" if p in finals else "; EC/UCL squad (category)"
            out.append({"answer": v[0], "enwiki": p, "detail": f"WC {', '.join(v[2])} ({v[1]}){ec}"})
    return out


# --------------------------------------------------------------------------------------- p052-p058
def squad(title, team, note):
    """Players of one team section in a 'YYYY ... squads' article."""
    soup = BeautifulSoup(page_html(title), "lxml")
    for sup in soup.select("sup.reference"):
        sup.decompose()
    h = next(h for h in soup.find_all(["h3", "h4"]) if h.get_text(strip=True) == team)
    t = (h.parent if "mw-heading" in " ".join(h.parent.get("class", [])) else h).find_next("table")
    rs = list(rows(t))
    hdr = [c.split(" [")[0] for c in rs[0][0]]
    pi = next(i for i, c in enumerate(hdr) if c.startswith("Player"))
    qi = next(i for i, c in enumerate(hdr) if c.startswith("Pos"))
    ci = next((i for i, c in enumerate(hdr) if c.startswith("Club")), None)
    out = []
    for tx, ln in rs[1:]:
        ps = [x for x in ln[pi] if not x.startswith("Captain")]
        if not ps:
            continue
        name = re.sub(r"\s*\(\s*(c|captain|vc)\s*\)", "", tx[pi]).strip()
        pos = re.sub(r"^\d\s*", "", tx[qi])
        club = tx[ci] if ci is not None else ""
        out.append({"answer": name, "enwiki": ps[-1],
                    "detail": f"#{tx[0]} {pos}, {club}" + (f" — {note}" if note else "")})
    return out


SQUADS = [
    ("p052", "Brazil's 2002 FIFA World Cup-winning squad", "2002 FIFA World Cup squads", "Brazil"),
    ("p053", "Spain's 2010 FIFA World Cup-winning squad", "2010 FIFA World Cup squads", "Spain"),
    ("p054", "Germany's 2014 FIFA World Cup-winning squad", "2014 FIFA World Cup squads", "Germany"),
    ("p055", "France's 2018 FIFA World Cup-winning squad", "2018 FIFA World Cup squads", "France"),
    ("p056", "Argentina's 2022 FIFA World Cup-winning squad", "2022 FIFA World Cup squads", "Argentina"),
    ("p057", "Greece's UEFA Euro 2004-winning squad", "UEFA Euro 2004 squads", "Greece"),
    ("p058", "Italy's 2006 FIFA World Cup-winning squad", "2006 FIFA World Cup squads", "Italy"),
]
for _pid, _what, _title, _team in SQUADS:
    prompt(_pid, f"Name a player in {_what} (full registered tournament squad)",
           f"en:{_title} — {_team} section")(lambda t=_title, tm=_team: squad(t, tm, ""))


# --------------------------------------------------------------------------------------------- p059
def _managers(title):
    t = _table(title, [_hdr(wikitables(title)[0])[0], "Winning manager"])
    out = {}
    for tx, ln in list(rows(t))[1:]:
        if ln[1] and re.match(r"\d{4}", tx[0]):
            rec = out.setdefault(ln[1][-1], {"answer": tx[1], "enwiki": ln[1][-1], "y": []})
            rec["y"].append(f"{tx[0]} {tx[3]}")
    return [{"answer": r["answer"], "enwiki": r["enwiki"], "detail": "; ".join(r["y"])} for r in out.values()]


@prompt("p059", "Name a manager who has won the men's FIFA World Cup (1930–2026)",
        "en:List of FIFA World Cup winning managers")
def wc_managers():
    return _managers("List of FIFA World Cup winning managers")


@prompt("p060", "Name a manager who has won the men's UEFA European Championship (1960–2024)",
        "en:List of UEFA European Championship winning managers")
def euro_managers():
    return _managers("List of UEFA European Championship winning managers")


# --------------------------------------------------------------------------------------------- p061
STADIUM_NAMES = {"Wembley Stadium (1923)": "Wembley Stadium (original)",
                 "Nissan Stadium (Yokohama)": "International Stadium Yokohama (Nissan Stadium)",
                 "FNB Stadium": "Soccer City (FNB Stadium)",
                 "Stade Yves-du-Manoir": "Stade Olympique de Colombes (Yves-du-Manoir)",
                 "Estadio Nacional Julio Martínez Prádanos": "Estadio Nacional (Santiago)",
                 "Stadio Nazionale PNF": "Stadio Nazionale PNF (Rome)",
                 "Olimpiyskiy National Sports Complex": "NSC Olimpiyskiy Stadium (Kyiv)"}


@prompt("p061", "Name a stadium that has hosted a men's FIFA World Cup final (incl. the 1950 decisive match; 1930–2026)",
        "en:List of FIFA World Cup finals — venue column")
def wc_final_stadiums():
    t = _table("List of FIFA World Cup finals", ["Year", "Winners", "Score"])
    out = {}
    for tx, ln in list(rows(t))[1:]:
        if not ln[4] or not tx[0].isdigit():
            continue
        link = ln[4][-1]
        name = _stadium_name(link, [tx[4]])
        rec = out.setdefault(link, {"answer": name, "enwiki": link, "y": [], "c": tx[5]})
        rec["y"].append(tx[0])
    return [{"answer": r["answer"], "enwiki": r["enwiki"], "detail": f"{r['c'].replace(' , ', ', ')}: {', '.join(r['y'])}"}
            for r in out.values()]


# --------------------------------------------------------------------------------------------- p062
def _stadium_name(link, texts):
    """Display name: override > article title (generic '(stadium)' suffix dropped) when it matches the
    name used in the table > latest table name with the current article name appended (renamed venue)."""
    if link in STADIUM_NAMES:
        return STADIUM_NAMES[link]
    title = re.sub(r"\s*\((stadium|football stadium)\)$", "", link)
    latest = texts[-1]
    if "(" in title or latest in title or title in latest:
        return title
    return f"{latest} ({title})"


@prompt("p062", "Name a stadium that has hosted a European Cup / UEFA Champions League final (1956–2026)",
        "en:List of European Cup and UEFA Champions League finals — venue column (1974 replay included)")
def ucl_final_stadiums():
    t = _table(UCL_FINALS, ["Season", "Country", "Winners"])
    out = {}
    for tx, ln in list(rows(t))[1:]:
        if not ln[6] or not re.match(r"\d{4}", tx[0]):
            continue
        link = ln[6][-1]
        rec = out.setdefault(link, {"y": [], "names": []})
        rec["y"].append(str(int(tx[0][:4]) + 1))
        rec["names"].append(tx[6].split(" , ")[0].strip())
        rec["city"] = tx[6].split(" , ")[-1]
    res = []
    for link, r in out.items():
        names = list(dict.fromkeys(r["names"]))
        res.append({"answer": _stadium_name(link, names), "enwiki": link,
                    "detail": f"{r['city']}: {', '.join(dict.fromkeys(r['y']))}"
                              + (f" (as {' / '.join(names)})" if len(names) > 1 else "")})
    return res


# --------------------------------------------------------------------------------------------- p063
@prompt("p063", "Name a country that has played at a men's Copa América (South American Championship), "
        "guest nations included (1916–2024)",
        "en:Copa América records and statistics — all-time table")
def copa_teams():
    t = _table("Copa América records and statistics", ["Rank", "Team", "Part."])
    out = []
    for tx, ln in list(rows(t))[1:]:
        if ln[1] and tx[2].isdigit():
            out.append({"answer": tx[1], "enwiki": ln[1][-1], "detail": _apps(tx[2])})
    return out
