"""ll126-ll133, ll195, ll198, ll199: transfers in/out from club season pages."""
import re

from ballion.registry import prompt
from prompts.collectors.ll_util import NAT_TEAM, clean, dedupe, season_label, tables

PAGE = {
    "rm": "{s} Real Madrid CF season", "fcb": "{s} FC Barcelona season", "atm": "{s} Atlético Madrid season",
    "gir": "{s} Girona FC season", "vil": "{s} Villarreal CF season", "sev": "{s} Sevilla FC season",
    "bet": "{s} Real Betis season", "rso": "{s} Real Sociedad season", "val": "{s} Valencia CF season",
}
NAME = {"rm": "Real Madrid", "fcb": "Barcelona", "atm": "Atlético Madrid", "gir": "Girona", "vil": "Villarreal",
        "sev": "Sevilla", "bet": "Real Betis", "rso": "Real Sociedad", "val": "Valencia"}

IN_HEADS = re.compile(r"^(In|Transfers? in|Players? in|Loans? in|Incoming( transfers)?|Arrivals|Transfers( \(in\))?)$", re.I)
OUT_HEADS = re.compile(r"^(Out|Transfers? out|Players? out|Outgoing( transfers)?|Departures|Transfers \(out\))$", re.I)
NOT_PERMANENT = re.compile(r"loan|promot|youth|academy|return|B team|reserve|Castilla|Atl[eé]tic[o]? B|\bB\b", re.I)
SKIP_OUT = re.compile(r"loan|return", re.I)


def moves(page, direction):
    heads = IN_HEADS if direction == "in" else OUT_HEADS
    out = []
    for tb in tables(page):
        if not heads.match(tb["head"]):
            continue
        h = [c.strip() for c in tb["hdr"]]
        pi = next((i for i, c in enumerate(h) if c.startswith("Player") or c.startswith("Name")), None)
        if pi is None:
            continue
        for tx, ln in tb["rows"]:
            if len(tx) <= pi or not ln[pi]:
                continue
            rest = " ".join(t for i, t in enumerate(tx) if i != pi)
            pl = [l for l in ln[pi] if not NAT_TEAM.search(l[0])]
            if not pl:
                continue
            out.append({"answer": clean(pl[0][1]), "enwiki": pl[0][0], "rest": rest, "tx": tx})
    return out


def _is_loan_return(rest):
    return bool(re.search(r"loan return|return(ed)? from loan|end of loan|returns? from|promot|youth|academy|from .* B\b|Castilla|reserve", rest, re.I))


def _collect(club, y0, y1, direction):
    recs = []
    for y in range(y0, y1 + 1):
        s = season_label(y)
        page = PAGE[club].format(s=s)
        for m in moves(page, direction):
            rest = m["rest"]
            if direction == "in":
                if _is_loan_return(rest):
                    continue
            elif re.search(r"loan|return|promot", rest, re.I):
                continue
            recs.append({"answer": m["answer"], "enwiki": m["enwiki"], "detail": f"{s}"})
    return dedupe(recs)


def _in(pid, club, y0, y1):
    @prompt(pid, f"Name a player {NAME[club]} signed between {season_label(y0)} and {season_label(y1)} (transfers and loans in; loan returns and academy promotions excluded)",
            f"en:{PAGE[club].format(s=season_label(y0))} … {PAGE[club].format(s=season_label(y1))} — In (excluding loan returns, promotions)",
            family="ll-transfers-in")
    def fn():
        return _collect(club, y0, y1, "in")
    return fn


def _out(pid, club, y0, y1):
    @prompt(pid, f"Name a player who permanently left {NAME[club]} between {season_label(y0)} and {season_label(y1)} (loans out and loan returns excluded)",
            f"en:{PAGE[club].format(s=season_label(y0))} … {PAGE[club].format(s=season_label(y1))} — Out (excluding loans)",
            family="ll-transfers-out")
    def fn():
        return _collect(club, y0, y1, "out")
    return fn


_in("ll126", "rm", 2019, 2025)
_in("ll127", "fcb", 2019, 2025)
_in("ll128", "atm", 2019, 2025)
_in("ll129", "sev", 2019, 2025)
_in("ll130", "rso", 2019, 2025)
_in("ll131", "gir", 2022, 2025)
_in("ll195", "vil", 2019, 2025)
_in("ll199", "bet", 2019, 2025)
_out("ll132", "fcb", 2019, 2025)
_out("ll133", "rm", 2018, 2025)
_out("ll198", "val", 2019, 2025)
