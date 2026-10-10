"""Shared helpers for the La Liga (ll) collectors."""
import re

from bs4 import BeautifulSoup

from ballion.tables import _link_title, _int_attr
from ballion.wiki import page_html, resolve

NAT_TEAM = re.compile(r"national (football|soccer|under)|national team|Olympic|Spain at|at the \d{4}", re.I)


def clean(name):
    name = re.sub(r"\[[^\]]*\]", "", name)
    name = re.sub(r"\((?:c|captain|vice-captain|vc|GK|loan|loaned)\)", "", name, flags=re.I)
    name = re.sub(r"[*†‡§#^]+", "", name)
    return re.sub(r"\s+", " ", name).strip(" ,;")


def soup_of(page):
    s = BeautifulSoup(page_html(page), "lxml")
    for sup in s.select("sup.reference, span.reference, .mw-editsection, style"):
        sup.decompose()
    for f in s.select("span.flagicon, span.flagicon-ru"):
        f.decompose()
    return s


def _rows(table):
    """(texts, links) per row; links are lists of (title, anchor text). Rowspans repeated down."""
    pending = {}
    for tr in table.find_all("tr"):
        cells = tr.find_all(["td", "th"], recursive=False)
        texts, links, col = [], [], 0
        it = iter(cells)
        while True:
            if col in pending:
                p = pending[col]
                texts.append(p[1]); links.append(p[2])
                p[0] -= 1
                if p[0] == 0:
                    del pending[col]
                col += 1
                continue
            c = next(it, None)
            if c is None:
                break
            for br in c.find_all("br"):
                br.replace_with(" ; ")
            t = c.get_text(" ", strip=True)
            ls = [(x, a.get_text(" ", strip=True)) for a in c.find_all("a") if (x := _link_title(a))]
            span, rs = _int_attr(c, "colspan"), _int_attr(c, "rowspan")
            for _ in range(span):
                if rs > 1:
                    pending[col] = [rs - 1, t, ls]
                texts.append(t); links.append(ls)
                col += 1
        yield texts, links


def heading_of(t):
    h = t.find_previous(["h2", "h3", "h4"])
    return h.get_text(" ", strip=True).replace("[edit]", "").strip() if h else ""


def tables(page, soup=None):
    """List of dicts {head, hdr, rows:[(texts, links)], el} for every wikitable on the page.
    hdr = first row texts."""
    soup = soup or soup_of(page)
    out = []
    for t in soup.select("table.wikitable, table.sortable"):
        rs = list(_rows(t))
        if not rs:
            continue
        hdr = [re.sub(r"^v t e\s*", "", c).strip() for c in rs[0][0]]
        out.append({"head": heading_of(t), "hdr": hdr, "rows": rs[1:], "el": t})
    return out


def find(page, first=None, need=(), head=None, soup=None, all_=False):
    """First table whose header row starts with `first` (if given), contains all `need` strings
    (substring match against header cells) and whose section heading contains `head`."""
    res = []
    for tb in tables(page, soup):
        h = tb["hdr"]
        if first is not None and not (h and h[0] == first):
            continue
        if not all(any(n in c for c in h) for n in need):
            continue
        if head and head not in tb["head"]:
            continue
        res.append(tb)
    if all_:
        return res
    if not res:
        raise LookupError(f"{page}: no table first={first} need={need} head={head}")
    return res[0]


def col(hdr, name, nth=0):
    idx = [i for i, c in enumerate(hdr) if name in c]
    if len(idx) <= nth:
        raise LookupError(f"no column {name!r} in {hdr}")
    return idx[nth]


def dedupe(recs):
    """Merge records resolving to the same article; drop red links/missing."""
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
            out[key]["enwiki"] = key
    return list(out.values())


def season_label(y):
    return f"{y}–{str(y + 1)[2:]}"


def season_pages(fmt, y0, y1):
    """fmt like '{s} La Liga'; y0..y1 inclusive start years."""
    return [(y, fmt.format(s=season_label(y))) for y in range(y0, y1 + 1)]


def person(links, skip_nat=True):
    """Last non-national-team link of a cell, as (title, text) or None."""
    ls = [l for l in links if not NAT_TEAM.search(l[0])] if skip_nat else links
    return ls[-1] if ls else None


from datetime import datetime


