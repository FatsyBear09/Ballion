"""pl132-pl149: clubs, leagues, promotion/relegation, cups and derbies."""
import re

from ballion.registry import prompt
from prompts.collectors.pl_util import Acc, dedupe, tables, section_boxes

CHAMP_TITLE = "Football League Championship"


def season(y):
    return f"{y}–{(y + 1) % 100:02d}"


def champ_page(y):
    return f"{season(y)} " + ("Football League Championship" if y <= 2015 else "EFL Championship")


def l1_page(y):
    return f"{season(y)} " + ("Football League One" if y <= 2015 else "EFL League One")


def l2_page(y):
    return f"{season(y)} " + ("Football League Two" if y <= 2015 else "EFL League Two")


def table_rows(page):
    """League table rows: [(team text, team article title, marks set, position)]"""
    for hs, h, data in tables(page, ["Pos", "Pld", "Pts"]):
        ti = next(i for i, c in enumerate(h) if c in ("Team", "Club"))
        out = []
        for tx, ln in data:
            if not re.fullmatch(r"\d+", tx[0].strip()) or not ln[ti]:
                continue
            m = re.search(r"\(([A-Z, ]+)\)", tx[ti])
            marks = {x.strip() for x in m.group(1).split(",")} if m else set()
            out.append((re.sub(r"\s*\([A-Z, ]+\)", "", tx[ti]).strip(), ln[ti][-1], marks, int(tx[0])))
        if len(out) >= 10:
            return out
    # pre-season pages have no table yet: fall back to the participants table
    for hs, h, data in tables(page, ["Team", "Location"]):
        return [(tx[0], ln[0][-1], set(), i + 1) for i, (tx, ln) in enumerate(data) if ln[0]]
    raise LookupError(f"{page}: no league table")


def clubs_in(pages, label):
    acc = Acc()
    for page, lab in pages:
        for name, title, marks, pos in table_rows(page):
            acc.add(title, name, lab)
    return acc.out(maxev=3)


@prompt("pl132", "Name a club that has played in the Championship since 2015–16",
        "en:2015–16 Football League Championship … 2025–26 EFL Championship — league tables", family="pl-club-played-in-league")
def pl132():
    return clubs_in([(champ_page(y), season(y)) for y in range(2015, 2026)], "")


@prompt("pl133", "Name a club that has played in League One since 2015–16",
        "en:2015–16 Football League One … 2025–26 EFL League One — league tables", family="pl-club-played-in-league")
def pl133():
    return clubs_in([(l1_page(y), season(y)) for y in range(2015, 2026)], "")


@prompt("pl134", "Name a club that has played in League Two since 2015–16",
        "en:2015–16 Football League Two … 2025–26 EFL League Two — league tables", family="pl-club-played-in-league")
def pl134():
    return clubs_in([(l2_page(y), season(y)) for y in range(2015, 2026)], "")


@prompt("pl136", "Name a club in the 2026–27 Championship",
        "en:2026–27 EFL Championship — league table / participants (list frozen at scrape date)", family="pl-club-season-league")
def pl136():
    return clubs_in([("2026–27 EFL Championship", "2026–27")], "")


@prompt("pl141", "Name a club that has played in the Championship since 2004–05 (the season it was renamed)",
        "en:2004–05 Football League Championship … 2025–26 EFL Championship — league tables", family="pl-club-played-in-league")
def pl141():
    return clubs_in([(champ_page(y), season(y)) for y in range(2004, 2026)], "")


def _marked(pages, mark):
    acc = Acc()
    for page, lab in pages:
        for name, title, marks, pos in table_rows(page):
            if mark in marks:
                acc.add(title, name, lab)
    return acc.out()


@prompt("pl138", "Name a club relegated from the Championship to League One since 2015–16",
        "en:2015–16 Football League Championship … 2025–26 EFL Championship — league tables, (R) marks", family="pl-club-movement")
def pl138():
    return _marked([(champ_page(y), season(y)) for y in range(2015, 2026)], "R")


@prompt("pl139", "Name a club promoted from League One to the Championship since 2015–16",
        "en:2015–16 Football League One … 2025–26 EFL League One — league tables, (P) marks", family="pl-club-movement")
def pl139():
    return _marked([(l1_page(y), season(y)) for y in range(2015, 2026)], "P")


# ---- promoted to the PL / UCL qualification, from List of Premier League seasons
def pl_seasons_table():
    for hs, h, data in tables("List of Premier League seasons", ["Season", "Champions (Titles)"]):
        return h, data
    raise LookupError("List of Premier League seasons table not found")


@prompt("pl137", "Name a club promoted to the Premier League since 2015–16",
        "en:List of Premier League seasons — 'Promoted' column, 2015–16 to 2026–27", family="pl-club-movement")
def pl137():
    h, data = pl_seasons_table()
    pi = next(i for i, c in enumerate(h) if c.startswith("Promoted"))
    acc = Acc()
    for tx, ln in data:
        m = re.match(r"(\d{4})–", tx[0])
        if m and int(m.group(1)) >= 2015:
            for t in ln[pi]:
                acc.add(t, re.sub(r"\s*(F\.C\.|A\.F\.C\.)$", "", t), f"promoted for {tx[0]}")
    return acc.out()


@prompt("pl142", "Name a club that has qualified for the Champions League through its Premier League finish (champions included)",
        "en:List of Premier League seasons — 'Champions' and 'UEFA Champions League' columns, 1992–93 onward",
        family="pl-club-ucl-qualified")
