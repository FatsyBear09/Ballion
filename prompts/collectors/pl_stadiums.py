"""pl150-pl154: English stadiums."""
import re

from ballion.registry import prompt
from prompts.collectors.pl_util import Acc, clean, tables


def _num(s):
    return int(re.sub(r"\D", "", s.split("(")[0]) or 0)


def league_stadiums(page):
    acc = Acc()
    for hs, h, data in tables(page, ["Team", "Stadium", "Capacity"]):
        si, ti = h.index("Stadium"), h.index("Team")
        for tx, ln in data:
            if ln[si]:
                acc.add(ln[si][-1], re.sub(r"\s*\(.*", "", tx[si]), f"{tx[ti]} ({tx[h.index('Capacity')]})")
        break
    return acc.out()


@prompt("pl150", "Name the home stadium of a Championship club in 2025–26",
        "en:2025–26 EFL Championship — Stadiums and locations", family="pl-stadium-league")
def pl150():
    return league_stadiums("2025–26 EFL Championship")


@prompt("pl151", "Name the home stadium of a League One club in 2025–26",
        "en:2025–26 EFL League One — Stadiums and locations", family="pl-stadium-league")
def pl151():
    return league_stadiums("2025–26 EFL League One")


@prompt("pl153", "Name the home stadium of a League Two club in 2025–26",
        "en:2025–26 EFL League Two — Stadiums and locations", family="pl-stadium-league")
def pl153():
    return league_stadiums("2025–26 EFL League Two")


@prompt("pl152", "Name a Premier League stadium that opened in 2000 or later",
        "en:List of Premier League stadiums — grounds with an Opened year of 2000 or later", family="pl-stadium-pl")
def pl152():
    acc = Acc()
    for hs, h, data in tables("List of Premier League stadiums", ["Stadium", "Club", "Opened"]):
        si, ci, oi = h.index("Stadium"), h.index("Club"), h.index("Opened")
        for tx, ln in data:
            m = re.match(r"(\d{4})", tx[oi].strip())
            if m and int(m.group(1)) >= 2000 and ln[si]:
                name = re.sub(r"\s*\(also known as ([^)]*)\)", r" (\1)", tx[si])
                name = re.split(r"\s+Formerly\s+", name)[0].strip()
                acc.add(ln[si][-1], re.sub(r"\s*\(.*", "", name), f"{tx[ci]}, opened {m.group(1)}")
        break
    return acc.out()


@prompt("pl154", "Name a football stadium in England with a capacity of 30,000 or more",
        "en:List of football stadiums in England — current stadiums with capacity >= 30,000", family="pl-stadium-capacity")
def pl154():
    acc = Acc()
    for hs, h, data in tables("List of football stadiums in England", ["Stadium", "Capacity", "Home team"]):
        si, ci = h.index("Stadium"), h.index("Capacity")
        for tx, ln in data:
            if _num(tx[ci]) >= 30000 and ln[si] and not re.search(r"Cardiff|Swansea|Wrexham", " ".join(tx)):
                acc.add(ln[si][-1], re.sub(r"\s*\(.*", "", tx[si]), f"{tx[ci]}")
        break
    return acc.out()
