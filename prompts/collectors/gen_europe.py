"""gen087-gen107, gen187-gen189, gen200: Netherlands, Portugal, Scotland, Turkey, unbeaten seasons."""
import datetime as dt
import re

from ballion.registry import prompt
from prompts.collectors.gen_bundesliga import _topn
from prompts.collectors.gen_util import (Acc, dedupe, find_tab, find_tabs, first_person, hattricks, managers_since,
                                         people, season_label, squad_apps, tabs, team_col_clubs, top_scorers,
                                         league_table_clubs, resolve)

FAM_SQUAD = "gen-club-season-squad"


@prompt("gen087", "Name a player who made an Eredivisie appearance for Ajax in 2018–19",
        "en:2018–19 AFC Ajax season — player statistics table (Eredivisie apps ≥ 1)", family=FAM_SQUAD)
def ajax_1819():
    return squad_apps("2018–19 AFC Ajax season", "Eredivisie").out()


@prompt("gen088", "Name a player who made an Eredivisie appearance for Feyenoord in their 2022–23 title season",
        "en:2022–23 Feyenoord season — appearances table (Eredivisie apps ≥ 1)", family=FAM_SQUAD)
def feyenoord_2223():
    return squad_apps("2022–23 Feyenoord season", "Eredivisie").out()


@prompt("gen089", "Name a player who has scored an Eredivisie hat-trick since the start of 2015–16",
        "en:List of Eredivisie hat-tricks — dated 2015-08-01 or later", family="gen-league-hattricks")
def ere_hattricks():
    return hattricks("List of Eredivisie hat-tricks", dt.date(2015, 8, 1), extra_hdr=("Club", "Goals")).out()


@prompt("gen090", "Name a player who finished as Eredivisie top scorer in a season from 2005–06 to 2025–26",
        "en:2005–06 Eredivisie … en:2025–26 Eredivisie — top scorers tables, rank 1 incl. ties",
        family="gen-league-top-scorer")
def ere_topscorers():
    return _topn("{s} Eredivisie", 2005, 2025, 1)


@prompt("gen189", "Name a player who finished in the top 5 of the Eredivisie scoring chart in a season from 2020–21 to 2025–26",
        "en:2020–21 Eredivisie … en:2025–26 Eredivisie — top scorers tables, ranks 1–5 incl. ties",
        family="gen-league-top5-scorers")
def ere_top5():
    return _topn("{s} Eredivisie", 2020, 2025, 5)


@prompt("gen091", "Name a winner of the Eredivisie Player of the Month award (2017–18 onward)",
        "en:Eredivisie Player of the Month — list of winners")
def ere_potm():
    tb = find_tab("Eredivisie Player of the Month", ["Month", "Year", "Player"], heading="List of winners")
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[1]) and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], f"{tx[0]} {tx[1]}")
    return acc.out()


@prompt("gen092", "Name a club playing in the 2026–27 Eredivisie", "en:2026–27 Eredivisie — stadiums and locations (club column)",
        family="gen-current-league-clubs")
def ere_clubs():
    return team_col_clubs("2026–27 Eredivisie").out()


@prompt("gen187", "Name the home stadium of a club in the 2026–27 Eredivisie", "en:2026–27 Eredivisie — stadiums and locations",
        family="gen-league-stadiums")
def ere_stadiums():
    return team_col_clubs("2026–27 Eredivisie", stadium=True).out()


# ---------------------------------------------------------------- Portugal
@prompt("gen095", "Name a player in Sporting CP's first-team squad in their 2020–21 title season",
        "en:2020–21 Sporting CP season — 'First-team squad' tables", family=FAM_SQUAD)
def sporting_2021():
    acc = Acc()
    for tb in tabs("2020–21 Sporting CP season"):
        if tb.heading != "First-team squad" or "Player" not in tb.hdr:
            continue
        ci = tb.col("Player")
        for tx, ln in tb.body:
            if p := first_person(ln[ci]):
                acc.add(p[0], p[1], "squad")
    return acc.out()


@prompt("gen096", "Name a player who finished as Primeira Liga top scorer in a season from 2000–01 to 2025–26",
        "en:List of Portuguese football champions — 'Bota de Prata (Top Scorer)' column, 2000–01 onward",
        family="gen-league-top-scorer")
def pl_topscorers():
    tb = find_tab("List of Portuguese football champions", [], heading="List of champions and top scorers")
    h2 = tb.rows[1][0]
    pi = next(i for i, h in enumerate(h2) if "Top Scorer" in h)
    acc = Acc()
    for tx, ln in tb.rows[2:]:
        m = re.match(r"(\d{4})", tx[1])
        if not m or int(m.group(1)) < 2000:
            continue
        for t, a in people(ln[pi]):
            acc.add(t, a, tx[1])
    return acc.out()


