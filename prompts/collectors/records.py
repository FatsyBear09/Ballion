"""p024-p043: stats, records, finals, transfers."""
import re

from bs4 import BeautifulSoup

from ballion.registry import prompt
from ballion.tables import _link_title, rows, wikitables
from ballion.wiki import page_html, resolve


def num(s):
    """'1,234' / '24 #' / '87 (3)' -> first integer, or None."""
    m = re.search(r"\d[\d,]*", s)
    return int(m.group().replace(",", "")) if m else None


def clean(s):
    """Strip markers like '‡', '†', '*', '(2)', '( list )', trailing 'P' from display names."""
    s = re.sub(r"\(\s*(list|\d+|c)\s*\)", "", s)
    s = re.sub(r"[‡†*§#^¤]+", "", s)
    return re.sub(r"\s+", " ", s).strip()


def frows(t):
    """rows() with flag-icon links removed (so a player cell without its own article yields no link)."""
    flags = {_link_title(a) for a in t.select(".flagicon a")} - {None}
    for tx, ln in rows(t):
        yield tx, [[x for x in c if x not in flags] for c in ln]


def ranked_list(page, ti, pcol, vcol, minimum, unit, extra=None):
    """Generic 'Rank | Player | value ...' table filter; player link = last non-flag link.
    Players with no English article (e.g. only an interlanguage [fr] link) are skipped."""
    out = []
    for tx, ln in list(frows(wikitables(page)[ti]))[1:]:
        if len(tx) <= max(pcol, vcol) or not ln[pcol]:
            continue
        v = num(tx[vcol])
        if v is None or v < minimum:
            continue
        d = f"{v} {unit}" + (f" ({extra(tx)})" if extra else "")
        out.append({"answer": clean(tx[pcol]), "enwiki": ln[pcol][-1], "detail": d})
    return out


# ---------------------------------------------------------------- league goals
@prompt("p024", "Name a player who has scored 100 or more Premier League goals",
        "en:List of footballers with 100 or more Premier League goals")
def pl_100():
    return ranked_list("List of footballers with 100 or more Premier League goals", 0, 1, 2, 100, "PL goals",
                       lambda tx: f"{tx[5]}–{tx[6]}")


@prompt("p025", "Name a player who has scored 100 or more Bundesliga goals",
        "en:List of Bundesliga top scorers — all-time table (≥100 goals)")
def bl_100():
    return ranked_list("List of Bundesliga top scorers", 0, 1, 2, 100, "Bundesliga goals",
                       lambda tx: f"{tx[5]}–{tx[6]}")


@prompt("p026", "Name a player who has scored 100 or more Serie A goals",
        "en:List of Serie A players with 100 or more goals")
def sa_100():
    return ranked_list("List of Serie A players with 100 or more goals", 0, 1, 2, 100, "Serie A goals",
                       lambda tx: f"{tx[5]}–{tx[6]}")


@prompt("p027", "Name a player who has scored 100 or more Ligue 1 (French top-flight) goals",
        "en:List of Ligue 1 top scorers — all-time table (≥100 goals, incl. Division 1 era)")
def l1_100():
    return ranked_list("List of Ligue 1 top scorers", 0, 1, 2, 100, "Ligue 1 goals",
                       lambda tx: f"{tx[5]}–{tx[6]}")


@prompt("p028", "Name a player who has scored 30 or more goals in the European Cup / UEFA Champions League "
                "(main competition, qualifying excluded)",
        "en:List of UEFA Champions League top scorers — all-time table (≥30 goals, 1955– )")
def ucl_30():
    return ranked_list("List of UEFA Champions League top scorers", 0, 1, 2, 30, "goals",
                       lambda tx: tx[5])


# ---------------------------------------------------------------- international
@prompt("p029", "Name a men's footballer who has scored 50 or more international goals",
        "en:List of men's footballers with 50 or more international goals")
def intl_50():
    return ranked_list("List of men's footballers with 50 or more international goals", 1, 1, 4, 50,
                       "goals", lambda tx: tx[2])


@prompt("p030", "Name a men's footballer who has won 150 or more international caps",
        "en:List of men's footballers with 100 or more international caps (≥150)")
def caps_150():
    return ranked_list("List of men's footballers with 100 or more international caps", 1, 1, 4, 150,
                       "caps", lambda tx: tx[2])


