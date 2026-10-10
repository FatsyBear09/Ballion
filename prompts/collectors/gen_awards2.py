"""gen010-gen027: clubs/countries from Ballon d'Or tables, Kopa/Yashin, Best FIFA, Puskas, FIFPRO, UEFA TOTY."""
import re

from ballion.registry import prompt
from prompts.collectors.gen_awards import bdo_table
from prompts.collectors.gen_util import Acc, NAT_TEAM, country_rec, dedupe, find_tab, people, tabs


def _club_links(cell):
    return [(t, a) for t, a in cell if not NAT_TEAM.search(t)]


@prompt("gen010", "Name a club whose player won the men's Ballon d'Or (the player's club at the time)",
        "en:Ballon d'Or — 'Wins by club' table")
def bdo_winner_clubs():
    tb = find_tab("Ballon d'Or", ["Club", "Players", "Wins"], heading="Wins by club")
    ci, wi = tb.col("Club"), tb.col("Wins")
    acc = Acc("club")
    for tx, ln in tb.body:
        for t, a in _club_links(ln[ci])[-1:]:
            acc.add(t, a, f"{tx[wi]} win(s)")
    return acc.out()


@prompt("gen011", "Name a club that had a player nominated for the 2024, 2025 or 2026 Ballon d'Or",
        "en:2024 Ballon d'Or, 2025 Ballon d'Or, 2026 Ballon d'Or — club column of the men's nominee tables")
def bdo_nominee_clubs():
    acc = Acc("club")
    for y in (2024, 2025, 2026):
        tb = bdo_table(y)
        ci = tb.col("Club", "Club(s)")
        for tx, ln in tb.body:
            for t, a in _club_links(ln[ci]):
                acc.add(t, a, str(y))
    return acc.out()


@prompt("gen012", "Name a country with a player nominated for the 2024, 2025 or 2026 Ballon d'Or",
        "en:2024 Ballon d'Or, 2025 Ballon d'Or, 2026 Ballon d'Or — nationality column of the men's nominee tables")
def bdo_nominee_countries():
    out = {}
    for y in (2024, 2025, 2026):
        tb = bdo_table(y)
        ni = tb.col("Nationality")
        for tx, ln in tb.body:
            if len(tx) > ni and tx[ni].strip():
                r = out.setdefault(tx[ni].strip(), country_rec(tx[ni].strip(), ""))
                r["detail"] += (", " if r["detail"] else "") + str(y)
    return dedupe(list(out.values()))


def _ranked(page, heading, hdr, maxrank, acc, label, rank_col="Rank", person_col="Player", year_col=None):
    tb = find_tab(page, hdr, heading=heading)
    ci, ri = tb.col(person_col), tb.col(rank_col)
    yi = tb.col(year_col) if year_col else None
    for tx, ln in tb.body:
        if len(tx) <= max(ci, ri):
            continue
        m = re.match(r"\d+", tx[ri])
        if not m or int(m.group()) > maxrank:
            continue
        yr = tx[yi][:4] if yi is not None else ""
        for t, a in people(ln[ci])[-1:]:
            acc.add(t, a, f"{label}{yr}".strip())
    return acc


@prompt("gen013", "Name a player who finished in the top 3 for the Kopa Trophy (2018–2025, men's)",
        "en:Kopa Trophy — men's winners table, ranks 1–3", family="gen-bdo-nominees")
def kopa_top3():
    return _ranked("Kopa Trophy", "Men's winners", ["Year", "Rank", "Player"], 3, Acc(), "", year_col="Year").out()


@prompt("gen014", "Name a goalkeeper who finished in the top 3 for the men's Yashin Trophy or The Best FIFA Men's Goalkeeper",
        "en:Yashin Trophy — men's winners; en:The Best FIFA Goalkeeper — men's table (ranks 1–3)")
def keeper_top3():
    acc = Acc()
    _ranked("Yashin Trophy", "Men's winners", ["Year", "Rank", "Player"], 3, acc, "Yashin ", year_col="Year")
    _ranked("The Best FIFA Goalkeeper", "Men's Goalkeeper", ["Year", "Rank", "Player"], 3, acc, "Best ", year_col="Year")
    return acc.out()


@prompt("gen015", "Name a player nominated for The Best FIFA Men's Player (2016–2025)",
        "en:The Best FIFA Football Awards 2016 … 2025 — men's player finalists")
def best_fifa_nominees():
    acc = Acc()
    for y in range(2016, 2026):
        tb = find_tab(f"The Best FIFA Football Awards {y}", ["Player"], heading=r"\bMen's Player")
        ci = tb.col("Player")
        for tx, ln in tb.body:
            for t, a in people(ln[ci])[-1:]:
                acc.add(t, a, str(y))
    return acc.out()


@prompt("gen016", "Name a coach who finished in the top 3 for The Best FIFA Men's Coach (2016–2025)",
        "en:The Best FIFA Football Coach — men's winners table, ranks 1–3")
def best_coach_top3():
    return _ranked("The Best FIFA Football Coach", "Men's Coach", ["Year", "Rank", "Coach"], 3, Acc(), "",
                   person_col="Coach", year_col="Year").out()


def _puskas_tables():
    return [tb for tb in tabs("FIFA Puskás Award") if tb.hdr[:2] == ["Rank", "Player"] and re.fullmatch(r"\d{4}", tb.heading)]


