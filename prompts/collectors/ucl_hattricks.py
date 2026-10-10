"""ucl124-ucl132: Champions League hat-tricks (List of UEFA Champions League hat-tricks)."""
import re
from datetime import datetime
from functools import lru_cache

from ballion.registry import prompt
from ballion.tables import rows, wikitables
from prompts.collectors.ucl_finals_parse import country_rec, name_of
from prompts.collectors.ucl_matches import FED
from prompts.collectors.ucl_util import dedupe

PAGE = "List of UEFA Champions League hat-tricks"
CUTOFF = datetime(2026, 7, 1)  # freeze at the end of 2025–26 (the list also holds 2026–27 rows)
BIG5 = {"England", "Spain", "Germany", "Italy", "France"}
UEFA = {"Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium", "Bosnia and Herzegovina",
        "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "England", "Estonia", "Faroe Islands",
        "Finland", "France", "Georgia", "Georgia (country)", "Germany", "Gibraltar", "Greece", "Hungary", "Iceland",
        "Israel", "Italy", "Kazakhstan", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta",
        "Moldova", "Montenegro", "Netherlands", "North Macedonia", "Northern Ireland", "Norway", "Poland", "Portugal",
        "Republic of Ireland", "Romania", "Russia", "San Marino", "Scotland", "Serbia", "Slovakia", "Slovenia",
        "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine", "Wales", "Yugoslavia", "FR Yugoslavia",
        "Serbia and Montenegro", "Czechoslovakia", "Soviet Union", "Ireland"}


@lru_cache(maxsize=None)
def hattricks():
    t = wikitables(PAGE)[1]
    out = []
    for tx, ln in list(rows(t))[1:]:
        if len(tx) < 5 or len(ln[0]) < 1 or len(ln[1]) < 1:
            continue
        try:
            d = datetime.strptime(tx[4].strip(), "%d %B %Y")
        except ValueError:
            continue
        if d >= CUTOFF:
            continue
        player = ln[0][-1]
        nat = ln[0][0] if len(ln[0]) > 1 else ""
        club_country = FED.get(ln[1][0], ln[1][0]) if len(ln[1]) > 1 else ""
        goals = re.search(r"\s([45])\b", tx[0])
        out.append({"title": player, "name": name_of(player), "nat": nat, "club": tx[1], "country": club_country,
                    "date": d, "goals": int(goals.group(1)) if goals else 3, "vs": tx[2]})
    return out


def _recs(pred):
    recs = [{"answer": h["name"], "enwiki": h["title"],
             "detail": f"{h['date']:%Y-%m-%d} {h['club']} v {h['vs']}" + (f" ({h['goals']} goals)" if h["goals"] > 3 else "")}
            for h in hattricks() if pred(h)]
    return dedupe(recs)


prompt("ucl124", "Name a player who has scored a Champions League hat-trick from 2015–16 to 2025–26",
       f"en:{PAGE} — hat-tricks dated 1 July 2015 to 30 June 2026", family="ucl-hattricks")(
    lambda: _recs(lambda h: h["date"] >= datetime(2015, 7, 1)))
prompt("ucl125", "Name a player who has scored a Champions League hat-trick in 2024–25 or 2025–26 "
                 "(the league-phase era)",
       f"en:{PAGE} — hat-tricks dated 1 July 2024 to 30 June 2026", family="ucl-hattricks")(
    lambda: _recs(lambda h: h["date"] >= datetime(2024, 7, 1)))
prompt("ucl126", "Name a player who has scored four or more goals in a Champions League match (to 2025–26)",
       f"en:{PAGE} — rows marked with 4 or 5 goals", family="ucl-hattricks")(
    lambda: _recs(lambda h: h["goals"] >= 4))
prompt("ucl127", "Name a player who has scored a Champions League hat-trick for an English club (to 2025–26)",
       f"en:{PAGE} — 'For' club is English", family="ucl-hattricks")(
    lambda: _recs(lambda h: h["country"] == "England"))
prompt("ucl128", "Name a player who has scored a Champions League hat-trick for a Spanish club (to 2025–26)",
       f"en:{PAGE} — 'For' club is Spanish", family="ucl-hattricks")(
    lambda: _recs(lambda h: h["country"] == "Spain"))
prompt("ucl129", "Name a player who has scored a Champions League hat-trick for a club outside the big five leagues "
                 "(to 2025–26; big five = England, Spain, Germany, Italy, France)",
       f"en:{PAGE} — 'For' club not from England, Spain, Germany, Italy or France", family="ucl-hattricks")(
    lambda: _recs(lambda h: h["country"] not in BIG5))
prompt("ucl130", "Name a player from outside Europe who has scored a Champions League hat-trick "
                 "(by national team; to 2025–26)",
       f"en:{PAGE} — player's flag icon is a non-UEFA nation", family="ucl-hattricks")(
    lambda: _recs(lambda h: h["nat"] and h["nat"] not in UEFA))
prompt("ucl131", "Name a player who scored a Champions League hat-trick from 1992–93 to 2014–15",
       f"en:{PAGE} — hat-tricks dated before 1 July 2015", family="ucl-hattricks")(
    lambda: _recs(lambda h: h["date"] < datetime(2015, 7, 1)))


@prompt("ucl132", "Name a country whose national team has had a player score a Champions League hat-trick (to 2025–26)",
        f"en:{PAGE} — nationality of the hat-trick scorers (flag icon)", family="ucl-hattricks-countries")
def countries():
    seen = {}
    for h in hattricks():
        if h["nat"]:
            seen.setdefault(re.sub(r"\s*\(.*\)$", "", h["nat"]), []).append(h["name"])
    return dedupe([{**country_rec(c), "detail": f"e.g. {ps[0]}"} for c, ps in seen.items()])
