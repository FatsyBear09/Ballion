"""ucl142-ucl172, ucl174-176, ucl178-188: clubs and countries."""
import re

from ballion.registry import prompt
from prompts.collectors.ucl_clubs import (PLAYED, canon, group_teams, performance, perf_recs, season_tables,
                                          tie_winner)
from prompts.collectors.ucl_finals_parse import country_rec
from prompts.collectors.ucl_knockout import ko_matches, ko_page, season
from prompts.collectors.ucl_matches import matches
from prompts.collectors.ucl_util import dedupe, final_match

# ---------------------------------------------------------------- participants by season (ucl142-151)

KIND = {2024: "league phase", 2025: "league phase", 2026: "league phase"}


def _participants(y):
    def fn():
        return dedupe([{"answer": n, "enwiki": t, "detail": f"{season(y)} participant"} for _, n, t in group_teams(y)])
    return fn


for _pid, _y in [("ucl142", 2015), ("ucl143", 2016), ("ucl144", 2017), ("ucl145", 2019), ("ucl146", 2022),
                 ("ucl147", 2024), ("ucl148", 2025), ("ucl149", 2026), ("ucl150", 2004), ("ucl151", 2009)]:
    phase = KIND.get(_y, "group stage")
    text = f"Name a club that played in the {season(_y)} Champions League {phase}"
    if _y == 2026:
        text = "Name a club in the 2026–27 Champions League league phase (the 36 clubs drawn for it, as of October 2026)"
    prompt(_pid, text, f"en:{season(_y)} UEFA Champions League — {phase} table",
           family="ucl-season-clubs")(_participants(_y))


# ---------------------------------------------------------------- league phase positions (ucl156-158)

def _positions(lo, hi, label):
    def fn():
        recs = []
        for y in (2024, 2025):
            for pos, n, t in group_teams(y):
                if lo <= pos <= hi:
                    recs.append({"answer": n, "enwiki": t, "detail": f"{season(y)}: {pos}th"})
        return dedupe(recs)
    return fn


prompt("ucl156", "Name a club that finished in the top eight of a Champions League league phase "
                 "(2024–25 or 2025–26)",
       "en:2024–25 and 2025–26 UEFA Champions League — league phase table, positions 1–8",
       family="ucl-lp-position")(_positions(1, 8, "top8"))
prompt("ucl157", "Name a club that finished 9th–24th in a Champions League league phase (2024–25 or 2025–26)",
       "en:2024–25 and 2025–26 UEFA Champions League — league phase table, positions 9–24",
       family="ucl-lp-position")(_positions(9, 24, "9-24"))
prompt("ucl158", "Name a club that finished 25th–36th in a Champions League league phase and went out "
                 "(2024–25 or 2025–26)",
       "en:2024–25 and 2025–26 UEFA Champions League — league phase table, positions 25–36",
       family="ucl-lp-position")(_positions(25, 36, "25-36"))


@prompt("ucl159", "Name a club involved in a Champions League league-phase match decided by four or more goals "
                  "(2024–25 or 2025–26)",
        "en:2024–25 and 2025–26 UEFA Champions League league phase — match results with a margin of 4+",
        family="ucl-lp-position")
def big_margin():
    recs = []
    for y in (2024, 2025):
        for m in matches(f"{season(y)} UEFA Champions League league phase"):
            sc = re.match(r"\s*(\d+)\s*[–-]\s*(\d+)", m["score"])
            if sc and abs(int(sc.group(1)) - int(sc.group(2))) >= 4:
                for n, t in ((m["hn"], m["home"]), (m["an"], m["away"])):
                    recs.append({"answer": n, "enwiki": t, "detail": f"{season(y)}: {m['score']}"})
    return dedupe(recs)


# ---------------------------------------------------------------- how far they went

def _stage_clubs(years, stages, detail):
    def fn():
        recs = []
        for y in years:
            for m in ko_matches(y, stages):
                recs += [{"answer": m["hn"], "enwiki": m["home"], "detail": f"{season(y)} {detail}"},
                         {"answer": m["an"], "enwiki": m["away"], "detail": f"{season(y)} {detail}"}]
        return dedupe(recs)
    return fn


prompt("ucl152", "Name a club that reached the Champions League quarter-finals, 2015–16 to 2025–26",
       "en:2015–16 to 2025–26 UEFA Champions League knockout phase pages — quarter-final teams",
       family="ucl-reached-round")(_stage_clubs(range(2015, 2026), {"qf"}, "quarter-finalist"))
prompt("ucl153", "Name a club that reached the Champions League semi-finals, 2012–13 to 2025–26",
       "en:2012–13 to 2025–26 UEFA Champions League knockout phase pages — semi-final teams",
       family="ucl-reached-round")(_stage_clubs(range(2012, 2026), {"sf"}, "semi-finalist"))
