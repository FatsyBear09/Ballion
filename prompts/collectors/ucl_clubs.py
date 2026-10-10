"""Club-level helpers: season participants, group tables, aggregate ties, performance comparison table."""
import re
from functools import lru_cache

from ballion.tables import rows, wikitables
from ballion.wiki import resolve
from prompts.collectors.ucl_finals_parse import name_of
from prompts.collectors.ucl_knockout import season

ASSOC = re.compile(r"Football (Association|Federation|Union)|Association of Football|Football Federation|"
                   r"Federation of|Football Associations?|Away goals|Penalty shoot", re.I)


def season_page(y):
    return f"{season(y)} UEFA Champions League"


def club_link(links):
    """The club article from a cell's links (the association link is dropped)."""
    good = [t for t in links if not ASSOC.search(t)]
    return good[-1] if good else None


def short(txt):
    txt = re.sub(r"\[.*?\]|\(.*?\)|v t e", "", txt)
    return re.sub(r"\s+", " ", txt).strip()


@lru_cache(maxsize=None)
def season_tables(y):
    """{'groups': [[(pos, name, title), ...] per group table, in page order],
        'ties': [(stage_index, name1, title1, name2, title2, agg_text)] after the first group table,
        'before': [... ties before the first group table (qualifying)]}"""
    groups, ties, before, qual = [], [], [], []
    started = False
    for tb in wikitables(season_page(y)):
        rs = list(rows(tb))
        if not rs:
            continue
        h = [c.strip() for c in rs[0][0]]
        if h[:1] == ["Pos"] and any(c.startswith("Team") for c in h) and "Grp" not in h:
            ti = next(i for i, c in enumerate(h) if c.startswith("Team"))
            g = []
            for tx, ln in rs[1:]:
                t = club_link(ln[ti]) if len(ln) > ti else None
                if t and tx[0].strip()[:2].rstrip(".").isdigit():
                    g.append((int(re.match(r"\d+", tx[0]).group()), short(tx[ti]), t))
            if g:
                groups.append(g)
                started = True
        elif h[:1] == ["Team 1"] and len(h) >= 3:
            cur = []
            for tx, ln in rs[1:]:
                if len(ln) < 3 or not ln[0] or not ln[2]:
                    continue
                a, b = club_link(ln[0]), club_link(ln[2])
                if a and b:
                    tie = (short(tx[0]), a, short(tx[2]), b, tx[1])
                    (ties if started else before).append(tie)
                    cur.append(tie)
            if not started and cur:
                qual.append(cur)
    return {"groups": groups, "ties": ties, "before": before, "qual": qual}


def group_teams(y):
    return [t for g in season_tables(y)["groups"] for t in g]


@lru_cache(maxsize=None)
def canon(title):
    return resolve([title])[title]["title"]


def tie_winner(agg):
    """Winner index (0/1) of an aggregate text like '2–2 (10–11 p)', '4–3', '1–1 (a)'; None if unclear."""
    m = re.search(r"\((\d+)\s*[–-]\s*(\d+)\s*p", agg)
    if m:
        return 0 if int(m.group(1)) > int(m.group(2)) else 1
    m = re.match(r"\s*(\d+)\s*[–-]\s*(\d+)", agg)
    if m and m.group(1) != m.group(2):
        return 0 if int(m.group(1)) > int(m.group(2)) else 1
    return None


# ---------------------------------------------------------------- performance comparison

PERF = "UEFA Champions League clubs performance comparison"
PLAYED = {"GS", "LP", "KO", "R16", "QF", "SF", "F", "C", "GS2"}


@lru_cache(maxsize=None)
def performance():
    """[{'name','title','country','seasons': {2015: 'QF', ...}}] for every club row (seasons 1992..2025)."""
    t = wikitables(PERF)[1]
    rs = list(rows(t))
    hdr = rs[0][0]
    years = {i: 1900 + int(c[:2]) if int(c[:2]) >= 90 else 2000 + int(c[:2])
             for i, c in enumerate(hdr) if re.match(r"\d\d–\d\d", c)}
    out, country = [], None
    for tx, ln in rs[1:]:
        if not tx[0].strip():
            country = re.sub(r"\s*\(\d+\)", "", tx[1]).title().replace("Czech Republic", "Czech Republic")
            continue
        title = club_link(ln[1]) if ln[1] else None
        if not title:
            continue
        seasons = {years[i]: tx[i].strip() for i in years if i < len(tx) and years[i] <= 2025}
        out.append({"name": re.sub(r"\s*\(\d+\)$", "", tx[1]).strip(), "title": title, "country": country,
                    "seasons": seasons})
    return out


def perf_recs(pred, detail):
    """Records for clubs whose seasons dict satisfies pred(seasons) -> (bool, detail str)."""
    out = []
    for c in performance():
        ok, d = pred(c["seasons"])
        if ok:
            out.append({"answer": c["name"], "enwiki": c["title"], "detail": d or detail})
    return out


@lru_cache(maxsize=None)
def group_rows(y):
    """[(pos, name, title, pld, w, d, l)] for every group table on the season page (not league phase)."""
    out = []
    for tb in wikitables(season_page(y)):
        rs = list(rows(tb))
        if not rs:
            continue
        h = [c.strip() for c in rs[0][0]]
        if h[:1] != ["Pos"] or "Grp" in h or not all(c in h for c in ("Pld", "W", "D", "L")):
            continue
        ti = next(i for i, c in enumerate(h) if c.startswith("Team"))
        for tx, ln in rs[1:]:
            t = club_link(ln[ti]) if len(ln) > ti else None
            if t and re.match(r"\d", tx[0].strip()):
                try:
                    out.append((int(re.match(r"\d+", tx[0]).group()), short(tx[ti]), t, int(tx[h.index("Pld")]),
                                int(tx[h.index("W")]), int(tx[h.index("D")]), int(tx[h.index("L")])))
                except ValueError:
                    pass
    return out
