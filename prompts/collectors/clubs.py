"""p064-p083: clubs, competitions, stadiums."""
import re

from bs4 import BeautifulSoup

from ballion.registry import prompt
from ballion.tables import rows, wikitables
from ballion.wiki import page_html, resolve

# ---------------------------------------------------------------- helpers


def clean(name):
    """Strip footnote marks / asterisks / daggers from a club display name."""
    name = re.sub(r"[*†‡§#]+", "", name)
    name = re.sub(r"\s*\((?:LIB|CWC)\s*\)?", "", name)
    return re.sub(r"\s+", " ", name).strip()


def header(t):
    h = next(rows(t))[0]
    return [re.sub(r"^v t e\s*", "", c).strip() for c in h]


def find_table(page, first, need=(), tables=None):
    """First wikitable whose header starts with `first` and contains every column in `need`."""
    for t in tables if tables is not None else wikitables(page):
        h = header(t)
        if h and h[0] == first and all(n in h for n in need):
            return t, h
    raise LookupError(f"{page}: no table with header {first!r} + {need}")


def dedupe(recs):
    """Merge records whose enwiki titles resolve to the same canonical article.
    Keeps the first record's answer; joins distinct details; drops red links."""
    res = resolve([r["enwiki"] for r in recs])
    out = {}
    for r in recs:
        info = res[r["enwiki"]]
        if info["missing"]:
            continue
        key = info["title"]
        if key in out:
            if r["detail"] and r["detail"] not in out[key]["detail"]:
                out[key]["detail"] += "; " + r["detail"]
        else:
            out[key] = dict(r)
    return list(out.values())


def years(s):
    return re.findall(r"\d{4}(?:[–-]\d{2,4})?", s)


def titles_detail(n, yrs, word="Winners"):
    if not yrs:
        return f"{word} ×{n}"
    if len(yrs) <= 3:
        return f"{word} " + ", ".join(yrs)
    return f"{word} ×{n} ({yrs[0]} to {yrs[-1]})"


def num(s):
    m = re.match(r"\d+", s.strip())
    return int(m.group()) if m else 0


def per_club(page, first="Club", win_col=None, ru_col=None, wy_col=None, ry_col=None,
             finalists=False, word="Winners"):
    """Generic per-club summary table parser (club in column 0, last link = club article)."""
    t, h = find_table(page, first, [c for c in (win_col, ru_col) if c])
    wi, ri = h.index(win_col), h.index(ru_col) if ru_col else None
    wyi = h.index(wy_col) if wy_col else None
    ryi = h.index(ry_col) if ry_col else None
    out = []
    for tx, ln in list(rows(t))[1:]:
        if len(tx) <= wi or not ln[0] or not tx[wi].strip()[:1].isdigit():
            continue
        w = num(tx[wi])
        r = num(tx[ri]) if ri is not None else 0
        if w == 0 and not (finalists and r > 0):
            continue
        parts = []
        if w:
            parts.append(titles_detail(w, years(tx[wyi]) if wyi is not None else [], word))
        if finalists and r:
            ry = years(tx[ryi]) if ryi is not None else []
            parts.append(titles_detail(r, ry, "Runners-up"))
        out.append({"answer": clean(tx[0]), "enwiki": ln[0][-1], "detail": "; ".join(parts)})
    return out


def season_clubs(page):
    """Participants of a season article: first table with header Club/Team + Location/City/Venue."""
    for t in wikitables(page):
        h = header(t)
        if h and h[0] in ("Club", "Team") and len(h) > 1 and re.search(r"Location|City|Town|Venue|Stadium", h[1]):
            return [(clean(tx[0]), ln[0][-1]) for tx, ln in list(rows(t))[1:] if ln and ln[0]]
    return []


def league_members(recs, season_pages):
    """Union list-article records with current-season participants (in case the list lags)."""
    extra = []
    for sp in season_pages:
        for name, title in season_clubs(sp):
            extra.append({"answer": name, "enwiki": title, "detail": f"in {sp.split(' ')[0]} season"})
    res = resolve([r["enwiki"] for r in recs + extra])
    known = {res[r["enwiki"]]["title"] for r in recs}
    return dedupe(recs + [r for r in extra if res[r["enwiki"]]["title"] not in known])