@prompt("gen097", "Name a winner of the LPFP Primeira Liga Player of the Year award",
        "en:LPFP Primeira Liga Player of the Year — list of winners (2005–06 onward)")
def pl_poty():
    tb = find_tab("LPFP Primeira Liga Player of the Year", ["Season", "Player", "Club"], heading="List of winners")
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], tx[0])
    return acc.out()


@prompt("gen098", "Name a club playing in the 2026–27 Primeira Liga",
        "en:2026–27 Primeira Liga — location and stadiums table", family="gen-current-league-clubs")
def pl_clubs():
    return team_col_clubs("2026–27 Primeira Liga", heading="Location and stadiums", col="Team").out()


@prompt("gen188", "Name the home stadium of a club in the 2026–27 Primeira Liga",
        "en:2026–27 Primeira Liga — location and stadiums table", family="gen-league-stadiums")
def pl_stadiums():
    return team_col_clubs("2026–27 Primeira Liga", heading="Location and stadiums", col="Team", stadium=True).out()


@prompt("gen099", "Name an FC Porto head coach since 2000", "en:List of FC Porto managers — tenures touching 2000 or later",
        family="gen-club-managers")
def porto_managers():
    return managers_since("List of FC Porto managers").out()


@prompt("gen100", "Name a Benfica head coach since 2000", "en:List of S.L. Benfica managers — tenures touching 2000 or later",
        family="gen-club-managers")
def benfica_managers():
    return managers_since("List of S.L. Benfica managers").out()


# ---------------------------------------------------------------- Scotland
@prompt("gen102", "Name a player who made a Scottish Premiership appearance for Celtic in their 2016–17 invincible season",
        "en:2016–17 Celtic F.C. season — squad appearances table (league apps ≥ 1)", family=FAM_SQUAD)
def celtic_1617():
    return squad_apps("2016–17 Celtic F.C. season", "League").out()


@prompt("gen103", "Name a club that has played in the Scottish Premiership (2013–14 to 2026–27)",
        "en:2013–14 Scottish Premiership … en:2026–27 Scottish Premiership — league tables")
def spfl_clubs():
    acc = Acc("club")
    for y in range(2013, 2027):
        s = season_label(y)
        for t, a in league_table_clubs(f"{s} Scottish Premiership"):
            acc.add(t, a, s)
    return acc.out()


@prompt("gen200", "Name a club playing in the 2026–27 Scottish Premiership",
        "en:2026–27 Scottish Premiership — league table", family="gen-current-league-clubs")
def spfl_2627():
    acc = Acc("club")
    for t, a in league_table_clubs("2026–27 Scottish Premiership"):
        acc.add(t, a, "2026–27")
    return acc.out()


# ---------------------------------------------------------------- Turkey
@prompt("gen104", "Name a player who finished as Süper Lig top scorer in a season from 2000–01 to 2025–26",
        "en:List of Süper Lig top scorers — top scorers by season, 2000–01 onward", family="gen-league-top-scorer")
def sl_topscorers():
    tb = find_tab("List of Süper Lig top scorers", ["Season", "Top scorer(s)"], heading="Top scorers by season")
    ci = tb.col("Top scorer(s)")
    acc = Acc()
    for tx, ln in tb.body:
        m = re.match(r"(\d{4})", tx[0])
        if not m or int(m.group(1)) < 2000:
            continue
        for t, a in people(ln[ci]):
            acc.add(t, a, tx[0])
    return acc.out()


@prompt("gen105", "Name a club playing in the 2026–27 Süper Lig", "en:2026–27 Süper Lig — stadiums and locations (team column)",
        family="gen-current-league-clubs")
def sl_clubs():
    return team_col_clubs("2026–27 Süper Lig").out()


@prompt("gen107", "Name a European club that went a whole top-flight league season unbeaten (men's)",
        "en:List of unbeaten football club seasons — Europe (men's)")
def unbeaten():
    tb = find_tabs("List of unbeaten football club seasons", ["Season", "Nation", "Club", "Matches"], heading="Europe")[0]
    ci = tb.col("Club")
    acc = Acc("club")
    for tx, ln in tb.body:
        if ln[ci]:
            acc.add(ln[ci][0][0], ln[ci][0][1], f"{tx[0]} ({tx[1]})")
    return acc.out()