prompt("ucl154", "Name a club that reached the Champions League round of 16, 2015–16 to 2025–26 "
                 "(knockout play-off losers excluded)",
       "en:2015–16 to 2025–26 UEFA Champions League knockout phase pages — round of 16 teams",
       family="ucl-reached-round")(_stage_clubs(range(2015, 2026), {"r16"}, "round of 16"))
prompt("ucl155", "Name a club that played in the Champions League knockout phase in 2024–25 or 2025–26 "
                 "(play-offs included)",
       "en:2024–25 and 2025–26 UEFA Champions League knockout phase pages — play-off and round of 16 teams",
       family="ucl-reached-round")(_stage_clubs([2024, 2025], {"po", "r16"}, "knockout phase"))


def _group_finish(pos):
    def fn():
        recs = []
        for y in range(2015, 2024):
            for p, n, t in group_teams(y):
                if p == pos:
                    recs.append({"answer": n, "enwiki": t, "detail": f"{season(y)} group"})
        return dedupe(recs)
    return fn


prompt("ucl160", "Name a club that topped its Champions League group, 2015–16 to 2023–24",
       "en:2015–16 to 2023–24 UEFA Champions League season pages — group tables, 1st place",
       family="ucl-group-finish")(_group_finish(1))
prompt("ucl161", "Name a club that finished bottom of its Champions League group, 2015–16 to 2023–24",
       "en:2015–16 to 2023–24 UEFA Champions League season pages — group tables, 4th place",
       family="ucl-group-finish")(_group_finish(4))


@prompt("ucl162", "Name a club that made its Champions League group/league-phase debut between 2015–16 and 2025–26",
        "en:UEFA Champions League clubs performance comparison — first season with a group or league-phase place",
        family="ucl-clubs-misc")
def debuts():
    def pred(s):
        played = [y for y in sorted(s) if s[y] in PLAYED]
        return (bool(played) and played[0] >= 2015, f"debut {played[0]}–{(played[0] + 1) % 100:02d}" if played else "")
    return dedupe(perf_recs(pred, ""))


@prompt("ucl163", "Name a club that won a Champions League play-off round tie to reach the group or league phase, "
                  "2021–22 to 2026–27",
        "en:2021–22 to 2026–27 UEFA Champions League pages — qualifying ties won by clubs that reached the group/league "
        "phase (play-off round)", family="ucl-clubs-misc")
def playoff_winners():
    recs = []
    for y in range(2021, 2027):
        st = season_tables(y)
        field = {canon(t) for _, _, t in group_teams(y)}
        for n1, t1, n2, t2, agg in st["before"]:
            w = tie_winner(agg)
            if w is None:
                continue
            n, t = (n1, t1) if w == 0 else (n2, t2)
            if canon(t) in field:
                recs.append({"answer": n, "enwiki": t, "detail": f"{season(y)} play-off round"})
    return dedupe(recs)


# ---------------------------------------------------------------- knockout ties (ucl164-166)

NEXT = {"po": "r16", "r16": "qf", "qf": "sf", "sf": "f"}


def ko_ties(y):
    """[(stage, (name_a, title_a, country_a), (name_b, title_b, country_b), winner 0/1)] for po..sf ties."""
    ms = matches(ko_page(y))
    teams_in = {}
    for m in ms:
        teams_in.setdefault(m["stage"], set()).update([canon(m["home"]), canon(m["away"])])
    seen, out = set(), []
    for m in ms:
        st = m["stage"]
        if st not in NEXT:
            continue
        key = (st, frozenset([canon(m["home"]), canon(m["away"])]))
        if key in seen:
            continue
        seen.add(key)
        a, b = (m["hn"], m["home"], m["hc"]), (m["an"], m["away"], m["ac"])
        in_a, in_b = canon(a[1]) in teams_in.get(NEXT[st], ()), canon(b[1]) in teams_in.get(NEXT[st], ())
        if in_a == in_b:
            continue
        out.append((st, a, b, 0 if in_a else 1))
    return out


def _faced(club_title):
    def fn():
        recs = []
        for y in range(2015, 2026):
            for m in ko_matches(y, {"po", "r16", "qf", "sf"}):
                if canon(m["home"]) == club_title:
                    recs.append({"answer": m["an"], "enwiki": m["away"], "detail": f"{season(y)} knockout"})
                elif canon(m["away"]) == club_title:
                    recs.append({"answer": m["hn"], "enwiki": m["home"], "detail": f"{season(y)} knockout"})
        return dedupe(recs)
    return fn


prompt("ucl165", "Name a club Bayern Munich have faced in a Champions League knockout tie, 2015–16 to 2025–26 "
                 "(play-offs to semi-finals; finals excluded)",
       "en:2015–16 to 2025–26 UEFA Champions League knockout phase pages — Bayern's opponents",
       family="ucl-ko-opponents")(_faced("FC Bayern Munich"))
