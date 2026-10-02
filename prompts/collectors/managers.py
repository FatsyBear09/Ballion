"""p084-p103: managers and career paths.

p084-p094 parse English Wikipedia manager lists.
p095-p103 ("played for both X and Y"): candidates = Wikidata P54 (member of sports team) on both
senior-club items  ∪  every article linked from the derby article's "played for both clubs"
section.  Each candidate is then verified against the "Senior career" block of their enwiki
infobox: both main senior clubs must appear there (B / youth / women's teams link to other
articles, so they don't match), with at least one spell per club not explicitly showing 0 league
apps.  Loan spells count.  Spells for `detail` come from the infobox.
"""
import re
from collections import OrderedDict, defaultdict
from urllib.parse import unquote

from bs4 import BeautifulSoup

from ballion.registry import prompt
from ballion.tables import rows, wikitables
from ballion.wiki import api, page_html, resolve
from ballion.wikidata import enwiki_title, sparql

# ---------------------------------------------------------------- helpers

MARKS = re.compile(r"\s*(\((caretaker|interim)\)|\(\s*caretaker\s*\)|\(\d+\)|[†‡*]|\bp\b)\s*", re.I)


def clean(name):
    """'Ryan Giggs p (caretaker)' -> 'Ryan Giggs'; 'Fred Pentland (2)' -> 'Fred Pentland'."""
    prev = None
    while prev != name:
        prev, name = name, MARKS.sub(" ", name).strip()
    return re.sub(r"\s+", " ", name)


def canon(titles):
    """Map titles -> canonical (redirect-resolved) enwiki title; None if missing."""
    r = resolve(list(titles))
    return {t: (None if r[t]["missing"] else r[t]["title"]) for t in titles}


def person_link(links, text):
    """Last link in a person cell that isn't a flag/federation/role link."""
    bad = re.compile(r"national football team|Football Association|Federation|Caretaker manager|^[A-Z][a-z]+$")
    cand = [l for l in links if not bad.search(l) or clean(text).split()[-1] in l]
    return cand[-1] if cand else None


def finish(recs):
    """recs: OrderedDict enwiki-ish title -> {"answer", "detail"}; canonicalise + dedupe."""
    c = canon(recs)
    out = OrderedDict()
    for t, r in recs.items():
        ct = c[t]
        if not ct:
            continue
        if ct in out:
            out[ct]["detail"] += "; " + r["detail"]
        else:
            out[ct] = {"answer": r["answer"], "enwiki": ct, "detail": r["detail"]}
    return list(out.values())


def grouped(pairs):
    """[(club, year), ...] -> 'Milan 2003, 2007; Real Madrid 2014'."""
    g = OrderedDict()
    for club, y in pairs:
        g.setdefault(club, []).append(y)
    return "; ".join(f"{c} {', '.join(ys)}" for c, ys in g.items())


def season_winners(page, season_col, mgr_col, club_col, skip=("—", "Cancelled", "Stripped")):
    """Per-season winners table (first wikitable). Repeated names are often unlinked, so
    names are mapped to the link of their first linked occurrence."""
    t = wikitables(page)[0]
    name2link, wins = {}, OrderedDict()
    for tx, ln in list(rows(t))[1:]:
        if len(tx) <= max(season_col, mgr_col, club_col):
            continue
        name = clean(tx[mgr_col])
        if not name or any(s in tx[mgr_col] for s in skip):
            continue
        link = person_link(ln[mgr_col], name) if ln[mgr_col] else None
        if link:
            name2link.setdefault(name, link)
        wins.setdefault(name, []).append((tx[club_col], tx[season_col]))
    recs = OrderedDict()
    for name, ws in wins.items():
        if name in name2link:  # unlinked everywhere -> no article (e.g. Robert Middleton)
            recs[name2link[name]] = {"answer": name, "detail": grouped(ws)}
    return recs


