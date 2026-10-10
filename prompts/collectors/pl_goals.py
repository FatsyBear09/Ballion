"""pl022-pl034: hat-tricks, top scorers and clean sheets."""
import re
from datetime import datetime
from urllib.parse import unquote

from bs4 import BeautifulSoup

from ballion.registry import prompt
from ballion.tables import _link_title, wikitables
from prompts.collectors.pl_util import Acc, clean, person_title, season_start, tables

HT_PAGE = "List of Premier League hat-tricks"
BIG6 = {"Arsenal F.C.", "Chelsea F.C.", "Liverpool F.C.", "Manchester City F.C.", "Manchester United F.C.",
        "Tottenham Hotspur F.C."}


def season(y):
    return f"{y}–{(y + 1) % 100:02d}"


def pl_page(y):
    return f"{season(y)} Premier League"


def champ_page(y):
    return f"{season(y)} " + ("Football League Championship" if y <= 2015 else "EFL Championship")


_hat_cache = []


def hat_tricks():
    """[{player, title, name, date(datetime), goals, club(scoring side article title)}]"""
    if _hat_cache:
        return _hat_cache
    t = [x for x in wikitables(HT_PAGE) if len(x.find_all("tr")) > 300][0]
    for tr in t.find_all("tr")[1:]:
        th = tr.find("th")
        tds = tr.find_all("td", recursive=False)
        if th is None or len(tds) < 5:
            continue
        a = th.find("a")
        title = _link_title(a) if a else None
        sups = th.find_all("sup")
        sup = "".join(x.get_text() for x in sups)
        goals = 5 if "5" in sup else 4 if "4" in sup else 3
        for x in th.find_all(["sup", "small"]):
            x.decompose()
        name = clean(th.get_text(" ", strip=True))
        home, away = (_link_title(td.find("a")) if td.find("a") else None for td in (tds[1], tds[3]))
        res = tds[2]
        # bold marks the scoring side's goals: "<b>5</b>–0" (home) or "2–<b>3</b>" (away)
        bolds = res.find_all("b")
        txt = res.get_text("", strip=True)
        side = None
        if bolds:
            b = bolds[0].get_text(strip=True)
            side = "home" if txt.startswith(b) else "away"
        m = re.search(r"\d{1,2} \w+ \d{4}", tds[4].get_text(" ", strip=True))
        date = datetime.strptime(m.group(), "%d %B %Y") if m else (_hat_cache[-1]["date"] if _hat_cache else datetime(1992, 8, 15))
        _hat_cache.append({"title": title, "name": name, "goals": goals, "date": date,
                           "club": home if side == "home" else away if side == "away" else None,
                           "home": home, "away": away, "result": txt})
    return _hat_cache


def _ht_acc(pred, ev):
    acc = Acc()
    for r in hat_tricks():
        if pred(r):
            acc.add(r["title"], r["name"], r["date"].strftime("%Y-%m-%d") + " " + ev(r))
    return acc.out()


def _fmt(r):
    return f"{r['result']}" + (f" ({r['goals']} goals)" if r["goals"] > 3 else "")


@prompt("pl022", "Name a player who has scored a Premier League hat-trick since 2015",
        "en:List of Premier League hat-tricks — hat-tricks dated 2015-08-01 onward", family="pl-hattrick")
def pl022():
    return _ht_acc(lambda r: r["date"] >= datetime(2015, 8, 1), _fmt)


@prompt("pl023", "Name a player who has scored a Premier League hat-trick for a club outside the 'Big Six' since 2015 "
        "(Big Six: Arsenal, Chelsea, Liverpool, Man City, Man United, Tottenham)",
        "en:List of Premier League hat-tricks — scoring side (bold score) not a Big Six club, 2015-08-01 onward",
        family="pl-hattrick")
def pl023():
    return _ht_acc(lambda r: r["date"] >= datetime(2015, 8, 1) and r["club"] and r["club"] not in BIG6, _fmt)


@prompt("pl024", "Name a player who has scored four or more goals in a single Premier League match",
        "en:List of Premier League hat-tricks — rows marked with 4 or 5 goals", family="pl-hattrick")
