"""pl155-pl161: players in cup finals, the Community Shield, semi-finals and play-off finals."""
import re

from ballion.registry import prompt
from prompts.collectors.pl_util import Acc, final_page, section_boxes, tables


def season(y):
    return f"{y}–{(y + 1) % 100:02d}"


def starters(pages, label):
    acc = Acc()
    for p in pages:
        d = final_page(p)
        yr = p[:4]
        for (st, sub, mgr), team in zip(d["lineups"], (d["home"], d["away"])):
            for nm, t in st:
                acc.add(t, nm, f"{yr} {label} ({(team or '').replace(' F.C.', '').replace(' A.F.C.', '')})")
    return acc.out(maxev=3)


@prompt("pl155", "Name a player who started an FA Cup final from 2021 to 2026",
        "en:2021 FA Cup final … 2026 FA Cup final — starting XIs", family="pl-final-starters")
def pl155():
    return starters([f"{y} FA Cup final" for y in range(2021, 2027)], "FA Cup final")


@prompt("pl156", "Name a player who started a League Cup final from 2021 to 2026",
        "en:2021 EFL Cup final … 2026 EFL Cup final — starting XIs", family="pl-final-starters")
def pl156():
    return starters([f"{y} EFL Cup final" for y in range(2021, 2027)], "League Cup final")


@prompt("pl161", "Name a player who started a Community Shield match from 2020 to 2026",
        "en:2020 FA Community Shield … 2026 FA Community Shield — starting XIs", family="pl-final-starters")
def pl161():
    return starters([f"{y} FA Community Shield" for y in range(2020, 2027)], "Community Shield")


def match_scorers(d, tag):
    """Scorers of a parsed final: real goals only (a minute marker), no own goals, no shoot-out takers."""
    out = []
    for side in ("home", "away"):
        for nm, t, txt in d["goals_" + side]:
            if "'" not in txt or re.search(r"o\.g\.|own goal", txt, re.I):
                continue
            out.append((nm, t, tag))
    return out


def efl_final_pages(since):
    pages = []
    for hs, h, data in tables("List of EFL Cup finals", ["Winners", "Runners-up"]):
        if len(data) < 60:
            continue
        for tx, ln in data:
            fin = next((t for cell in ln for t in cell if re.fullmatch(r"\d{4} (Football League Cup|EFL Cup) [Ff]inal", t)), None)
            if fin and int(fin[:4]) >= since:
                pages.append(fin)
        break
    return pages


@prompt("pl157", "Name a player who has scored in a League Cup final since 2000 (own goals and penalty shoot-outs excluded)",
        "en:List of EFL Cup finals → each final's article, 2000 to 2026 — scorers of goals in play", family="pl-final-scorers")
def pl157():
    acc = Acc()
    for p in efl_final_pages(2000):
        d = final_page(p)
        for nm, t, tag in match_scorers(d, f"{p[:4]} League Cup final"):
            acc.add(t, nm, tag)
    return acc.out()


@prompt("pl158", "Name a player who has scored in the Community Shield since 2010 (own goals and penalty shoot-outs excluded)",
        "en:2010 FA Community Shield … 2026 FA Community Shield — scorers of goals in play", family="pl-final-scorers")
def pl158():
    acc = Acc()
    for y in range(2010, 2027):
        d = final_page(f"{y} FA Community Shield")
        for nm, t, tag in match_scorers(d, f"{y} Community Shield"):
            acc.add(t, nm, tag)
    return acc.out()


@prompt("pl159", "Name a player who has scored in an FA Cup semi-final since 2015–16",
        "en:2015–16 FA Cup … 2025–26 FA Cup — Semi-finals, scorers (own goals excluded)", family="pl-final-scorers")
def pl159():
    acc = Acc()
    for y in range(2015, 2026):
        for b in section_boxes(f"{season(y)} FA Cup", r"^Semi-?finals?$"):
            for nm, t, tag in match_scorers({"goals_home": b["goals_home"], "goals_away": b["goals_away"]}, f"{season(y)} semi-final"):
                acc.add(t, nm, tag)
    return acc.out()


@prompt("pl160", "Name a player who has scored in a Championship play-off final since 2016 (own goals and penalty shoot-outs excluded)",
        "en:EFL Championship play-offs → each play-off final article, 2016 to 2026 — scorers of goals in play", family="pl-final-scorers")
def pl160():
    acc = Acc()
    for hs, h, data in tables("EFL Championship play-offs", ["Year", "Winner", "Final", "Runner-up"]):
        fi = h.index("Final")
        for tx, ln in data:
            m = re.match(r"(\d{4})", tx[0])
            if not m or int(m.group(1)) < 2016 or not ln[fi]:
                continue
            fin = ln[fi][0]
            try:
                d = final_page(fin)
            except Exception:
                continue
            for nm, t, tag in match_scorers(d, f"{m.group(1)} play-off final"):
                acc.add(t, nm, tag)
        break
    return acc.out()