def tenure_list(page, name_col, from_col, to_col, keep=lambda tx: True, table=0):
    t = wikitables(page)[table]
    name2link, spells = {}, OrderedDict()
    for tx, ln in list(rows(t))[1:]:
        if len(tx) <= max(name_col, from_col, to_col) or tx[name_col] in ("Total", "Manager", "Name"):
            continue
        name = clean(tx[name_col])
        if not name or not keep(tx):
            continue
        link = person_link(ln[name_col], name) if ln[name_col] else None
        if link:
            name2link.setdefault(name, link)
        yrs = lambda s: (re.findall(r"\d{4}", s) or ["present" if "resent" in s or not s.strip() else s])[-1]
        if to_col == from_col:  # single 'Tenure' column, e.g. '1946–1962', '2025–'
            span = re.sub(r"\s+", "", tx[from_col]).rstrip("–") or "?"
            span += "–present" if tx[from_col].strip().endswith("–") else ""
        else:
            a, b = yrs(tx[from_col]), yrs(tx[to_col])
            span = f"{a}–{b}" if b and b != a else a
        caret = " (caretaker)" if re.search(r"caretaker|†", tx[name_col], re.I) else \
            " (interim)" if re.search(r"interim", tx[name_col], re.I) else ""
        sp = spells.setdefault(name, [])
        if span + caret not in sp:
            sp.append(span + caret)
    recs = OrderedDict()
    for name, sp in spells.items():
        if name in name2link:
            recs[name2link[name]] = {"answer": name, "detail": ", ".join(sp)}
    return recs


# ---------------------------------------------------------------- managers: trophies

@prompt("p084", "Name a manager who has won the European Cup / UEFA Champions League (up to the 2026 final)",
        "en:List of European Cup and UEFA Champions League winning managers — winners by final")
def ucl_managers():
    return finish(season_winners("List of European Cup and UEFA Champions League winning managers",
                                 season_col=0, mgr_col=2, club_col=4))


@prompt("p085", "Name a manager who has won the English top-flight league title (1888–89 to 2025–26)",
        "en:List of English football championship–winning managers — winners by season")
def eng_champ_managers():
    return finish(season_winners("List of English football championship–winning managers",
                                 season_col=0, mgr_col=2, club_col=3))


@prompt("p086", "Name a manager who has won the Bundesliga (since 1963–64, up to 2025–26)",
        "en:List of Bundesliga managers — Bundesliga title-winning managers table")
def bundesliga_managers():
    t = next(t for t in wikitables("List of Bundesliga managers")
             if next(rows(t))[0][:4] == ["Rank", "Manager", "Nat.", "Titles"])
    recs = OrderedDict()
    for tx, ln in list(rows(t))[1:]:
        if ln[1]:
            recs[ln[1][-1]] = {"answer": clean(tx[1]), "detail": f"{tx[3]}× — " + re.sub(r"\s+,", ",", tx[4])}
    return finish(recs)


@prompt("p087", "Name a manager who has won La Liga (1929 to 2025–26)",
        "en:List of La Liga winning managers — winners by season")
def laliga_managers():
    return finish(season_winners("List of La Liga winning managers", season_col=0, mgr_col=2, club_col=3))


@prompt("p088", "Name a manager who has won Serie A (single-division era since 1929–30, up to 2025–26)",
        "en:List of Serie A winning managers — winners by season (2004–05 revoked title excluded)")
def seriea_managers():
    return finish(season_winners("List of Serie A winning managers", season_col=0, mgr_col=1, club_col=3))


# ---------------------------------------------------------------- managers: teams

@prompt("p089", "Name a manager of the England men's national team since 1946 (caretakers included, as of 2026)",
        "en:England national football team manager — list of managers (incl. caretakers)")
def england_managers():
    return finish(tenure_list("England national football team manager", 1, 2, 2))


@prompt("p090", "Name a manager of Manchester United (caretakers/interims included, as of 2026)",
        "en:List of Manchester United F.C. managers — main table")
def manutd_managers():
    return finish(tenure_list("List of Manchester United F.C. managers", 1, 3, 4))


@prompt("p091", "Name a head coach of Real Madrid (all-time, incl. interim spells listed by Wikipedia, as of 2026)",
        "en:List of Real Madrid CF managers — main table")