# ---------------------------------------------------------------- leagues

PL_LIST = "List of Premier League clubs"


def _pl_rows():
    t, h = find_table(PL_LIST, "Club", ["Total seasons", "Most recent relegation"])
    return h, [(tx, ln) for tx, ln in list(rows(t))[1:] if ln[0] and tx[2].isdigit()]


@prompt("p064", "Name a club that has played in the Premier League (1992–93 to 2026–27)",
        "en:List of Premier League clubs — all-time clubs table")
def pl_clubs():
    h, rr = _pl_rows()
    si = h.index("Total seasons")
    return dedupe([{"answer": tx[0], "enwiki": ln[0][-1], "detail": f"{tx[si]} PL season{'' if tx[si] == '1' else 's'}"} for tx, ln in rr])


@prompt("p065", "Name a club that has been relegated from the Premier League (as of the end of 2025–26)",
        "en:List of Premier League clubs — clubs with a 'most recent relegation' entry")
def pl_relegated():
    h, rr = _pl_rows()
    ri, si = h.index("Most recent relegation"), h.index("Total spells")
    out = []
    for tx, ln in rr:
        if not re.search(r"\d{4}", tx[ri]):
            continue
        out.append({"answer": tx[0], "enwiki": ln[0][-1],
                    "detail": f"last relegated {tx[ri]}; {tx[si]} PL spell(s)"})
    return dedupe(out)


def _seasons_list(page, ci, si, first_i=None):
    t = wikitables(page)[0]
    out = []
    for tx, ln in list(rows(t))[1:]:
        if len(tx) <= max(ci, si) or not ln[ci] or not tx[si].strip().isdigit():
            continue
        d = f"{tx[si]} season" + ("" if tx[si].strip() == "1" else "s")
        if first_i is not None:
            d += f", debut {tx[first_i]}"
        out.append({"answer": clean(tx[ci]), "enwiki": ln[ci][-1], "detail": d})
    return out


@prompt("p066", "Name a club that has played in the Bundesliga (1963–64 to 2026–27)",
        "en:List of clubs in the Bundesliga — all-time table (+ 2026–27 participants)")
def bundesliga_clubs():
    recs = _seasons_list("List of clubs in the Bundesliga", 0, 1, 3)
    return league_members(recs, ["2026–27 Bundesliga"])


@prompt("p067", "Name a club that has played in La Liga (1929 to 2026–27)",
        "en:List of La Liga clubs — all-time table (+ 2026–27 participants)")
def laliga_clubs():
    t = wikitables("List of La Liga clubs")[0]
    h = header(t)
    ci, si, di = h.index("Club"), h.index("S"), h.index("Debut")
    recs = []
    for tx, ln in list(rows(t))[1:]:
        if not tx[0].isdigit() or not ln[ci]:
            continue
        recs.append({"answer": clean(tx[ci]), "enwiki": ln[ci][-1], "detail": f"{tx[si]} season{'' if tx[si] == '1' else 's'}, debut {tx[di]}"})
    return league_members(recs, ["2026–27 La Liga"])


@prompt("p068", "Name a club that has played in Serie A (single-table era, 1929–30 to 2026–27)",
        "en:List of Serie A clubs — all-time table (+ 2026–27 participants)")
def seriea_clubs():
    recs = _seasons_list("List of Serie A clubs", 0, 1, 3)
    return league_members(recs, ["2026–27 Serie A"])


@prompt("p069", "Name a club that has played in the French top flight (Division 1 / Ligue 1, 1932–33 to 2026–27)",
        "en:List of Ligue 1 clubs (+ 2025–26 and 2026–27 participants)")
def ligue1_clubs():
    soup = BeautifulSoup(page_html("List of Ligue 1 clubs"), "lxml")
    for sup in soup.select("sup.reference"):
        sup.decompose()
    t = soup.find("table", class_="sortable")
    h = header(t)
    ci, si, fi = h.index("Club"), h.index("Seasons in D1/L1"), h.index("First season in D1/L1")
    recs = []
    for tx, ln in list(rows(t))[1:]:
        if not ln[ci] or not tx[si].isdigit():
            continue
        # region link comes first, club link last
        recs.append({"answer": clean(tx[ci]), "enwiki": ln[ci][-1], "detail": f"debut {tx[fi]}; {tx[si]} season{'' if tx[si] == '1' else 's'} (count as of 2024–25)"})
    return league_members(recs, ["2025–26 Ligue 1", "2026–27 Ligue 1"])