def pl024():
    return _ht_acc(lambda r: r["goals"] >= 4, _fmt)


def _club_ht(club_title, label):
    return _ht_acc(lambda r: r["club"] == club_title, _fmt)


for _pid, _club, _label in [("pl025", "Chelsea F.C.", "Chelsea"), ("pl026", "Arsenal F.C.", "Arsenal"),
                            ("pl027", "Manchester City F.C.", "Manchester City"),
                            ("pl028", "Liverpool F.C.", "Liverpool"),
                            ("pl029", "Manchester United F.C.", "Manchester United")]:
    def _mk(pid, club, label):
        @prompt(pid, f"Name a player who has scored a Premier League hat-trick for {label}",
                f"en:List of Premier League hat-tricks — rows where {label} is the scoring side", family="pl-hattrick-club")
        def f():
            return _club_ht(club, label)
        return f
    _mk(_pid, _club, _label)


# ------------------------------------------------------------ season tables

def season_table(page, stat, rank_ok=lambda r, v: True):
    """Rows of the season page's 'Rank | Player | Club | <stat>' table(s): [(rank, name, title, value)]."""
    out = []
    for hs, h, data in tables(page, ["Rank", "Player", stat]):
        if "Club" not in h:
            continue
        for tx, ln in data:
            v = re.match(r"\d+", tx[h.index(stat)])
            if not v:
                continue
            pi = h.index("Player")
            out.append((tx[0], clean(re.sub(r"\s\d+$", "", tx[pi])), person_title(ln[pi], re.sub(r"\s\d+$", "", tx[pi])),
                        int(v.group())))
        if out:
            break
    return out


@prompt("pl030", "Name a player who has scored 20+ Premier League goals in a single season since 2015–16",
        "en:2015–16 Premier League … 2025–26 Premier League — Top scorers tables, 20+ goals", family="pl-season-goals")
def pl030():
    acc = Acc()
    for y in range(2015, 2026):
        for rk, name, title, v in season_table(pl_page(y), "Goals"):
            if v >= 20:
                acc.add(title, name, f"{v} goals, {season(y)}")
    return acc.out()


@prompt("pl031", "Name a player who finished in the top ten of a Premier League season's scoring charts since 2015–16",
        "en:2015–16 Premier League … 2025–26 Premier League — Top scorers tables", family="pl-season-goals")
def pl031():
    acc = Acc()
    for y in range(2015, 2026):
        for rk, name, title, v in season_table(pl_page(y), "Goals"):
            acc.add(title, name, f"{v} goals, {season(y)}")
    return acc.out()


@prompt("pl032", "Name a goalkeeper who finished in the top ten of a Premier League season's clean-sheets chart since 2015–16",
        "en:2015–16 Premier League … 2025–26 Premier League — Clean sheets tables", family="pl-season-cleansheets")
def pl032():
    acc = Acc()
    for y in range(2015, 2026):
        for rk, name, title, v in season_table(pl_page(y), "Clean sheets"):
            acc.add(title, name, f"{v} clean sheets, {season(y)}")
    return acc.out()


@prompt("pl033", "Name a player who finished in the top ten of an EFL Championship season's scoring charts since 2020–21",
        "en:2020–21 EFL Championship … 2025–26 EFL Championship — Top scorers tables", family="pl-season-goals-champ")
def pl033():
    acc = Acc()
    for y in range(2020, 2026):
        for rk, name, title, v in season_table(champ_page(y), "Goals"):
            acc.add(title, name, f"{v} goals, {season(y)}")
    return acc.out()


@prompt("pl034", "Name a player who has been the Championship's top scorer (including shared) in a season since 2010–11",
        "en:2010–11 Football League Championship … 2025–26 EFL Championship — Top scorers table, rank 1", family="pl-season-goals-champ")
def pl034():
    acc = Acc()
    for y in range(2010, 2026):
        for rk, name, title, v in season_table(champ_page(y), "Goals"):
            if rk.strip() == "1":
                acc.add(title, name, f"{v} goals, {season(y)}")
    return acc.out()
