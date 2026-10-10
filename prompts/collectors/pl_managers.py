"""pl074-pl099: Premier League and Championship managers."""
import re
from datetime import datetime

from ballion.registry import prompt
from prompts.collectors.pl_util import (Acc, clean, dedupe, final_page, person_title, season_start, tables)

PLM = "List of Premier League managers"
BIG6_T = {"Arsenal F.C.", "Chelsea F.C.", "Liverpool F.C.", "Manchester City F.C.", "Manchester United F.C.",
          "Tottenham Hotspur F.C."}
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
          "november", "december"]


def season(y):
    return f"{y}–{(y + 1) % 100:02d}"


def parse_date(s):
    """-> (year, month or None, day or None) or None if ongoing/unknown."""
    s = (s or "").strip()
    if not s or re.search(r"present|incumbent|current|^—$|^-$", s, re.I):
        return None
    m = re.search(r"(?:(\d{1,2})\s+)?([A-Za-z]+)?\s*((?:18|19|20)\d\d)", s)
    if not m:
        return None
    mon = None
    if m.group(2) and m.group(2).lower() in MONTHS:
        mon = MONTHS.index(m.group(2).lower()) + 1
    return int(m.group(3)), mon, int(m.group(1)) if m.group(1) else None


def ended_since(s, y, mon=1):
    """True if a tenure ending `s` ended on/after (y, mon) or is ongoing."""
    d = parse_date(s)
    if d is None:
        return True
    return (d[0], d[1] or 12) >= (y, mon)


_pl_rows = []


def pl_manager_rows():
    """[{name, title, nat, club (article title), from, until, caretaker, row text}] from the PL managers table."""
    if _pl_rows:
        return _pl_rows
    for hs, h, data in tables(PLM, ["Name", "Club", "From", "Until"]):
        for tx, ln in data:
            if len(tx) < 5 or not tx[2].strip():
                continue
            nat = ln[1][-1] if ln[1] else ""
            club = ln[2][-1] if ln[2] else None
            _pl_rows.append({"name": tx[0], "title": person_title(ln[0], tx[0]), "nat": nat, "club": club,
                             "from": tx[3], "until": tx[4], "caretaker": "‡" in tx[0], "years": tx[6] if len(tx) > 6 else ""})
        break
    return _pl_rows


def _from_rows(pred, ev):
    acc = Acc()
    for r in pl_manager_rows():
        if pred(r):
            acc.add(r["title"], r["name"], ev(r))
    return acc.out()


def _ev(r):
    return f"{r['club'].replace(' F.C.', '').replace(' A.F.C.', '')} {r['from']} – {r['until']}"


@prompt("pl074", "Name a manager who has managed a Premier League club since 2020–21 (caretakers included)",
        "en:List of Premier League managers — tenures ending on or after 1 August 2020 (or ongoing)", family="pl-managers-since")
def pl074():
    return _from_rows(lambda r: ended_since(r["until"], 2020, 8), _ev)


@prompt("pl075", "Name a caretaker or interim manager of a Premier League club since 2015–16",
        "en:List of Premier League managers — caretaker (‡) tenures ending on or after 1 August 2015", family="pl-managers-caretaker")
def pl075():
    return _from_rows(lambda r: r["caretaker"] and ended_since(r["until"], 2015, 8), _ev)


def changes_tables(page):
    for hs, h, data in tables(page, ["Team", "Outgoing manager", "Incoming manager"]):
        yield h, data


@prompt("pl076", "Name a manager who was sacked by a Premier League club between 2015–16 and 2025–26",
        "en:2015–16 Premier League … 2025–26 Premier League — Managerial changes, 'Sacked'", family="pl-managers-sacked")
def pl076():
    acc = Acc()
    for y in range(2015, 2026):
        for h, data in changes_tables(f"{season(y)} Premier League"):
            oi, mi = h.index("Outgoing manager"), h.index("Manner of departure")
            for tx, ln in data:
                if re.fullmatch(r"sacked", tx[mi].strip(), re.I):
                    acc.addrow(ln[oi], tx[oi], f"{tx[0]}, {season(y)}")
            break
    return acc.out()


def season_managers(y, preseason_only_in=True):
    """Managers of a PL season: Personnel table + incoming managers + outgoing managers who left mid-season."""
    page = f"{season(y)} Premier League"
    acc = Acc()
    for hs, h, data in tables(page, ["Team", "Manager", "Captain"]):
        mi = h.index("Manager")
        for tx, ln in data:
            acc.addrow(ln[mi], tx[mi], f"{tx[0]} {season(y)}")
        break
    for h, data in changes_tables(page):
        oi, ii, pi = h.index("Outgoing manager"), h.index("Incoming manager"), h.index("Position in table") if "Position in table" in h else h.index("Position in the table")
        for tx, ln in data:
            acc.addrow(ln[ii], tx[ii], f"{tx[0]} {season(y)}")
            if tx[pi].strip().lower() != "pre-season":
                acc.addrow(ln[oi], tx[oi], f"{tx[0]} {season(y)}")
        break
    return acc


