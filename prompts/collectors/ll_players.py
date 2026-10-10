"""ll119-ll123, ll125, ll191: club player lists and captains."""
import re

from ballion.registry import prompt
from prompts.collectors.ll_util import NAT_TEAM, clean, dedupe, find, season_label, tables

RMP = "List of Real Madrid CF players"
FCBP = "List of FC Barcelona players"
ATMP = "List of Atlético Madrid players"
RSP = "List of Real Sociedad players"


def career_bounds(s):
    """(first year, last year) of a career string like '1994–2010', '2025–', '1912–1916 ; 1918–1927'."""
    ys = [int(y) for y in re.findall(r"\d{4}", s)]
    if not ys:
        return None
    last = max(ys)
    if re.search(r"\d{4}\s*[–-]\s*(?!\d)", s.strip() + " ") and re.search(r"[–-]\s*$", s.strip()):
        last = 2026
    return min(ys), last


def _list(page, head, name_col, career_col, pred, pos_col=None, extra=None):
    tb = find(page, name_col if name_col else None, [career_col], head=head)
    h = tb["hdr"]
    ni = h.index(name_col)
    ci = [i for i, c in enumerate(h) if c.startswith(career_col)][0]
    out = []
    for tx, ln in tb["rows"]:
        if len(tx) <= ci or not ln[ni] or tx[ni] == name_col:
            continue
        b = career_bounds(tx[ci])
        if not b or not pred(b, tx, h):
            continue
        out.append({"answer": clean(re.sub(r"Spanish article", "", tx[ni])), "enwiki": ln[ni][0][0], "detail": tx[ci]})
    return dedupe(out)


@prompt("ll119", "Name a player who has made an official appearance for Real Madrid since 2020–21",
        "en:List of Real Madrid CF players — career ending 2021 or later", family="ll-club-players")
def ll119():
    return _list(RMP, "List of players", "Player", "Career", lambda b, tx, h: b[1] >= 2021)


@prompt("ll120", "Name a player who played for Real Madrid in the Galácticos era (2000–01 to 2005–06)",
        "en:List of Real Madrid CF players — Real Madrid career overlapping 2000–01 to 2005–06", family="ll-club-players")
def ll120():
    return _list(RMP, "List of players", "Player", "Career", lambda b, tx, h: b[0] <= 2005 and b[1] >= 2001)


@prompt("ll121", "Name a goalkeeper who has played for Real Madrid since 2000–01",
        "en:List of Real Madrid CF players — position GK, career ending 2001 or later", family="ll-club-players")
def ll121():
    return _list(RMP, "List of players", "Player", "Career", lambda b, tx, h: b[1] >= 2001 and tx[h.index("P")] == "GK")


@prompt("ll122", "Name a Barcelona player with 100 or more league appearances who played for the club in 2008 or later",
        "en:List of FC Barcelona players — 100+ league appearances, Barcelona career ending 2008 or later", family="ll-club-players")
def ll122():
    def pred(b, tx, h):
        m = re.match(r"\d+", tx[h.index("League appearances")].replace(",", ""))
        return b[1] >= 2008 and m is not None and int(m.group()) >= 100
    return _list(FCBP, "List of players", "Name", "Barcelona career", pred)


@prompt("ll123", "Name an Atlético Madrid player listed among the club's notable players whose Atlético career ran into 2012 or later",
        "en:List of Atlético Madrid players — Atlético career ending 2012 or later", family="ll-club-players")
def ll123():
    return _list(ATMP, "Players", "Player", "Atlético Madrid career", lambda b, tx, h: b[1] >= 2012)


@prompt("ll191", "Name a Real Sociedad player listed among the club's notable players whose spell there ran into 2010 or later",
        "en:List of Real Sociedad players — 'To' year 2010 or later", family="ll-club-players")
def ll191():
    tb = find(RSP, "Name", ["From", "To"], head="List of players")
    out = []
    for tx, ln in tb["rows"]:
        if len(tx) < 3 or not ln[0] or tx[0] == "Name":
            continue
        m = re.search(r"\d{4}", tx[2])
        if m and int(m.group()) >= 2010 or "present" in tx[2].lower():
            out.append({"answer": clean(tx[0]), "enwiki": ln[0][0][0], "detail": f"{tx[1]}–{tx[2]}"})
    return dedupe(out)


@prompt("ll125", "Name a player who has been named as captain of a La Liga club since 2020–21 (to 2026–27)",
        "en:2020–21 La Liga … 2026–27 La Liga — Personnel and kits (captain column)")
def ll125():
    out = []
    for y in range(2020, 2027):
        page = f"{season_label(y)} La Liga"
        for tb in tables(page):
            h = tb["hdr"]
            if h and h[0].startswith("Team") and any(c.startswith("Captain") for c in h):
                ci = [i for i, c in enumerate(h) if c.startswith("Captain")][0]
                for tx, ln in tb["rows"]:
                    if len(tx) > ci and ln[ci]:
                        pl = [l for l in ln[ci] if not NAT_TEAM.search(l[0])]
                        if pl:
                            out.append({"answer": clean(pl[0][1]), "enwiki": pl[0][0], "detail": f"{tx[0]}, {season_label(y)}"})
                break
    return dedupe(out)
