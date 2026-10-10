"""gen138-gen156, gen195: Europa League, Conference League, Super Cup."""
import datetime as dt
import re

from ballion.registry import prompt
from prompts.collectors.gen_util import (Acc, NAT_TEAM, box_scorers, country_rec, dedupe, find_tab, find_tabs,
                                         first_person, hattricks, people, season_label, squad_apps, tabs)
from ballion.wiki import resolve

CLUB_NOT = re.compile(r"Association|Federation|Football Union|national|Confederation", re.I)


def _clubs(cell):
    return [(t, a) for t, a in cell if not CLUB_NOT.search(t)]


@prompt("gen138", "Name a player who has scored in a UEFA Europa League final from 2010 to 2026 (own goals and shoot-outs excluded)",
        "en:2010 UEFA Europa League final … en:2026 UEFA Europa League final — football-box scorers",
        family="gen-final-scorers")
def uel_final_scorers():
    acc = Acc()
    for y in range(2010, 2027):
        box_scorers(f"{y} UEFA Europa League final", acc, str(y))
    return acc.out()


@prompt("gen139", "Name a manager who has won the UEFA Cup or Europa League since 2000",
        "en:List of UEFA Cup and Europa League–winning managers — 'By year' table, 2000 onward")
def uel_managers():
    tb = find_tab("List of UEFA Cup and Europa League winning managers", ["Final", "Winning manager"], heading="By year")
    ci = tb.col("Winning manager")
    acc = Acc()
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and int(tx[0][:4]) >= 2000 and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], tx[0])
    return acc.out()


@prompt("gen140", "Name a player who finished as top scorer of a UEFA Cup / Europa League season from 2009–10 to 2025–26",
        "en:List of UEFA Cup and Europa League top scorers — 'Top scorers by season' tables, 2009–10 onward",
        family="gen-league-top-scorer")
def uel_topscorers():
    acc = Acc()
    for tb in find_tabs("List of UEFA Cup and Europa League top scorers", ["Season", "Player", "Goal"], heading="Top scorers by season"):
        ci = tb.col("Player")
        for tx, ln in tb.body:
            if re.match(r"\d{4}", tx[0]) and int(tx[0][:4]) >= 2009 and (p := first_person(ln[ci])):
                acc.add(p[0], p[1], tx[0])
    return acc.out()


@prompt("gen141", "Name a player in the all-time UEFA Cup / Europa League top scorers table (group or league phase to final)",
        "en:List of UEFA Cup and Europa League top scorers — all-time table (group stage/league phase to final)")
def uel_alltime():
    tb = find_tab("List of UEFA Cup and Europa League top scorers", ["Rank", "Player", "Goal"], heading=r"All-time top scorers \(group")
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if tx[0].strip().isdigit() and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], f"{tx[2]} goals")
    return acc.out()


@prompt("gen142", "Name a player who has scored a UEFA Europa League hat-trick since 2015–16",
        "en:List of UEFA Europa League hat-tricks — dated 2015-07-01 or later", family="gen-league-hattricks")
def uel_hattricks():
    return hattricks("List of UEFA Europa League hat-tricks", dt.date(2015, 7, 1), extra_hdr=("For", "Against")).out()


@prompt("gen144", "Name a player who scored in the 2025–26 UEFA Europa League knockout phase (own goals and shoot-outs excluded)",
        "en:2025–26 UEFA Europa League knockout phase — football-box scorers", family="gen-knockout-scorers")
def uel_ko_2526():
    return box_scorers("2025–26 UEFA Europa League knockout phase").out()


@prompt("gen145", "Name a player who scored in the 2024–25 UEFA Europa League knockout phase (own goals and shoot-outs excluded)",
        "en:2024–25 UEFA Europa League knockout phase — football-box scorers", family="gen-knockout-scorers")
def uel_ko_2425():
    return box_scorers("2024–25 UEFA Europa League knockout phase").out()


@prompt("gen146", "Name a player who scored in the 2025–26 UEFA Conference League knockout phase (own goals and shoot-outs excluded)",
        "en:2025–26 UEFA Conference League knockout phase — football-box scorers", family="gen-knockout-scorers")
def uecl_ko_2526():
    return box_scorers("2025–26 UEFA Conference League knockout phase").out()


@prompt("gen195", "Name a player who scored in the 2024–25 UEFA Conference League knockout phase (own goals and shoot-outs excluded)",
        "en:2024–25 UEFA Conference League knockout phase — football-box scorers", family="gen-knockout-scorers")
def uecl_ko_2425():
    return box_scorers("2024–25 UEFA Conference League knockout phase").out()


def _semis(pages):
    acc = Acc("club")
    for label, page in pages:
        tb = find_tab(page, ["Team 1", "Team 2"], heading="Semi-finals")
        for tx, ln in tb.body:
            for ci in (0, 2):
                for t, a in _clubs(ln[ci])[:1]:
                    acc.add(t, a, label)
    return acc.out()


@prompt("gen147", "Name a club that reached a UEFA Europa League semi-final from 2015–16 to 2025–26",
        "en:2015–16 UEFA Europa League … en:2025–26 UEFA Europa League — 'Semi-finals' tables",
        family="gen-semifinalists")
def uel_semis():
    return _semis([(season_label(y), f"{season_label(y)} UEFA Europa League") for y in range(2015, 2026)])


@prompt("gen148", "Name a club that reached a UEFA Conference League semi-final (2021–22 to 2025–26)",
        "en:2021–22 UEFA Europa Conference League … en:2025–26 UEFA Conference League — 'Semi-finals' tables",
        family="gen-semifinalists")
