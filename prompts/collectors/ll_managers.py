"""ll107-ll118, ll194: managers."""
import re

from ballion.registry import prompt
from ballion.wiki import resolve
from ballion.wikidata import sparql
from prompts.collectors.ll_util import NAT_TEAM, clean, dedupe, find, matches, parse_date, season_label, tables

LL = "{s} La Liga"
SD = "{s} Segunda División"


def _person(links):
    """First link in a manager cell that looks like a person (not a club or national team)."""
    for t, a in links:
        if re.search(r"F\.?C\.?$|^FC |CF$|^CD |^UD |^SD |^Real |Club|Deportivo|Athletic|Atl[eé]tico|Sporting|Racing|Football|Interim|Caretaker", t) and "(" not in t:
            continue
        if NAT_TEAM.search(t):
            continue
        return t, a
    return None


def season_staff(page, pre_season_only=False, in_season_only=False, club=None):
    """Managers on a league season page: personnel table + managerial changes (outgoing and incoming)."""
    out = []
    for tb in tables(page):
        h = tb["hdr"]
        if not h or not h[0].startswith("Team"):
            continue
        cols = []
        if any(re.match(r"(Head coach|Manager)", c, re.I) for c in h) and not any("Outgoing" in c for c in h) and not in_season_only:
            cols = [i for i, c in enumerate(h) if re.match(r"(Head coach|Manager)", c, re.I)][:1]
            kind = "start"
        elif any("Outgoing" in c for c in h):
            cols = [i for i, c in enumerate(h) if "Outgoing" in c or re.match(r"(Replaced by|Incoming)", c)]
            kind = "change"
        else:
            continue
        pos = next((i for i, c in enumerate(h) if c.startswith("Position")), None)
        for tx, ln in tb["rows"]:
            if len(tx) <= max(cols):
                continue
            if club and not (ln[0] and club in ln[0][0][0]) and club not in tx[0]:
                continue
            if kind == "change" and pos is not None:
                pre = bool(re.search(r"pre|off|summer", tx[pos], re.I))
                if in_season_only and pre:
                    continue
            for ci in cols:
                p = _person(ln[ci])
                if p:
                    out.append({"answer": clean(p[1]), "enwiki": p[0], "detail": f"{page.split(' ')[0]}: {tx[0]}"})
    return out


def _range(fmt, y0, y1, **kw):
    out = []
    for y in range(y0, y1 + 1):
        out += season_staff(fmt.format(s=season_label(y)), **kw)
    return dedupe(out)


@prompt("ll107", "Name a manager who took charge of a La Liga club in 2025–26 (at the start of the season or later)",
        "en:2025–26 La Liga — Personnel and kits; Managerial changes", family="ll-managers-era")
def ll107():
    return _range(LL, 2025, 2025)


@prompt("ll108", "Name a manager involved in a mid-season La Liga managerial change from 2022–23 to 2026–27 (outgoing or incoming)",
        "en:2022–23 La Liga … 2026–27 La Liga — Managerial changes (not pre-season)")
def ll108():
    return _range(LL, 2022, 2026, in_season_only=True)


@prompt("ll109", "Name a manager who managed a La Liga club between 2015–16 and 2019–20",
        "en:2015–16 La Liga … 2019–20 La Liga — Personnel; Managerial changes", family="ll-managers-era")
def ll109():
    return _range(LL, 2015, 2019)


@prompt("ll110", "Name a manager who managed a La Liga club between 2020–21 and 2024–25",
        "en:2020–21 La Liga … 2024–25 La Liga — Personnel; Managerial changes", family="ll-managers-era")
def ll110():
    return _range(LL, 2020, 2024)


@prompt("ll111", "Name a non-Spanish manager who has managed a La Liga club since 2015–16 (to 2026–27)",
        "en:2015–16 La Liga … 2026–27 La Liga — Personnel; Managerial changes, filtered by Wikidata citizenship (no Spanish citizenship)")
def ll111():
    recs = _range(LL, 2015, 2026)
    res = resolve([r["enwiki"] for r in recs])
    q = {res[r["enwiki"]]["qid"]: r for r in recs if res[r["enwiki"]]["qid"]}
    ids = list(q)
    spanish = set()
    known = set()
    for i in range(0, len(ids), 80):
        chunk = ids[i:i + 80]
        rows = sparql("SELECT ?i ?c WHERE { VALUES ?i { " + " ".join("wd:" + x for x in chunk) + " } ?i wdt:P27 ?c }")
        for r in rows:
            qi = r["i"].rsplit("/", 1)[1]
            known.add(qi)
            if r["c"].endswith("/Q29"):
                spanish.add(qi)
    return [q[x] for x in ids if x in known and x not in spanish]


# ---------------------------------------------------------------- club manager lists

def _years(s):
    return [int(y) for y in re.findall(r"\d{4}", s)]


def _list_mgrs(page, since, name_col=0):
    out = []
    for tb in tables(page):
        h = tb["hdr"]
        if not h or h[0] not in ("Name", "Manager", "Coach", "Head coach"):
            continue
        for tx, ln in tb["rows"]:
            if not ln or not ln[name_col]:
                continue
            ys = _years(" ".join(tx[1:5]))
            if re.search(r"present|current", " ".join(tx[1:5]), re.I):
                ys.append(2026)
            if ys and max(ys) >= since:
                out.append({"answer": clean(tx[name_col]), "enwiki": ln[name_col][-1][0], "detail": " ".join(tx[1:4])[:60]})
        if out:
            break
    return dedupe(out)


