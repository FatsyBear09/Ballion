"""gen168-gen180 (excluding club pairs): cross-league titles and records, ownership, stadiums, video games, Kings League."""
import re

from bs4 import BeautifulSoup

from ballion.registry import prompt
from ballion.tables import _link_title
from ballion.wiki import page_html, resolve
from prompts.collectors.gen_util import (Acc, NAT_TEAM, dedupe, find_tab, find_tabs, first_person, league_table_clubs,
                                         people, season_label, tabs, wd_filter)

FOOTBALLER = "Q937857"


# ---------------------------------------------------------------- big-five champions
LEAGUES = ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]


def _champions():
    out = []
    for y in range(2014, 2026):
        s = season_label(y)
        for lg in LEAGUES:
            page = f"{s} {lg}"
            club = league_table_clubs(page)[0]
            out.append((s, lg, page, club))
    return out


@prompt("gen171", "Name a club that has won the league title in England, Spain, Germany, Italy or France between 2014–15 and 2025–26",
        "en:2014–15 … 2025–26 Premier League, La Liga, Bundesliga, Serie A, Ligue 1 — first row of each final league table")
def big5_champions():
    acc = Acc("club")
    for s, lg, page, (t, a) in _champions():
        acc.add(t, a, f"{lg} {s}")
    return acc.out()


# gen172 dropped: season pages don't reliably name the champion's manager (2014–15 Chelsea has none).
def big5_champion_managers():
    acc = Acc()
    for s, lg, page, (t, a) in _champions():
        pt = next(tb for tb in tabs(page) if any(re.fullmatch(r"Manager|Head coach", h) for h in tb.hdr)
                  and any(re.fullmatch(r"Captain|Kit.*|Kit maker", h) for h in tb.hdr))
        mi = next(i for i, h in enumerate(pt.hdr) if re.fullmatch(r"Manager|Head coach", h))
        rows = [(ln[0], ln[mi]) for tx, ln in pt.rows[1:] if len(ln) > mi and ln[0]]
        res = resolve([t] + [c[0][0] for c, m in rows])
        target = res[t]["title"]
        found = [m for c, m in rows if res[c[0][0]]["title"] == target]
        if not found or not found[0]:
            raise LookupError(f"{page}: no manager found for {t}")
        mt, ma = found[0][0]
        acc.add(mt, ma, f"{lg} {s}")
    return acc.out()


# ---------------------------------------------------------------- records
def _int(s):
    return int(re.sub(r"[^\d]", "", s) or 0)


@prompt("gen173", "Name a footballer who has scored 500 or more career goals",
        "en:List of footballers with 500 or more goals — main table")
def goals_500():
    tb = find_tab("List of footballers with 500 or more goals", ["Rank", "Player", "Total"], heading="Footballers with 500")
    ci, ti = tb.col("Player"), tb.col("Total")
    acc = Acc()
    for tx, ln in tb.body:
        if tx[0].strip().isdigit() and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], f"{tx[ti]} goals")
    return acc.out()


@prompt("gen174", "Name a men's footballer who has made 1,000 or more official appearances",
        "en:List of men's footballers with 1,000 or more official appearances — ranking table, total ≥ 1,000")
def apps_1000():
    tb = find_tab("List of men's footballers with 1,000 or more official appearances", ["Rank", "Player", "Total"], heading="Ranking")
    ci, ti = tb.col("Player"), tb.col("Total")
    acc = Acc()
    for tx, ln in tb.body:
        if tx[0].strip().isdigit() and _int(tx[ti]) >= 1000 and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], f"{tx[ti]} apps")
    return acc.out()


@prompt("gen175", "Name a club that the City Football Group owns or has owned",
        "en:City Football Group — 'CFG-owned clubs' and 'Former clubs' tables (partner clubs excluded)")
def cfg_clubs():
    acc = Acc("club")
    for heading in ("CFG-owned clubs", "Former clubs"):
        tb = find_tab("City Football Group", ["Club", "City", "Country"], heading=heading)
        ci = tb.col("Club")
        for tx, ln in tb.body:
            if ln[ci]:
                acc.add(ln[ci][0][0], ln[ci][0][1], heading.split()[0])
    return acc.out()


@prompt("gen176", "Name a football stadium with a capacity of 60,000 or more",
        "en:List of association football stadiums by capacity — seating capacity ≥ 60,000")
