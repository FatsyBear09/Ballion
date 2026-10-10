"""pl001-pl021: Premier League / EFL individual and club awards."""
import re

from ballion.registry import prompt
from prompts.collectors.pl_util import Acc, dedupe, season_start, tables, year_of

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def _since_aug2015(month, yeartxt):
    y = year_of(yeartxt)
    return y is not None and (y > 2015 or (y == 2015 and month.strip() in MONTHS[7:]))


def monthly(page, col, since=_since_aug2015):
    acc = Acc()
    for hs, h, data in tables(page, ["Month", "Year", col]):
        ci, mi, yi = h.index(col), h.index("Month"), h.index("Year")
        for tx, ln in data:
            if tx[mi] not in MONTHS or not since(tx[mi], tx[yi]):
                continue
            acc.addrow(ln[ci], tx[ci], f"{tx[mi]} {year_of(tx[yi])}")
        break
    return acc.out()


def monthly_all(page, col):
    return monthly(page, col, lambda m, y: True)


@prompt("pl001", "Name a player who has won Premier League Player of the Month since 2015–16",
        "en:Premier League Player of the Month — winners table from August 2015", family="pl-award-monthly-player")
def pl001():
    return monthly("Premier League Player of the Month", "Player")


@prompt("pl002", "Name a manager who has won Premier League Manager of the Month since 2015–16",
        "en:Premier League Manager of the Month — winners table from August 2015", family="pl-award-monthly-manager")
def pl002():
    return monthly("Premier League Manager of the Month", "Manager")


def goal_or_save(page):
    acc = Acc()
    for hs, h, data in tables(page, ["Month", "Year", "Player"]):
        ci, mi, yi = h.index("Player"), h.index("Month"), h.index("Year")
        for tx, ln in data:
            if tx[mi] in MONTHS:
                acc.addrow(ln[ci], tx[ci], f"{tx[mi]} {year_of(tx[yi])}")
    return acc.out()


@prompt("pl003", "Name a player who has won Premier League Goal of the Month",
        "en:Premier League Goal of the Month — winners table (award began 2016–17)", family="pl-award-goal-month")
def pl003():
    return goal_or_save("Premier League Goal of the Month")


@prompt("pl004", "Name a goalkeeper who has won Premier League Save of the Month",
        "en:Premier League Save of the Month — winners table", family="pl-award-save-month")
def pl004():
    return goal_or_save("Premier League Save of the Month")


def pfa_toty(pages, league_re, season_ok):
    acc = Acc()
    for page in pages:
        for hs, h, data in tables(page, ["Pos.", "Player", "Club"]):
            _, season, league = hs
            if not re.fullmatch(league_re, league) or not season_ok(season_start(season)):
                continue
            for tx, ln in data:
                acc.addrow(ln[h.index("Player")], tx[h.index("Player")], season.replace("-", "–"))
    return acc.out()


@prompt("pl005", "Name a player picked in the PFA Premier League Team of the Year since 2015–16",
        "en:PFA Team of the Year (2010s) + (2020s) — 'Premier League' team, 2015–16 onward", family="pl-pfa-toty")
def pl005():
    return pfa_toty(["PFA Team of the Year (2010s)", "PFA Team of the Year (2020s)"], r"Premier League",
                    lambda y: y is not None and y >= 2015)


@prompt("pl006", "Name a player picked in the PFA Championship Team of the Year since 2019–20",
        "en:PFA Team of the Year (2020s) — 'Championship' team, 2019–20 onward", family="pl-pfa-toty")
def pl006():
    return pfa_toty(["PFA Team of the Year (2020s)"], r"Championship", lambda y: y is not None and y >= 2019)


@prompt("pl007", "Name a player who has won EFL Championship Player of the Month since 2015–16",
        "en:EFL Championship Player of the Month — winners table from August 2015", family="pl-award-monthly-champ-player")
def pl007():
    return monthly("EFL Championship Player of the Month", "Player")


@prompt("pl008", "Name a manager who has won EFL Championship Manager of the Month since 2015–16",
        "en:EFL Championship Manager of the Month — winners table from August 2015", family="pl-award-monthly-champ-manager")
def pl008():
    return monthly("EFL Championship Manager of the Month", "Manager")


@prompt("pl010", "Name a winner of the PFA Young Player of the Year since 1999–2000",
        "en:PFA Young Player of the Year — winners table, 1999–2000 onward", family="pl-pfa-young")
def pl010():
    acc = Acc()
    for hs, h, data in tables("PFA Young Player of the Year", ["Year", "Player", "Club"]):
        for tx, ln in data:
            y = season_start(tx[0])
            if y and y >= 1999:
                acc.addrow(ln[2], tx[2], tx[0])
        break
    return acc.out()


@prompt("pl011", "Name a player who has won Premier League Goal of the Season",
        "en:Premier League Goal of the Season — winners tables", family="pl-award-goal-season")
def pl011():
    acc = Acc()
    for hs, h, data in tables("Premier League Goal of the Season", ["Season", "Player", "Team"]):
        for tx, ln in data:
            if season_start(tx[0]):
                acc.addrow(ln[1], tx[1], tx[0])
    return acc.out()


