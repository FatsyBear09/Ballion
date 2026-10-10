"""ucl133-ucl141 (+ ucl050 cross-check): season awards, top scorers, records pages."""
import re

from ballion.registry import prompt
from ballion.tables import rows, wikitables
from prompts.collectors.ucl_finals_parse import country_rec, name_of
from prompts.collectors.ucl_knockout import ko_page, season
from prompts.collectors.ucl_matches import matches
from prompts.collectors.ucl_util import dedupe

REC = "European Cup and UEFA Champions League records and statistics"


def season_page(y):
    return f"{season(y)} UEFA Champions League"


def _squad_rows(y):
    """[(pos, title, country)] from the season page's Squad / Team of the Season table."""
    for t in wikitables(season_page(y)):
        rs = list(rows(t))
        h = [c.strip() for c in rs[0][0]]
        if h and h[0].startswith("Pos") and any(c.startswith("Team") for c in h) and ("Name" in h or "Player" in h) and "Pld" not in h:
            ni = h.index("Name") if "Name" in h else h.index("Player")
            out = []
            for tx, ln in rs[1:]:
                if len(tx) > ni and ln[ni] and tx[0] in ("GK", "DF", "MF", "FW"):
                    nat = ln[ni][0] if len(ln[ni]) > 1 else ""
                    out.append((tx[0], ln[ni][-1], re.sub(r"\s*\(.*\)$", "", nat)))
            if out:
                return out
    raise LookupError(f"{season_page(y)}: squad table not found")


def _squad_recs(years, gk_only=False):
    recs = []
    for y in years:
        for pos, title, nat in _squad_rows(y):
            if gk_only and pos != "GK":
                continue
            recs.append({"answer": name_of(title), "enwiki": title, "detail": f"{season(y)} squad of the season",
                         "_nat": nat})
    return recs


def _countries(years):
    seen = {}
    for r in _squad_recs(years):
        if r["_nat"]:
            seen.setdefault(r["_nat"], r["detail"])
    return dedupe([{**country_rec(c), "detail": d} for c, d in seen.items()])


prompt("ucl133", "Name a player named in a Champions League Squad of the Season, 2015–16 to 2020–21",
       "en:2015–16 to 2020–21 UEFA Champions League season pages — Squad of the Season",
       family="ucl-squad-season")(lambda: dedupe(_squad_recs(range(2015, 2021))))
prompt("ucl134", "Name a player named in a Champions League Team of the Season, 2021–22 to 2025–26",
       "en:2021–22 to 2025–26 UEFA Champions League season pages — Team of the Season",
       family="ucl-squad-season")(lambda: dedupe(_squad_recs(range(2021, 2026))))
prompt("ucl135", "Name a goalkeeper named in a Champions League Squad or Team of the Season, 2015–16 to 2025–26",
       "en:2015–16 to 2025–26 UEFA Champions League season pages — goalkeepers in the Squad/Team of the Season",
       family="ucl-squad-season")(lambda: dedupe(_squad_recs(range(2015, 2026), gk_only=True)))
prompt("ucl136", "Name a country with a player named in a Champions League Team of the Season, 2021–22 to 2025–26",
       "en:2021–22 to 2025–26 UEFA Champions League season pages — Team of the Season flag icons",
       family="ucl-squad-season-countries")(lambda: _countries(range(2021, 2026)))
prompt("ucl137", "Name a country with a player named in a Champions League Squad of the Season, 2015–16 to 2020–21",
       "en:2015–16 to 2020–21 UEFA Champions League season pages — Squad of the Season flag icons",
       family="ucl-squad-season-countries")(lambda: _countries(range(2015, 2021)))


@prompt("ucl138", "Name a player who appears in a season's Champions League top goalscorers table, "
                  "2015–16 to 2025–26 (qualifying goals excluded)",
        "en:2015–16 to 2025–26 UEFA Champions League season pages — Statistics > Top goalscorers",
        family="ucl-top-scorers")
def top_scorers():
    recs = []
    for y in range(2015, 2026):
        for t in wikitables(season_page(y)):
            rs = list(rows(t))
            h = [c.strip() for c in rs[0][0]]
            if h[:2] == ["Rank", "Player"] and "Goals" in h:
                for tx, ln in rs[1:]:
                    if len(ln) > 1 and ln[1]:
                        recs.append({"answer": name_of(ln[1][-1]), "enwiki": ln[1][-1],
                                     "detail": f"{season(y)} top scorers"})
                break
    return dedupe(recs)


@prompt("ucl139", "Name a player who has made 100 or more Champions League appearances",
        "en:List of footballers with 100 or more UEFA Champions League appearances", family="ucl-records")
def hundred_apps():
    t = wikitables("List of footballers with 100 or more UEFA Champions League appearances")[0]
    recs = []
    for tx, ln in list(rows(t))[1:]:
        if len(tx) > 3 and ln[1] and tx[3].strip().isdigit():
            recs.append({"answer": name_of(ln[1][-1]), "enwiki": ln[1][-1], "detail": f"{tx[3]} appearances"})
    return dedupe(recs)


@prompt("ucl140", "Name a player who has won the European Cup / Champions League four or more times",
        f"en:{REC} — most wins by a player", family="ucl-records")
def four_wins():
    for t in wikitables(REC):
        rs = list(rows(t))
        h = [c.strip() for c in rs[0][0]]
        if h[:2] == ["No. of wins", "Player"]:
            recs = []
            for tx, ln in rs[1:]:
                if tx[0].strip().isdigit() and int(tx[0]) >= 4 and ln[1]:
                    recs.append({"answer": name_of(ln[1][-1]), "enwiki": ln[1][-1], "detail": f"{tx[0]} wins"})
            return dedupe(recs)
    raise LookupError("most-wins table not found")


@prompt("ucl141", "Name a player who took a penalty in a Champions League knockout-phase shoot-out, "
                  "2015–16 to 2025–26 (scored or missed)",
        "en:2015–16 to 2025–26 UEFA Champions League knockout phase pages — penalty shoot-outs "
        "(incl. the 2016 and 2026 finals)", family="ucl-shootout")
def ko_shootouts():
    recs = []
    for y in range(2015, 2026):
        for m in matches(ko_page(y)):
            for side, t in m["pens"]:
                recs.append({"answer": name_of(t), "enwiki": t,
                            "detail": f"{m['home'] if side == 0 else m['away']}, {season(y)} shoot-out"})
    return dedupe(recs)
