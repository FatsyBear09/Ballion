"""ucl052-ucl087: club season pages (Champions League appearances and goals)."""
import re
from functools import lru_cache

from ballion.registry import prompt
from ballion.tables import rows, wikitables
from prompts.collectors.ucl_finals_parse import name_of
from prompts.collectors.ucl_util import clean, dedupe

UCL_COL = re.compile(r"^(UEFA )?(Champions League|UCL|European Cup)$|^Europe(an)?( competitions?)?$|^UEFA$", re.I)
SUB = {"apps", "goals", "starts", "app", "gls", "", "a", "g", "tot"}


BAD_LINK = re.compile(r"^(Captain \(association football\)|Own goal|Vice-captain|Loan \(sports\)|Association football positions)", re.I)


def _pick(links):
    good = [t for t in links if not BAD_LINK.match(t)]
    return good[-1] if good else None


def _name_idx(h):
    for key in ("Player", "Name"):
        if key in h:
            return h.index(key)
    return None


@lru_cache(maxsize=None)
def season_stats(page):
    """(apps, goals): {enwiki: {'answer', 'apps'|'g'}} from the page's Champions League column(s)."""
    apps, goals = {}, {}
    got_apps = got_goals = False
    for tb in wikitables(page):
        rs = list(rows(tb))
        if len(rs) < 3:
            continue
        nr = next((i for i, r in enumerate(rs[:3]) if _name_idx(r[0]) is not None), None)
        if nr is None:
            continue
        norm = lambda c: {"app": "apps", "gls": "goals", "sts": "starts"}.get(c.strip().lower(), c.strip().lower())
        cr = next((i for i, r in enumerate(rs[:3]) if any(UCL_COL.match(re.sub(r"\s+", " ", c.strip()))
                                                          for c in r[0])), None)
        if cr is None or cr > nr:
            continue
        h = [c.strip() for c in rs[cr][0]]
        ucl = [i for i, c in enumerate(h) if UCL_COL.match(re.sub(r"\s+", " ", c))]
        ni = _name_idx(rs[nr][0])
        is_rank = "Rank" in h or "Rk." in h
        sub = None
        if is_rank:
            data = rs[nr + 1:]
        elif cr < nr:  # competition row above the column-label row
            sub = [norm(c) for c in rs[nr][0]]
            data = rs[nr + 1:]
        else:
            data = rs[nr + 1:]
            if nr + 1 < len(rs):
                cand = [norm(c) for c in rs[nr + 1][0]]
                if any(c in ("apps", "goals", "starts") for c in cand[ni + 1:]):
                    sub = cand
                    data = rs[nr + 2:]

        def val(tx, i):
            return sum(int(n) for n in re.findall(r"\d+", tx[i])) if i is not None and i < len(tx) else 0

        if is_rank:
            if got_goals:
                continue
            for tx, ln in data:
                if ni < len(ln) and ln[ni] and len(tx) > ucl[0]:
                    t = _pick(ln[ni])
                    if t:
                        goals[t] = {"answer": name_of(t), "g": val(tx, ucl[0])}
            got_goals = got_goals or bool(goals)
            continue
        if got_apps:
            # goals fallback: next table with a single Champions League column (goals ranking)
            if not got_goals and sub is None and len(ucl) == 1:
                for tx, ln in data:
                    if ni < len(ln) and ln[ni] and len(tx) > ucl[0]:
                        t = _pick(ln[ni])
                        if t:
                            goals[t] = {"answer": name_of(t), "g": val(tx, ucl[0])}
                got_goals = bool(goals)
            continue
        ai, gi = ucl[0], None
        if sub:
            if sub[ai] != "apps":
                continue
            if sub[ai + 1:ai + 2] == ["goals"]:
                gi = ai + 1
        elif len(ucl) >= 2:
            gi = ucl[1]
        for tx, ln in data:
            if len(tx) <= ai or ni >= len(ln) or not ln[ni]:
                continue
            t = _pick(ln[ni])
            if not t:
                continue
            apps[t] = {"answer": name_of(t), "apps": val(tx, ai)}
            if gi is not None and not got_goals:
                goals[t] = {"answer": name_of(t), "g": val(tx, gi)}
        got_apps = bool(apps)
        if gi is not None and goals:
            got_goals = True
    return apps, goals


def appeared(page):
    apps, _ = season_stats(page)
    return [{"answer": r["answer"], "enwiki": t, "detail": "UCL apps %d" % r["apps"]}
            for t, r in apps.items() if r["apps"] > 0]


def scored(page):
    apps, goals = season_stats(page)
    return [{"answer": r["answer"], "enwiki": t, "detail": "%d UCL goal%s" % (r["g"], "" if r["g"] == 1 else "s")}
            for t, r in goals.items() if r["g"] > 0]


def season_page(club, year):
    """club is the title suffix, e.g. 'Real Madrid CF' -> '2016–17 Real Madrid CF season'."""
    return f"{year}–{str(year + 1)[2:]} {club} season" if year != 1999 else f"1999–2000 {club} season"


# ---------------------------------------------------------------- squads (ucl052-070)