@prompt("pl012", "Name a winner of Premier League Manager of the Season",
        "en:Premier League Manager of the Season — winners table", family="pl-award-manager-season")
def pl012():
    acc = Acc()
    for hs, h, data in tables("Premier League Manager of the Season", ["Season", "Manager", "Club"]):
        for tx, ln in data:
            if season_start(tx[0]):
                acc.addrow(ln[1], tx[1], tx[0])
        break
    return acc.out()


@prompt("pl013", "Name a Premier League Hall of Fame inductee",
        "en:Premier League Hall of Fame — player and managerial inductees", family="pl-hall-of-fame")
def pl013():
    acc = Acc()
    for col in ("Player", "Manager"):
        for hs, h, data in tables("Premier League Hall of Fame", ["Year", col]):
            for tx, ln in data:
                if re.fullmatch(r"\d{4}", tx[0]):
                    acc.addrow(ln[h.index(col)], tx[h.index(col)], f"inducted {tx[0]}")
            break
    return acc.out()


@prompt("pl014", "Name a winner of the Alan Hardaker Trophy (League Cup final man of the match)",
        "en:Alan Hardaker Trophy — winners table", family="pl-hardaker")
def pl014():
    acc = Acc()
    for hs, h, data in tables("Alan Hardaker Trophy", ["Final", "Player", "Team"]):
        for tx, ln in data:
            if re.fullmatch(r"\d{4}", tx[0]):
                acc.addrow(ln[1], tx[1], tx[0])
        break
    return acc.out()


@prompt("pl015", "Name a winner of the LMA Manager of the Year award",
        "en:League Managers Association Awards — LMA Manager of the Year table", family="pl-lma")
def pl015():
    acc = Acc()
    for hs, h, data in tables("League Managers Association Awards", ["Year", "Manager", "Club"]):
        for tx, ln in data:
            if re.fullmatch(r"\d{4}", tx[0]):
                acc.addrow(ln[1], tx[1], tx[0])
        break
    return acc.out()


@prompt("pl016", "Name a winner of Chelsea's Player of the Season award since 2000",
        "en:Chelsea F.C. Player of the Season — award recipients, 2000 onward", family="pl-club-pots")
def pl016():
    acc = Acc()
    for hs, h, data in tables("Chelsea F.C. Player of the Season", ["Year", "Player", "Position"]):
        for tx, ln in data:
            if re.fullmatch(r"\d{4}", tx[0]) and int(tx[0]) >= 2000:
                acc.addrow(ln[1], tx[1], tx[0])
        break
    return acc.out()


@prompt("pl017", "Name a winner of Manchester United's Sir Matt Busby Player of the Year since 2000",
        "en:Sir Matt Busby Player of the Year — winners table, 1999–2000 onward", family="pl-club-pots")
def pl017():
    acc = Acc()
    for hs, h, data in tables("Sir Matt Busby Player of the Year", ["Season", "Name", "Position"]):
        for tx, ln in data:
            y = season_start(tx[0])
            if y and y >= 1999:
                acc.addrow(ln[1], tx[1], tx[0])
        break
    return acc.out()


@prompt("pl018", "Name a winner of the PFA Fans' Player of the Year in the Premier League",
        "en:PFA Fans' Player of the Year — top-flight winner each year", family="pl-pfa-fans")
def pl018():
    acc = Acc()
    for hs, h, data in tables("PFA Fans' Player of the Year", ["League", "Player", "Club"]):
        for tx, ln in data[:1]:
            if "Premier" in tx[0]:
                acc.addrow(ln[1], tx[1], hs[0])
    return acc.out()


@prompt("pl019", "Name a player picked in the PFA Premier League Team of the Year in the 2000s",
        "en:PFA Team of the Year (2000s) — 'FA Premier League' team, 2000–01 to 2009–10", family="pl-pfa-toty-decade")
def pl019():
    return pfa_toty(["PFA Team of the Year (2000s)"], r"(FA )?Premier League", lambda y: y is not None and 2000 <= y <= 2009)


@prompt("pl020", "Name a player picked in the PFA Premier League Team of the Year in the 1990s",
        "en:PFA Team of the Year (1990s) + (2000s) — top-flight team, 1992–93 to 1999–2000", family="pl-pfa-toty-decade")
def pl020():
    a = pfa_toty(["PFA Team of the Year (1990s)"], r"(FA )?Premier(ship| League)", lambda y: y is not None and y >= 1992)
    b = pfa_toty(["PFA Team of the Year (2000s)"], r"(FA )?Premier League", lambda y: y == 1999)
    return dedupe(a + b)


@prompt("pl021", "Name a winner of the EFL Championship Player of the Season award",
        "en:EFL Awards — 'Championship Player of the Year' row in each yearly table", family="pl-efl-award")
def pl021():
    acc = Acc()
    for hs, h, data in tables("EFL Awards", ["Award", "Winner"]):
        for tx, ln in data:
            if re.fullmatch(r"Championship Player of the (Year|Season)", tx[0].strip()) and ln[1]:
                acc.add(ln[1][0], re.sub(r"\s*\(.*", "", tx[1]), hs[0].split()[0])
    return acc.out()