def realmadrid_managers():
    return finish(tenure_list("List of Real Madrid CF managers", 0, 2, 3))


@prompt("p092", "Name a head coach of FC Barcelona (all-time, incl. interim spells listed by Wikipedia, as of 2026)",
        "en:List of FC Barcelona managers — main table")
def barcelona_managers():
    return finish(tenure_list("List of FC Barcelona managers", 0, 1, 2))


def _since_2003(tx):
    to = tx[4]
    yrs = re.findall(r"\d{4}", to)
    return "resent" in to or bool(yrs and int(yrs[-1]) >= 2004)  # nobody left Chelsea Jul–Dec 2003


@prompt("p093", "Name a manager of Chelsea since the Abramovich takeover in July 2003 (caretakers included, as of 2026)",
        "en:List of Chelsea F.C. managers — managers in charge at any point from July 2003")
def chelsea_managers():
    return finish(tenure_list("List of Chelsea F.C. managers", 1, 3, 4, keep=_since_2003))


@prompt("p094", "Name a manager of Arsenal (caretakers included, as of 2026)",
        "en:List of Arsenal F.C. managers — main table (unnamed/no-article caretakers dropped)")
def arsenal_managers():
    return finish(tenure_list("List of Arsenal F.C. managers", 0, 2, 3))


# ---------------------------------------------------------------- played for both

def _wikidata_both(qa, qb):
    """enwiki title -> {qid: [(start, end), ...]} for people with P54 statements on both items."""
    q = f"""SELECT ?art ?team ?s ?e WHERE {{
      ?p wdt:P54 wd:{qa} ; wdt:P54 wd:{qb} .
      ?art schema:about ?p ; schema:isPartOf <https://en.wikipedia.org/> .
      ?p p:P54 ?st . ?st ps:P54 ?team . FILTER(?team IN (wd:{qa}, wd:{qb}))
      OPTIONAL {{ ?st pq:P580 ?s }} OPTIONAL {{ ?st pq:P582 ?e }} }}"""
    out = {}
    for r in sparql(q):
        sp = out.setdefault(enwiki_title(r["art"]), {qa: [], qb: []})[r["team"].rsplit("/", 1)[1]]
        span = (r.get("s", "")[:4], r.get("e", "")[:4])
        if span not in sp:
            sp.append(span)
    return out


def _links_both_clubs(title, club_titles):
    """For articles without an infobox: does the article body link to both club articles?"""
    soup = BeautifulSoup(page_html(title), "lxml")
    links = {unquote(a["href"][6:].split("#")[0]).replace("_", " ")
             for a in soup.select(".mw-parser-output > p a[href^='/wiki/']")}
    c = canon(links) if links else {}
    return all(ct in set(c.values()) for ct in club_titles)


def _section_links(page, pattern):
    """Article links inside the section(s) of `page` whose heading matches `pattern`."""
    secs = api(action="parse", page=page, prop="sections", redirects=1)["parse"]["sections"]
    out = []
    for s in secs:
        if not re.search(pattern, s["line"], re.I):
            continue
        html = api(action="parse", page=page, prop="text", section=s["index"], redirects=1)["parse"]["text"]
        soup = BeautifulSoup(html, "lxml")
        for x in soup.select("sup.reference, .reflist, .references, .navbox"):
            x.decompose()
        for a in soup.find_all("a"):
            h = a.get("href", "")
            if h.startswith("/wiki/") and ":" not in h[6:]:
                out.append(unquote(h[6:].split("#")[0]).replace("_", " "))
    return list(dict.fromkeys(out))


