"""gen030-gen046, gen183, gen184: Bundesliga."""
import datetime as dt
import re

from ballion.registry import prompt
from prompts.collectors.gen_util import (Acc, box_scorers, dedupe, find_tab, find_tabs, first_person, foreign_list,
                                         hattricks, people, promoted_relegated, season_label, season_coaches, squad_apps, tabs,
                                         team_changes, team_col_clubs, top_scorers)


# ---------------------------------------------------------------- squads
@prompt("gen030", "Name a player who made a Bundesliga appearance for Bayer Leverkusen in their unbeaten 2023–24 title season",
        "en:2023–24 Bayer 04 Leverkusen season — appearances table (Bundesliga apps ≥ 1)", family="gen-club-season-squad")
def lev_2324():
    return squad_apps("2023–24 Bayer 04 Leverkusen season", "Bundesliga").out()


@prompt("gen031", "Name a player who made a Bundesliga appearance for Bayern Munich in 2024–25 or 2025–26",
        "en:2024–25 FC Bayern Munich season; en:2025–26 FC Bayern Munich season — Bundesliga apps ≥ 1",
        family="gen-club-season-squad")
def bayern_kompany():
    acc = Acc()
    for s in ("2024–25", "2025–26"):
        squad_apps(f"{s} FC Bayern Munich season", "Bundesliga", label=s, acc=acc)
    return acc.out()


@prompt("gen032", "Name a player who has scored a Bundesliga hat-trick since the start of 2015–16",
        "en:List of Bundesliga hat-tricks — hat-trick table, dated 2015-08-01 or later", family="gen-league-hattricks")
def bl_hattricks():
    return hattricks("List of Bundesliga hat-tricks", dt.date(2015, 8, 1), heading="Hat-tricks", extra_hdr=("Nationality",)).out()


@prompt("gen033", "Name a player named in the Bundesliga Team of the Season (2017–18 to 2025–26)",
        "en:Bundesliga Awards — Team of the Season winners table (+ 2025–26 season page)")
def bl_toty():
    acc = Acc()
    tb = find_tab("Bundesliga Awards", ["Season", "Goalkeeper"], outer=True)
    for tx, ln in tb.body:
        m = re.match(r"(\d{4})–", tx[0])
        if not m or int(m.group(1)) < 2017:
            continue
        for ci in range(1, 5):
            for t, a in ln[ci]:
                acc.add(t, a, tx[0])
    return acc.out()


def _topn(fmt, y0, y1, n, page_kind="Goals"):
    acc = Acc()
    for y in range(y0, y1 + 1):
        s = season_label(y)
        top_scorers(fmt.format(s=s), n, acc, s, heading=r"scorers", kind=page_kind)
    return acc.out()


@prompt("gen034", "Name a player who finished in the top 5 of the Bundesliga scoring chart in a season from 2017–18 to 2025–26",
        "en:2017–18 Bundesliga … en:2025–26 Bundesliga — top goalscorers table, ranks 1–5 incl. ties",
        family="gen-league-top5-scorers")
def bl_top5():
    return _topn("{s} Bundesliga", 2017, 2025, 5)


# ---------------------------------------------------------------- foreign players
def _foreign(heading, label):
    return foreign_list("List of foreign Bundesliga players", heading, label=label).out()


@prompt("gen035", "Name an American who has played in the Bundesliga", "en:List of foreign Bundesliga players — United States",
        family="gen-nationality-in-league")
def bl_usa():
    return _foreign("United States", "USA")


@prompt("gen036", "Name a Japanese player who has played in the Bundesliga", "en:List of foreign Bundesliga players — Japan",
        family="gen-nationality-in-league")
def bl_japan():
    return _foreign("Japan", "Japan")


@prompt("gen037", "Name an English player who has played in the Bundesliga", "en:List of foreign Bundesliga players — England",
        family="gen-nationality-in-league")
def bl_england():
    return _foreign("England", "England")


@prompt("gen038", "Name a South Korean who has played in the Bundesliga", "en:List of foreign Bundesliga players — Korea Republic",
        family="gen-nationality-in-league")
def bl_korea():
    return _foreign("Korea Republic", "South Korea")


@prompt("gen183", "Name a Moroccan who has played in the Bundesliga", "en:List of foreign Bundesliga players — Morocco",
        family="gen-nationality-in-league")
def bl_morocco():
    return _foreign("Morocco", "Morocco")


# ---------------------------------------------------------------- clubs
@prompt("gen039", "Name a club promoted to the Bundesliga between 2015 and 2026",
        "en:2014–15 Bundesliga … en:2026–27 Bundesliga — league tables: clubs in a season but not the previous one",
        family="gen-promoted-relegated")
def bl_promoted():
    return promoted_relegated("{s} Bundesliga", 2015, 2026, "promoted").out()


@prompt("gen184", "Name a club relegated from the Bundesliga between 2015–16 and 2025–26",
        "en:2015–16 Bundesliga … en:2026–27 Bundesliga — league tables: clubs in a season but not the next",
        family="gen-promoted-relegated")
def bl_relegated():
    return promoted_relegated("{s} Bundesliga", 2015, 2025, "relegated").out()


@prompt("gen040", "Name a head coach who managed a Bundesliga club during 2025–26",
        "en:2025–26 Bundesliga — personnel table + managerial changes", family="gen-season-coaches")
def bl_coaches():
    return season_coaches("2025–26 Bundesliga").out()


@prompt("gen041", "Name the home stadium of a club in the 2026–27 Bundesliga",
        "en:2026–27 Bundesliga — stadiums and locations", family="gen-league-stadiums")
def bl_stadiums():
    return team_col_clubs("2026–27 Bundesliga", stadium=True).out()


@prompt("gen042", "Name a club playing in the 2026–27 2. Bundesliga",
        "en:2026–27 2. Bundesliga — stadiums and locations (team column)", family="gen-current-league-clubs")
def bl2_clubs():
    return team_col_clubs("2026–27 2. Bundesliga").out()


# ---------------------------------------------------------------- DFB-Pokal
@prompt("gen043", "Name a player who has scored in a DFB-Pokal final from 2010 to 2026 (own goals and shoot-outs excluded)",
        "en:2010 DFB-Pokal final … en:2026 DFB-Pokal final — football-box scorers", family="gen-final-scorers")
def dfb_final_scorers():
    acc = Acc()
    for y in range(2010, 2027):
        box_scorers(f"{y} DFB-Pokal final", acc, str(y))
    return acc.out()


@prompt("gen044", "Name a club that has played in a DFB-Pokal final since 2000",
        "en:List of DFB-Pokal finals — winners and runners-up, 2000 onward", family="gen-cup-finalists")
def dfb_finalists():
    tb = find_tab("List of DFB-Pokal finals", ["Season", "Winners", "Runners-up"], heading="Finals")
    wi, ri = tb.col("Winners"), tb.col("Runners-up")
    acc = Acc("club")
    for tx, ln in tb.body:
        m = re.match(r"\d{4}", tx[0])
        if not m or int(m.group()) < 2000:
            continue
        for ci in (wi, ri):
            for t, a in ln[ci][:1]:
                acc.add(t, a, tx[0])
    return acc.out()


@prompt("gen045", "Name a winner of Germany's Footballer of the Year award since 2000",
        "en:Footballer of the Year (Germany) — men's winners table, 2000 onward")
def german_foty():
    tb = find_tab("Footballer of the Year (Germany)", ["Year", "Player", "Club"], heading="Footballer of the Year", nth=0)
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and int(tx[0][:4]) >= 2000 and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], tx[0])
    return acc.out()
