"""gen108-gen123, gen191-gen193: MLS and North America."""
import datetime as dt
import re

from ballion.registry import prompt
from prompts.collectors.gen_bundesliga import _topn
from prompts.collectors.gen_util import (Acc, box_scorers, find_tab, find_tabs, first_person, hattricks, people,
                                         season_coaches, squad_apps, tabs, team_col_clubs)


@prompt("gen108", "Name a player who has played for Inter Miami since the start of 2023 (the Messi era)",
        "en:2023 Inter Miami CF season … en:2026 Inter Miami CF season — appearances tables (total apps ≥ 1)",
        family="gen-club-season-squad")
def inter_miami():
    acc = Acc()
    for y in range(2023, 2027):
        squad_apps(f"{y} Inter Miami CF season", "Total", label=str(y), acc=acc)
    return acc.out()


@prompt("gen109", "Name a Designated Player of Inter Miami or LAFC",
        "en:Designated Player Rule — Inter Miami CF and Los Angeles FC sections", family="gen-designated-players")
def dp_miami_lafc():
    acc = Acc()
    for h in ("Inter Miami CF", "Los Angeles FC"):
        tb = find_tab("Designated Player Rule", ["Player", "Years as DP"], heading=f"^{h}$")
        ci = tb.col("Player")
        for tx, ln in tb.body:
            if p := first_person(ln[ci]):
                acc.add(p[0], p[1], h)
    return acc.out()


@prompt("gen110", "Name a Designated Player of the LA Galaxy",
        "en:Designated Player Rule — LA Galaxy section", family="gen-designated-players")
def dp_galaxy():
    tb = find_tab("Designated Player Rule", ["Player", "Years as DP"], heading=r"^LA Galaxy$")
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if p := first_person(ln[ci]):
            acc.add(p[0], p[1], tx[tb.col("Years as DP")])
    return acc.out()


def _season_table(page, heading, hdr):
    tb = find_tab(page, hdr, heading=heading)
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], tx[0])
    return acc


@prompt("gen111", "Name a winner of the MLS MVP award (1996–2025)",
        "en:Landon Donovan MVP Award — winners table")
def mls_mvp():
    return _season_table("Landon Donovan MVP Award", "Winners", ["Season", "Player", "Club"]).out()


@prompt("gen112", "Name a winner of the MLS Golden Boot (1996–2025)",
        "en:MLS Golden Boot — winners tables (1996–2004 and 2005–present)")
def mls_golden_boot():
    acc = Acc()
    for tb in find_tabs("MLS Golden Boot", ["Season", "Player", "Club"]):
        ci = tb.col("Player")
        for tx, ln in tb.body:
            if re.match(r"\d{4}", tx[0]) and (p := first_person(ln[ci])):
                acc.add(p[0], p[1], tx[0])
    return acc.out()


def _best_xi(since):
    from ballion.wiki import resolve
    cl = [ln[0][0][0] for tx, ln in find_tab("MLS Best XI", ["Club", "Apps"], heading="Appearances by team").body if ln and ln[0]]
    tb = find_tab("MLS Best XI", ["Year", "Goalkeeper"], heading="Winners")
    cand = []
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and int(tx[0]) >= since:
            for cell in ln[1:]:
                cand += [(t, a, tx[0]) for t, a in cell if not t.endswith("season")]
    res = resolve(cl + [t for t, _, _ in cand])
    clubs = {res[t]["title"] for t in cl}
    acc = Acc()
    for t, a, y in cand:
        if res[t]["title"] not in clubs:
            acc.add(t, a, y)
    return acc


@prompt("gen113", "Name a player named in the MLS Best XI since 2015",
        "en:MLS Best XI — winners table, 2015 onward (player links; club links excluded)")
def mls_best_xi():
    return _best_xi(2015).out()


@prompt("gen114", "Name a winner of the MLS Newcomer of the Year award",
        "en:MLS Newcomer of the Year Award — winners table")
def mls_newcomer():
    return _season_table("MLS Newcomer of the Year Award", "Winners", ["Season", "Player", "Club"]).out()


@prompt("gen115", "Name a player who has scored an MLS hat-trick since the start of 2015 (regular season or playoffs)",
        "en:List of Major League Soccer hat-tricks — 2010s, 2020s and playoff tables, dated 2015-01-01 or later",
        family="gen-league-hattricks")
def mls_hattricks():
    return hattricks("List of Major League Soccer hat-tricks", dt.date(2015, 1, 1), extra_hdr=("Nationality", "For")).out()


