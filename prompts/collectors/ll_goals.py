"""ll001-ll017: goals and scoring records."""
import re

from ballion.registry import prompt
from prompts.collectors.ll_util import clean, dedupe, find, parse_date, season_label, season_top

TOP = "List of La Liga top scorers"
HT = "List of La Liga hat-tricks"


def _hundred():
    tb = find(TOP, "Rank", ["Goals"], head="100 or more")
    out = []
    for tx, ln in tb["rows"]:
        if not tx[0].isdigit() or not ln[1]:
            continue
        out.append({"answer": clean(tx[1]), "enwiki": ln[1][-1][0], "last": int(tx[6][:4]),
                    "detail": f"{tx[2]} La Liga goals ({tx[5]}–{tx[6]})"})
    return out


def _strip(rs):
    return [{k: v for k, v in r.items() if k != "last"} for r in rs]


@prompt("ll001", "Name a player who has scored 100 or more La Liga goals",
        "en:List of La Liga top scorers — La Liga players with 100 or more goals")
def ll001():
    return dedupe(_strip(_hundred()))


@prompt("ll002", "Name a player who has scored 100 or more La Liga goals and played in La Liga in 2010 or later",
        "en:List of La Liga top scorers — 100+ goals table, 'Last' season >= 2010")
def ll002():
    return dedupe(_strip([r for r in _hundred() if r["last"] >= 2010]))


def _top_union(y0, y1, minval=0, kind="goal", fmt="{s} La Liga", word="goals"):
    recs = []
    for y in range(y0, y1 + 1):
        s = season_label(y)
        for name, title, club, val in season_top(fmt.format(s=s), kind):
            if val >= minval:
                recs.append({"answer": name, "enwiki": title, "detail": f"{val} {word}, {s}"})
    return dedupe(recs)


@prompt("ll003", "Name a player who finished in La Liga's top 10 scorers in a season from 2015–16 to 2025–26",
        "en:2015–16 La Liga … 2025–26 La Liga — Top goalscorers", family="ll-topscorers-era")
def ll003():
    return _top_union(2015, 2025)


@prompt("ll004", "Name a player who finished in La Liga's top 10 scorers in a season from 2009–10 to 2014–15",
        "en:2009–10 La Liga … 2014–15 La Liga — Top goalscorers", family="ll-topscorers-era")
def ll004():
    return _top_union(2009, 2014)


@prompt("ll005", "Name a player who finished in La Liga's top scorers table in a season from 2000–01 to 2008–09",
        "en:2000–01 La Liga … 2008–09 La Liga — Top goalscorers / Pichichi Trophy", family="ll-topscorers-era")
def ll005():
    return _top_union(2000, 2008)


@prompt("ll006", "Name a player who scored 20 or more La Liga goals in a season since 2010–11",
        "en:2010–11 La Liga … 2025–26 La Liga — Top goalscorers (20+ goals)")
def ll006():
    return _top_union(2010, 2025, 20)


@prompt("ll011", "Name a player who finished in La Liga's top 10 for assists in a season from 2015–16 to 2023–24",
        "en:2015–16 La Liga … 2023–24 La Liga — Top assists")
def ll011():
    return _top_union(2015, 2023, kind="assist", word="assists")


# ---------------------------------------------------------------- hat-tricks

def _ht_rows():
    tb = find(HT, "No.", ["Player", "Against", "Date"])
    h = tb["hdr"]
    pi, fi, ai, di = h.index("Player"), h.index("For"), h.index("Against"), h.index("Date")
    out = []
    for tx, ln in tb["rows"]:
        if len(tx) <= di or not ln[pi]:
            continue
        d = parse_date(tx[di])
        if not d:
            continue
        big = re.search(r"\s([4-9])$", tx[pi].strip())
        out.append({"player": (clean(re.sub(r"\s[4-9]$", "", tx[pi].strip())), ln[pi][-1][0]),
                    "for": tx[fi], "against": (clean(tx[ai]), ln[ai][-1][0] if ln[ai] else None),
                    "date": d, "goals": int(big.group(1)) if big else 3})
    return out