SQUADS = [
    ("ucl052", "Barcelona", "FC Barcelona", [2014]),
    ("ucl053", "Real Madrid", "Real Madrid CF", [2016]),
    ("ucl054", "Liverpool", "Liverpool F.C.", [2018]),
    ("ucl055", "Tottenham", "Tottenham Hotspur F.C.", [2018]),
    ("ucl056", "Bayern Munich", "FC Bayern Munich", [2019]),
    ("ucl057", "Chelsea", "Chelsea F.C.", [2020]),
    ("ucl058", "Real Madrid", "Real Madrid CF", [2021]),
    ("ucl059", "Manchester City", "Manchester City F.C.", [2022]),
    ("ucl060", "Inter", "Inter Milan", [2022]),
    ("ucl061", "Real Madrid", "Real Madrid CF", [2023]),
    ("ucl062", "Borussia Dortmund", "Borussia Dortmund", [2023]),
    ("ucl063", "PSG", "Paris Saint-Germain FC", [2024]),
    ("ucl064", "Barcelona", "FC Barcelona", [2024]),
    ("ucl065", "Inter", "Inter Milan", [2024]),
    ("ucl066", "Liverpool", "Liverpool F.C.", [2024]),
    ("ucl067", "Aston Villa", "Aston Villa F.C.", [2024]),
    ("ucl069", "Arsenal", "Arsenal F.C.", [2025]),
    ("ucl070", "Bayern Munich", "FC Bayern Munich", [2025]),
]


def _squad(club, years):
    def fn():
        recs = []
        for y in years:
            recs += appeared(season_page(club, y))
        return dedupe(recs)
    return fn


for _pid, _name, _club, _yrs in SQUADS:
    _y = _yrs[0]
    prompt(_pid, f"Name a player who made a Champions League appearance for {_name} in {_y}–{str(_y + 1)[2:]}",
           f"en:{season_page(_club, _y)} — squad statistics, Champions League appearances ≥ 1",
           family="ucl-squad")(_squad(_club, _yrs))


@prompt("ucl068", "Name a player who made a Champions League appearance for Newcastle United "
                  "(in 2023–24 or 2025–26)",
        "en:2023–24 and 2025–26 Newcastle United F.C. season — squad statistics, Champions League appearances ≥ 1",
        family="ucl-squad")
def newcastle():
    return _squad("Newcastle United F.C.", [2023, 2025])()


# ---------------------------------------------------------------- goalscorers by club era (ucl071-087)

def _goals(club, years):
    def fn():
        recs = []
        for y in years:
            recs += scored(season_page(club, y))
        return dedupe(recs)
    return fn


SCORERS = [
    ("ucl071", "Real Madrid", "Real Madrid CF", [2015, 2016, 2017], "in 2015–16, 2016–17 or 2017–18"),
    ("ucl072", "Real Madrid", "Real Madrid CF", [2021, 2022, 2023, 2024], "from 2021–22 to 2024–25"),
    ("ucl073", "Manchester City", "Manchester City F.C.", list(range(2016, 2023)), "from 2016–17 to 2022–23"),
    ("ucl074", "Liverpool", "Liverpool F.C.", list(range(2017, 2022)), "from 2017–18 to 2021–22"),
    ("ucl075", "Arsenal", "Arsenal F.C.", [2023, 2024, 2025], "from 2023–24 to 2025–26"),
    ("ucl076", "PSG", "Paris Saint-Germain FC", [2023, 2024, 2025], "from 2023–24 to 2025–26"),
    ("ucl077", "Barcelona", "FC Barcelona", [2023, 2024, 2025], "from 2023–24 to 2025–26"),
    ("ucl078", "Bayern Munich", "FC Bayern Munich", list(range(2019, 2026)), "from 2019–20 to 2025–26"),
    ("ucl079", "Manchester United", "Manchester United F.C.", [2017, 2018, 2021, 2023],
     "since 2017–18"),
    ("ucl080", "Chelsea", "Chelsea F.C.", [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2025], "since 2015–16"),
    ("ucl081", "Newcastle United", "Newcastle United F.C.", [2023, 2025], "in 2023–24 or 2025–26"),
    ("ucl082", "Atlético Madrid", "Atlético Madrid", list(range(2015, 2026)), "since 2015–16"),
    ("ucl083", "Juventus", "Juventus FC", list(range(2015, 2026)), "since 2015–16"),
    ("ucl084", "Real Madrid", "Real Madrid CF", list(range(2009, 2014)), "from 2009–10 to 2013–14"),
    ("ucl085", "Arsenal", "Arsenal F.C.", list(range(2003, 2010)), "from 2003–04 to 2009–10"),
    ("ucl086", "Barcelona", "FC Barcelona", list(range(2005, 2011)), "from 2005–06 to 2010–11"),
    ("ucl087", "Chelsea", "Chelsea F.C.", list(range(2003, 2012)), "from 2003–04 to 2011–12"),
]


def _safe_goals(club, years):
    def fn():
        recs = []
        for y in years:
            try:
                recs += scored(season_page(club, y))
            except Exception as e:  # season without a UCL column (e.g. not in the competition)
                print(f"  note: {season_page(club, y)}: {e!r}")
        return dedupe(recs)
    return fn


for _pid, _name, _club, _yrs, _when in SCORERS:
    prompt(_pid, f"Name a player who scored a Champions League goal for {_name} {_when}",
           f"en:{_name} season pages {_yrs[0]}–{str(_yrs[0] + 1)[2:]} to {_yrs[-1]}–{str(_yrs[-1] + 1)[2:]} — "
           "squad statistics, Champions League goals ≥ 1",
           family="ucl-club-scorers")(_safe_goals(_club, _yrs))
