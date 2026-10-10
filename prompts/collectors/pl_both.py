"""pl120-pl131: players who have played for both of two English clubs (Premier League era).

Uses the verified-candidate machinery from managers.py (Wikidata P54 on both clubs, then each
candidate's enwiki infobox 'Senior career' must show both clubs with >= 1 league appearance in some
spell; loans count, wartime guest spells don't).  The result is then limited to the stated era: the
last spell at each club must end in (or after) the cut-off year.
"""
import re

from ballion.registry import prompt
from ballion.wikidata import enwiki_title, sparql
from prompts.collectors import managers
from prompts.collectors.managers import played_both


def _wd_both(qa, qb):
    """Like managers._wikidata_both, but uses p:P54/ps:P54 so that preferred-rank 'current club'
    statements don't hide other clubs (wdt:P54 only returns preferred/normal-rank values)."""
    q = f"""SELECT ?art ?team ?s ?e WHERE {{
      ?p p:P54/ps:P54 wd:{qa} . ?p p:P54/ps:P54 wd:{qb} .
      ?art schema:about ?p ; schema:isPartOf <https://en.wikipedia.org/> .
      ?p p:P54 ?st . ?st ps:P54 ?team . FILTER(?team IN (wd:{qa}, wd:{qb}))
      OPTIONAL {{ ?st pq:P580 ?s }} OPTIONAL {{ ?st pq:P582 ?e }} }}"""
    out = {}
    for r in sparql(q):
        sp = out.setdefault(enwiki_title(r["art"]), {qa: [], qb: []})[r["team"].rsplit("/", 1)[1]]
        span = (r.get("s", "")[:4], r.get("e", "")[:4])
        if span not in sp:
            sp.append(span)
    return out


def played_both2(a, b):
    old = managers._wikidata_both
    managers._wikidata_both = _wd_both
    try:
        return played_both(a, b)
    finally:
        managers._wikidata_both = old

NOTE = "(≥1 league appearance for each club; loans count)"


def _last_year(seg):
    ys = [int(y) for y in re.findall(r"(?:18|19|20)\d\d", seg)]
    return max(ys) if ys else None


def era_filter(rows, labels, since):
    out = []
    for r in rows:
        ok = True
        for lab in labels:
            m = re.search(re.escape(lab) + r" ([^;\[]*)", r["detail"])
            ly = _last_year(m.group(1)) if m else None
            # open-ended spell ("2019–") shows only the start year, which is fine for a lower bound
            if ly is None or ly < since:
                ok = False
        if ok:
            out.append(r)
    return out


PAIRS = [
    ("pl120", ("Chelsea", "Chelsea F.C."), ("Manchester United", "Manchester United F.C."), 1993, "(Premier League era)"),
    ("pl121", ("Liverpool", "Liverpool F.C."), ("Manchester City", "Manchester City F.C."), 1993, "(Premier League era)"),
    ("pl122", ("Liverpool", "Liverpool F.C."), ("Chelsea", "Chelsea F.C."), 1993, "(Premier League era)"),
    ("pl123", ("Arsenal", "Arsenal F.C."), ("Manchester City", "Manchester City F.C."), 1993, "(Premier League era)"),
    ("pl124", ("Chelsea", "Chelsea F.C."), ("Manchester City", "Manchester City F.C."), 1993, "(Premier League era)"),
    ("pl125", ("Liverpool", "Liverpool F.C."), ("Tottenham", "Tottenham Hotspur F.C."), 1993, "(Premier League era)"),
    ("pl126", ("Everton", "Everton F.C."), ("Manchester United", "Manchester United F.C."), 1993, "(Premier League era)"),
    ("pl127", ("West Ham", "West Ham United F.C."), ("Tottenham", "Tottenham Hotspur F.C."), 1993, "(Premier League era)"),
    ("pl128", ("Newcastle", "Newcastle United F.C."), ("Sunderland", "Sunderland A.F.C."), 1993, "(Premier League era)"),
    ("pl129", ("Brighton", "Brighton & Hove Albion F.C."), ("Chelsea", "Chelsea F.C."), 2000, "since 2000"),
    ("pl130", ("Southampton", "Southampton F.C."), ("Liverpool", "Liverpool F.C."), 2000, "since 2000"),
    ("pl131", ("Leicester", "Leicester City F.C."), ("Chelsea", "Chelsea F.C."), 1993, "(Premier League era)"),
]


def _mk(pid, a, b, since, era):
    text = f"Name a player who has played for both {a[0]} and {b[0]} " + (
        f"({NOTE[1:-1]}; Premier League era)" if since == 1993 else f"({NOTE[1:-1]}; spells since {since})")

    @prompt(pid, text, f"Wikidata P54 for {a[0]} + {b[0]}, verified on enwiki infobox senior career; spells from {since} on",
            family="pl-played-for-both")
    def f():
        rows = played_both2(a, b)
        return era_filter(rows, [a[0], b[0]], since)
    return f


for _p in PAIRS:
    _mk(*_p)
