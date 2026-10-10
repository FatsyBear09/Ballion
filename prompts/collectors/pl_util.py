"""Shared helpers for the Premier League theme collectors (pl*.py)."""
import re
import sys
import unicodedata

from ballion.tables import rows, wikitables
from ballion.wiki import resolve

NAT_TEAM = re.compile(r"national (football|soccer) team|national under-|Football Association$|Football Federation|Football Union", re.I)
BAD_LINK = re.compile(r"\(association football\)|^(Goalkeeper|Defender|Midfielder|Forward|Striker)$|^Captain|Caretaker", re.I)

MARKS = re.compile(r"\s*(\(\s*(?:caretaker|interim|captain|c|gk|vc)\s*\)|\(\d+\)|\[\w+\]|[†‡§*#^¤♦≠]+)\s*", re.I)


def clean(name):
    """'Edwin van der Sar †' / 'Alex Ferguson (1)' -> plain display name."""
    prev = None
    while prev != name:
        prev, name = name, MARKS.sub(" ", name).strip()
    return re.sub(r"\s+", " ", name)


def disp(title):
    """Display name from an article title: drop a trailing '(footballer, born 1993)' style qualifier."""
    return re.sub(r"\s*\([^)]*\)$", "", title).strip()


def year_of(s):
    ys = re.findall(r"(?:19|20)\d\d", s or "")
    return int(ys[-1]) if ys else None


def season_start(s):
    """'2015–16' -> 2015, '1999–2000' -> 1999."""
    m = re.search(r"((?:19|20)\d\d)\s*[–-]", s or "")
    return int(m.group(1)) if m else None


def header(t):
    h = next(rows(t))[0]
    return [re.sub(r"^v t e\s*", "", c).strip() for c in h]


def tables(page, need=(), first=None):
    """Yield (headings, header, data_rows) for every wikitable of `page` whose header contains all
    of `need` (and starts with `first`).  headings = [h2, h3, h4] text before the table.
    data_rows = list of (texts, links); banner rows (all cells identical) are dropped."""
    for t in wikitables(page):
        rs = list(rows(t))
        if not rs:
            continue
        h = [re.sub(r"(?<=[A-Za-z])\s+\d$", "", re.sub(r"\s*v t e$", "", re.sub(r"^v t e\s*", "", c))).strip() for c in rs[0][0]]
        if first and (not h or h[0] != first):
            continue
        if not all(n in h for n in need):
            continue
        hs = []
        for tag in ("h2", "h3", "h4"):
            x = t.find_previous(tag)
            hs.append(x.get_text(" ", strip=True) if x else "")
        data = [(tx, ln) for tx, ln in rs[1:] if len(tx) > 1 and not (len(set(tx)) == 1 and len(tx) > 3)]
        yield hs, h, data


def _toks(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).casefold()
    return {t for t in re.findall(r"[a-z]{3,}", s)}


def person_title(links, text):
    """Best article title for a person cell: the last link that isn't a national-team/role link and
    whose name shares a word with the cell text (so a flag's country link is never picked)."""
    tt = _toks(text)
    for l in reversed(links):
        if NAT_TEAM.search(l) or BAD_LINK.search(l):
            continue
        if _toks(re.sub(r"\s*\([^)]*\)$", "", l)) & tt:
            return l
    return None


