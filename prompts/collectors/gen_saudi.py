"""gen124-gen133, gen190, gen194: Saudi Pro League and Asia."""
import datetime as dt
import re

from ballion.registry import prompt
from prompts.collectors.gen_bundesliga import _topn
from prompts.collectors.gen_util import (Acc, box_scorers, find_tab, find_tabs, first_person, foreign_list, hattricks,
                                         people, season_coaches, squad_apps, tabs, team_col_clubs)

FAM_SQUAD = "gen-club-season-squad"


@prompt("gen124", "Name a club playing in the 2026–27 Saudi Pro League",
        "en:2026–27 Saudi Pro League — stadiums table (team column)", family="gen-current-league-clubs")
def spl_clubs():
    return team_col_clubs("2026–27 Saudi Pro League", heading="Stadiums").out()


@prompt("gen125", "Name a player who finished as top scorer of a Saudi top-flight season",
        "en:Saudi Pro League — 'Top scorers by season' table (1974–75 onward)", family="gen-league-top-scorer")
def spl_topscorers():
    tb = find_tab("Saudi Pro League", ["Season", "Top scorer(s)", "Goals"], heading="Top scorers by season")
    ci = tb.col("Top scorer(s)")
    acc = Acc()
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]):
            for t, a in people(ln[ci]):
                acc.add(t, a, tx[0])
    return acc.out()


@prompt("gen126", "Name a player who made a Saudi Pro League appearance for Al-Nassr in 2023–24",
        "en:2023–24 Al-Nassr FC season — appearances table (league apps ≥ 1)", family=FAM_SQUAD)
def nassr_2324():
    return squad_apps("2023–24 Al-Nassr FC season", "League|Pro League").out()


@prompt("gen127", "Name a player who made a Saudi Pro League appearance for Al-Hilal in their record-breaking 2023–24 season",
        "en:2023–24 Al Hilal SFC season — appearances table (league apps ≥ 1)", family=FAM_SQUAD)
def hilal_2324():
    return squad_apps("2023–24 Al Hilal SFC season", "League|Pro League").out()


@prompt("gen128", "Name a player who made a Saudi Pro League appearance for Al-Ittihad in their 2024–25 title season",
        "en:2024–25 Al-Ittihad Club season — appearances table (league apps ≥ 1)", family=FAM_SQUAD)
def ittihad_2425():
    return squad_apps("2024–25 Al-Ittihad Club season", "League|Pro League").out()


@prompt("gen129", "Name a Portuguese player who has played in the Saudi Pro League",
        "en:List of foreign Saudi Professional League players — Portugal", family="gen-nationality-in-league")
def spl_portugal():
    return foreign_list("List of foreign Saudi Professional League players", "Portugal").out()


@prompt("gen130", "Name a French player who has played in the Saudi Pro League",
        "en:List of foreign Saudi Professional League players — France", family="gen-nationality-in-league")
def spl_france():
    return foreign_list("List of foreign Saudi Professional League players", "France").out()


@prompt("gen131", "Name a player who has scored a Saudi Pro League hat-trick since the start of 2023–24",
        "en:List of Saudi Pro League hat-tricks — dated 2023-08-01 or later", family="gen-league-hattricks")
def spl_hattricks():
    return hattricks("List of Saudi Pro League hat-tricks", dt.date(2023, 8, 1)).out()


@prompt("gen132", "Name a head coach who managed a Saudi Pro League club between 2023–24 and 2025–26",
        "en:2023–24 … 2025–26 Saudi Pro League — personnel tables + managerial changes", family="gen-season-coaches")
def spl_coaches():
    acc = Acc()
    for s in ("2023–24", "2024–25", "2025–26"):
        # merge by title
        for r in season_coaches(f"{s} Saudi Pro League").d.values():
            acc.add(r["enwiki"], r["answer"], s)
    return acc.out()


@prompt("gen133", "Name a club in the league stage of the 2025–26 AFC Champions League Elite",
        "en:2025–26 AFC Champions League Elite — West and East Region league-stage tables", family="gen-current-league-clubs")
def acle_clubs():
    acc = Acc("club")
    for tb in tabs("2025–26 AFC Champions League Elite"):
        if tb.hdr[:1] == ["Pos"] and tb.heading in ("West Region", "East Region") and len(tb.body) == 12:
            ti = next(i for i, h in enumerate(tb.hdr) if h.startswith("Team"))
            for tx, ln in tb.body:
                if ln[ti]:
                    acc.add(ln[ti][-1][0], ln[ti][-1][1], tb.heading)
    return acc.out()


@prompt("gen190", "Name a player who finished in the top 10 of the Saudi Pro League scoring chart in a season from 2023–24 to 2025–26",
        "en:2023–24 … 2025–26 Saudi Pro League — top scorers table, ranks 1–10 incl. ties",
        family="gen-league-top5-scorers")
def spl_top5():
    return _topn("{s} Saudi Pro League", 2023, 2025, 10)


@prompt("gen194", "Name a player who scored in the 2024–25 AFC Champions League Elite knockout stage (own goals excluded)",
        "en:2024–25 AFC Champions League Elite knockout stage — football-box scorers", family="gen-final-scorers")
def acle_scorers():
    return box_scorers("2024–25 AFC Champions League Elite knockout stage").out()