@prompt("p070", "Name a club that has played in Major League Soccer (1996 to 2026, incl. defunct clubs)",
        "en:Major League Soccer — current clubs + former clubs tables")
def mls_clubs():
    ts = wikitables("Major League Soccer")
    cur, h = find_table(None, "Conference", ["Club", "Joined"], ts)
    ci, ji = h.index("Club"), h.index("Joined")
    recs = [{"answer": tx[ci], "enwiki": ln[ci][-1], "detail": f"joined {tx[ji]}"}
            for tx, ln in list(rows(cur))[1:] if ln[ci]]
    old, h = find_table(None, "Club", ["Joined", "Final season"], ts)
    for tx, ln in list(rows(old))[1:]:
        if ln[0]:
            recs.append({"answer": tx[0], "enwiki": ln[0][-1], "detail": f"defunct, {tx[4]}–{tx[5]}"})
    return dedupe(recs)


# ---------------------------------------------------------------- European competitions

@prompt("p071", "Name a club that has reached a European Cup / UEFA Champions League final (winners or runners-up, to 2026)",
        "en:List of European Cup and UEFA Champions League finals — performances by club")
def ucl_finalists():
    return dedupe(per_club("List of European Cup and UEFA Champions League finals", "Club", "Title(s)", "Runners-up",
                           "Seasons won", "Seasons runner-up", finalists=True))


@prompt("p072", "Name a club that has won the UEFA Cup / UEFA Europa League (to 2026)",
        "en:List of UEFA Cup and Europa League finals — performances by club")
def uel_winners():
    return dedupe(per_club("List of UEFA Cup and Europa League finals", "Club", "Winners", "Runners-up", "Years won"))


@prompt("p073", "Name a club that has won the European Cup Winners' Cup (1960–61 to 1998–99)",
        "en:List of UEFA Cup Winners' Cup finals — performances by club")
def cwc_winners():
    return dedupe(per_club("List of UEFA Cup Winners' Cup finals", "Club", "Titles", "Runners-up", "Years won"))


# ---------------------------------------------------------------- domestic cups

def _first_last(page, finalists=False):
    t, h = find_table(page, "Club", ["Wins", "First final won", "Last final won", "Runners-up"])
    wi, fi, li, ri = (h.index(c) for c in ("Wins", "First final won", "Last final won", "Runners-up"))
    out = []
    for tx, ln in list(rows(t))[1:]:
        if not tx[wi].isdigit():
            continue
        w, r = int(tx[wi]), num(tx[ri])
        if w == 0 and not (finalists and r):
            continue
        if w == 0:
            d = f"Runners-up ×{r}"
        elif w == 1:
            d = f"Winners {tx[fi]}"
        else:
            d = f"Winners ×{w} ({tx[fi]}–{tx[li]})"
        if finalists and w and r:
            d += f"; runners-up ×{r}"
        out.append({"answer": clean(tx[0]), "enwiki": ln[0][-1] if ln[0] else clean(tx[0]), "detail": d})
    return out


@prompt("p074", "Name a club that has won the FA Cup (to the 2026 final)",
        "en:List of FA Cup finals — results by team")
def fa_cup_winners():
    return dedupe(_first_last("List of FA Cup finals"))


@prompt("p075", "Name a club that has won the English Football League Cup (to the 2026 final)",
        "en:List of EFL Cup finals — results by team")
def league_cup_winners():
    return dedupe(per_club("List of EFL Cup finals", "Club", "Winners", "Runners-up", "Years won"))


@prompt("p076", "Name a club that has reached the Copa del Rey final (winners or runners-up, to 2026)",
        "en:List of Copa del Rey finals — results by team")
def copa_del_rey_finalists():
    # winners-only is just 16 clubs (one of them, Racing de Irún, has no article) -> finalists
    return dedupe(_first_last("List of Copa del Rey finals", finalists=True))


# ---------------------------------------------------------------- other confederations