def _ht_players(pred):
    recs = [{"answer": r["player"][0], "enwiki": r["player"][1],
             "detail": f"{r['goals']} goals for {r['for']}, {r['date'].year}"}
            for r in _ht_rows() if pred(r)]
    return dedupe(recs)


AUG15 = parse_date("1 August 2015")
BIG3 = re.compile(r"Real Madrid|Barcelona|Atl[eé]tico")


@prompt("ll007", "Name a player who has scored a La Liga hat-trick since 2015–16",
        "en:List of La Liga hat-tricks — matches from August 2015", family="ll-hattrick")
def ll007():
    return _ht_players(lambda r: r["date"] >= AUG15)


@prompt("ll008", "Name a player who has scored a La Liga hat-trick since 2015–16 for a club other than Real Madrid, Barcelona or Atlético Madrid",
        "en:List of La Liga hat-tricks — 'For' column not Real Madrid/Barcelona/Atlético", family="ll-hattrick")
def ll008():
    return _ht_players(lambda r: r["date"] >= AUG15 and not BIG3.search(r["for"]))


@prompt("ll009", "Name a player who scored a La Liga hat-trick between 2004–05 and 2014–15",
        "en:List of La Liga hat-tricks — matches Aug 2004 to Jul 2015", family="ll-hattrick")
def ll009():
    return _ht_players(lambda r: parse_date("1 August 2004") <= r["date"] < AUG15)


@prompt("ll010", "Name a player who has scored 4 or more goals in a single La Liga match since 2000",
        "en:List of La Liga hat-tricks — matches marked 4/5 goals since 2000", family="ll-hattrick")
def ll010():
    return _ht_players(lambda r: r["goals"] >= 4 and r["date"].year >= 2000)


def _against(pred):
    recs = [{"answer": r["against"][0], "enwiki": r["against"][1], "detail": str(r["date"].year)}
            for r in _ht_rows() if pred(r) and r["against"][1]]
    return dedupe(recs)


@prompt("ll012", "Name a club Lionel Messi scored a La Liga hat-trick against",
        "en:List of La Liga hat-tricks — Messi rows, 'Against' column", family="ll-hattrick-against")
def ll012():
    return _against(lambda r: r["player"][1] == "Lionel Messi")


@prompt("ll013", "Name a club Cristiano Ronaldo scored a La Liga hat-trick against",
        "en:List of La Liga hat-tricks — Ronaldo rows, 'Against' column", family="ll-hattrick-against")
def ll013():
    return _against(lambda r: r["player"][1] == "Cristiano Ronaldo")


@prompt("ll014", "Name a club that has conceded a La Liga hat-trick since 2015–16",
        "en:List of La Liga hat-tricks — 'Against' column, matches from August 2015", family="ll-hattrick-against")
def ll014():
    return _against(lambda r: r["date"] >= AUG15)


@prompt("ll015", "Name a player who has made 400 or more La Liga appearances",
        "en:List of footballers with 400 or more La Liga appearances — list of players")
def ll015():
    tb = find("List of footballers with 400 or more La Liga appearances", "Rank", ["Apps"])
    out = []
    for tx, ln in tb["rows"]:
        if tx[0].isdigit() and ln[1]:
            out.append({"answer": clean(tx[1]), "enwiki": ln[1][-1][0], "detail": f"{tx[3]} La Liga apps"})
    return dedupe(out)


@prompt("ll016", "Name a player who finished in the Segunda División top scorers table in a season from 2019–20 to 2025–26",
        "en:2019–20 Segunda División … 2025–26 Segunda División — Top goalscorers")
def ll016():
    return _top_union(2019, 2025, fmt="{s} Segunda División")


@prompt("ll017", "Name a player who scored 3 or more goals in a single Copa del Rey season from 2022–23 to 2025–26",
        "en:2022–23 Copa del Rey … 2025–26 Copa del Rey — Top scorers (3+ goals)")
def ll017():
    return _top_union(2022, 2025, 3, fmt="{s} Copa del Rey")