@prompt("p031", "Name a player who has scored 20 or more goals for England's men's national team",
        "en:List of England international footballers (≥10 caps table; Goals ≥ 20)")
def england_20():
    t = wikitables("List of England international footballers")[1]
    out = []
    for tx, ln in list(frows(t))[2:]:
        g = num(tx[3]) if len(tx) > 3 else None
        if g is None or g < 20 or not ln[0]:
            continue
        out.append({"answer": clean(tx[0]), "enwiki": ln[0][-1], "detail": f"{g} goals in {tx[2]} caps"})
    return out


# ---------------------------------------------------------------- Premier League records
@prompt("p032", "Name a player who has made 500 or more Premier League appearances",
        "en:List of footballers with 500 or more Premier League appearances")
def pl_500():
    return ranked_list("List of footballers with 500 or more Premier League appearances", 0, 1, 4, 500,
                       "PL apps", lambda tx: f"{tx[5]}–{tx[6]}")


@prompt("p033", "Name a player who has scored 3 or more Premier League hat-tricks",
        "en:List of Premier League hat-tricks — multiple hat-tricks by player table (≥3)")
def pl_hattricks():
    t = next(t for t in wikitables("List of Premier League hat-tricks")
             if t.find("caption") and "Multiple" in t.find("caption").get_text())
    out = []
    for tx, ln in list(frows(t))[1:]:
        n = num(tx[2])
        if n is None or n < 3 or not ln[1]:
            continue
        out.append({"answer": clean(tx[1]), "enwiki": ln[1][-1], "detail": f"{n} PL hat-tricks"})
    return out


# ---------------------------------------------------------------- World Cup
@prompt("p034", "Name a player who has scored a hat-trick at a men's FIFA World Cup finals tournament",
        "en:List of FIFA World Cup hat-tricks")
def wc_hattricks():
    t = next(t for t in wikitables("List of FIFA World Cup hat-tricks")
             if t.find("caption") and "hat-tricks" in t.find("caption").get_text())
    out = {}
    for tx, ln in list(frows(t))[1:]:
        if not ln[2]:
            continue
        title = ln[2][-1]
        r = out.setdefault(title, {"answer": clean(tx[2]), "enwiki": title, "det": []})
        r["det"].append(f"{tx[1].split(',')[0]} v {tx[7]}")
    return [{"answer": r["answer"], "enwiki": r["enwiki"], "detail": "; ".join(r["det"])} for r in out.values()]


@prompt("p035", "Name a player who has played (not just been in the squad) at 4 or more men's FIFA World Cups",
        "en:List of players who have appeared in the most FIFA World Cups — squads table, 'Played' ≥ 4")
def wc_4():
    t = wikitables("List of players who have appeared in the most FIFA World Cups")[1]
    out = []
    for tx, ln in list(frows(t))[1:]:
        n = num(tx[3])
        if n is None or n < 4 or not ln[1]:
            continue
        out.append({"answer": clean(tx[1]), "enwiki": ln[1][-1],
                    "detail": f"{n} World Cups played ({tx[0]}: {tx[4]})"})
    return out


# ---------------------------------------------------------------- final goalscorers
MINUTE = re.compile(r"\d+(?:\s*\+\s*\d+)?\s*'")


def final_scorers(page):
    """[(player title, display, n goals)] from footballbox goal cells of a final article.
    Penalty-shootout kicks carry no minute so are skipped; own goals ('o.g.') are excluded."""
    soup = BeautifulSoup(page_html(page), "lxml")
    out = []
    for box in soup.select(".footballbox"):
        for td in box.select("td.fhgoal, td.fagoal"):
            groups = [(fb, fb.get_text(" ", strip=True)) for fb in td.select("span.fb-goal")]
            for icon in td.select('span[title="Golden goal"], span[title="Silver goal"]'):
                if icon.find_parent("span", class_="fb-goal") is None:  # e.g. Euro 1996/2000 golden goals
                    wrap = icon.find_parent("span", attrs={"typeof": "mw:File"}) or icon
                    nxt = wrap.find_next_sibling("span")
                    groups.append((wrap, nxt.get_text(" ", strip=True) if nxt else ""))
            for fb, text in groups:
                parts = [p for p in re.split(r",(?![^()]*\))", text) if MINUTE.search(p)]
                parts = [p for p in parts if not re.search(r"o\.\s*g\.", p)]
                if not parts:
                    continue
                a = fb.find_previous("a")
                while a is not None and (a.find_parent("span", class_="fb-goal") is not None
                                         or not _link_title(a)):
                    a = a.find_previous("a")
                if a is not None:
                    out.append((_link_title(a), a.get_text(" ", strip=True), len(parts)))
    return out