def uecl_semis():
    pages = []
    for y in range(2021, 2026):
        s = season_label(y)
        pages.append((s, f"{s} UEFA Europa Conference League" if y < 2024 else f"{s} UEFA Conference League"))
    return _semis(pages)


def _phase_table(page):
    for tb in tabs(page):
        if tb.heading == "Table" and tb.hdr[:1] == ["Pos"] and len(tb.body) >= 36:
            return tb
    raise LookupError(f"{page}: no league-phase table")


@prompt("gen149", "Name a club in the 2026–27 UEFA Europa League league phase",
        "en:2026–27 UEFA Europa League — league phase table", family="gen-current-league-clubs")
def uel_phase_clubs():
    tb = _phase_table("2026–27 UEFA Europa League")
    ti = next(i for i, h in enumerate(tb.hdr) if h.startswith("Team"))
    acc = Acc("club")
    for tx, ln in tb.body:
        for t, a in _clubs(ln[ti])[:1]:
            acc.add(t, a, "league phase")
    return acc.out()


@prompt("gen150", "Name a country with a club in the 2026–27 UEFA Conference League league phase",
        "en:2026–27 UEFA Conference League — league phase table, association of each club", family="gen-current-league-clubs")
def uecl_phase_countries():
    page = "2026–27 UEFA Conference League"
    # federation -> country map from the association ranking tables (flag icon next to each federation link)
    fed = {}
    for tb in tabs(page):
        if tb.heading == "Association ranking" and "Association" in tb.hdr:
            ai = tb.col("Association")
            for (tx, ln), fl in zip(tb.body, tb.bflags):
                if ln[ai] and tx[ai].strip():
                    fed[ln[ai][0][0]] = tx[ai].strip()
    tb = _phase_table(page)
    ti = next(i for i, h in enumerate(tb.hdr) if h.startswith("Team"))
    out = {}
    for (tx, ln), fl in zip(tb.body, tb.bflags):
        f = next((t for t in fl[ti] if t in fed), None)
        if f is None:
            f = next((t for t, a in ln[ti] if t in fed), None)
        if f:
            r = out.setdefault(fed[f], country_rec(fed[f]))
            r["detail"] = ""
    if len(out) < 12:
        raise LookupError(f"only {len(out)} countries mapped")
    return dedupe(list(out.values()))


@prompt("gen151", "Name a player who made a UEFA Europa League appearance for Atalanta in their 2023–24 winning run",
        "en:2023–24 Atalanta BC season — appearances table (Europa League apps ≥ 1)", family="gen-club-season-squad")
def atalanta_2324():
    return squad_apps("2023–24 Atalanta BC season", "Europa League").out()


@prompt("gen152", "Name a player who made a UEFA Europa League appearance for Eintracht Frankfurt in their 2021–22 winning run",
        "en:2021–22 Eintracht Frankfurt season — appearances table (Europa League apps ≥ 1)", family="gen-club-season-squad")
def frankfurt_2122():
    return squad_apps("2021–22 Eintracht Frankfurt season", "Europa League").out()


@prompt("gen153", "Name a stadium that has hosted a UEFA Cup or Europa League final since 1998",
        "en:List of UEFA Cup and Europa League finals — venue of single-match finals (1997–98 onward)",
        family="gen-final-venues")
def uel_final_venues():
    tb = find_tab("List of UEFA Cup and Europa League finals", ["Season", "Winners", "Runners-up", "Venue"], heading="List of finals")
    vi = tb.col("Venue")
    acc = Acc("club")
    for tx, ln in tb.body:
        m = re.match(r"(\d{4})", tx[0])
        if m and int(m.group(1)) >= 1997 and ln[vi]:
            acc.add(ln[vi][0][0], ln[vi][0][1], tx[0])
    return acc.out()


def _super_cup():
    return find_tab("List of UEFA Super Cup matches", ["Year", "Winner", "Runner-up", "Venue"], heading="Winners")


@prompt("gen154", "Name a stadium that has hosted a UEFA Super Cup since 1998",
        "en:List of UEFA Super Cup matches — venue column, 1998 onward", family="gen-final-venues")
def super_cup_venues():
    tb = _super_cup()
    vi = tb.col("Venue")
    acc = Acc("club")
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and int(tx[0][:4]) >= 1998 and ln[vi]:
            acc.add(ln[vi][0][0], ln[vi][0][1], tx[0])
    return acc.out()


@prompt("gen155", "Name a player who has scored in a UEFA Super Cup from 2010 to 2026 (own goals and shoot-outs excluded)",
        "en:2010 UEFA Super Cup … en:2026 UEFA Super Cup — football-box scorers", family="gen-final-scorers")
def super_cup_scorers():
    acc = Acc()
    for y in range(2010, 2027):
        box_scorers(f"{y} UEFA Super Cup", acc, str(y))
    return acc.out()


@prompt("gen156", "Name a club that has played in the UEFA Super Cup since 2000",
        "en:List of UEFA Super Cup matches — winner and runner-up columns, 2000 onward", family="gen-cup-finalists")
def super_cup_clubs():
    tb = _super_cup()
    wi, ri = tb.col("Winner"), tb.col("Runner-up")
    acc = Acc("club")
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and int(tx[0][:4]) >= 2000:
            for ci in (wi, ri):
                for t, a in _clubs(ln[ci])[:1]:
                    acc.add(t, a, tx[0])
    return acc.out()