class Acc:
    """Accumulate answers keyed by enwiki title; remembers evidence; later `out()` dedupes via resolve()."""

    def __init__(self):
        self.d = {}
        self.nolink = []

    def add(self, title, name, ev=""):
        name = clean(name)
        if title and len(name.split()) == 1 and name.lower() in title.lower() and disp(title) != name:
            name = disp(title)  # surname-only cell ("Fowler") -> the article's full name
        if not title:
            self.nolink.append(name)
            title = name  # fallback: article named like the display text (checked by resolve)
        r = self.d.setdefault(title, {"answer": name, "enwiki": title, "ev": []})
        if ev and ev not in r["ev"]:
            r["ev"].append(ev)

    def addrow(self, links, text, ev=""):
        """Add the person of a table cell; a cell naming several people (e.g. joint caretakers) adds each."""
        tt = _toks(text)
        ppl = [l for l in links if not NAT_TEAM.search(l) and not BAD_LINK.search(l)
               and _toks(re.sub(r"\s*\([^)]*\)$", "", l)) & tt]
        ppl = list(dict.fromkeys(ppl))
        if len(ppl) >= 2 and not re.search(r"\(\s*\d+\s*\)$", text.strip()) and len(re.findall(r"[A-ZÀ-Ý]", text)) >= 4:
            for l in ppl:
                self.add(l, disp(l), ev)
            return
        self.add(person_title(links, text), text, ev)

    def out(self, joiner="; ", maxev=3):
        recs = []
        for r in self.d.values():
            ev = r["ev"]
            d = joiner.join(ev[:maxev]) + (f" (+{len(ev) - maxev} more)" if len(ev) > maxev else "")
            recs.append({"answer": r["answer"], "enwiki": r["enwiki"], "detail": d})
        res = dedupe(recs)
        return res


def dedupe(recs):
    """Merge records resolving to the same article; drop red links; use article title for display if
    answer is the raw fallback."""
    res = resolve([r["enwiki"] for r in recs])
    out = {}
    for r in recs:
        info = res[r["enwiki"]]
        if info["missing"]:
            print(f"  [dedupe] dropped missing {r['enwiki']!r}", file=sys.stderr)
            continue
        key = info["title"]
        if key in out:
            if r["detail"] and r["detail"] not in out[key]["detail"]:
                out[key]["detail"] += "; " + r["detail"]
        else:
            out[key] = dict(r)
            out[key]["enwiki"] = key
    return list(out.values())


# ------------------------------------------------------------ club season squads

PCOLS = ("player", "name", "player name", "players")
LEAGUE_LABELS = ("Premier League", "FA Premier League", "Premiership", "FA Premiership", "League", "League Division One")
_APPS = re.compile(r"\d+")


def _apps(cell):
    """'7+5' -> 12, '38 (2)' -> 40, '0' -> 0, '–' -> 0."""
    cell = cell.strip()
    m = re.fullmatch(r"(\d+)\s*\+\s*(\d+)", cell)
    if m:
        return int(m.group(1)) + int(m.group(2))
    m = re.fullmatch(r"(\d+)\s*\((\d+)\)", cell)
    if m:
        return int(m.group(1)) + int(m.group(2))
    m = re.fullmatch(r"\d+", cell)
    return int(cell) if m else 0


def season_squad(page, min_apps=1, with_pos=False):
    """Players with >= min_apps league (Premier League) appearances in a club season article.
    Returns [(display text, article title or None, apps)]."""
    best = None
    for t in wikitables(page):
        rs = list(rows(t))
        if len(rs) < 8:
            continue
        top = None
        for k in range(min(3, len(rs))):
            hdr = [c.strip() for c in rs[k][0]]
            lowered = [c.lower() for c in hdr]
            if any(x in lowered for x in PCOLS):
                top = k
        if top is None:
            continue
        # competition labels may be on the header row above or the same row
        pcol = next((i for i, c in enumerate(rs[top][0]) if c.strip().lower() in PCOLS), None)
        lcol = None
        for k in range(0, min(3, len(rs))):
            labs = [c.strip() for c in rs[k][0]]
            for lab in LEAGUE_LABELS:
                if lab in labs:
                    lcol = labs.index(lab)
                    break
            if lcol is not None:
                break
        if pcol is None or lcol is None:
            continue
        # must be an appearances table, not a goalscorers / discipline / awards table
        hd = " ".join((t.find_previous(tag).get_text(" ", strip=True) if t.find_previous(tag) else "") for tag in ("h2", "h3"))
        if re.search(r"goal|disciplin|clean|captain|call-up|award|transfer|loan|suspension|milestone|debut", hd, re.I)                 and not re.search(r"appearance", hd, re.I):
            continue
        if any(c.strip().lower() in ("rk.", "rk", "rank", "ranking", "pos", "position") and False for c in rs[top][0]):
            continue
        if any(c.strip().lower() in ("rk.", "rk", "rank", "ranking") for k in range(min(3, len(rs))) for c in rs[k][0]):
            continue
        # if there's a sub-header row (Apps | Goals) after the labels, the label column is the Apps column
        data_start = max(top, k) + 1
        # skip header rows that are subheaders
        while data_start < len(rs) and not (rs[data_start][0] and re.fullmatch(r"\d+|—|–|-|", rs[data_start][0][0].strip() or "")
                                              or (rs[data_start][0] and len(rs[data_start][0]) > pcol and rs[data_start][0][pcol].strip() and rs[data_start][0][pcol].strip().lower() not in ("player", "name", "apps", "goals"))):
            data_start += 1
        poscol = next((i for i, c in enumerate(rs[top][0]) if c.strip().lower() in ("pos", "pos.", "position", "position(s)")), None)
        out = []
        for tx, ln in rs[data_start:]:
            if len(tx) <= max(pcol, lcol):
                continue
            nm = tx[pcol].strip()
            if not nm or nm.lower() in ("player", "name", "total", "totals") or nm.lower().startswith("own goal"):
                continue
            a = _apps(tx[lcol])
            pos = tx[poscol].strip() if poscol is not None and poscol < len(tx) else ""
            out.append((nm, person_title(ln[pcol], nm), a, pos) if with_pos else (nm, person_title(ln[pcol], nm), a))
        if len(out) >= 8 and (best is None or len(out) > len(best)):
            best = out
    if best is None:
        raise LookupError(f"{page}: no squad statistics table found")
    return [r for r in best if r[2] >= min_apps]