def stadiums_60k():
    tb = find_tab("List of association football stadiums by capacity", ["Rank", "Stadium", "Seating capacity"], heading="Football stadiums by capacity")
    si, ci = tb.col("Stadium"), tb.col("Seating capacity")
    acc = Acc("club")
    for tx, ln in tb.body:
        if tx[0].strip().isdigit() and _int(tx[ci]) >= 60000 and ln[si]:
            acc.add(ln[si][0][0], ln[si][0][1], tx[ci])
    return acc.out()


# ---------------------------------------------------------------- video games
def _cover_lines(page):
    soup = BeautifulSoup(page_html(page), "lxml")
    out = []
    for el in soup.find_all(["p", "div", "li", "dd"]):
        t = el.get_text(" ", strip=True)
        if re.match(r"Cover athletes?\b", t) and not el.find(["p", "div"]):
            h = el.find_previous(["h2", "h3", "h4"])
            links = [(x, a.get_text(" ", strip=True)) for a in el.find_all("a") if (x := _link_title(a))]
            out.append((h.get_text(" ", strip=True).replace("[edit]", "").strip() if h else "", links))
    return out


def _cover_section(page):
    soup = BeautifulSoup(page_html(page), "lxml")
    for h in soup.find_all(["h2", "h3"]):
        if h.get_text(" ", strip=True).replace("[edit]", "").strip().lower() in ("cover art", "cover athletes", "cover"):
            box = h.parent if h.parent.name == "div" else h
            sib = box.find_next_sibling()
            links = []
            while sib is not None and not (sib.name == "div" and "mw-heading" in (sib.get("class") or [])) \
                    and sib.name not in ("h2", "h3"):
                links += [(x, a.get_text(" ", strip=True)) for a in sib.find_all("a") if (x := _link_title(a))]
                sib = sib.find_next_sibling()
            return links
    return []


def _humans(acc_pairs, occupation=FOOTBALLER):
    keep = wd_filter([t for t, a, ev in acc_pairs], occupation)
    acc = Acc()
    for t, a, ev in acc_pairs:
        if t in keep:
            acc.add(t, a, ev)
    return acc.out()


@prompt("gen177", "Name a footballer who has been a FIFA or EA Sports FC cover athlete (FIFA 15 to EA Sports FC 26)",
        "en:FIFA (video game series) — 'Cover athlete' lines FIFA 15–FIFA 23; en:EA Sports FC 24/25/26 — cover art sections",
        family="gen-cover-athletes")
def fifa_covers_modern():
    pairs = []
    want = {f"FIFA {n}" for n in range(15, 24)}
    for h, links in _cover_lines("FIFA (video game series)"):
        if h in want:
            pairs += [(t, a, h) for t, a in links]
    for n in (24, 25, 26):
        pairs += [(t, a, f"FC {n}") for t, a in _cover_section(f"EA Sports FC {n}")]
    return _humans(pairs)


@prompt("gen178", "Name a footballer who was a FIFA cover athlete from FIFA 2001 to FIFA 09",
        "en:FIFA (video game series) — 'Cover athlete' lines FIFA 2001 to FIFA 09, regional covers included",
        family="gen-cover-athletes")
def fifa_covers_classic():
    want = {"FIFA 2001", "FIFA Football 2002", "FIFA Football 2003", "FIFA Football 2004", "FIFA Football 2005",
            "FIFA 06", "FIFA 07", "FIFA 08", "FIFA 09"}
    pairs = []
    for h, links in _cover_lines("FIFA (video game series)"):
        if h in want:
            pairs += [(t, a, h) for t, a in links]
    return _humans(pairs)


@prompt("gen179", "Name a person who has been a Pro Evolution Soccer / eFootball PES cover star",
        "en:Pro Evolution Soccer — 'Cover athlete' lines (players and referee Pierluigi Collina; teams excluded)",
        family="gen-cover-athletes")
def pes_covers():
    pairs = []
    for h, links in _cover_lines("Pro Evolution Soccer"):
        pairs += [(t, a, h) for t, a in links]
    keep = wd_filter([t for t, a, h in pairs])  # humans only (teams drop out)
    acc = Acc()
    for t, a, h in pairs:
        if t in keep:
            acc.add(t, a, h)
    return acc.out()


@prompt("gen180", "Name a footballer (current or former) who is or was a Kings League team chairperson",
        "en:Kings League — team tables (chairperson column), footballers only per Wikidata occupation")
def kings_league_chairs():
    pairs = []
    for tb in tabs("Kings League"):
        ci = next((i for i, h in enumerate(tb.hdr) if h.startswith("Chairperson")), None)
        if ci is None:
            continue
        for tx, ln in tb.body:
            pairs += [(t, a, tb.heading) for t, a in ln[ci]]
    return _humans(pairs)