def pl142():
    h, data = pl_seasons_table()
    ui = next(i for i, c in enumerate(h) if c == "UEFA Champions League")
    acc = Acc()
    for tx, ln in data:
        if re.match(r"\d{4}–", tx[0]) and len(tx) > ui:
            for t in ln[1][-1:] + ln[ui]:
                if True:
                    acc.add(t, re.sub(r"\s*(F\.C\.|A\.F\.C\.|A\.F\.C)$", "", t), tx[0])
    return acc.out()


@prompt("pl143", "Name a club that played in the inaugural 1992–93 Premier League",
        "en:1992–93 FA Premier League — league table", family="pl-club-season-league")
def pl143():
    return clubs_in([("1992–93 FA Premier League", "1992–93")], "")


# ---- play-offs
@prompt("pl140", "Name a club that has reached the Championship play-off final (2005 to 2026)",
        "en:EFL Championship play-offs — winners and runners-up of the finals, 2005 onward", family="pl-club-playoff-final")
def pl140():
    acc = Acc()
    for hs, h, data in tables("EFL Championship play-offs", ["Year", "Winner", "Runner-up"]):
        wi, ri = h.index("Winner"), h.index("Runner-up")
        for tx, ln in data:
            m = re.match(r"(\d{4})", tx[0])
            if not m or int(m.group(1)) < 2005:
                continue
            for i, role in ((wi, "winner"), (ri, "runner-up")):
                if ln[i]:
                    acc.add(ln[i][-1], re.sub(r"\s*\(\d+\)", "", tx[i]), f"{m.group(1)} {role}")
        break
    return acc.out()


# ---- cups
@prompt("pl144", "Name a club that has won the Community Shield (formerly the Charity Shield)",
        "en:FA Community Shield — 'By number of wins (clubs)' table", family="pl-club-cup-winners")
def pl144():
    acc = Acc()
    for hs, h, data in tables("FA Community Shield", ["Team"]):
        if not any(c.startswith("Wins") for c in h) or "outright" not in " ".join(h):
            continue
        for tx, ln in data:
            if ln[0] and re.match(r"\d", tx[1]):
                acc.add(ln[0][-1], tx[0], tx[1])
        break
    return acc.out()


def finalists(list_page, since_final_year, season_col_has_year=False):
    acc = Acc()
    for hs, h, data in tables(list_page, ["Winners", "Runners-up"]):
        if len(data) < 60:
            continue
        wi, ri = h.index("Winners"), h.index("Runners-up")
        for tx, ln in data:
            m = re.match(r"(\d{4})", tx[0])
            if not m:
                continue
            fy = int(m.group(1)) + (0 if season_col_has_year or "–" not in tx[0] and len(tx[0]) == 4 else 1)
            if re.match(r"\d{4}–\d", tx[0]):
                fy = int(m.group(1)) + 1
            if fy >= since_final_year:
                for i, role in ((wi, "winners"), (ri, "runners-up")):
                    if ln[i]:
                        acc.add(ln[i][-1], re.sub(r"\s*\(\d+\)", "", tx[i]), f"{fy} {role}")
        break
    return acc.out()


@prompt("pl145", "Name a club that has reached the FA Cup final since 2000 (winners or runners-up)",
        "en:List of FA Cup finals — winners and runners-up, finals from 2000 to 2026", family="pl-club-cup-finalists")
def pl145():
    return finalists("List of FA Cup finals", 2000)


@prompt("pl146", "Name a club that has reached the League Cup final since 2000 (winners or runners-up)",
        "en:List of EFL Cup finals — winners and runners-up, finals from 2000 to 2026", family="pl-club-cup-finalists")
def pl146():
    return finalists("List of EFL Cup finals", 2000)


def semis(page_fn, years, heading=r"^Semi-?finals?$"):
    acc = Acc()
    for y in years:
        page = page_fn(y)
        for b in section_boxes(page, heading):
            for t in (b["home"], b["away"]):
                if t:
                    acc.add(t, re.sub(r"\s*(F\.C\.|A\.F\.C\.)$", "", t), season(y))
    return acc.out()


@prompt("pl147", "Name a club that has reached the FA Cup semi-finals since 2015–16",
        "en:2015–16 FA Cup … 2025–26 FA Cup — Semi-finals", family="pl-club-cup-semis")
def pl147():
    return semis(lambda y: f"{season(y)} FA Cup", range(2015, 2026))


@prompt("pl148", "Name a club that has reached the League Cup semi-finals since 2015–16",
        "en:2015–16 Football League Cup … 2025–26 EFL Cup — Semi-finals", family="pl-club-cup-semis")
def pl148():
    return semis(lambda y: f"{season(y)} " + ("Football League Cup" if y == 2015 else "EFL Cup"), range(2015, 2026))


def promoted_managers():
    from prompts.collectors.pl_util import Acc
    acc = Acc()
    for y in range(2015, 2026):
        page = champ_page(y)
        promoted = {name for name, t, marks, pos in table_rows(page) if "P" in marks}
        for hs, h, data in tables(page, ["Team", "Manager", "Captain"]):
            mi = h.index("Manager")
            for tx, ln in data:
                if tx[0].strip() in promoted:
                    acc.addrow(ln[mi], tx[mi], f"{tx[0]}, promoted {season(y)}")
            break
        else:
            raise LookupError(f"{page}: personnel table")
    return acc.out()


@prompt("pl082", "Name a manager who won promotion from the Championship to the Premier League between 2015–16 and 2025–26",
        "en:2015–16 Football League Championship … 2025–26 EFL Championship — promoted clubs (league table) and their manager in the Personnel table",
        family="pl-managers-promotion")
def pl082():
    return promoted_managers()