@prompt("gen017", "Name a goalscorer nominated for the FIFA Puskás Award (2019–2025)",
        "en:FIFA Puskás Award — year sections 2019–2025, all ranked nominees")
def puskas_nominees():
    acc = Acc()
    for tb in _puskas_tables():
        if int(tb.heading) < 2019:
            continue
        ci = tb.col("Player")
        for tx, ln in tb.body:
            if len(tx) > ci and tx[0].strip():
                for t, a in people(ln[ci])[-1:]:
                    acc.add(t, a, tb.heading)
    return acc.out()


@prompt("gen182", "Name a winner of the FIFA Puskás Award (2009–2025)",
        "en:FIFA Puskás Award — 1st place in each year section")
def puskas_winners():
    acc = Acc()
    for tb in _puskas_tables():
        ci = tb.col("Player")
        for tx, ln in tb.body:
            if tx[0].startswith("1st") and ln[ci]:
                for t, a in people(ln[ci])[-1:]:
                    acc.add(t, a, tb.heading)
    return acc.out()


@prompt("gen018", "Name a country with a FIFA Puskás Award winner (2009–2025)",
        "en:FIFA Puskás Award — nationality (flag) of the 1st-placed player each year")
def puskas_countries():
    out = {}
    for tb in _puskas_tables():
        ci = tb.col("Player")
        for (tx, ln), fl in zip(tb.body, tb.bflags):
            if tx[0].startswith("1st") and fl[ci]:
                r = out.setdefault(fl[ci][0], country_rec(fl[ci][0]))
                r["detail"] += (", " if r["detail"] else "") + f"{tb.heading} {tx[ci]}"
    return dedupe(list(out.values()))


def _world11(tb, cols=None, since=2000, flags=False):
    """Players (or countries) from a FIFPRO World 11 'Winners' table (one row per year)."""
    acc = Acc()
    ctry = {}
    yi = tb.col("Year")
    for (tx, ln), fl in zip(tb.body, tb.bflags):
        if not re.match(r"\d{4}", tx[yi]) or int(tx[yi][:4]) < since:
            continue
        for ci, h in enumerate(tb.hdr):
            if ci == yi or (cols and not re.search(cols, h)):
                continue
            if flags:
                for f in fl[ci]:
                    r = ctry.setdefault(f, country_rec(f))
                    if tx[yi][:4] not in r["detail"]:
                        r["detail"] += (", " if r["detail"] else "") + tx[yi][:4]
            else:
                for t, a in people(ln[ci]):
                    acc.add(t, a, tx[yi][:4])
    return list(ctry.values()) if flags else acc


def _w11_tab(nth):
    return find_tab("FIFPRO World 11", ["Year", "Goalkeeper"], nth=nth, outer=True)


@prompt("gen019", "Name a player named in a FIFPRO Men's World 11 since 2015",
        "en:FIFPRO World 11 — men's winners table, 2015 onward", family="gen-fifpro")
def fifpro_men_since_2015():
    return _world11(_w11_tab(0), since=2015).out()


@prompt("gen020", "Name a goalkeeper or defender named in a FIFPRO Men's World 11 (2005–2025)",
        "en:FIFPRO World 11 — men's winners table, goalkeeper and defender columns", family="gen-fifpro")
def fifpro_men_gk_def():
    return _world11(_w11_tab(0), cols=r"Goalkeeper|Defender").out()


@prompt("gen021", "Name a country represented in a FIFPRO Men's World 11 since 2015",
        "en:FIFPRO World 11 — men's winners table, nationality flags, 2015 onward", family="gen-fifpro")
def fifpro_men_countries():
    return dedupe(_world11(_w11_tab(0), since=2015, flags=True))


@prompt("gen027", "Name a player named in a FIFPRO Women's World 11 (2015 onward)",
        "en:FIFPRO World 11 — women's winners table", family="gen-fifpro")
def fifpro_women():
    return _world11(_w11_tab(1), since=2015).out()


@prompt("gen022", "Name a player named in a UEFA Team of the Year (2001–2020)",
        "en:UEFA Team of the Year — year sections 2001–2020")
def uefa_toty():
    acc = Acc()
    for tb in tabs("UEFA Team of the Year"):
        m = re.fullmatch(r"Team of the Year (\d{4})", tb.heading)
        if not m or int(m.group(1)) > 2020 or "Player" not in tb.hdr:
            continue
        ci = tb.col("Player")
        for tx, ln in tb.body:
            for t, a in people(ln[ci])[-1:]:
                acc.add(t, a, m.group(1))
    return acc.out()


@prompt("gen023", "Name a winner of the Golden Foot award (men's, 2003–2025)",
        "en:Golden Foot — 'Award winners' table")
def golden_foot():
    tb = find_tab("Golden Foot", ["Year", "Player", "Club"], heading="Award winners")
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        for t, a in people(ln[ci])[-1:]:
            acc.add(t, a, tx[0])
    return acc.out()


@prompt("gen024", "Name a player on the 2020 Ballon d'Or Dream Team shortlist",
        "en:Ballon d'Or Dream Team — all position tables of nominees")
def dream_team():
    acc = Acc()
    for tb in tabs("Ballon d'Or Dream Team"):
        if "Player" not in tb.hdr or "Years" not in tb.hdr:
            continue
        ci = tb.col("Player")
        for tx, ln in tb.body:
            for t, a in people(ln[ci])[-1:]:
                acc.add(t, a, tb.heading)
    return acc.out()