@prompt("p077", "Name a club that has won the Copa Libertadores (to 2025)",
        "en:List of Copa Libertadores finals — performances by club")
def libertadores_winners():
    return dedupe(per_club("List of Copa Libertadores finals", "Club", "Titles", "Runners-up", "Seasons won"))


@prompt("p078", "Name a club that has reached the Copa Sudamericana final (winners or runners-up, 2002–2025)",
        "en:List of Copa Sudamericana finals — performances by club")
def sudamericana_finalists():
    return dedupe(per_club("List of Copa Sudamericana finals", "Team", "Won", "Lost", "Years won", "Years lost",
                           finalists=True))


@prompt("p079", "Name a club that has won the Asian Club Championship / AFC Champions League (Elite) (to 2025–26)",
        "en:List of Asian Club Championship and AFC Champions League Elite finals — performances by club")
def acl_winners():
    return dedupe(per_club("List of Asian Club Championship and AFC Champions League Elite finals", "Club",
                           "Title(s)", "Runners-up", "Seasons won"))


@prompt("p080", "Name a club that has won the African Cup of Champions Clubs / CAF Champions League (to 2026)",
        "en:List of African Cup of Champions Clubs and CAF Champions League finals — performances by club")
def caf_cl_winners():
    return dedupe(per_club("List of African Cup of Champions Clubs and CAF Champions League finals", "Club",
                           "Titles", "Runners-up", "Seasons won"))


@prompt("p081", "Name a club that has won the Intercontinental Cup (1960–2004), the FIFA Club World Cup "
                "or the FIFA Intercontinental Cup (2024–)",
        "en:List of Intercontinental Cup matches + List of FIFA Club World Cup finals (by club) + FIFA Intercontinental Cup")
def world_club_winners():
    recs = [{**r, "detail": "Intercontinental Cup: " + r["detail"]}
            for r in per_club("List of Intercontinental Cup matches", "Team", "Winners", "Runners-up", "Years won")]
    recs += [{**r, "detail": "Club World Cup: " + r["detail"]}
             for r in per_club("List of FIFA Club World Cup finals", "Club", "Titles", "Runners-up", "Years won")]
    t, h = find_table("FIFA Intercontinental Cup", "Year", ["Winners"])
    for tx, ln in list(rows(t))[2:]:
        if tx[0].isdigit() and ln[2]:
            recs.append({"answer": tx[2], "enwiki": ln[2][-1], "detail": f"FIFA Intercontinental Cup: Winners {tx[0]}"})
    return dedupe(recs)


@prompt("p082", "Name a club that has been Dutch national football champions (since 1888–89, incl. pre-Eredivisie era)",
        "en:List of Dutch football champions — titles by club")
def dutch_champions():
    return dedupe(per_club("List of Dutch football champions", "Club", "Winner", "Runner-up", "Winning years",
                           word="Champions"))


# ---------------------------------------------------------------- stadiums

@prompt("p083", "Name a stadium that has been the home ground of a Premier League club during a Premier League "
                "season (1992–93 to 2026–27, incl. former and temporary grounds)",
        "en:List of Premier League stadiums")
def pl_stadiums():
    t, h = find_table("List of Premier League stadiums", "Stadium", ["Club", "Opened", "Closed"])
    si, ci, ci_closed = h.index("Stadium"), h.index("Club"), h.index("Closed")
    out = []
    for tx, ln in list(rows(t))[1:]:
        if not ln[si]:
            continue
        name = tx[si]
        m = re.match(r"(.*?)\s*\(also known as (.*?)\)", name)
        if m:
            name = f"{m.group(1)} ({m.group(2)})"
        name = re.split(r"\s+Formerly\s+", name)[0].strip()
        clubs = " & ".join(re.sub(r"^A\.?F\.?C\.? |\s+A?\.?F\.C\.$", "", c) for c in ln[ci])
        if ln[si][-1] == "Wembley Stadium" and not clubs:
            clubs = "Tottenham Hotspur (temporary, 2017–18 and 2018–19)"
        d = clubs + (f"; closed {tx[ci_closed]}" if tx[ci_closed].strip() else "")
        out.append({"answer": name, "enwiki": ln[si][-1], "detail": d})
    return dedupe(out)