@prompt("ll114", "Name a manager of Valencia since 2000 (caretakers included)", "en:List of Valencia CF managers",
        family="ll-club-managers")
def ll114():
    return _list_mgrs("List of Valencia CF managers", 2000)


@prompt("ll115", "Name a manager of Atlético Madrid since 1995 (caretakers included)", "en:List of Atlético Madrid managers",
        family="ll-club-managers")
def ll115():
    return _list_mgrs("List of Atlético Madrid managers", 1995)


@prompt("ll116", "Name a manager of Athletic Club since 2000 (caretakers included)", "en:List of Athletic Bilbao managers",
        family="ll-club-managers")
def ll116():
    out = []
    tb = find("List of Athletic Bilbao managers", "Coach", ["Stage"], head="List of managers")
    for tx, ln in tb["rows"]:
        if len(tx) < 3 or not ln[0]:
            continue
        ys = _years(tx[2])
        if "present" in tx[2].lower():
            ys.append(2026)
        if ys and max(ys) >= 2000:
            out.append({"answer": clean(tx[0]), "enwiki": ln[0][-1][0], "detail": tx[2][:50]})
    return dedupe(out)


@prompt("ll117", "Name a manager of Real Sociedad since 2000 (caretakers included)", "en:List of Real Sociedad managers",
        family="ll-club-managers")
def ll117():
    out = []
    tb = find("List of Real Sociedad managers", "Manager", ["To"], head="List of managers")
    for tx, ln in tb["rows"]:
        if len(tx) < 3 or not ln[0]:
            continue
        ys = _years(" ".join(tx[1:4]))
        if re.search(r"present|current", " ".join(tx[1:4]), re.I):
            ys.append(2026)
        if ys and max(ys) >= 2000:
            out.append({"answer": clean(tx[0]), "enwiki": ln[0][-1][0], "detail": " ".join(tx[1:4])[:50]})
    return dedupe(out)


@prompt("ll118", "Name a head coach of Sevilla from 2015–16 to 2026–27 (caretakers included)",
        "en:2015–16 La Liga … 2026–27 La Liga — Sevilla's head coach in the personnel and managerial-changes tables", family="ll-club-managers")
def ll118():
    out = []
    for y in range(2015, 2027):
        out += season_staff(LL.format(s=season_label(y)), club="Sevilla")
    return dedupe(out)


@prompt("ll194", "Name a manager who took charge of a Segunda División club in 2025–26 (at the start of the season or later)",
        "en:2025–26 Segunda División — Personnel and sponsorship; Managerial changes")
def ll194():
    return _range(SD, 2025, 2025)


# ---------------------------------------------------------------- Copa del Rey winning managers

@prompt("ll112", "Name a manager who has won the Copa del Rey since 2000 (final of 2000 to 2026)",
        "en:List of Copa del Rey finals + 2000–2026 Copa del Rey final pages — manager of the winning side", family="ll-managers-trophy")
def ll112():
    tb = find("List of Copa del Rey finals", "Season", ["Winners", "Runners-up"], head="List of finals")
    win = {}
    for tx, ln in tb["rows"]:
        m = re.match(r"(\d{4})(?:[–-](\d{2,4}))?", tx[0])
        if m and len(ln) > 1 and ln[1]:
            yr = int(m.group(1))
            if m.group(2):
                e = int(m.group(2))
                yr = e if e > 100 else (yr // 100) * 100 + e
            win[yr] = ln[1][-1][0]
    res = resolve(list(win.values()))
    out = []
    for y in range(2000, 2027):
        if y not in win:
            continue
        ms = matches(f"{y} Copa del Rey final")
        m = ms[0]
        for side, lu in zip(("home", "away"), m["lineups"] or []):
            if res[win[y]]["title"] == resolve([m[side][1]])[m[side][1]]["title"] and lu["manager"]:
                out.append({"answer": clean(lu["manager"][1]), "enwiki": lu["manager"][0], "detail": f"{y} Copa del Rey, {m[side][0]}"})
    return dedupe(out)


@prompt("ll113", "Name a manager who has won the Supercopa de España since 2000 (editions of 2000 to January 2026)",
        "en:Supercopa de España + 2000–2026 Supercopa de España pages — manager of the winning side", family="ll-managers-trophy")
def ll113():
    pages = {}  # page -> winner title
    two = find("Supercopa de España", "Year", ["Winners", "Runners-up"], head="Two-team format")
    for tx, ln in two["rows"]:
        if tx[0].isdigit() and 2000 <= int(tx[0]) <= 2018 and ln[1]:
            pages[f"{tx[0]} Supercopa de España"] = ln[1][0][0]
    four = find("Supercopa de España", "Year", ["Winners", "Semi-finalists"], head="Four-team format")
    for tx, ln in four["rows"]:
        if tx[0].isdigit() and ln[1]:
            pages[f"{int(tx[0]) + 1} Supercopa de España final"] = ln[1][0][0]
    out = []
    for pg, w in pages.items():
        wt = resolve([w])[w]["title"]
        for m in matches(pg):
            for side, lu in zip(("home", "away"), m["lineups"] or []):
                if lu["manager"] and resolve([m[side][1]])[m[side][1]]["title"] == wt:
                    out.append({"answer": clean(lu["manager"][1]), "enwiki": lu["manager"][0], "detail": f"{pg[:4]} Supercopa, {m[side][0]}"})
    return dedupe(out)