def finals_list(page, score_col, keep=lambda season: True):
    """[(season, final article title)] from a list-of-finals table (first table with a Score column)."""
    t = next(t for t in wikitables(page) if "Score" in next(rows(t))[0])
    out = []
    for tx, ln in list(frows(t))[1:]:
        f = [l for l in ln[score_col] if "final" in l.lower() or " v " in l]
        if f and keep(tx[0]) and f[0] not in [x[1] for x in out]:
            out.append((tx[0], f[0]))
    return out


def scorers_prompt(finals, label):
    goals = {}  # title -> {year: n}
    for season, page in finals:
        yr = re.search(r"\d{4}", page).group()
        for title, disp, n in final_scorers(page):
            y = goals.setdefault(title, {})
            y[yr] = y.get(yr, 0) + n
    canon = resolve(list(goals))  # redirect -> canonical title, for a clean full-name answer
    out = []
    for title, ys in goals.items():
        name = re.sub(r"\s*\(.*\)$", "", canon[title]["title"])
        det = ", ".join(f"{y}" + (f" ({n})" if n > 1 else "") for y, n in ys.items())
        out.append({"answer": name, "enwiki": title, "detail": f"{label}: {det}"})
    return out


@prompt("p036", "Name a player who has scored in a men's FIFA World Cup final (incl. the 1950 deciding match; "
                "own goals and penalty-shootout kicks excluded)",
        "en:List of FIFA World Cup finals → each final article's match box")
def wc_final_scorers():
    return scorers_prompt(finals_list("List of FIFA World Cup finals", 2), "WC final")


@prompt("p037", "Name a player who has scored in a UEFA Champions League final (1993 onward; own goals and "
                "penalty-shootout kicks excluded)",
        "en:List of European Cup and UEFA Champions League finals → each final article's match box (1993–)")
def ucl_final_scorers():
    fs = finals_list("List of European Cup and UEFA Champions League finals", 3,
                     lambda s: int(s[:4]) >= 1992)
    return scorers_prompt(fs, "UCL final")


@prompt("p038", "Name a player who has scored in an FA Cup final (1990 onward, replays included; own goals "
                "and penalty-shootout kicks excluded)",
        "en:List of FA Cup finals → each final article's match box (1990–)")
def fa_final_scorers():
    fs = finals_list("List of FA Cup finals", 2, lambda s: s[:4].isdigit() and int(s[:4]) >= 1989)
    return scorers_prompt(fs, "FA Cup final")


@prompt("p039", "Name a player who has scored in a men's UEFA European Championship final (replays included; "
                "own goals and penalty-shootout kicks excluded)",
        "en:List of UEFA European Championship finals → each final article's match box")
def euro_final_scorers():
    return scorers_prompt(finals_list("List of UEFA European Championship finals", 2), "Euro final")


# ---------------------------------------------------------------- transfers / awards
@prompt("p040", "Name a player whose transfer set a new world-record transfer fee",
        "en:List of most expensive association football transfers — world transfer record progression table")
def world_record_transfers():
    t = next(t for t in wikitables("List of most expensive association football transfers")
             if next(rows(t))[0][:4] == ["Year", "Player", "From", "To"])
    out = {}
    for tx, ln in list(frows(t))[1:]:
        name = clean(tx[1])
        if not tx[0][:4].isdigit() or not (ln[1] or name in out):
            continue  # repeat record-holders' rows may carry only a flag link -> key by name
        r = out.setdefault(name, {"answer": name, "enwiki": ln[1][-1] if ln[1] else None, "det": []})
        r["det"].append(f"{tx[0]} {tx[2]}→{tx[3]} (£{tx[4]})")
    return [{"answer": r["answer"], "enwiki": r["enwiki"], "detail": "; ".join(r["det"])} for r in out.values()]


