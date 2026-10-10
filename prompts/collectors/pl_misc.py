"""pl162-pl179: transfers, captains, officials, media, kits/sponsors and goalkeepers."""
import re

from bs4 import BeautifulSoup

from ballion.registry import prompt
from ballion.tables import _link_title, rows, wikitables
from ballion.wiki import page_html, resolve
from prompts.collectors.pl_util import Acc, club_season, dedupe, person_title, season_squad, tables

BIG6 = {"Arsenal F.C.", "Chelsea F.C.", "Liverpool F.C.", "Manchester City F.C.", "Manchester United F.C.",
        "Tottenham Hotspur F.C."}


def season(y):
    return f"{y}–{(y + 1) % 100:02d}"


# ------------------------------------------------------------ transfers
def transfers_to(page, clubs, jan_year=None):
    acc = Acc()
    for hs, h, data in tables(page, ["Moving to"]):
        pi = h.index("Player") if "Player" in h else h.index("Name")
        ti = h.index("Moving to")
        kind = "loan" if hs[0].startswith("Loans") else "transfer"
        for tx, ln in data:
            dest = [l for l in ln[ti] if l in clubs]
            if dest and (jan_year is None or _in_january(tx[0], jan_year)):
                acc.addrow(ln[pi], tx[pi], f"{kind} to {tx[ti]}, {tx[0]}")
    return acc.out()


def _mk_big6(pid, y):
    @prompt(pid, f"Name a player who joined a 'Big Six' club in the summer {y} transfer window "
                 "(loans included; Big Six: Arsenal, Chelsea, Liverpool, Man City, Man United, Tottenham)",
            f"en:List of English football transfers summer {y} — 'Moving to' a Big Six club (transfers and loans)",
            family="pl-transfers-big6")
    def f():
        return transfers_to(f"List of English football transfers summer {y}", BIG6)
    return f


for _pid, _y in [("pl162", 2025), ("pl163", 2024), ("pl164", 2023), ("pl165", 2022)]:
    _mk_big6(_pid, _y)


def pl_clubs_of(y):
    """Article titles of the clubs in a Premier League season (from its league table)."""
    from prompts.collectors.pl_clubs import table_rows
    return {t for _, t, _, _ in table_rows(f"{season(y)} Premier League")}


def _skip_flag():
    return None


def _in_january(datetxt, year):
    m = re.search(r"(\d{1,2}) (\w+) (\d{4})", datetxt)
    if not m or int(m.group(3)) != year:
        return False
    mon, day = m.group(2), int(m.group(1))
    return mon == "January" or (mon == "February" and day <= 3)


def _mk_winter(pid, window, y):
    @prompt(pid, f"Name a player who joined a Premier League club in the January {y + 1} transfer window "
                 f"(loans included; clubs of the {season(y)} Premier League)",
            f"en:List of English football transfers winter {season(y)} — 'Moving to' a {season(y)} Premier League club",
            family="pl-transfers-winter")
    def f():
        return transfers_to(f"List of English football transfers winter {season(y)}", pl_clubs_of(y), y + 1)
    return f


for _pid, _w, _y in [("pl166", "", 2025), ("pl167", "", 2024)]:
    _mk_winter(_pid, _w, _y)


# ------------------------------------------------------------ captains / kits / sponsors
def personnel(y, col):
    for hs, h, data in tables(f"{season(y)} Premier League", ["Team", "Manager", "Captain"]):
        ci = next(i for i, c in enumerate(h) if c.startswith(col))
        return h, ci, data
    raise LookupError(f"{season(y)} personnel table")


def captains(years):
    acc = Acc()
    for y in years:
        h, ci, data = personnel(y, "Captain")
        for tx, ln in data:
            acc.addrow(ln[ci], tx[ci], f"{tx[0]} {season(y)}")
    return acc.out()


@prompt("pl168", "Name a Premier League club captain from 2015–16 to 2019–20",
        "en:2015–16 Premier League … 2019–20 Premier League — Personnel and kits, Captain column", family="pl-captains")
def pl168():
    return captains(range(2015, 2020))


@prompt("pl169", "Name a Premier League club captain from 2020–21 to 2025–26",
        "en:2020–21 Premier League … 2025–26 Premier League — Personnel and kits, Captain column", family="pl-captains")
def pl169():
    return captains(range(2020, 2026))


KIT_TITLES = {"puma": "Puma SE", "nike": "Nike, Inc.", "adidas": "Adidas", "umbro": "Umbro", "new balance": "New Balance",
              "under armour": "Under Armour", "hummel": "Hummel International", "macron": "Macron (sportswear)",
              "castore": "Castore", "joma": "Joma", "kappa": "Kappa (brand)", "erreà": "Erreà", "kelme": "Kelme (company)",
              "jd sports": "JD Sports", "jd": "JD Sports", "dryworld": "Dryworld"}


