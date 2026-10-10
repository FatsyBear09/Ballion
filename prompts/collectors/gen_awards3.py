"""gen025-gen029: UEFA Golden Jubilee poll, women's football."""
import re

from ballion.registry import prompt
from prompts.collectors.gen_awards2 import _ranked
from prompts.collectors.gen_util import Acc, NAT_TEAM, find_tab, people


@prompt("gen025", "Name a player in the top 50 of the UEFA Golden Jubilee Poll (2004)",
        "en:UEFA Golden Jubilee Poll — 'Full results' table")
def golden_jubilee():
    tb = find_tab("UEFA Golden Jubilee Poll", ["Player", "Nation", "Votes"])
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        for t, a in people(ln[ci])[-1:]:
            acc.add(t, a, f"#{tx[0]}")
    return acc.out()


@prompt("gen026", "Name a woman who finished in the top 3 for the Ballon d'Or Féminin (2018–2025)",
        "en:Ballon d'Or Féminin — winners table, ranks 1–3")
def bdo_feminin_top3():
    return _ranked("Ballon d'Or Féminin", "Winners", ["Year", "Rank", "Player"], 3, Acc(), "", year_col="Year").out()


@prompt("gen028", "Name a player on the list of the most expensive women's football transfers",
        "en:List of most expensive women's association football transfers — 'Most expensive player transfers' table")
def women_transfers():
    tb = find_tab("List of most expensive women's association football transfers", ["Rank", "Player", "From", "To"],
                  heading="Most expensive player transfers")
    ci = tb.col("Player")
    acc = Acc()
    for tx, ln in tb.body:
        if not tx[0].strip().isdigit():
            continue
        for t, a in people(ln[ci])[-1:]:
            acc.add(t, a, f"#{tx[0]}")
    return acc.out()


@prompt("gen029", "Name a club that has played in the NWSL (2013–2026, incl. former clubs)",
        "en:National Women's Soccer League — current teams + former teams tables")
def nwsl_clubs():
    acc = Acc("club")
    for heading in ("Current teams", "Former teams"):
        tb = find_tab("National Women's Soccer League", ["Team", "Location", "Stadium"], heading=heading)
        ci = tb.col("Team")
        for tx, ln in tb.body:
            for t, a in ln[ci][:1]:
                acc.add(t, a, heading.split()[0].lower())
    return acc.out()


@prompt("gen181", "Name a player nominated for the men's Kopa Trophy or Yashin Trophy in 2026",
        "en:2026 Ballon d'Or — Men's Kopa Trophy and Men's Yashin Trophy nominee lists")
def kopa_yashin_2026():
    acc = Acc()
    for heading in ("Men's Kopa Trophy", "Men's Yashin Trophy"):
        tb = find_tab("2026 Ballon d'Or", ["Player"], heading=heading)
        ci = tb.col("Player")
        for tx, ln in tb.body:
            for t, a in people(ln[ci])[-1:]:
                acc.add(t, a, heading.split()[1])
    return acc.out()