@prompt("pl077", "Name a manager who managed a Premier League club during 2015–16 (caretakers included)",
        "en:2015–16 Premier League — Personnel and kits + Managerial changes", family="pl-managers-season")
def pl077():
    return season_managers(2015).out()


@prompt("pl078", "Name a manager in charge of a Premier League club in 2026–27 (up to October 2026)",
        "en:2026–27 Premier League — Personnel and kits + Managerial changes (frozen at scrape date)", family="pl-managers-season")
def pl078():
    return season_managers(2026).out()


@prompt("pl079", "Name a manager of a 'Big Six' club since 2015–16 (Arsenal, Chelsea, Liverpool, Man City, Man United or Tottenham; caretakers included)",
        "en:List of Premier League managers — Big Six clubs, tenures ending on or after 1 July 2015", family="pl-managers-since")
def pl079():
    return _from_rows(lambda r: r["club"] in BIG6_T and ended_since(r["until"], 2015, 7), _ev)


# ---- cup-winning managers (via the final articles' lineup boxes)
def _final_winner_manager(list_page, since_year):
    acc = Acc()
    for hs, h, data in tables(list_page, ["Winners", "Runners-up"]):
        wi = h.index("Winners")
        for tx, ln in data:
            m = re.match(r"(\d{4})", tx[0])
            if not m:
                continue
            fin = next((t for cell in ln for t in cell if re.fullmatch(r"\d{4} (FA Cup|Football League Cup|EFL Cup) [Ff]inal", t)), None)
            if not fin or int(fin[:4]) < since_year:
                continue
            win = next((t for t in ln[wi] if "F.C." in t or "A.F.C." in t or t), None)
            d = final_page(fin)
            for side, (st, sub, mgr) in zip(("home", "away"), d["lineups"]):
                if d[side] == win and mgr and mgr[1]:
                    acc.add(mgr[1], mgr[0], f"{fin.split(' ', 1)[0]} {fin.split(' ', 1)[1].replace(' final', '')} winners ({tx[wi].split(' (')[0]})")
        break
    return acc


@prompt("pl080", "Name a manager who has won the FA Cup or the League Cup (finals from 2015 to 2026)",
        "en:List of FA Cup finals + List of EFL Cup finals — winning manager in each final's lineup box, 2016–2026",
        family="pl-cup-winning-managers")
def pl080():
    a = _final_winner_manager("List of FA Cup finals", 2015)
    b = _final_winner_manager("List of EFL Cup finals", 2015)
    for k, v in b.d.items():
        a.add(k, v["answer"], "; ".join(v["ev"]))
    return a.out()


@prompt("pl081", "Name a manager who managed an EFL Championship club in 2025–26 (caretakers included)",
        "en:2025–26 EFL Championship — Personnel and sponsorship + Managerial changes", family="pl-managers-season")
def pl081():
    page = "2025–26 EFL Championship"
    acc = Acc()
    for hs, h, data in tables(page, ["Team", "Manager"]):
        mi = h.index("Manager")
        for tx, ln in data:
            if tx[mi].strip() != "Manager":
                acc.addrow(ln[mi], tx[mi], f"{tx[0]} 2025–26")
        break
    for h, data in changes_tables(page):
        oi, ii = h.index("Outgoing manager"), h.index("Incoming manager")
        pi = next((i for i, c in enumerate(h) if c.startswith("Position")), None)
        for tx, ln in data:
            acc.addrow(ln[ii], tx[ii], f"{tx[0]} 2025–26")
            if pi is None or tx[pi].strip().lower() != "pre-season":
                acc.addrow(ln[oi], tx[oi], f"{tx[0]} 2025–26")
    return acc.out()


# ---- nationality of PL managers
def _nat(*nats):
    return _from_rows(lambda r: r["nat"] in nats, lambda r: f"{r['nat']}; " + _ev(r))


@prompt("pl083", "Name a Spanish or Portuguese manager who has managed in the Premier League",
        "en:List of Premier League managers — nationality flag Spain or Portugal", family="pl-managers-nationality")
def pl083():
    return _nat("Spain", "Portugal")


@prompt("pl084", "Name an Italian manager who has managed in the Premier League",
        "en:List of Premier League managers — nationality flag Italy", family="pl-managers-nationality")
def pl084():
    return _nat("Italy")


@prompt("pl085", "Name a manager who has managed 300 or more Premier League matches",
        "en:List of Premier League managers — Most games managed in the Premier League", family="pl-managers-games")