prompt("ucl166", "Name a club Real Madrid have faced in a Champions League knockout tie, 2015–16 to 2025–26 "
                 "(play-offs to semi-finals; finals excluded)",
       "en:2015–16 to 2025–26 UEFA Champions League knockout phase pages — Real Madrid's opponents",
       family="ucl-ko-opponents")(_faced("Real Madrid CF"))


# ---------------------------------------------------------------- opponents over many seasons (ucl167-171)

def opponents(club_title, y0, y1):
    recs = []
    for y in range(y0, y1 + 1):
        if y >= 2024:
            lp = f"{season(y)} UEFA Champions League league phase"
            ms = list(matches(lp)) + list(matches(ko_page(y)))
            for m in ms:
                if canon(m["home"]) == club_title:
                    recs.append({"answer": m["an"], "enwiki": m["away"], "detail": season(y)})
                elif canon(m["away"]) == club_title:
                    recs.append({"answer": m["hn"], "enwiki": m["home"], "detail": season(y)})
            continue
        st = season_tables(y)
        for g in st["groups"]:
            if any(canon(t) == club_title for _, _, t in g):
                recs += [{"answer": n, "enwiki": t, "detail": f"{season(y)} group"} for _, n, t in g
                         if canon(t) != club_title]
        for n1, t1, n2, t2, agg in st["ties"]:
            if canon(t1) == club_title:
                recs.append({"answer": n2, "enwiki": t2, "detail": f"{season(y)} knockout"})
            elif canon(t2) == club_title:
                recs.append({"answer": n1, "enwiki": t1, "detail": f"{season(y)} knockout"})
        try:
            fm = final_match(y + 1)
            tt = [canon(x) for x in fm["teams"]]
            if club_title in tt:
                o = fm["teams"][1 - tt.index(club_title)]
                recs.append({"answer": o, "enwiki": o, "detail": f"{y + 1} final"})
        except Exception:
            pass
    return dedupe(recs)


for _pid, _name, _title, _y0, _y1, _when, _fam in [
        ("ucl167", "Manchester City", "Manchester City F.C.", 2011, 2025, "2011–12 to 2025–26", None),
        ("ucl168", "Arsenal", "Arsenal F.C.", 1998, 2025, "1998–99 to 2025–26", None),
        ("ucl169", "Liverpool", "Liverpool F.C.", 2001, 2025, "2001–02 to 2025–26", None),
        ("ucl170", "Manchester United", "Manchester United F.C.", 1993, 2012,
         "1993–94 to 2012–13, the Alex Ferguson years", None),
        ("ucl171", "Chelsea", "Chelsea F.C.", 1999, 2025, "1999–2000 to 2025–26", None)]:
    prompt(_pid, f"Name a club {_name} have faced in the Champions League ({_when}; qualifying rounds excluded)",
           f"en:UEFA Champions League season pages {_when} — group/league-phase and knockout opponents of {_name}",
           family="ucl-club-opponents")(
        (lambda t, a, b: (lambda: opponents(t, a, b)))(_title, _y0, _y1))


# ---------------------------------------------------------------- performance table prompts

@prompt("ucl172", "Name a club with ten or more Champions League group/league-phase participations (1992–93 to 2025–26)",
        "en:UEFA Champions League clubs performance comparison — number of seasons with a group or league-phase place",
        family="ucl-clubs-misc")
def ten_plus():
    return dedupe(perf_recs(lambda s: (sum(v in PLAYED for v in s.values()) >= 10,
                                       f"{sum(v in PLAYED for v in s.values())} participations"), ""))


def _reached(codes, y0, y1, label):
    def fn():
        def pred(s):
            ys = [y for y in range(y0, y1 + 1) if s.get(y) in codes]
            return (bool(ys), f"{label} in " + ", ".join(f"{y}–{(y + 1) % 100:02d}" for y in ys[:3]))
        return dedupe(perf_recs(pred, ""))
    return fn


prompt("ucl174", "Name a club that reached the Champions League semi-finals, 1992–93 to 2011–12",
       "en:UEFA Champions League clubs performance comparison — semi-final, final or title seasons 1992–93 to 2011–12",
       family="ucl-reached-round-old")(_reached({"SF", "F", "C"}, 1992, 2011, "semi-finalist"))
prompt("ucl175", "Name a club that reached the Champions League quarter-finals, 2000–01 to 2014–15",
       "en:UEFA Champions League clubs performance comparison — quarter-final or better, 2000–01 to 2014–15",
       family="ucl-reached-round-old")(_reached({"QF", "SF", "F", "C"}, 2000, 2014, "quarter-finalist"))
