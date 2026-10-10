"""gen001-gen029: Ballon d'Or, global awards, women's football."""
import re

from ballion.registry import prompt
from prompts.collectors.gen_util import (Acc, country_rec, dedupe, find_tab, find_tabs, people, strip_paren, tabs,
                                         NAT_TEAM, clean_name)


def bdo_page(y):
    return f"{y} FIFA Ballon d'Or" if 2010 <= y <= 2015 else f"{y} Ballon d'Or"


def bdo_table(y, **kw):
    """Men's ranking table (first table) of a Ballon d'Or year page."""
    return find_tab(bdo_page(y), ["Player"], first="Rank", **kw)


def bdo_tables(y):
    """Men's ranking tables: 2010-15 pages split the ranking over two tables."""
    if 2010 <= y <= 2015:
        return find_tabs(bdo_page(y), ["Player"], first="Rank", heading=r"^FIFA Ballon d'Or$")
    return [bdo_table(y)]


def bdo_players(years, acc=None, maxrank=None, label=True):
    acc = acc or Acc()
    for y in years:
        for tb in bdo_tables(y):
            ci = tb.col("Player")
            ri = tb.col("Rank")
            for tx, ln in tb.body:
                if len(tx) <= ci:
                    continue
                m = re.match(r"\d+", tx[ri])
                if maxrank and (not m or int(m.group()) > maxrank):
                    continue
                for t, a in people(ln[ci])[-1:]:
                    acc.add(t, a, str(y))
    return acc


def _mk_nominees(year):
    @prompt(f"gen{2027 - year:03d}", f"Name a player nominated for the {year} Ballon d'Or",
            f"en:{year} Ballon d'Or — men's nominee table", family="gen-bdo-nominees")
    def f():
        return bdo_players([year]).out()
    return f


for _y in range(2026, 2020, -1):
    _mk_nominees(_y)


@prompt("gen007", "Name a player nominated for the Ballon d'Or between 2016 and 2019",
        "en:2016 Ballon d'Or … en:2019 Ballon d'Or — men's nominee tables", family="gen-bdo-nominees")
def bdo_2016_19():
    return bdo_players(range(2016, 2020)).out()


@prompt("gen008", "Name a player on the FIFA Ballon d'Or shortlist between 2010 and 2015",
        "en:2010 FIFA Ballon d'Or … en:2015 FIFA Ballon d'Or — men's shortlist tables", family="gen-bdo-nominees")
def fifa_bdo_shortlists():
    return bdo_players(range(2010, 2016)).out()


BDO_YEARS_SINCE_2010 = [y for y in range(2010, 2026) if y != 2020]


@prompt("gen009", "Name a player who finished in the Ballon d'Or top 10 in a year from 2010 to 2025",
        "en:2010 FIFA Ballon d'Or … en:2025 Ballon d'Or — men's ranking tables, places 1–10 (no 2020 edition)",
        family="gen-bdo-nominees")
def bdo_top10():
    return bdo_players(BDO_YEARS_SINCE_2010, maxrank=10).out()
