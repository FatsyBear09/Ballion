"""ll084-ll103, ll190: clubs, competitions, stadiums, cities, brands."""
import re

from ballion.registry import prompt
from ballion.wiki import resolve
from prompts.collectors.ll_util import (clean, dedupe, find, matches, season_label, soup_of, tables)

LL = "{s} La Liga"
SD = "{s} Segunda División"


def league_table(page):
    """Rows (pos, name, title) of the season's league table (first table headed Pos / Team)."""
    for tb in tables(page):
        h = tb["hdr"]
        if h[:1] == ["Pos"] and len(h) > 2 and h[1].startswith(("Team", "Club")) and "Pld" in h:
            out = []
            for tx, ln in tb["rows"]:
                if len(tx) > 1 and tx[0].strip().isdigit() and ln[1]:
                    out.append((int(tx[0]), clean(re.sub(r"\([A-Z, ]+\)", "", tx[1])), ln[1][0][0], tx[-1]))
            if out:
                return out
    raise LookupError(f"{page}: no league table")


def stadium_rows(page):
    """(team, team_title, stadium, stadium_title, city, city_title) from the 'Stadiums and locations' table."""
    for tb in tables(page):
        h = tb["hdr"]
        if h and h[0].startswith("Team") and any(c.startswith(("Stadium", "Venue")) for c in h) and "Capacity" in h:
            si = [i for i, c in enumerate(h) if c.startswith(("Stadium", "Venue"))][0]
            ci = [i for i, c in enumerate(h) if c.startswith(("Location", "Home city", "Club home city", "City"))]
            out = []
            for tx, ln in tb["rows"]:
                if len(tx) <= si or not ln[si] or not tx[-1].replace(",", "").strip()[:1].isdigit():
                    continue
                out.append({"team": tx[0], "team_t": ln[0][0][0] if ln[0] else None, "stad": clean(tx[si]),
                            "stad_t": ln[si][0][0], "city": tx[ci[0]] if ci else None,
                            "city_t": ln[ci[0]][0][0] if ci and ln[ci[0]] else None})
            if out:
                return out
    raise LookupError(f"{page}: no stadium table")


def team_set(fmt, y):
    return {t: n for _, n, t, _ in league_table(fmt.format(s=season_label(y)))}


# ---------------------------------------------------------------- clubs in La Liga

@prompt("ll084", "Name a club that has played in La Liga since 2015–16 (to 2026–27)",
        "en:2015–16 La Liga … 2026–27 La Liga — league tables")
def ll084():
    recs = []
    for y in range(2015, 2027):
        for t, n in team_set(LL, y).items():
            recs.append({"answer": n, "enwiki": t, "detail": f"in {season_label(y)}"})
    return dedupe(recs)


@prompt("ll085", "Name a club that played in La Liga between 2000–01 and 2008–09",
        "en:2000–01 La Liga … 2008–09 La Liga — league tables")
def ll085():
    recs = []
    for y in range(2000, 2009):
        for t, n in team_set(LL, y).items():
            recs.append({"answer": n, "enwiki": t, "detail": f"in {season_label(y)}"})
    return dedupe(recs)


@prompt("ll086", "Name a club that has been relegated from La Liga since 2010–11 (to 2025–26)",
        "en:2010–11 La Liga … 2026–27 La Liga — clubs in one season's table that are missing the next season")
def ll086():
    recs = []
    prev = team_set(LL, 2010)
    for y in range(2011, 2027):
        cur = team_set(LL, y)
        for t, n in prev.items():
            if t not in cur:
                recs.append({"answer": n, "enwiki": t, "detail": f"relegated {season_label(y - 1)}"})
        prev = cur
    return dedupe(recs)


@prompt("ll087", "Name a club that has been promoted to La Liga since 2015–16 (to 2026–27)",
        "en:2014–15 La Liga … 2026–27 La Liga — clubs in one season's table that were absent the season before")
def ll087():
    recs = []
    prev = team_set(LL, 2014)
    for y in range(2015, 2027):
        cur = team_set(LL, y)
        for t, n in cur.items():
            if t not in prev:
                recs.append({"answer": n, "enwiki": t, "detail": f"promoted for {season_label(y)}"})
        prev = cur
    return dedupe(recs)


@prompt("ll089", "Name a club that has played in the Segunda División since 2020–21 (to 2026–27)",
        "en:2020–21 Segunda División … 2026–27 Segunda División — league tables")
def ll089():
    recs = []
    for y in range(2020, 2027):
        for t, n in team_set(SD, y).items():
            recs.append({"answer": n, "enwiki": t, "detail": f"in {season_label(y)}"})
    return dedupe(recs)


@prompt("ll092", "Name a club that has finished in La Liga's top seven since 2010–11 (to 2025–26)",
        "en:2010–11 La Liga … 2025–26 La Liga — league tables, positions 1–7")
def ll092():
    recs = []
    for y in range(2010, 2026):
        for pos, n, t, _ in league_table(LL.format(s=season_label(y)))[:7]:
            recs.append({"answer": n, "enwiki": t, "detail": f"{pos}th, {season_label(y)}"})
    return dedupe(recs)


@prompt("ll096", "Name a club that has played in Liga F, Spain's top women's league (2022–23 to 2026–27)",
        "en:2022–23 Liga F … 2026–27 Liga F — standings", family="ll-women")
def ll096():
    recs = []
    for y in range(2022, 2027):
        for t, n in team_set("{s} Liga F", y).items():
            recs.append({"answer": n, "enwiki": t, "detail": f"in {season_label(y)}"})
    return dedupe(recs)


# ---------------------------------------------------------------- stadiums, cities, kits, sponsors