prompt("ucl176", "Name a club that reached the Champions League round of 16, 2003–04 to 2014–15",
       "en:UEFA Champions League clubs performance comparison — round of 16 or better, 2003–04 to 2014–15",
       family="ucl-reached-round-old")(_reached({"R16", "QF", "SF", "F", "C"}, 2003, 2014, "round of 16"))


# ---------------------------------------------------------------- clubs and countries from the performance table

def _from_countries(countries):
    def fn():
        def pred(s):
            n = sum(v in PLAYED for v in s.values())
            return (n > 0, f"{n} participation{'s' if n != 1 else ''}")
        recs = []
        for c in performance():
            if c["country"] in countries:
                ok, d = pred(c["seasons"])
                if ok:
                    recs.append({"answer": c["name"], "enwiki": c["title"], "detail": d})
        for m in matches("2026–27 UEFA Champions League league phase"):  # clubs drawn for 2026–27
            for c, n, t in ((m["hc"], m["hn"], m["home"]), (m["ac"], m["an"], m["away"])):
                if c in countries:
                    recs.append({"answer": n, "enwiki": t, "detail": "2026–27 league phase"})
        return dedupe(recs)
    return fn


COUNTRY_GROUPS = [
    ("ucl178", "a Spanish club", {"Spain"}),
    ("ucl179", "a German club", {"Germany"}),
    ("ucl180", "an Italian club", {"Italy"}),
    ("ucl181", "a French club", {"France"}),
    ("ucl182", "a Portuguese, Dutch or Belgian club", {"Portugal", "Netherlands", "Belgium"}),
    ("ucl183", "a Russian, Ukrainian, Turkish or Greek club", {"Russia", "Ukraine", "Turkey", "Greece"}),
    ("ucl184", "a club from Scandinavia, Finland, Switzerland, Austria or Scotland",
     {"Norway", "Sweden", "Denmark", "Finland", "Switzerland", "Austria", "Scotland"}),
    ("ucl185", "a club from Central or Eastern Europe, the Balkans, Cyprus, Israel or the Caucasus",
     {"Czech Republic", "Slovakia", "Hungary", "Poland", "Slovenia", "Romania", "Croatia", "Serbia", "Bulgaria",
      "Belarus", "Azerbaijan", "Kazakhstan", "Moldova", "Cyprus", "Israel"}),
]
for _pid, _who, _cs in COUNTRY_GROUPS:
    prompt(_pid, f"Name {_who} that has played in the Champions League group stage or league phase "
                 "(1992–93 to 2026–27; qualifying rounds excluded)",
           "en:UEFA Champions League clubs performance comparison (+ 2026–27 league phase) — clubs by association",
           family="ucl-clubs-by-country")(_from_countries(_cs))


@prompt("ucl186", "Name a country whose club has played in the Champions League group stage or league phase "
                  "(1992–93 to 2025–26)",
        "en:UEFA Champions League clubs performance comparison — association blocks",
        family="ucl-countries")
def club_countries():
    seen = {}
    for c in performance():
        if any(v in PLAYED for v in c["seasons"].values()):
            seen.setdefault(c["country"], c["name"])
    return dedupe([{**country_rec(k), "detail": f"e.g. {v}"} for k, v in seen.items()])


def _countries_of(match_lists):
    seen = {}
    for ms in match_lists:
        for m in ms:
            for c, n in ((m["hc"], m["hn"]), (m["ac"], m["an"])):
                if c:
                    seen.setdefault(c, n)
    return dedupe([{**country_rec(k), "detail": f"e.g. {v}"} for k, v in seen.items()])


@prompt("ucl187", "Name a country with a club in a Champions League league phase (2024–25, 2025–26 or 2026–27)",
        "en:2024–25, 2025–26, 2026–27 UEFA Champions League league phase — clubs' associations",
        family="ucl-countries")
def lp_countries():
    return _countries_of([matches(f"{season(y)} UEFA Champions League league phase") for y in (2024, 2025, 2026)])


@prompt("ucl188", "Name a country with a club that played in the Champions League knockout phase, "
                  "2015–16 to 2025–26 (play-offs included)",
        "en:2015–16 to 2025–26 UEFA Champions League knockout phase pages — clubs' associations",
        family="ucl-countries")
def ko_countries():
    return _countries_of([ko_matches(y, {"po", "r16", "qf", "sf", "f"}) for y in range(2015, 2026)])


@prompt("ucl173", "Name a club that lost all six of its Champions League group matches (1992–93 to 2023–24)",
        "en:1992–93 to 2023–24 UEFA Champions League season pages — group tables with six played and six lost",
        family="ucl-clubs-misc")
def six_losses():
    from prompts.collectors.ucl_clubs import group_rows
    recs = []
    for y in range(1992, 2024):
        for pos, n, t, pld, w, d, l in group_rows(y):
            if pld == 6 and l == 6:
                recs.append({"answer": n, "enwiki": t, "detail": f"{season(y)}"})
    return dedupe(recs)
