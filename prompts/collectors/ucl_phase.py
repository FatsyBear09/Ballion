"""ucl112-ucl123: league-phase / group-stage goalscorers; ucl142-ucl151 style participants lists live here too."""
from ballion.registry import prompt
from prompts.collectors.ucl_matches import matches, scorer_recs
from prompts.collectors.ucl_util import dedupe

LP25 = "2025–26 UEFA Champions League league phase"
LP24 = "2024–25 UEFA Champions League league phase"
GS23 = "2023–24 UEFA Champions League group stage"
BIG5 = {"England", "Spain", "Germany", "Italy", "France"}


def _lp(page, pred, label):
    def fn():
        ms = matches(page)
        return dedupe(scorer_recs(ms, lambda m, side: pred(m["hc"] if side == 0 else m["ac"]), detail=label))
    return fn


SPECS = [
    ("ucl112", LP25, "an English club", "2025–26 league phase", lambda c: c == "England"),
    ("ucl113", LP25, "a Spanish club", "2025–26 league phase", lambda c: c == "Spain"),
    ("ucl114", LP25, "a German club", "2025–26 league phase", lambda c: c == "Germany"),
    ("ucl115", LP25, "an Italian club", "2025–26 league phase", lambda c: c == "Italy"),
    ("ucl116", LP25, "a club from outside the big five leagues (England, Spain, Germany, Italy, France)",
     "2025–26 league phase", lambda c: c not in BIG5),
    ("ucl117", LP24, "an English club", "2024–25 league phase", lambda c: c == "England"),
    ("ucl118", LP24, "a German club", "2024–25 league phase", lambda c: c == "Germany"),
    ("ucl119", LP24, "a French club", "2024–25 league phase", lambda c: c == "France"),
    ("ucl120", LP24, "a Spanish club", "2024–25 league phase", lambda c: c == "Spain"),
    ("ucl121", LP24, "a Dutch or Portuguese club", "2024–25 league phase", lambda c: c in ("Netherlands", "Portugal")),
    ("ucl122", LP25, "a French or Portuguese club", "2025–26 league phase", lambda c: c in ("France", "Portugal")),
    ("ucl123", GS23, "an English club", "2023–24 group stage", lambda c: c == "England"),
]
for _pid, _page, _who, _label, _pred in SPECS:
    if _pid == "ucl116":
        _text = ("Name a player who scored for a club outside the big five leagues in the 2025–26 Champions League "
                 "league phase (big five = England, Spain, Germany, Italy, France; own goals excluded)")
    else:
        _text = f"Name a player who scored for {_who} in the {_label[:7]} Champions League {_label[8:]} (own goals excluded)"
    prompt(_pid, _text, f"en:{_page} — match goals by clubs' association (flag icon)",
           family="ucl-lp-scorers")(_lp(_page, _pred, _label))