def _brand_acc(col_re, years, allow_fallback):
    acc = Acc()
    for y in years:
        for hs, h, data in tables(f"{season(y)} Premier League", ["Team", "Manager", "Captain"]):
            cols = [i for i, c in enumerate(h) if re.search(col_re, c)]
            for tx, ln in data:
                for ci in cols:
                    if ci >= len(tx):
                        continue
                    txt = re.sub(r"\s*\[.*", "", tx[ci]).strip()
                    if not txt or txt.lower() in ("n/a", "none", "—", "-"):
                        continue
                    txt = re.sub(r"\s+\d+$", "", txt)
                    if not re.match(r"\w", txt):
                        continue
                    t = KIT_TITLES.get(txt.lower()) if allow_fallback else None
                    if t is None:
                        t = person_title(ln[ci], txt)
                    if t is None and not allow_fallback:
                        continue
                    acc.add(t, txt, f"{tx[0]} {season(y)}")
            break
    return acc.out()


@prompt("pl175", "Name a kit manufacturer used by a Premier League club since 2015–16",
        "en:2015–16 Premier League … 2025–26 Premier League — Personnel and kits, Kit manufacturer column", family="pl-kit-sponsors")
def pl175():
    return _brand_acc(r"^Kit manufacturer", range(2015, 2026), True)


@prompt("pl176", "Name a company that has been a Premier League club's main shirt sponsor since 2015–16",
        "en:2015–16 Premier League … 2025–26 Premier League — Personnel and kits, shirt sponsor (chest) column; sponsors without an article dropped",
        family="pl-kit-sponsors")
def pl176():
    return [r for r in _brand_acc(r"^Shirt sponsor(?! \((left )?sleeve)", range(2015, 2026), False)
            if r["enwiki"] != "TeamViewer"]  # the software article duplicates 'TeamViewer (company)'


# ------------------------------------------------------------ officials & media
def section_links(page, h2_re, h3_re=None):
    soup = BeautifulSoup(page_html(page), "lxml")
    out = []
    cur2 = cur3 = ""
    for el in soup.find_all(["h2", "h3", "h4", "li"]):
        if el.name == "h2":
            cur2, cur3 = el.get_text(" ", strip=True), ""
        elif el.name in ("h3", "h4"):
            cur3 = el.get_text(" ", strip=True)
        elif re.search(h2_re, cur2) and (h3_re is None or re.search(h3_re, cur3)):
            a = next((x for x in el.find_all("a") if _link_title(x)), None)
            if a is not None and not el.find_parent(["table"]):
                out.append((a.get_text(" ", strip=True), _link_title(a), cur3))
    return out


@prompt("pl172", "Name a referee in the Premier League's Select Group (Professional Referee Group) of match officials",
        "en:Select Group — Referees › Professional Referee Group", family="pl-referees")
def pl172():
    acc = Acc()
    for nm, t, sec in section_links("Select Group", r"^Referees$", r"Professional Referee Group"):
        acc.add(t, nm, "current referee")
    return acc.out()


@prompt("pl173", "Name a former Premier League Select Group referee (retired or dropped from the Select Group)",
        "en:Select Group — Former Select Group officials › Referees", family="pl-referees")
def pl173():
    acc = Acc()
    for nm, t, sec in section_links("Select Group", r"Former Select Group", r"^Referees$"):
        acc.add(t, nm, "former referee")
    return acc.out()


@prompt("pl174", "Name a presenter or pundit who has appeared on Match of the Day (studio presenters and analysts)",
        "en:Match of the Day — current/previous presenters and analysts tables", family="pl-motd")
def pl174():
    acc = Acc()
    for hs, h, data in tables("Match of the Day", ["Duration"]):
        for tx, ln in data:
            if ln[0]:
                acc.addrow(ln[0], tx[0], f"{hs[1]} {tx[1]}")
    return acc.out()


# ------------------------------------------------------------ goalkeepers
def goalkeepers(y):
    acc = Acc()
    for club in sorted(pl_clubs_of(y)):
        page = club_season(club, y)
        try:
            squad = season_squad(page, with_pos=True)
        except Exception:
            alt = club.replace("A.F.C. Bournemouth", "AFC Bournemouth")
            squad = season_squad(club_season(alt, y), with_pos=True)
        for nm, t, apps, pos in squad:
            if pos.upper().startswith("GK") or pos.lower().startswith("goalkeeper"):
                acc.add(t, nm, f"{apps} apps, {club.replace(' F.C.', '').replace(' A.F.C.', '')}")
    return acc.out()


@prompt("pl178", "Name a goalkeeper who made a Premier League appearance in 2025–26",
        "en:2025–26 Premier League clubs' season articles — squad statistics, goalkeepers with >= 1 league appearance",
        family="pl-goalkeepers")
def pl178():
    return goalkeepers(2025)


@prompt("pl179", "Name a goalkeeper who made a Premier League appearance in 2015–16",
        "en:2015–16 Premier League clubs' season articles — squad statistics, goalkeepers with >= 1 league appearance",
        family="pl-goalkeepers")
def pl179():
    return goalkeepers(2015)