def parse_date(s):
    s = re.sub(r"\[.*?\]", "", s).strip()
    for fmt in ("%d %B %Y", "%B %d, %Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    m = re.search(r"\d{1,2} \w+ \d{4}", s)
    if m:
        try:
            return datetime.strptime(m.group(), "%d %B %Y")
        except ValueError:
            pass
    return None


def season_top(page, kind="goal"):
    """Rows (name, enwiki, club, value) of a season page's top goalscorers / assists table."""
    pat = re.compile(r"assist" if kind == "assist" else r"scorer|pichichi", re.I)
    for tb in tables(page):
        h = tb["hdr"]
        if "Player" in h and pat.search(tb["head"]) and len(h) <= 6:
            pi = h.index("Player")
            ci = h.index("Club") if "Club" in h else None
            out = []
            for tx, ln in tb["rows"]:
                if len(tx) <= pi or not ln[pi]:
                    continue
                val = int(re.sub(r"\D", "", tx[-1]) or 0)
                out.append((clean(tx[pi]), ln[pi][-1][0], tx[ci] if ci is not None else "", val))
            return out
    return []


# ---------------------------------------------------------------- match pages (football boxes + line-ups)

def _link_of(el):
    for a in el.find_all("a"):
        t = _link_title(a)
        if t:
            return t, a.get_text(" ", strip=True)
    return None


def _team(cell):
    ls = [(t, x) for a in cell.find_all("a") if (t := _link_title(a)) and (x := a.get_text(" ", strip=True))]
    return (ls[0][1], ls[0][0]) if ls else (cell.get_text(" ", strip=True), None)


def _goals(cell):
    out = []
    if cell is None:
        return out
    for sp in cell.select("span.fb-goal"):
        a = sp.find_previous("a")
        lk = (_link_title(a), a.get_text(" ", strip=True)) if a is not None and _link_title(a) else None
        if not lk:
            continue
        txt = sp.get_text(" ", strip=True)
        for sib in sp.next_siblings:
            if getattr(sib, "name", None) in ("a", "br"):
                break
            txt += " " + (sib.get_text(" ", strip=True) if hasattr(sib, "get_text") else str(sib))
        og = bool(re.search(r"o\.\s?g\.?|own goal", txt, re.I)) or any(
            "own goal" in (i.get("alt", "") + i.get("title", "")).lower() for i in sp.find_all(["img", "span"]))
        out.append({"title": lk[0], "name": lk[1], "og": og, "text": txt})
    return out


def _lineup(inner):
    """Parse one team's line-up table -> dict(starters, used, unused, manager); each a list of (title, name)."""
    res = {"starters": [], "used": [], "unused": [], "manager": None}
    mode = "starters"
    for tr in inner.find_all("tr"):
        txt = tr.get_text(" ", strip=True)
        if txt.startswith("Substitutes"):
            mode = "subs"
            continue
        if txt.startswith("Manager") or txt.startswith("Head coach") or txt.startswith("Coach"):
            mode = "mgr"
            continue
        lk = _link_of(tr)
        if mode == "mgr":
            if lk and not res["manager"]:
                res["manager"] = lk
            continue
        if not lk or len(tr.find_all("td")) < 3:
            continue
        if mode == "starters":
            res["starters"].append(lk)
        else:
            on = any("on" in (i.get("alt", "") + " " + (i.parent.get("title", "") if i.parent else "")).lower().replace("down", "")
                     and "green" in i.get("alt", "").lower() for i in tr.find_all("img"))
            on = on or any("Substituted on" in (s.get("title", "")) for s in tr.find_all("span"))
            (res["used"] if on else res["unused"]).append(lk)
    return res


def matches(page):
    """All matches on a page: list of dict(home=(name,title), away=..., score, hg, ag, lineups=[home, away] or None)."""
    soup = soup_of(page)
    out = []
    for t in soup.find_all("table"):
        cls = t.get("class") or []
        if "fevent" in cls:
            h, a = t.select_one(".fhome"), t.select_one(".faway")
            if not h or not a:
                continue
            sc = t.select_one(".fscore")
            out.append({"home": _team(h), "away": _team(a), "score": sc.get_text(" ", strip=True) if sc else "",
                        "hg": _goals(t.select_one(".fhgoal")), "ag": _goals(t.select_one(".fagoal")), "lineups": None})
        elif (t.get("width") == "100%" or "width:100%" in (t.get("style") or "").replace(" ", "")) and out and out[-1]["lineups"] is None:
            inner = t.select("table[cellpadding]")
            if len(inner) >= 2:
                out[-1]["lineups"] = [_lineup(inner[0]), _lineup(inner[1])]
    return out


# ---------------------------------------------------------------- club season pages

_SKIP_LINK = re.compile(r"^(Captain|Vice-captain|Third-captain|Fourth-captain|Association football|Loan \(|Free transfer|Bosman|"
                        r"Transfer|Goalkeeper|Defender|Midfielder|Forward|Winger|Wing-back|Full-back)", re.I)


def _name_cell(tx, ln, ci):
    """(display name, title) for a player-name cell: prefer the link whose anchor starts the cell text."""
    text = clean(re.sub(r"\((?:on loan|loan|captain|vice).*?\)", "", tx[ci], flags=re.I))
    text = re.sub(r"\s*\(.*$", "", text).strip()
    text = re.sub(r"\s+\d+$", "", text)
    links = [l for l in ln[ci] if not _SKIP_LINK.match(l[0]) and not NAT_TEAM.search(l[0])]
    for t, a in links:
        if a and text and (text.startswith(a) or a.startswith(text) or a in text):
            return text, t
    return (text, links[0][0]) if links and "(" not in tx[ci] else (text, None)


SQUAD_HEADS = re.compile(r"^(Players?|First[- ]team( squad)?|Squad( list)?|Current squad|Team squad|Senior squad)$", re.I)


def squad(page, extra_heads=()):
    """Players of a club-season page's first-team squad tables -> list of (name, title, pos)."""
    out = []
    for tb in tables(page):
        h = tb["hdr"]
        hn = [re.sub(r"[\s;]+$", "", c) for c in h]
        if not SQUAD_HEADS.match(tb["head"]) and tb["head"] not in extra_heads:
            continue
        pos = [i for i, c in enumerate(hn) if c.startswith("Pos") or c in ("P", "Position")]
        nm_ = [i for i, c in enumerate(hn) if c in ("Player", "Name") or c.startswith("Name") or c.startswith("Player")]
        if not pos or not nm_:
            continue
        ci = nm_[0]
        for tx, ln in tb["rows"]:
            if len(tx) <= ci or tx[pos[0]] not in ("GK", "DF", "MF", "FW", "D", "M", "F", "G", "CB", "LB", "RB", "DM", "CM", "AM", "LW", "RW", "CF", "ST", "WG"):
                continue
            name, title = _name_cell(tx, ln, ci)
            if title:
                out.append((name, title, tx[pos[0]]))
    return out


_GOAL_HEAD = re.compile(r"goal ?scorers|^goals$|top scorers|goals scored", re.I)
_STAT_HEAD = re.compile(r"squad statistics|appearances and goals|squad, appearances and goals|player statistics|^overall$", re.I)


def club_scorers(page):
    """Scorers (any competition) on a club-season page -> list of (name, title, goals).
    Union of the goalscorers table and the squad-statistics table."""
    tbs = tables(page)
    found = {}
    for tb in tbs:
        if not _GOAL_HEAD.search(tb["head"]):
            continue
        h = [re.sub(r"[\s;]+$", "", c) for c in tb["hdr"]]
        pc = [i for i, c in enumerate(h) if c in ("Player", "Players", "Name")]
        if not pc or len(tb["rows"]) < 3:
            continue
        pi = pc[0]
        vi = h.index("Total") if "Total" in h else len(h) - 1
        for tx, ln in tb["rows"]:
            if len(tx) <= max(pi, vi):
                continue
            g = re.sub(r"\D", "", tx[vi])
            if not g or int(g) == 0:
                continue
            name, title = _name_cell(tx, ln, pi)
            if title and not title.startswith("Own goal"):
                found.setdefault(title, (name, title, int(g)))
    for tb in tbs:
        if not _STAT_HEAD.search(tb["head"]) or "Player" not in tb["hdr"]:
            continue
        sub = tb["rows"][0][0]
        if "Goals" not in sub:
            continue
        pi, gi = tb["hdr"].index("Player"), sub.index("Goals")
        for tx, ln in tb["rows"][1:]:
            if len(tx) <= gi or not tx[gi].strip().isdigit() or int(tx[gi]) == 0:
                continue
            name, title = _name_cell(tx, ln, pi)
            if title and not title.startswith("Own goal"):
                found.setdefault(title, (name, title, int(tx[gi])))
    if not found:
        raise LookupError(f"{page}: no scorers table")
    return list(found.values())
