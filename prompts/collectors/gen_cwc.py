"""gen157-gen167, gen196, gen197: Club World Cup and South America."""
import re

from bs4 import BeautifulSoup

from ballion.registry import prompt
from ballion.tables import _link_title
from ballion.wiki import page_html, resolve
from prompts.collectors.gen_util import (Acc, box_scorers, country_rec, dedupe, find_tab, find_tabs, first_person,
                                         people, season_label, tabs, team_col_clubs, wd_property_label)

CWC25 = "2025 FIFA Club World Cup"
FED = re.compile(r"Association|Federation|Football Union|Confederation|Soccer Federation|^New Zealand Football$", re.I)


def _club(cell):
    c = [(t, a) for t, a in cell if not FED.search(t)]
    return c[-1] if c else None


def _cwc25_groups():
    return [tb for tb in tabs(CWC25) if tb.heading == "Groups" and tb.hdr[:2] == ["Pos", "Team"]]


@prompt("gen157", "Name a club that played at the 2025 FIFA Club World Cup",
        "en:2025 FIFA Club World Cup — group tables (32 teams)", family="gen-cwc-2025")
def cwc25_clubs():
    acc = Acc("club")
    for tb in _cwc25_groups():
        ti = tb.col("Team")
        for tx, ln in tb.body:
            if c := _club(ln[ti]):
                acc.add(c[0], c[1], "2025")
    return acc.out()


@prompt("gen158", "Name a player who scored in the 2025 FIFA Club World Cup knockout stage (own goals and shoot-outs excluded)",
        "en:2025 FIFA Club World Cup knockout stage — football-box scorers", family="gen-cwc-2025")
def cwc25_ko_scorers():
    return box_scorers("2025 FIFA Club World Cup knockout stage").out()


@prompt("gen159", "Name a stadium that hosted a 2025 FIFA Club World Cup match",
        "en:2025 FIFA Club World Cup — venues table", family="gen-cwc-2025")
def cwc25_stadiums():
    tb = find_tab(CWC25, [], heading="^Venues$")
    acc = Acc("club")
    rows = tb.rows
    for i, (tx, ln) in enumerate(rows[:-1]):
        nxt = rows[i + 1][0]
        if nxt and nxt[0].startswith("Capacity"):
            for cell in ln:
                if cell and len(cell) == 1 and cell[0][1]:
                    acc.add(cell[0][0], cell[0][1], "venue")
    return acc.out()


@prompt("gen160", "Name a country with a club at the 2025 FIFA Club World Cup",
        "en:2025 FIFA Club World Cup — group tables; country of each club's football association", family="gen-cwc-2025")
def cwc25_countries():
    feds = set()
    for tb in _cwc25_groups():
        ti = tb.col("Team")
        for (tx, ln), fl in zip(tb.body, tb.bflags):
            feds.update(f for f in fl[ti])
            feds.update(t for t, a in ln[ti] if FED.search(t))
    lab = wd_property_label(sorted(feds), "P17")
    out = {}
    for f in feds:
        if f in lab:
            name = "England" if lab[f] == "United Kingdom" else lab[f]
            out.setdefault(name, country_rec(name))
    if len(out) < 12:
        raise LookupError(f"{len(out)} countries from {len(feds)} federations")
    return dedupe(list(out.values()))


@prompt("gen196", "Name a player who scored for a non-European club at the 2025 FIFA Club World Cup (own goals excluded)",
        "en:2025 FIFA Club World Cup Group A … Group H and knockout stage — scorers for clubs outside UEFA", family="gen-cwc-2025")
def cwc25_non_european_scorers():
    non_uefa = []
    for tb in tabs(CWC25):
        if tb.heading == "Draw" and tb.hdr[:3] == ["Team", "Confed.", "Pts"]:
            for tx, ln in tb.body:
                if tx[1].strip() != "UEFA" and (c := _club(ln[0])):
                    non_uefa.append(c[0])
    res = resolve(non_uefa)
    ok = {res[t]["title"] for t in non_uefa}
    cache = {}

    def team_ok(t):
        if t not in cache:
            cache[t] = resolve([t])[t]["title"] in ok
        return cache[t]

    acc = Acc()
    for g in "ABCDEFGH":
        box_scorers(f"{CWC25} Group {g}", acc, "group", team_ok=team_ok)
    box_scorers(f"{CWC25} knockout stage", acc, "knockout", team_ok=team_ok)
    return acc.out()


@prompt("gen197", "Name a head coach who led a club at the 2025 FIFA Club World Cup",
        "en:2025 FIFA Club World Cup squads — 'Manager:' line of each team", family="gen-cwc-2025")