def _list(page, label):
    tb = find_tab(page, ["Rank", "Player"], heading="List")
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if tx[0].strip().isdigit() and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], tx[2])
    return acc.out()


@prompt("gen116", "Name a player who has scored 100 or more MLS regular-season goals",
        "en:List of Major League Soccer players with 100 or more goals", family="gen-mls-milestones")
def mls_100_goals():
    return _list("List of Major League Soccer players with 100 or more goals", "goals")


@prompt("gen117", "Name a player who has made 400 or more MLS regular-season appearances",
        "en:List of Major League Soccer players with 400 or more games played", family="gen-mls-milestones")
def mls_400_games():
    return _list("List of Major League Soccer players with 400 or more games played", "apps")


@prompt("gen118", "Name a club that has won the MLS Cup (1996–2025)",
        "en:MLS Cup — 'MLS Cup titles' table, clubs with at least one title")
def mls_cup_winners():
    tb = find_tab("MLS Cup", ["Apps", "Team", "Champion(s)"], heading="MLS Cup titles")
    ci, wi = tb.col("Team"), tb.col("Champion(s)")
    acc = Acc("club")
    for tx, ln in tb.body:
        if tx[wi].strip().isdigit() and int(tx[wi]) > 0 and ln[ci]:
            acc.add(ln[ci][0][0], ln[ci][0][1], f"{tx[wi]} title(s)")
    return acc.out()


@prompt("gen119", "Name a player who has scored in an MLS Cup final from 2010 to 2025 (own goals and shoot-outs excluded)",
        "en:MLS Cup 2010 … en:MLS Cup 2025 — football-box scorers", family="gen-final-scorers")
def mls_cup_scorers():
    acc = Acc()
    for y in range(2010, 2026):
        box_scorers(f"MLS Cup {y}", acc, str(y))
    return acc.out()


@prompt("gen120", "Name a stadium that is or was home to an MLS club",
        "en:List of Major League Soccer stadiums — current, former and defunct-team stadium tables")
def mls_stadiums():
    acc = Acc("club")
    for tb in find_tabs("List of Major League Soccer stadiums", ["Stadium", "Capacity", "Opened"]):
        if tb.heading in ("Future stadiums",):
            continue
        ci = tb.col("Stadium")
        for tx, ln in tb.body:
            if ln[ci]:
                acc.add(ln[ci][0][0], ln[ci][0][1], tb.heading)
    return acc.out()


@prompt("gen121", "Name a club that has played the MLS All-Stars in an MLS All-Star Game",
        "en:MLS All-Star Game — 'MLS All-Stars vs invited opponents' table")
def mls_allstar_opponents():
    tb = find_tab("MLS All-Star Game", ["Team", "Won", "Lost"], heading="invited opponents")
    acc = Acc("club")
    for tx, ln in tb.body:
        if tx[0].startswith("MLS All-Stars") or not ln[0] or re.search(r"All-Star|national|Federation", ln[0][-1][0] + " " + tx[0]) or tx[0] == "United States" or ln[0][-1][0] == "Liga MX":
            continue
        acc.add(ln[0][-1][0], ln[0][-1][1], tx[3] + " game(s)")
    return acc.out()


@prompt("gen122", "Name a head coach who managed an MLS club in the 2026 season (to October 2026)",
        "en:2026 Major League Soccer season — personnel table + coaching changes", family="gen-season-coaches")
def mls_coaches():
    return season_coaches("2026 Major League Soccer season").out()


@prompt("gen123", "Name a club playing in the 2026–27 Liga MX season",
        "en:2026–27 Liga MX season — stadiums and locations (club column)", family="gen-current-league-clubs")
def ligamx_clubs():
    return team_col_clubs("2026–27 Liga MX season", col="Club").out()


@prompt("gen192", "Name a player in either squad for the 2025 MLS All-Star Game (MLS All-Stars or Liga MX All-Stars)",
        "en:2025 MLS All-Star Game — MLS All-Stars and Liga MX All-Stars squad tables")
def allstar_2025():
    acc = Acc()
    for h in ("MLS All-Stars", "Liga MX All-Stars"):
        tb = find_tab("2025 MLS All-Star Game", ["Player", "Club"], heading=f"^{h}$")
        ci = tb.col("Player")
        for tx, ln in tb.body:
            if p := first_person(ln[ci]):
                acc.add(p[0], p[1], h)
    return acc.out()
