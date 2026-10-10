"""gen134-gen137: transfers and money."""
import re

from ballion.registry import prompt
from prompts.collectors.gen_util import Acc, NAT_TEAM, country_rec, dedupe, find_tab, first_person, people

PAGE = "List of most expensive association football transfers"


def _top50():
    return find_tab(PAGE, ["Rank", "Player", "From", "To", "Fee"], heading="Highest transfer records")


def _clubs(cell):
    return [(t, a) for t, a in cell if not NAT_TEAM.search(t)]


@prompt("gen134", "Name a player on the list of the 50 most expensive football transfers",
        "en:List of most expensive association football transfers — top-50 table", family="gen-transfer-records")
def top50_players():
    tb = _top50()
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if tx[0].strip().isdigit() and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], f"#{tx[0]} {tx[tb.col('Year')]}")
    return acc.out()


@prompt("gen135", "Name a club that bought or sold a player in one of the 50 most expensive transfers",
        "en:List of most expensive association football transfers — From and To columns of the top-50 table",
        family="gen-transfer-records")
def top50_clubs():
    tb = _top50()
    fi, ti = tb.col("From"), tb.col("To")
    acc = Acc("club")
    for tx, ln in tb.body:
        if tx[0].strip().isdigit():
            for ci, lab in ((fi, "sold"), (ti, "bought")):
                for t, a in _clubs(ln[ci])[-1:]:
                    acc.add(t, a, lab)
    return acc.out()


@prompt("gen136", "Name a country whose players appear in the 50 most expensive football transfers",
        "en:List of most expensive association football transfers — nationality flags of the top-50 table",
        family="gen-transfer-records")
def top50_countries():
    tb = _top50()
    ci = tb.col("Player")
    out = {}
    for (tx, ln), fl in zip(tb.body, tb.bflags):
        if tx[0].strip().isdigit() and fl[ci]:
            r = out.setdefault(fl[ci][0], country_rec(fl[ci][0]))
            r["detail"] += (", " if r["detail"] else "") + re.sub(r"\s*\(\d+\)", "", tx[ci])
    return dedupe(list(out.values()))


@prompt("gen137", "Name a club that has paid a world-record transfer fee (1893 onward)",
        "en:List of most expensive association football transfers — 'Historical progression' table, buying club",
        family="gen-transfer-records")
def record_buyers():
    tb = find_tab(PAGE, ["Year", "Player", "From", "To"], heading="Historical progression")
    ti = tb.col("To")
    acc = Acc("club")
    for tx, ln in tb.body:
        if re.match(r"\d{4}", tx[0]):
            for t, a in _clubs(ln[ti])[-1:]:
                acc.add(t, a, tx[0])
    return acc.out()