def _senior_career(title):
    """[(years, club link title, apps or None, 'loan'/'guest'/'')] from the infobox 'Senior career' block."""
    d = api(action="parse", page=title, prop="text", section=0, redirects=1)
    if "parse" not in d:
        return None
    soup = BeautifulSoup(d["parse"]["text"], "lxml")
    out, on = [], False
    for tr in soup.select("table.infobox tr"):
        hdr = tr.find("th", class_="infobox-header", recursive=False)
        if hdr is not None:
            on = hdr.get_text(" ", strip=True).startswith("Senior career")
            continue
        if not on:
            continue
        th = tr.find("th", recursive=False)
        tds = tr.find_all("td", recursive=False)
        if th is None or not tds:
            continue
        team = tds[0]
        links = [unquote(a["href"][6:].split("#")[0]).replace("_", " ") for a in team.find_all("a")
                 if a.get("href", "").startswith("/wiki/")]
        if not links:
            continue
        apps = tds[1].get_text(" ", strip=True) if len(tds) > 1 else ""
        n = int(apps) if re.fullmatch(r"\d+", apps) else None
        tt = team.get_text(" ", strip=True).lower()
        loan = "loan" if "loan" in tt else "guest" if "guest" in tt else ""
        out.append((th.get_text("", strip=True), links[0], n, loan))
    return out


def _short_years(y):
    """'1997–2000' -> '1997–2000' (kept), strips stray spaces."""
    return re.sub(r"\s+|\[\w+\]", "", y)


DEBUG = {}


def played_both(club_a, club_b, derby_page=None, section=None):
    """club_x = (label, enwiki title). Returns verified answer rows."""
    (la, ta), (lb, tb) = club_a, club_b
    qa, qb = (resolve([ta])[ta]["qid"], resolve([tb])[tb]["qid"])
    wd = _wikidata_both(qa, qb)
    listed = _section_links(derby_page, section) if derby_page else []
    cands = list(dict.fromkeys(list(wd) + listed))
    ccands = canon(cands)
    people = list(dict.fromkeys(c for c in ccands.values() if c))
    careers = {p: _senior_career(p) for p in people}
    club_links = {l for car in careers.values() if car for _, l, _, _ in car}
    cl = canon(club_links)
    want = {la: canon([ta])[ta], lb: canon([tb])[tb]}
    wd_c = {ccands[t] for t in wd}
    dbg = DEBUG[(la, lb)] = {"no_infobox": [], "one_club": [], "zero_apps": []}
    out = []
    for p in people:
        car = careers[p]
        if not car:
            # no infobox: accept Wikidata candidates whose article prose links both clubs
            src = next((t for t in wd if ccands[t] == p), None)
            if src and _links_both_clubs(p, list(want.values())):
                def fmt(spans):
                    return ", ".join("–".join(x for x in se if x) or "dates n/a" for se in sorted(spans))
                out.append({"answer": re.sub(r"\s*\([^)]*\)$", "", p), "enwiki": p,
                            "detail": f"{la} {fmt(wd[src][qa])}; {lb} {fmt(wd[src][qb])} [no infobox; Wikidata]",
                            "_first": min([x for se in wd[src][qa] + wd[src][qb] for x in se if x] or ["9999"])})
            dbg["no_infobox"].append((p, "wd" if p in wd_c else "list"))
            continue
        spells = defaultdict(list)
        for yrs, link, n, loan in car:
            for lab, ct in want.items():
                if cl.get(link) == ct:
                    spells[lab].append((yrs, n, loan))
        if len(spells) < 2:
            if spells:
                dbg["one_club"].append((p, "wd" if p in wd_c else "list", dict(spells)))
            continue
        # drop if every spell at a club explicitly shows 0 league apps, or is a wartime guest spell
        if any(all(n == 0 or tag == "guest" for _, n, tag in spells[lab]) for lab in want):
            dbg["zero_apps"].append((p, "wd" if p in wd_c else "list", dict(spells)))
            continue
        det = []
        for lab in want:
            ss = ", ".join((_short_years(y) or "?") + (f" ({loan})" if loan else "") for y, _, loan in spells[lab])
            det.append(f"{lab} {ss}")
        name = re.sub(r"\s*\([^)]*\)$", "", p)
        out.append({"answer": name, "enwiki": p, "detail": "; ".join(det),
                    "_first": min(re.findall(r"\d{4}", " ".join(y for y, _, _ in spells[la] + spells[lb])) or ["9999"])})
    out.sort(key=lambda r: r.pop("_first"))
    return out