@prompt("ll098", "Name a stadium that has hosted La Liga matches since 2015–16 (to 2026–27)",
        "en:2015–16 La Liga … 2026–27 La Liga — Stadiums and locations")
def ll098():
    recs = []
    for y in range(2015, 2027):
        for r in stadium_rows(LL.format(s=season_label(y))):
            recs.append({"answer": r["stad"], "enwiki": r["stad_t"], "detail": f"{r['team']}, {season_label(y)}"})
    return dedupe(recs)


@prompt("ll190", "Name a stadium used by a Segunda División club in 2025–26",
        "en:2025–26 Segunda División — Stadiums and locations")
def ll190():
    return dedupe([{"answer": r["stad"], "enwiki": r["stad_t"], "detail": r["team"]}
                   for r in stadium_rows("2025–26 Segunda División")])


@prompt("ll101", "Name a city or town that has had a La Liga club since 2015–16 (to 2026–27)",
        "en:2015–16 La Liga … 2026–27 La Liga — Stadiums and locations (location column)")
def ll101():
    recs = []
    for y in range(2015, 2027):
        for r in stadium_rows(LL.format(s=season_label(y))):
            if r["city_t"]:
                recs.append({"answer": clean(r["city"]), "enwiki": r["city_t"], "detail": f"{r['team']}, {season_label(y)}"})
    return dedupe(recs)


def _personnel(page):
    for tb in tables(page):
        h = tb["hdr"]
        if h and h[0].startswith("Team") and any("sponsor" in c.lower() for c in h):
            return tb
    raise LookupError(f"{page}: no personnel table")


def _brand_cols(h, kind):
    if kind == "kit":
        return [i for i, c in enumerate(h) if c.lower().startswith("kit") and "sponsor" not in c.lower()][:1]
    return [i for i, c in enumerate(h) if re.search(r"main|shirt sponsor|front|kit sponsor", c.lower()) and not c.lower().startswith("kit m")][:1]


def _brands(kind):
    recs = []
    for y in range(2015, 2027):
        tb = _personnel(LL.format(s=season_label(y)))
        cols = _brand_cols(tb["hdr"], kind)
        for tx, ln in tb["rows"]:
            if len(tx) <= max(cols or [0]) or not tx[0].strip() or not cols:
                continue
            links = ln[cols[0]]
            if kind == "kit":
                links = links[:1]
            for t, a in links:
                recs.append({"answer": clean(a), "enwiki": t, "detail": f"{tx[0]}, {season_label(y)}"})
    return dedupe(recs)


@prompt("ll102", "Name a kit manufacturer that has supplied a La Liga club since 2015–16 (to 2026–27)",
        "en:2015–16 La Liga … 2026–27 La Liga — Personnel and kits (kit manufacturer column)")
def ll102():
    return _brands("kit")


# ---------------------------------------------------------------- Copa del Rey

@prompt("ll093", "Name a club that has played in a Copa del Rey final since 2000 (to 2026)",
        "en:2000 Copa del Rey final … 2026 Copa del Rey final — finalists")
def ll093():
    recs = []
    for y in range(2000, 2027):
        m = matches(f"{y} Copa del Rey final")[0]
        for side in ("home", "away"):
            n, t = m[side]
            recs.append({"answer": n, "enwiki": t, "detail": f"{y} final"})
    return dedupe(recs)


def _draw_teams(page, rnd):
    """Teams listed in the pots of a round's Draw table, as {title: (name, pot header)}."""
    soup = soup_of(page)
    out = {}
    for t in soup.select("table.wikitable"):
        h2 = t.find_previous("h2")
        if not h2 or h2.get_text(" ", strip=True).replace("[edit]", "").strip() != rnd:
            continue
        rows = t.find_all("tr")
        if len(rows) < 2:
            continue
        heads = [c.get_text(" ", strip=True) for c in rows[0].find_all(["th", "td"])]
        cells = rows[1].find_all(["td", "th"])
        for hd, c in zip(heads, cells):
            for a in c.find_all("a"):
                href = a.get("href", "")
                if href.startswith("/wiki/") and ":" not in href[6:]:
                    from urllib.parse import unquote
                    out.setdefault(unquote(href[6:]).replace("_", " "), (a.get_text(" ", strip=True), hd))
        if out:
            break
    return out


@prompt("ll094", "Name a club that has reached the Copa del Rey quarter-finals since 2019–20 (to 2025–26)",
        "en:2019–20 Copa del Rey … 2025–26 Copa del Rey — quarter-final draw (the eight clubs left)")
def ll094():
    recs = []
    for y in range(2019, 2026):
        s = season_label(y)
        for t, (n, _) in _draw_teams(f"{s} Copa del Rey", "Quarter-finals").items():
            recs.append({"answer": n, "enwiki": t, "detail": s})
    return dedupe(recs)


@prompt("ll095", "Name a club that was outside La Liga and reached the Copa del Rey round of 16 in a season from 2019–20 to 2025–26 (not a La Liga club that season)",
        "en:2019–20 Copa del Rey … 2025–26 Copa del Rey — round-of-16 draw, minus that season's La Liga clubs")
def ll095():
    recs = []
    for y in range(2019, 2026):
        s = season_label(y)
        top = set(team_set(LL, y))
        got = _draw_teams(f"{s} Copa del Rey", "Round of 16")
        res = resolve(list(got) + list(top))
        topc = {res[t]["title"] for t in top}
        for t, (n, _) in got.items():
            if res[t]["title"] not in topc:
                recs.append({"answer": n, "enwiki": t, "detail": s})
    return dedupe(recs)