def club_season(club, y):
    return f"{y}–{(y + 1) % 100:02d} {club} season"


def squad_list(page):
    """First-team squad tables (No. | Pos | Nat | Player) of an article without appearance stats."""
    out = []
    for hs, h, data in tables(page):
        if not ({"No.", "No", "N"} & set(h)) or not ({"Player", "Name"} & set(h)):
            continue
        if not re.search(r"squad|players", " ".join(hs[:2]), re.I) or re.search(r"transfer|loan|award|staff|statistic", " ".join(hs), re.I):
            continue
        pi = h.index("Player") if "Player" in h else h.index("Name")
        for tx, ln in data:
            if len(tx) > pi and tx[pi].strip():
                nm = re.sub(r"\s*\(.*", "", tx[pi])
                out.append((nm, person_title(ln[pi], nm)))
    if not out:
        raise LookupError(f"{page}: no squad list")
    return out


# ------------------------------------------------------------ cup final / match articles
from bs4 import BeautifulSoup  # noqa: E402
from ballion.tables import _link_title  # noqa: E402
from ballion.wiki import page_html  # noqa: E402


def _a_titles(node):
    return [x for x in (_link_title(a) for a in node.find_all("a")) if x]


def _lineup(tbl):
    """Inner lineup table -> (starters [(name, title)], subs [(name,title)], manager (name,title) or None)."""
    starters, subs, mgr = [], [], None
    phase, want_mgr = "start", False
    for tr in tbl.find_all("tr"):
        tds = tr.find_all("td", recursive=False)
        txt = tr.get_text(" ", strip=True)
        if txt.startswith("Substitutes"):
            phase = "subs"
            continue
        if re.match(r"(Manager|Head coach|Coach|Caretaker|Interim)", txt):
            want_mgr = True
            a = [x for x in tr.find_all("a") if _link_title(x)]
            if a:
                mgr = (a[-1].get_text(" ", strip=True), _link_title(a[-1]))
                want_mgr = False
            continue
        if want_mgr:
            a = [x for x in tr.find_all("a") if _link_title(x)]
            if a:
                mgr = (a[-1].get_text(" ", strip=True), _link_title(a[-1]))
            want_mgr = False
            continue
        if len(tds) < 3:
            continue
        cell = tds[2]
        a = [x for x in cell.find_all("a") if _link_title(x) and not x.find("img")
             and x.get_text(strip=True) not in ("c", "C", "(c)") and not _link_title(x).startswith("Captain")]
        if not a:
            continue
        a = a[-1]
        (starters if phase == "start" else subs).append((a.get_text(" ", strip=True), _link_title(a)))
    return starters, subs, mgr