BOTH = ("(≥1 league appearance for each senior team; loans count, wartime guest spells don't; "
        "per Wikipedia infoboxes, as of 2026)")


@prompt("p095", f"Name a player who has played for both Real Madrid and Barcelona {BOTH}",
        "Wikidata P54 ∪ en:El Clásico 'Personnel at both clubs', verified via enwiki infobox senior career")
def real_barca():
    return played_both(("Real Madrid", "Real Madrid CF"), ("Barcelona", "FC Barcelona"),
                       "El Clásico", r"^Personnel at both clubs$")


@prompt("p096", f"Name a player who has played for both Arsenal and Tottenham {BOTH}",
        "Wikidata P54 ∪ en:North London derby 'Crossing the divide', verified via enwiki infobox senior career")
def arsenal_spurs():
    return played_both(("Arsenal", "Arsenal F.C."), ("Tottenham", "Tottenham Hotspur F.C."),
                       "North London derby", r"^Crossing the divide$")


@prompt("p097", f"Name a player who has played for both Manchester United and Manchester City {BOTH}",
        "Wikidata P54 ∪ en:Manchester derby 'Players who have played for both clubs', verified via enwiki infobox")
def united_city():
    return played_both(("Manchester United", "Manchester United F.C."), ("Manchester City", "Manchester City F.C."),
                       "Manchester derby", r"^Players who have played for both clubs$")


@prompt("p098", f"Name a player who has played for both Liverpool and Everton {BOTH}",
        "Wikidata P54 ∪ en:Merseyside derby 'Crossing the park', verified via enwiki infobox senior career")
def liverpool_everton():
    return played_both(("Liverpool", "Liverpool F.C."), ("Everton", "Everton F.C."),
                       "Merseyside derby", r"^Crossing the park$")


@prompt("p099", f"Name a player who has played for both AC Milan and Inter {BOTH}",
        "Wikidata P54 ∪ en:Derby della Madonnina 'Players who played for both clubs', verified via enwiki infobox")
def milan_inter():
    return played_both(("Milan", "AC Milan"), ("Inter", "Inter Milan"),
                       "Derby della Madonnina", r"^Players who played for both clubs$")


@prompt("p100", f"Name a player who has played for both Celtic and Rangers {BOTH}",
        "Wikidata P54 ∪ en:Old Firm 'Played for both teams', verified via enwiki infobox senior career")
def celtic_rangers():
    return played_both(("Celtic", "Celtic F.C."), ("Rangers", "Rangers F.C."),
                       "Old Firm", r"^Played for both teams$")


@prompt("p101", f"Name a player who has played for both Chelsea and Arsenal {BOTH}",
        "Wikidata P54 ∪ en:Arsenal F.C.–Chelsea F.C. rivalry players section, verified via enwiki infobox")
def chelsea_arsenal():
    return played_both(("Chelsea", "Chelsea F.C."), ("Arsenal", "Arsenal F.C."),
                       "Arsenal F.C.–Chelsea F.C. rivalry", r"^Players who have played for or managed both")


@prompt("p102", f"Name a player who has played for both Bayern Munich and Borussia Dortmund {BOTH}",
        "Wikidata P54 ∪ en:Der Klassiker 'played for or managed both clubs', verified via enwiki infobox")
def bayern_dortmund():
    return played_both(("Bayern", "FC Bayern Munich"), ("Dortmund", "Borussia Dortmund"),
                       "Der Klassiker", r"^Players and managers who have played")


@prompt("p103", f"Name a player who has played for both Paris Saint-Germain and Marseille {BOTH}",
        "Wikidata P54 ∪ en:Le Classique 'Playing for both clubs', verified via enwiki infobox senior career")
def psg_marseille():
    return played_both(("PSG", "Paris Saint-Germain FC"), ("Marseille", "Olympique de Marseille"),
                       "Le Classique", r"^(Playing for both clubs|List of players)$")