def pl085():
    acc = Acc()
    for hs, h, data in tables(PLM, ["Rank", "Manager", "Games"]):
        mi, gi = h.index("Manager"), h.index("Games")
        for tx, ln in data:
            g = int(re.sub(r"\D", "", tx[gi]) or 0)
            if g >= 300:
                acc.addrow(ln[mi], tx[mi], f"{g} games")
        break
    return acc.out()


# ---- managers of one club
def pl_club(club_title, since_year, since_mon=1, label=None):
    return _from_rows(lambda r: r["club"] == club_title and ended_since(r["until"], since_year, since_mon), _ev)


def club_list_managers(page, since_year, since_mon=1):
    """Generic club 'List of X managers' parser: wikitable with Manager/Name + From + To."""
    acc = Acc()
    found = False
    for hs, h, data in tables(page):
        name_col = next((i for i, c in enumerate(h) if c in ("Manager", "Name")), None)
        fi = next((i for i, c in enumerate(h) if c in ("From", "Dates")), None)
        ti = next((i for i, c in enumerate(h) if c in ("To", "Until")), None)
        if name_col is None or fi is None or ti is None:
            continue
        found = True
        for tx, ln in data:
            if len(tx) <= max(name_col, ti) or tx[name_col].strip() in ("Manager", "Name") or not tx[name_col].strip():
                continue
            if ended_since(tx[ti], since_year, since_mon):
                acc.addrow(ln[name_col], tx[name_col], f"{tx[fi]} – {tx[ti]}")
        break
    if not found:
        raise LookupError(f"{page}: manager table not found")
    return acc.out()


CLUBS = [
    # pid, club label, list page / PL table club title, since (year, mon), 'since' wording, source kind
    ("pl086", "Tottenham Hotspur", "Tottenham Hotspur F.C.", 1992, 8, "pl"),
    ("pl087", "Newcastle United", "List of Newcastle United F.C. managers", 1992, 8, "list"),
    ("pl088", "Everton", "List of Everton F.C. managers", 1992, 8, "list"),
    ("pl089", "Manchester City", "List of Manchester City F.C. managers", 1992, 8, "list"),
    ("pl090", "West Ham United", "West Ham United F.C.", 1992, 8, "pl"),
    ("pl091", "Aston Villa", "List of Aston Villa F.C. managers", 1992, 8, "list"),
    ("pl092", "Watford", "List of Watford F.C. managers", 2012, 1, "list"),
    ("pl093", "Crystal Palace", "List of Crystal Palace F.C. managers", 2010, 1, "list"),
    ("pl094", "Southampton", "List of Southampton F.C. managers", 2010, 1, "list"),
    ("pl095", "Leeds United", "List of Leeds United F.C. managers", 2010, 1, "list"),
    ("pl096", "Leicester City", "List of Leicester City F.C. managers", 2000, 1, "list"),
    ("pl097", "Sunderland", "List of Sunderland A.F.C. managers", 2000, 1, "list"),
    ("pl098", "Liverpool", "List of Liverpool F.C. managers", 1900, 1, "list"),
]


def _mk_club(pid, label, src, y, mon, kind):
    since = f" since {y}" if y > 1900 else ""
    if kind == "pl":
        text = f"Name a manager who has managed {label} in the Premier League (caretakers included)"
        source = f"en:List of Premier League managers — {label} tenures"

        def f():
            return pl_club(src, y, mon)
    else:
        text = f"Name a manager of {label}{since} (caretakers included)"
        source = f"en:{src} — managers table" + (f", tenures ending in {y} or later" if y > 1900 else "")

        def f():
            return club_list_managers(src, y, mon)
    prompt(pid, text, source, family="pl-club-managers")(f)


for _c in CLUBS:
    _mk_club(*_c)


@prompt("pl099", "Name a manager who managed a Premier League club in the inaugural 1992–93 season (caretakers included)",
        "en:1992–93 FA Premier League — Personnel + Managerial changes", family="pl-managers-season")
def pl099():
    page = "1992–93 FA Premier League"
    acc = Acc()
    for hs, h, data in tables(page):
        if "Manager" in h and "Team" in h:
            mi = h.index("Manager")
            for tx, ln in data:
                acc.addrow(ln[mi], tx[mi], f"{tx[0]} 1992–93")
            break
    for hs, h, data in tables(page, ["Team", "Outgoing manager"]):
        oi = h.index("Outgoing manager")
        ii = h.index("Incoming manager") if "Incoming manager" in h else None
        for tx, ln in data:
            if ii is not None:
                acc.addrow(ln[ii], tx[ii], f"{tx[0]} 1992–93")
            acc.addrow(ln[oi], tx[oi], f"{tx[0]} 1992–93")
        break
    return acc.out()