def _goal_frags(cell):
    lis = cell.find_all("li")
    if lis:
        return [str(x) for x in lis]
    return [f for f in str(cell).split("<br") if "<a" in f]


def final_page(title):
    """Parse a cup-final / Community Shield article.
    Returns dict(home, away (article titles), score text, goals_home/goals_away [(name, title, text)],
                 lineups [(starters, subs, manager) x2])"""
    soup = BeautifulSoup(page_html(title), "lxml")
    fe = soup.select_one("table.fevent")
    out = {"title": title}
    home = fe.select_one(".fhome a")
    away = fe.select_one(".faway a")
    out["home"] = _link_title(home) if home else None
    out["away"] = _link_title(away) if away else None
    out["score"] = fe.select_one(".fscore").get_text(" ", strip=True)
    for side, cls in (("home", "fhgoal"), ("away", "fagoal")):
        gl = []
        for c in fe.select("td." + cls):
            for frag in _goal_frags(c):
                fs = BeautifulSoup(frag, "lxml")
                a = next((x for x in fs.find_all("a") if _link_title(x) and not x.find("img")), None)
                if a is not None:
                    gl.append((a.get_text(" ", strip=True), _link_title(a), fs.get_text(" ", strip=True)))
        out["goals_" + side] = gl
    inner = [t for t in soup.find_all("table") if t.get("cellpadding") == "0" and "font-size:90%" in (t.get("style") or "")]
    out["lineups"] = [_lineup(t) for t in inner[:2]]
    return out


def _scorers(cell):
    out = []
    if cell is None:
        return out
    for frag in _goal_frags(cell):
        fs = BeautifulSoup(frag, "lxml")
        a = next((x for x in fs.find_all("a") if _link_title(x) and not x.find("img")), None)
        if a is not None:
            out.append((a.get_text(" ", strip=True), _link_title(a), fs.get_text(" ", strip=True)))
    return out


def section_boxes(page, heading_re):
    """Football boxes under the first h2/h3 whose text matches heading_re, up to the next heading.
    -> [{home, away (article titles), score, goals_home, goals_away [(name, title, text)]}]"""
    soup = BeautifulSoup(page_html(page), "lxml")
    head = next((h for h in soup.find_all(["h2", "h3", "h4"]) if re.search(heading_re, h.get_text(" ", strip=True))), None)
    if head is None:
        raise LookupError(f"{page}: heading {heading_re!r} not found")
    start = head.parent if head.parent and "mw-heading" in (head.parent.get("class") or []) else head
    level = head.name
    boxes = []
    n = start.find_next_sibling()
    while n is not None:
        if n.name == "div" and "mw-heading" in (n.get("class") or []):
            h = n.find(["h2", "h3", "h4"])
            if h is not None and int(h.name[1]) <= int(level[1]):
                break
        for t in ([n] if n.name == "table" else n.find_all("table") if hasattr(n, "find_all") else []):
            teams = t.select("td.vcard.attendee")
            if len(teams) == 2:
                trs = t.find_all("tr")
                tds = trs[1].find_all("td") if len(trs) > 1 else []
                sc = trs[0].find_all("td")
                score = sc[2].get_text(" ", strip=True) if len(sc) > 2 else ""
                ta = [next((_link_title(a) for a in x.find_all("a") if _link_title(a)), None) for x in teams]
                boxes.append({"home": ta[0], "away": ta[1], "score": score,
                              "goals_home": _scorers(tds[1]) if len(tds) > 3 else [],
                              "goals_away": _scorers(tds[3]) if len(tds) > 3 else []})
            elif t.select_one(".fhome"):
                fe = t
                home, away = fe.select_one(".fhome a"), fe.select_one(".faway a")
                boxes.append({"home": _link_title(home) if home else None, "away": _link_title(away) if away else None,
                              "score": fe.select_one(".fscore").get_text(" ", strip=True),
                              "goals_home": _scorers(fe.select_one("td.fhgoal")),
                              "goals_away": _scorers(fe.select_one("td.fagoal"))})
        n = n.find_next_sibling()
    return boxes