@prompt("p041", "Name a goalkeeper who has won the Premier League Golden Glove (2004–05 onward)",
        "en:Premier League Golden Glove — winners table")
def golden_glove():
    t = next(t for t in wikitables("Premier League Golden Glove")
             if t.find("caption") and "winners" in t.find("caption").get_text())
    out = {}
    for tx, ln in list(frows(t))[1:]:
        if not ln[1] or not tx[0][:4].isdigit():
            continue
        title = ln[1][-1]
        r = out.setdefault(title, {"answer": clean(tx[1]), "enwiki": title, "det": []})
        r["det"].append(f"{clean(tx[0])} ({clean(tx[3])})")
    return [{"answer": r["answer"], "enwiki": r["enwiki"], "detail": "; ".join(r["det"])} for r in out.values()]


@prompt("p042", "Name a player who has won the Premier League with two or more different clubs",
        "en:List of Premier League winning players — Club(s) column with ≥2 clubs")
def pl_two_clubs():
    t = wikitables("List of Premier League winning players")[0]
    out = []
    for tx, ln in list(frows(t))[1:]:
        if not ln[0]:
            continue
        clubs = list(dict.fromkeys(l for l in ln[4] if not l.startswith("List of")))
        if len(clubs) >= 2:
            out.append({"answer": clean(tx[0]), "enwiki": ln[0][-1],
                        "detail": f"{tx[4]}"})
    return out


POS = re.compile(r"^[A-Z]{2,3}$")


def final_lineups(page):
    """Footballbox (home, away) link sets and lineup tables (list of [(player title, name)]) in page order."""
    soup = BeautifulSoup(page_html(page), "lxml")
    for sup in soup.select("sup.reference"):
        sup.decompose()
    boxes = []
    for b in soup.select(".footballbox"):
        boxes.append(tuple({_link_title(a) for a in b.select(f"th.{side} a")} - {None}
                           for side in ("fhome", "faway")))
    teams = []
    for t in soup.find_all("table"):
        if t.find_parent("table") is None or t.find("table"):
            continue
        if not t.get_text(" ", strip=True).startswith("GK"):
            continue
        players = []
        for tr in t.find_all("tr"):
            cells = tr.find_all(["td", "th"])
            if not cells:
                continue
            c0 = cells[0].get_text(" ", strip=True)
            if re.match(r"(Manager|Head coach|Coach|Trainer)", c0):
                break
            if not POS.match(c0):
                continue
            for c in cells[1:]:
                a = next((a for a in c.find_all("a")
                          if _link_title(a) and not a.find_parent(class_="flagicon")), None)
                if a is not None:
                    players.append((_link_title(a), a.get_text(" ", strip=True)))
                    break
        teams.append(players)
    return boxes, teams


@prompt("p043", "Name a player who was in a European Cup / Champions League-winning matchday squad "
                "(final line-up incl. listed substitutes) for two or more different clubs",
        "en:List of European Cup and UEFA Champions League finals → line-ups in each final article")
def ucl_two_clubs():
    t = next(t for t in wikitables("List of European Cup and UEFA Champions League finals")
             if "Score" in next(rows(t))[0])
    won = {}  # player -> {club: [years]}
    names = {}
    for tx, ln in list(frows(t))[1:]:
        f = [l for l in ln[3] if "final" in l.lower()]
        if not f or not ln[2]:
            continue
        winner, runner = tx[2], ln[4][-1] if ln[4] else None
        wtitle = ln[2][-1]
        boxes, teams = final_lineups(f[0])
        assert len(teams) == 2 * len(boxes), (f[0], len(boxes), len(teams))
        for i, (home, away) in enumerate(boxes):
            if wtitle in home or runner in away:
                side = 0
            elif wtitle in away or runner in home:
                side = 1
            else:
                raise ValueError(f"cannot place winner in {f[0]}")
            for title, name in teams[2 * i + side]:
                won.setdefault(title, {}).setdefault(winner, set()).add(re.search(r"\d{4}", f[0]).group())
                names.setdefault(title, name)
    out = []
    for title, clubs in won.items():
        if len(clubs) >= 2:
            det = "; ".join(f"{c} ({', '.join(sorted(y))})" for c, y in clubs.items())
            out.append({"answer": names[title], "enwiki": title, "detail": det})
    return out