def cwc25_coaches():
    soup = BeautifulSoup(page_html(f"{CWC25} squads"), "lxml")
    acc = Acc()
    for p in soup.find_all("p"):
        if p.get_text(" ", strip=True).startswith("Manager:"):
            a = next((a for a in p.find_all("a") if not a.find_parent(class_="flagicon")), None)
            if a and (x := _link_title(a)):
                acc.add(x, a.get_text(" ", strip=True), "2025")
    return acc.out()


def _editions():
    pages = [("2000", "2000 FIFA Club World Championship"), ("2005", "2005 FIFA Club World Championship")]
    pages += [(str(y), f"{y} FIFA Club World Cup") for y in range(2006, 2024)]
    return pages


@prompt("gen161", "Name a club that played at the FIFA Club World Cup / Club World Championship from 2000 to 2023",
        "en:2000, 2005–2023 FIFA Club World Cup editions — 'Qualified teams' tables (the 32-team 2025 edition excluded)")
def cwc_old_clubs():
    acc = Acc("club")
    for y, pg in _editions():
        tb = find_tab(pg, ["Team", "Confederation", "Qualification"], heading="Qualified teams")
        ti = tb.col("Team")
        for tx, ln in tb.body:
            # "TH" (title holders) annotations link back to an edition page, not a club.
            if (c := _club(ln[ti])) and "Club World" not in c[0]:
                acc.add(c[0], c[1], y)
    return acc.out()


@prompt("gen162", "Name a player who won the Golden Ball, Silver Ball or Bronze Ball at a FIFA Club World Cup (2000–2025)",
        "en:FIFA Club World Cup awards — Golden Ball table (Golden, Silver and Bronze Ball)")
def cwc_balls():
    tb = find_tab("FIFA Club World Cup awards", ["Edition", "Golden Ball", "Silver Ball", "Bronze Ball"], heading="Golden Ball")
    acc = Acc()
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]):
            for ci, lab in ((1, "Golden"), (2, "Silver"), (3, "Bronze")):
                for t, a in people(ln[ci])[:1]:
                    acc.add(t, a, f"{lab} Ball {tx[0][:4]}")
    return acc.out()


@prompt("gen163", "Name a player who has scored in a FIFA Club World Cup final (2000–2025; own goals and shoot-outs excluded)",
        "en:2000–2025 FIFA Club World Cup editions — football-box scorers of each final", family="gen-final-scorers")
def cwc_final_scorers():
    acc = Acc()
    for y, pg in _editions() + [("2025", CWC25)]:
        box_scorers(pg, acc, y, pick=lambda bs: bs[-1:])
    return acc.out()


@prompt("gen164", "Name a club that has played in a Copa Libertadores final since 2000",
        "en:List of Copa Libertadores finals — winners and runners-up, 2000 onward", family="gen-cup-finalists")
def libertadores_finalists():
    tb = find_tab("List of Copa Libertadores finals", ["Year", "Winner", "Runner-up"], heading="List of finals")
    wi, ri = tb.col("Winner"), tb.col("Runner-up")
    acc = Acc("club")
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]) and int(tx[0][:4]) >= 2000:
            for ci in (wi, ri):
                if c := _club(ln[ci]):
                    acc.add(c[0], c[1], tx[0][:4])
    return acc.out()


@prompt("gen165", "Name a player who has scored in a Copa Libertadores final from 2010 to 2025 (own goals and shoot-outs excluded)",
        "en:2010–2018 Copa Libertadores finals (two legs) and 2019–2025 Copa Libertadores final — football-box scorers",
        family="gen-final-scorers")
def libertadores_scorers():
    acc = Acc()
    for y in range(2010, 2026):
        box_scorers(f"{y} Copa Libertadores {'finals' if y <= 2018 else 'final'}", acc, str(y))
    return acc.out()


@prompt("gen166", "Name a club playing in the 2026 Campeonato Brasileiro Série A",
        "en:2026 Campeonato Brasileiro Série A — stadiums and locations (team column)", family="gen-current-league-clubs")
def brasileirao_clubs():
    return team_col_clubs("2026 Campeonato Brasileiro Série A").out()


@prompt("gen167", "Name a club playing in Argentina's 2026 Liga Profesional",
        "en:2026 AFA Liga Profesional de Fútbol — stadia and locations (club column)", family="gen-current-league-clubs")
def argentina_clubs():
    return team_col_clubs("2026 AFA Liga Profesional de Fútbol", heading="Stadia and locations", col="Club").out()
