"""gen069-gen086, gen186, gen199: Ligue 1."""
import datetime as dt
import re

from ballion.registry import prompt
from prompts.collectors.gen_bundesliga import _topn
from prompts.collectors.gen_util import (Acc, find_tab, find_tabs, first_person, hattricks, managers_since,
                                         promoted_relegated, season_coaches, squad_apps, tabs, team_col_clubs)

FAM_SQUAD = "gen-club-season-squad"


@prompt("gen069", "Name a player who made a Ligue 1 appearance for Monaco in their 2016–17 title season",
        "en:2016–17 AS Monaco FC season — appearances table (Ligue 1 apps ≥ 1)", family=FAM_SQUAD)
def monaco_1617():
    return squad_apps("2016–17 AS Monaco FC season", "Ligue 1").out()


@prompt("gen070", "Name a player who made a Ligue 1 appearance for Lille in their 2020–21 title season",
        "en:2020–21 Lille OSC season — appearances table (Ligue 1 apps ≥ 1)", family=FAM_SQUAD)
def lille_2021():
    return squad_apps("2020–21 Lille OSC season", "Ligue 1").out()


@prompt("gen071", "Name a player who made a Ligue 1 appearance for PSG under Luis Enrique (2023–24 to 2025–26)",
        "en:2023–24 … 2025–26 Paris Saint-Germain FC season — Ligue 1 apps ≥ 1", family=FAM_SQUAD)
def psg_enrique():
    acc = Acc()
    for s in ("2023–24", "2024–25", "2025–26"):
        squad_apps(f"{s} Paris Saint-Germain FC season", "Ligue 1", label=s, acc=acc)
    return acc.out()


def _unfp(heading, label=""):
    tb = find_tab("Trophées UNFP du football", ["Year", "Player", "Club"], heading=heading)
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], tx[0])
    return acc


@prompt("gen072", "Name a winner of the UNFP Ligue 1 Player of the Year award",
        "en:Ligue 1 Player of the Year — winners table (1993–94 onward)")
def l1_poty():
    tb = find_tab("Ligue 1 Player of the Year", ["Season", "Player", "Club"], heading="Winners")
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], tx[0])
    return acc.out()


@prompt("gen073", "Name a winner of the UNFP Ligue 1 Young Player of the Year award",
        "en:Ligue 1 Young Player of the Year — winners table")
def l1_young():
    tb = find_tab("Ligue 1 Young Player of the Year", ["Season", "Player", "Club"], heading="Winners")
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], tx[0])
    return acc.out()


@prompt("gen199", "Name a winner of the UNFP Ligue 1 Goalkeeper of the Year award",
        "en:Trophées UNFP du football — Goalkeeper of the Year table (2002 onward)")
def l1_keeper():
    return _unfp("Goalkeeper of the Year").out()


@prompt("gen074", "Name a player named in the UNFP Ligue 1 Team of the Year (2015–16 to 2025–26)",
        "en:Trophées UNFP du football — Team of the Year season sections from 2015–16")
def l1_toty():
    acc = Acc()
    for tb in tabs("Trophées UNFP du football"):
        m = re.fullmatch(r"(\d{4})–\d{2}", tb.heading)
        if not m or tb.section != "Ligue 1" or int(m.group(1)) < 2015 or "Player" not in tb.hdr:
            continue
        ci = tb.col("Player")
        for tx, ln in tb.body:
            if p := first_person(ln[ci]):
                acc.add(p[0], p[1], tb.heading)
    return acc.out()


@prompt("gen075", "Name a winner of the UNFP Ligue 1 Player of the Month award since August 2015",
        "en:UNFP Player of the Month — winners table, August 2015 onward")
def l1_potm():
    tb = find_tab("UNFP Player of the Month", ["Month", "Year", "Player"], heading="Winners")
    ci, mi, yi = tb.col("Player"), tb.col("Month"), tb.col("Year")
    acc = Acc()
    for tx, ln in tb.body:
        ys = re.findall(r"\d{4}", tx[yi])
        if not ys:
            continue
        y = int(ys[-1])
        if y > 2015 or (y == 2015 and tx[mi].strip() in ("August", "September", "October", "November", "December")):
            if p := first_person(ln[ci]):
                acc.add(p[0], p[1], f"{tx[mi]} {y}")
    return acc.out()


@prompt("gen076", "Name a player who has scored a Ligue 1 hat-trick since the start of 2015–16",
        "en:List of Ligue 1 hat-tricks — decade tables, dated 2015-08-01 or later", family="gen-league-hattricks")
def l1_hattricks():
    return hattricks("List of Ligue 1 hat-tricks", dt.date(2015, 8, 1), extra_hdr=("Nationality", "Against")).out()


@prompt("gen077", "Name a player who finished in the top 5 of the Ligue 1 scoring chart in a season from 2017–18 to 2025–26",
        "en:2017–18 Ligue 1 … en:2025–26 Ligue 1 — top goalscorers table, ranks 1–5 incl. ties",
        family="gen-league-top5-scorers")
def l1_top5():
    return _topn("{s} Ligue 1", 2017, 2025, 5)


@prompt("gen078", "Name a head coach who managed a Ligue 1 club during 2025–26",
        "en:2025–26 Ligue 1 — personnel table + managerial changes", family="gen-season-coaches")
def l1_coaches():
    return season_coaches("2025–26 Ligue 1").out()


@prompt("gen079", "Name a club promoted to Ligue 1 between 2015 and 2026",
        "en:2014–15 Ligue 1 … en:2026–27 Ligue 1 — league tables: clubs in a season but not the previous one",
        family="gen-promoted-relegated")
def l1_promoted():
    return promoted_relegated("{s} Ligue 1", 2015, 2026, "promoted").out()


@prompt("gen186", "Name a club relegated from Ligue 1 between 2015–16 and 2025–26",
        "en:2015–16 Ligue 1 … en:2026–27 Ligue 1 — league tables: clubs in a season but not the next",
        family="gen-promoted-relegated")
def l1_relegated():
    return promoted_relegated("{s} Ligue 1", 2015, 2025, "relegated").out()


@prompt("gen080", "Name the home stadium of a club in the 2026–27 Ligue 1",
        "en:2026–27 Ligue 1 — stadiums and locations", family="gen-league-stadiums")
def l1_stadiums():
    return team_col_clubs("2026–27 Ligue 1", stadium=True).out()


@prompt("gen081", "Name a club that has played in a Coupe de France final since 2000",
        "en:List of Coupe de France finals — winners and runners-up, 2000 onward", family="gen-cup-finalists")
def cdf_finalists():
    tb = find_tab("List of Coupe de France finals", ["Date", "Winners", "Runners-up"], heading="Finals")
    wi, ri = tb.col("Winners"), tb.col("Runners-up")
    acc = Acc("club")
    for tx, ln in tb.body:
        ys = re.findall(r"\d{4}", tx[0])
        if not ys or int(ys[-1]) < 2000:
            continue
        for ci in (wi, ri):
            for t, a in ln[ci][:1]:
                acc.add(t, a, ys[-1])
    return acc.out()


@prompt("gen082", "Name a PSG head coach since 2000",
        "en:List of Paris Saint-Germain FC managers — tenures touching 2000 or later", family="gen-club-managers")
def psg_managers():
    return managers_since("List of Paris Saint-Germain FC managers").out()
