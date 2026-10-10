"""ll018-ll023, ll134: El Clásico and the big two."""
import re

from ballion.registry import prompt
from prompts.collectors.ll_util import clean, dedupe, find, tables, parse_date

CL = "El Clásico"
CLM = "List of El Clásico matches"


def nm(title):
    return re.sub(r"\s*\([^)]*\)$", "", title)


@prompt("ll018", "Name a player who has scored in El Clásico since 2015–16 (own goals excluded)",
        "en:List of El Clásico matches — goalscorers in La Liga, Copa del Rey, Supercopa and Champions League meetings from 2015–16")
def ll018():
    out = []
    for tb in tables(CLM):
        h = tb["hdr"]
        if "Goals (home)" not in h or tb["head"].startswith(("Friendl", "Reserve", "Copa del Rey matches between", "Copa de la Coronaci")):
            continue
        gi, ga = h.index("Goals (home)"), h.index("Goals (away)")
        for tx, ln in tb["rows"]:
            if len(tx) <= ga:
                continue
            if "Date" in h:
                d = parse_date(tx[h.index("Date")])
                if not d or d.year * 100 + d.month < 201508:
                    continue
            else:
                m = re.match(r"(\d{4})", tx[0])
                if not m or int(m.group(1)) < 2015:
                    continue
            for ci in (gi, ga):
                for t, anchor in ln[ci]:
                    if t.startswith(("Penalty", "Own goal", "Association football")):
                        continue
                    cell = tx[ci]
                    mm = re.search(re.escape(anchor) + r"\s*\(([^)]*)\)", cell)
                    if mm and re.search(r"o\.\s?g", mm.group(1)):
                        continue
                    out.append({"answer": nm(t), "enwiki": t, "detail": f"{tx[0]}"})
    return dedupe(out)


@prompt("ll019", "Name a player who has scored a hat-trick in El Clásico",
        "en:El Clásico — Hat-tricks")
def ll019():
    tb = find(CL, "No.", ["Player", "Date"], head="Hat-tricks")
    pi = tb["hdr"].index("Player")
    out = []
    for tx, ln in tb["rows"]:
        if len(tx) > pi and ln[pi] and tx[0].isdigit():
            out.append({"answer": re.sub(r"\s+\d$", "", clean(tx[pi])), "enwiki": ln[pi][-1][0], "detail": f"{tx[2]}, {tx[4]}"})
    return dedupe(out)


@prompt("ll020", "Name a player among El Clásico's all-time top goalscorers (overall or in a single competition)",
        "en:El Clásico — Goalscoring tables (overall and per competition)")
def ll020():
    out = []
    for tb in tables(CL):
        h = tb["hdr"]
        if tb["head"] != "Goalscoring" or "Player" not in h or "Club" not in h:
            continue
        pi = h.index("Player")
        for tx, ln in tb["rows"]:
            if len(tx) > pi and ln[pi] and (tx[0].isdigit() or "Competition" in h):
                out.append({"answer": clean(tx[pi]), "enwiki": ln[pi][-1][0], "detail": tx[2] if len(tx) > 2 else ""})
    return dedupe(out)


def _top(page, idx_head, first="Rank", need=("Player",), nth=0):
    res = find(page, first, need, head=idx_head, all_=True)
    return res[nth]


def _people(tb, col="Player", detail_col=None):
    h = tb["hdr"]
    pi = h.index(col)
    out = []
    for tx, ln in tb["rows"]:
        if len(tx) > pi and ln[pi] and tx[0].strip().isdigit():
            out.append({"answer": clean(tx[pi]), "enwiki": ln[pi][-1][0],
                        "detail": (tx[h.index(detail_col)] if detail_col else "")})
    return out


RM = "List of Real Madrid CF records and statistics"
FCB = "List of FC Barcelona records and statistics"


@prompt("ll022", "Name a player in the all-time top 10 for appearances at Real Madrid or Barcelona",
        "en:List of Real Madrid CF records and statistics — Most appearances; List of FC Barcelona records and statistics — appearances")
def ll022():
    rm = _people(find(RM, "Rank", ["Player", "League", "Total"], head="Most appearances"), detail_col="Total")
    fc = _people(find(FCB, "Rank", ["Player", "League", "Total"], head="All competitions"), detail_col="Total")
    for r in rm:
        r["detail"] = "Real Madrid: " + r["detail"] + " apps"
    for r in fc:
        r["detail"] = "Barcelona: " + r["detail"] + " apps"
    return dedupe(rm + fc)


@prompt("ll023", "Name a player in the all-time top 10 goalscorers of Real Madrid or Barcelona",
        "en:List of Real Madrid CF records and statistics — Most goals; List of FC Barcelona records and statistics — All competitions (goals)")
def ll023():
    rm = _people(find(RM, "Rank", ["Player", "League", "Ratio"], head="Most goals"))
    fc = _people(find(FCB, "Rank", ["Player", "Official goals"]))
    for r in rm:
        r["detail"] = "Real Madrid top 10"
    for r in fc:
        r["detail"] = "Barcelona top 10"
    return dedupe(rm + fc)


@prompt("ll134", "Name a player in the top 10 of Real Madrid's or Barcelona's record transfer fees (paid or received)",
        "en:List of Real Madrid CF records and statistics / List of FC Barcelona records and statistics — highest transfer fees paid and received")
def ll134():
    out = []
    for page, tag in ((RM, "Real Madrid"), (FCB, "Barcelona")):
        for head in ("paid", "received"):
            tb = find(page, "Rank", ["Player"], head=("Highest transfer fees " + head) if page == RM else ("Transfer fee " + head))
            for r in _people(tb):
                r["detail"] = f"{tag} fee {head}"
                out.append(r)
    return dedupe(out)
