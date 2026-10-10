"""ucl189-ucl197: countries of winning managers, stadiums and cities."""
import re

from ballion.registry import prompt
from ballion.tables import rows, wikitables
from prompts.collectors.ucl_finals_parse import country_rec, name_of
from prompts.collectors.ucl_knockout import ko_matches, ko_page, season
from prompts.collectors.ucl_matches import matches
from prompts.collectors.ucl_util import dedupe


@prompt("ucl189", "Name a country that has produced a European Cup / Champions League-winning manager (1956 to 2026)",
        "en:List of European Cup and UEFA Champions League winning managers — nationality of winning managers",
        family="ucl-managers")
def manager_countries():
    t = wikitables("List of European Cup and UEFA Champions League winning managers")[0]
    seen = {}
    for tx, ln in list(rows(t))[1:]:
        if len(tx) > 2 and tx[0][:4].isdigit() and tx[1].strip():
            c = re.sub(r"\s*\(.*\)$", "", tx[1].strip())
            seen.setdefault("Germany" if c == "West Germany" else c, tx[2])
    return dedupe([{**country_rec(c), "detail": f"e.g. {m}"} for c, m in seen.items()])


def _venues(ms, key, label):
    recs = []
    for m in ms:
        t = m[key]
        if t:
            recs.append({"answer": name_of(t).split(",")[0] if key == "city" else name_of(t), "enwiki": t,
                         "detail": label})
    return dedupe(recs)


LP = "UEFA Champions League league phase"

for _pid, _page, _text, _label in [
        ("ucl190", f"2024–25 {LP}", "Name a stadium that hosted a 2024–25 Champions League league-phase match", "2024–25 league phase"),
        ("ucl191", f"2025–26 {LP}", "Name a stadium that hosted a 2025–26 Champions League league-phase match", "2025–26 league phase"),
        ("ucl192", "2023–24 UEFA Champions League group stage",
         "Name a stadium that hosted a 2023–24 Champions League group-stage match", "2023–24 group stage"),
        ("ucl195", f"2026–27 {LP}", "Name a stadium that hosts a 2026–27 Champions League league-phase match "
                                    "(scheduled fixtures as listed in October 2026)", "2026–27 league phase")]:
    prompt(_pid, _text, f"en:{_page} — match venues", family="ucl-stadiums")(
        (lambda p, l: (lambda: _venues(matches(p), "venue", l)))(_page, _label))


def _sf_stadiums(years):
    def fn():
        recs = []
        for y in years:
            recs += _venues(ko_matches(y, {"sf"}), "venue", f"{season(y)} semi-final")
        return dedupe(recs)
    return fn


prompt("ucl193", "Name a stadium that hosted a Champions League semi-final match, 2015–16 to 2025–26",
       "en:2015–16 to 2025–26 UEFA Champions League knockout phase pages — semi-final venues",
       family="ucl-stadiums")(_sf_stadiums(range(2015, 2026)))
prompt("ucl194", "Name a stadium that hosted a Champions League semi-final match, 2000–01 to 2014–15",
       "en:2000–01 to 2014–15 UEFA Champions League knockout stage/phase pages — semi-final venues",
       family="ucl-stadiums")(_sf_stadiums(range(2000, 2015)))


@prompt("ucl196", "Name a city that hosted a Champions League knockout-phase match, 2020–21 to 2025–26 "
                  "(play-offs and final included)",
        "en:2020–21 to 2025–26 UEFA Champions League knockout phase pages — match venue cities",
        family="ucl-cities")
def ko_cities():
    recs = []
    for y in range(2020, 2026):
        recs += _venues(ko_matches(y, {"po", "r16", "qf", "sf", "f"}), "city", f"{season(y)} knockout phase")
    return dedupe(recs)


@prompt("ucl197", "Name a city that hosts a home match in the 2026–27 Champions League league phase "
                  "(scheduled fixtures as listed in October 2026)",
        f"en:2026–27 {LP} — host cities of the listed matches", family="ucl-cities")
def lp27_cities():
    return _venues(matches(f"2026–27 {LP}"), "city", "2026–27 league phase")
