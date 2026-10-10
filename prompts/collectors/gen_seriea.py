"""gen047-gen068, gen185: Serie A."""
import datetime as dt
import re

from ballion.registry import prompt
from prompts.collectors.gen_bundesliga import _topn
from prompts.collectors.gen_util import (Acc, box_scorers, find_tab, first_person, foreign_list, hattricks,
                                         managers_since, promoted_relegated, season_coaches, squad_apps, tabs,
                                         team_col_clubs)

FAM_SQUAD = "gen-club-season-squad"


@prompt("gen047", "Name a player who made a Serie A appearance for Napoli in their 2022–23 Scudetto season",
        "en:2022–23 SSC Napoli season — appearances table (Serie A apps ≥ 1)", family=FAM_SQUAD)
def napoli_2223():
    return squad_apps("2022–23 SSC Napoli season", "Serie A").out()


@prompt("gen048", "Name a player who made a Serie A appearance for Napoli in their 2024–25 title season",
        "en:2024–25 SSC Napoli season — appearances table (Serie A apps ≥ 1)", family=FAM_SQUAD)
def napoli_2425():
    return squad_apps("2024–25 SSC Napoli season", "Serie A").out()


@prompt("gen049", "Name a player who made a Serie A appearance for Inter in their 2023–24 title season",
        "en:2023–24 Inter Milan season — appearances table (Serie A apps ≥ 1)", family=FAM_SQUAD)
def inter_2324():
    return squad_apps("2023–24 Inter Milan season", "Serie A").out()


@prompt("gen050", "Name a player who made a Serie A appearance for AC Milan in their 2021–22 title season",
        "en:2021–22 AC Milan season — appearances table (Serie A apps ≥ 1)", family=FAM_SQUAD)
def milan_2122():
    return squad_apps("2021–22 AC Milan season", "Serie A").out()


@prompt("gen051", "Name a player who made a Serie A appearance for Juventus in a title season from 2011–12 to 2019–20",
        "en:2011–12 Juventus FC season … en:2019–20 Juventus FC season — Serie A apps ≥ 1", family=FAM_SQUAD)
def juve_nine():
    acc = Acc()
    for y in range(2011, 2020):
        s = f"{y}–{str(y + 1)[2:]}"
        squad_apps(f"{s} Juventus FC season", "Serie A", label=s, acc=acc)
    return acc.out()


@prompt("gen052", "Name a player who has scored a Serie A hat-trick since the start of 2015–16",
        "en:List of Serie A hat-tricks — hat-trick table, dated 2015-08-01 or later", family="gen-league-hattricks")
def sa_hattricks():
    return hattricks("List of Serie A hat-tricks", dt.date(2015, 8, 1), heading="Hat-tricks", extra_hdr=("Nationality",)).out()


@prompt("gen053", "Name a player who finished in the top 5 of the Serie A scoring chart in a season from 2017–18 to 2025–26",
        "en:2017–18 Serie A … en:2025–26 Serie A — top goalscorers table, ranks 1–5 incl. ties",
        family="gen-league-top5-scorers")
def sa_top5():
    return _topn("{s} Serie A", 2017, 2025, 5)


@prompt("gen054", "Name a player named in the AIC Serie A Team of the Year (2018–19 to 2024–25)",
        "en:Serie A Team of the Year — season sections 2018–19 onward")
def sa_toty():
    acc = Acc()
    for tb in tabs("Serie A Team of the Year"):
        m = re.fullmatch(r"(\d{4})–\d{2}", tb.heading)
        if not m or int(m.group(1)) < 2018 or "Player" not in tb.hdr:
            continue
        ci = tb.col("Player")
        for tx, ln in tb.body:
            if p := first_person(ln[ci]):
                acc.add(p[0], p[1], tb.heading)
    return acc.out()


@prompt("gen055", "Name a winner of the Serie A Footballer of the Year (MVP) award",
        "en:Serie A Footballer of the Year — list of winners, 1996–97 to present")
def sa_foty():
    tb = find_tab("Serie A Footballer of the Year", ["Season", "Position", "Player"], heading="List of winners")
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], tx[0])
    return acc.out()


@prompt("gen056", "Name a winner of the Serie A Young Footballer of the Year award",
        "en:Serie A Young Footballer of the Year — winners table")
def sa_young():
    tb = find_tab("Serie A Young Footballer of the Year", ["Year", "Player", "Club"], heading="Winners")
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], tx[0])
    return acc.out()


@prompt("gen057", "Name an English player who has played in Serie A", "en:List of foreign Serie A players — England",
        family="gen-nationality-in-league")
def sa_england():
    return foreign_list("List of foreign Serie A players", "England").out()


@prompt("gen058", "Name a Japanese player who has played in Serie A", "en:List of foreign Serie A players — Japan",
        family="gen-nationality-in-league")
def sa_japan():
    return foreign_list("List of foreign Serie A players", "Japan").out()


@prompt("gen059", "Name a head coach who managed a Serie A club during 2025–26",
        "en:2025–26 Serie A — personnel table + managerial changes", family="gen-season-coaches")
def sa_coaches():
    return season_coaches("2025–26 Serie A").out()


@prompt("gen060", "Name a club relegated from Serie A between 2015–16 and 2025–26",
        "en:2015–16 Serie A … en:2026–27 Serie A — league tables: clubs in a season but not the next",
        family="gen-promoted-relegated")
def sa_relegated():
    return promoted_relegated("{s} Serie A", 2015, 2025, "relegated").out()


@prompt("gen185", "Name a club promoted to Serie A between 2015 and 2026",
        "en:2014–15 Serie A … en:2026–27 Serie A — league tables: clubs in a season but not the previous one",
        family="gen-promoted-relegated")
def sa_promoted():
    return promoted_relegated("{s} Serie A", 2015, 2026, "promoted").out()


@prompt("gen061", "Name the home stadium of a club in the 2026–27 Serie A",
        "en:2026–27 Serie A — stadiums and locations (shared grounds counted once)", family="gen-league-stadiums")
def sa_stadiums():
    return team_col_clubs("2026–27 Serie A", stadium=True).out()


@prompt("gen062", "Name a player who has scored in a Coppa Italia final from 2010 to 2026 (own goals and shoot-outs excluded)",
        "en:2010 Coppa Italia final … en:2026 Coppa Italia final — football-box scorers", family="gen-final-scorers")
def coppa_scorers():
    acc = Acc()
    for y in range(2010, 2027):
        box_scorers(f"{y} Coppa Italia final", acc, str(y))
    return acc.out()


@prompt("gen063", "Name a Juventus head coach since 2000", "en:List of Juventus FC managers — tenures touching 2000 or later",
        family="gen-club-managers")
def juve_managers():
    return managers_since("List of Juventus FC managers").out()


@prompt("gen064", "Name an AC Milan head coach since 2000", "en:List of AC Milan managers — seasons 2000 onward",
        family="gen-club-managers")
def milan_managers():
    return managers_since("List of AC Milan managers").out()


@prompt("gen065", "Name an Inter head coach since 2000", "en:List of Inter Milan managers — tenures 2000 onward",
        family="gen-club-managers")
def inter_managers():
    return managers_since("List of Inter Milan managers").out()
