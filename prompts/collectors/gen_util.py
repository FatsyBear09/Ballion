"""Shared helpers for the General-theme (gen) collectors."""
import re
from urllib.parse import unquote

from bs4 import BeautifulSoup

from ballion.tables import _link_title
from ballion.wiki import page_html, resolve

NAT_TEAM = re.compile(r"national (football|soccer|under)|national.*team|Football Association|Football Federation|"
                      r"Soccer Federation|Football Union|Olympic", re.I)


# ---------------------------------------------------------------- tables
def _int(v):
    return int(re.sub(r"\D", "", str(v)) or 1)


def _outer_links(c):
    """Links in a cell that are not inside parentheses (player links, not their '(club)' links)."""
    from bs4 import NavigableString
    depth, out = 0, []
    for n in c.descendants:
        if isinstance(n, NavigableString):
            depth = max(0, depth + n.count("(") - n.count(")"))
        elif n.name == "a" and depth == 0 and (x := _link_title(n)):
            out.append((x, n.get_text(" ", strip=True)))
    return out


def _rows(table, outer=False):
    """Rows of (texts, links); links per cell are [(title, anchor text)]. Flag icons dropped, rowspan/colspan expanded."""
    pending = {}
    for tr in table.find_all("tr"):
        cells = tr.find_all(["td", "th"], recursive=False)
        texts, links, flags, col = [], [], [], 0
        it = iter(cells)
        while True:
            if col in pending:
                p = pending[col]
                texts.append(p[1]); links.append(p[2]); flags.append(p[3])
                p[0] -= 1
                if p[0] == 0:
                    del pending[col]
                col += 1
                continue
            c = next(it, None)
            if c is None:
                break
            fl = []
            for f in c.select("span.flagicon"):
                fl += [x for a in f.find_all("a") if (x := _link_title(a))]
                f.decompose()
            t = c.get_text(" ", strip=True)
            ls = _outer_links(c) if outer else [(x, a.get_text(" ", strip=True)) for a in c.find_all("a") if (x := _link_title(a))]
            span, rs = _int(c.get("colspan", 1)), _int(c.get("rowspan", 1))
            for _ in range(span):
                if rs > 1:
                    pending[col] = [rs - 1, t, ls, fl]
                texts.append(t); links.append(ls); flags.append(fl)
                col += 1
        yield texts, links, flags


class Tab:
    def __init__(self, t, outer=False):
        h = t.find_previous(["h2", "h3", "h4"])
        self.heading = h.get_text(" ", strip=True).replace("[edit]", "").strip() if h else ""
        self.t = t
        h2 = t.find_previous("h2")
        self.section = h2.get_text(" ", strip=True).replace("[edit]", "").strip() if h2 else ""
        trip = list(_rows(t, outer))
        self.rows = [(a, b) for a, b, _ in trip]
        self.flags = [c for _, _, c in trip]  # flag-icon country links per cell, aligned with self.rows
        self.hdr = [re.sub(r"^v t e\s*", "", c).strip() for c in (self.rows[0][0] if self.rows else [])]
        self.body = self.rows[1:]
        self.bflags = self.flags[1:]

    def col(self, *names, regex=False):
        for n in names:
            for i, h in enumerate(self.hdr):
                if (re.search(n, h, re.I) if regex else h == n):
                    return i
        raise LookupError(f"no column {names} in {self.hdr}")


def tabs(page, lang="en", outer=False, soup=None):
    soup = BeautifulSoup(page_html(page, lang), "lxml")
    for sup in soup.select("sup.reference, sup.noprint"):
        sup.decompose()
    return [Tab(t, outer) for t in soup.select("table.wikitable")]


def find_tabs(page, hdr=(), heading=None, first=None, outer=False):
    """Tabs whose header contains every name in `hdr` (substring, case-insens.) and, optionally, whose heading matches."""
    out = []
    for tb in tabs(page, outer=outer):
        hj = [h.lower() for h in tb.hdr]
        if all(any(n.lower() in h for h in hj) for n in hdr) and (heading is None or re.search(heading, tb.heading, re.I)) \
                and (first is None or (tb.hdr and re.search(first, tb.hdr[0], re.I))):
            out.append(tb)
    return out


def find_tab(page, hdr=(), heading=None, nth=0, first=None, outer=False):
    ts = find_tabs(page, hdr, heading, first, outer)
    if len(ts) <= nth:
        raise LookupError(f"{page}: no table with {hdr} / {heading} (headers: {str([t.hdr[:5] for t in tabs(page)][:8])[:300]})")
    return ts[nth]


# ---------------------------------------------------------------- names
def strip_paren(t):
    return re.sub(r"\s*\([^)]*\)\s*$", "", t).strip()


def clean_name(s):
    s = re.sub(r"\[.*?\]", "", s)
    s = re.sub(r"\s*\((?:c|captain|vc|GK|loan|on loan|a|HG)\)\s*", " ", s, flags=re.I)
    s = re.sub(r"[*†‡§#^]+", "", s)
    return re.sub(r"\s+", " ", s).strip()


def people(cell_links):
    """Person-ish links in a cell: drop national-team / federation links."""
    return [(t, a) for t, a in cell_links if not NAT_TEAM.search(t)]


def person_rec(title, anchor, detail):
    name = strip_paren(title)
    return {"answer": name, "enwiki": title, "detail": detail}


def club_rec(title, anchor, detail):
    name = clean_name(anchor) if anchor else strip_paren(title)
    return {"answer": name or strip_paren(title), "enwiki": title, "detail": detail}


# ---------------------------------------------------------------- accumulation
class Acc:
    """Accumulate answers by enwiki title with a list of evidence strings."""

    def __init__(self, kind="person"):
        self.d = {}
        self.kind = kind

    def add(self, title, anchor, ev):
        r = self.d.get(title)
        if r is None:
            r = (person_rec if self.kind == "person" else club_rec)(title, anchor, "")
            r["ev"] = []
            self.d[title] = r
        if ev and ev not in r["ev"]:
            r["ev"].append(ev)

    def out(self, joiner=", ", maxev=6):
        res = []
        for r in self.d.values():
            ev = r["ev"]
            d = joiner.join(ev[:maxev]) + (f" (+{len(ev) - maxev})" if len(ev) > maxev else "")
            res.append({"answer": r["answer"], "enwiki": r["enwiki"], "detail": d})
        return dedupe(res)


def dedupe(recs):
    """Merge records resolving to the same article; drop red links."""
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


def season_label(y):
    return f"{y}–{str(y + 1)[2:]}"


def season_pages(fmt, y0, y1):
    return [(season_label(y), fmt.format(s=season_label(y), y=y)) for y in range(y0, y1 + 1)]


# ---------------------------------------------------------------- countries
_TEAM_SPECIAL = {"United States": "United States men's national soccer team", "USA": "United States men's national soccer team",
                 "Korea Republic": "South Korea national football team", "Republic of Korea": "South Korea national football team",
                 "Czechia": "Czech Republic national football team", "Türkiye": "Turkey national football team",
                 "Ivory Coast": "Ivory Coast national football team", "Côte d'Ivoire": "Ivory Coast national football team",
                 "DR Congo": "DR Congo national football team", "Ireland": "Republic of Ireland national football team",
                 "North Macedonia": "North Macedonia national football team", "China PR": "China national football team",
                 "Cape Verde": "Cape Verde national football team", "Cabo Verde": "Cape Verde national football team",
                 "Holland": "Netherlands national football team"}


def country_rec(name, detail=""):
    """{'answer','enwiki'} for a country using the men's national-team article."""
    name = clean_name(name)
    title = _TEAM_SPECIAL.get(name, f"{name} national football team")
    return {"answer": name, "enwiki": title, "detail": detail}


# ---------------------------------------------------------------- squads
def _apps_num(s):
    return sum(int(x) for x in re.findall(r"\d+", s))


def squad_apps(page, comp, label=None, minapps=1, acc=None):
    """Players with >= minapps appearances in competition `comp` (regex on the competition header) according to the
    season page's 'Appearances and goals' / statistics table (two header rows: competition, then Apps/Goals)."""
    acc = acc or Acc()
    found = False
    for tb in tabs(page):
        if len(tb.rows) < 3:
            continue
        h0, h1 = tb.rows[0][0], tb.rows[1][0]
        if not any(re.fullmatch(r"Players?|Name", c) for c in h0 + h1):
            continue
        pi = next(i for i, c in enumerate(h0 if any(re.fullmatch(r"Players?|Name", c) for c in h0) else h1)
                  if re.fullmatch(r"Players?|Name", c))
        cols = [j for j, (a, b) in enumerate(zip(h0, h1)) if re.search(comp, a, re.I) and re.match(r"Apps?|Appearances|Starts|Pld|GP|MP", b)]
        if not cols:
            continue
        cols = cols[:1]
        found = True
        for tx, ln in tb.rows[2:]:
            if len(tx) <= max(cols + [pi]) or not ln[pi]:
                continue
            n = sum(_apps_num(tx[j]) for j in cols)
            if n >= minapps:
                t, a = people(ln[pi])[0] if people(ln[pi]) else ln[pi][0]
                acc.add(t, a, label or "")
        break
    if not found:  # single-header-row layouts: Player | L App | ... ; Name | League | ...
        for tb in tabs(page):
            pi = next((i for i, c in enumerate(tb.hdr) if re.fullmatch(r"Players?|Name", c)), None)
            if pi is None or len(tb.rows) < 5:
                continue
            ai = next((i for i, c in enumerate(tb.hdr) if re.fullmatch(r"L\s*Apps?|League(\s*Apps?)?|Apps?|" + comp + r"(\s*Apps?)?", c, re.I)), None)
            if ai is None:
                continue
            found = True
            for tx, ln in tb.rows[1:]:
                if len(tx) <= max(ai, pi) or not ln[pi]:
                    continue
                if _apps_num(tx[ai]) >= minapps:
                    t, a = people(ln[pi])[0] if people(ln[pi]) else ln[pi][0]
                    acc.add(t, a, label or "")
            break
    if not found:
        raise LookupError(f"{page}: no appearances table with competition {comp!r}")
    return acc


# ---------------------------------------------------------------- foreign-player lists
def foreign_list(page, heading_re, acc=None, label=""):
    """Players listed under the h3 whose text matches heading_re on 'List of foreign X players' pages (ul/li, first link)."""
    acc = acc or Acc()
    soup = BeautifulSoup(page_html(page), "lxml")
    for h in soup.find_all(["h2", "h3"]):
        if re.fullmatch(heading_re, h.get_text(" ", strip=True).replace("[edit]", "").strip()):
            box = h.parent if h.parent.name == "div" and "mw-heading" in (h.parent.get("class") or []) else h
            sib = box.find_next_sibling()
            while sib is not None and not (sib.name == "div" and "mw-heading" in (sib.get("class") or [])) \
                    and sib.name not in ("h2", "h3"):
                if sib.name == "ul":
                    for li in sib.find_all("li", recursive=False):
                        a = li.find("a")
                        if a and (x := _link_title(a)):
                            acc.add(x, a.get_text(" ", strip=True), label)
                sib = sib.find_next_sibling()
            return acc
    raise LookupError(f"{page}: no heading {heading_re}")


# ---------------------------------------------------------------- match scorers (football boxes)
def box_scorers(page, acc=None, label="", boxes=None, pick=None, team_ok=None):
    """Scorers (own goals and penalty shoot-out kicks excluded) from every {{football box}} on the page. `boxes`
    optionally filters by a callable on the box's soup element."""
    acc = acc or Acc()
    soup = BeautifulSoup(page_html(page), "lxml")
    all_boxes = soup.select("div.footballbox")
    if pick:
        all_boxes = pick(all_boxes)
    for b in all_boxes:
        if boxes and not boxes(b):
            continue
        in_pens = False
        for tr in b.select("table.fevent tr"):
            if "penalt" in tr.get_text(" ", strip=True).lower() and not tr.find(class_="fhgoal"):
                in_pens = True
                continue
            if in_pens or "fgoals" not in (tr.get("class") or []):
                continue
            for td in tr.select("td.fhgoal, td.fagoal"):
                if team_ok:
                    side = b.select_one("th.fhome a" if "fhgoal" in td.get("class") else "th.faway a")
                    tt = _link_title(side) if side else None
                    if not tt or not team_ok(tt):
                        continue
                items = td.select("li")
                if not items:  # scorers separated by <br> instead of a list
                    items = [BeautifulSoup(seg, "lxml") for seg in re.split(r"<br\s*/?>", td.decode_contents()) if seg.strip()]
                for li in items:
                    txt = li.get_text(" ", strip=True)
                    n_goals = len(re.findall(r"\d+(?:\+\d+)?['′’]", txt))
                    n_og = len(re.findall(r"o\.g\.|own goal", txt, re.I))
                    if n_og and n_og >= n_goals:
                        continue
                    a = li.find("a")
                    if a and (x := _link_title(a)):
                        acc.add(x, a.get_text(" ", strip=True), label)
    return acc


# ---------------------------------------------------------------- dates / hat-tricks / top scorers
import datetime as _dt

_MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                         "September", "October", "November", "December"], 1)}


def parse_date(s):
    m = re.search(r"(\d{1,2})\s+([A-Z][a-z]+)\s+(\d{4})", s)
    if m and m.group(2) in _MONTHS:
        return _dt.date(int(m.group(3)), _MONTHS[m.group(2)], int(m.group(1)))
    m = re.search(r"([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4})", s)
    if m and m.group(1) in _MONTHS:
        return _dt.date(int(m.group(3)), _MONTHS[m.group(1)], int(m.group(2)))
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def first_person(cell):
    p = people(cell)
    return p[0] if p else None


def hattricks(page, since, until=None, acc=None, heading=None, extra_hdr=()):
    """Players in 'List of X hat-tricks' tables (Player + Date columns; one or several tables) dated >= since."""
    acc = acc or Acc()
    for tb in find_tabs(page, ["Player", "Date", *extra_hdr], heading=heading):
        ci, di = tb.col("Player"), tb.col("Date")
        for tx, ln in tb.body:
            if len(tx) <= max(ci, di):
                continue
            d = parse_date(tx[di])
            if d and d >= since and (not until or d <= until) and (p := first_person(ln[ci])):
                acc.add(p[0], p[1], d.strftime("%Y"))
    return acc


def top_scorers(page, maxrank=5, acc=None, label="", heading=r"scorers", kind="Goals"):
    """Players ranked <= maxrank (ties included) in a season page's top-scorers table (Player + Goals columns)."""
    acc = acc or Acc()
    tb = find_tab(page, ["Player", kind], heading=heading)
    ci = tb.col("Player")
    ri = next((i for i, h in enumerate(tb.hdr) if re.fullmatch(r"Rank|#|No\.|Pos\.?|Nr\.|R", h)), 0)
    last = 0
    for tx, ln in tb.body:
        m = re.match(r"\d+", tx[ri].replace("=", "").replace("T", "").strip())
        if m:
            last = int(m.group())
        elif tx[ri].strip():
            continue
        if last and last <= maxrank and (p := first_person(ln[ci])):
            acc.add(p[0], p[1], label)
    return acc


def team_changes(page, kind, acc=None, label=""):
    """Clubs in the 'Team changes' table column whose header starts with `kind` ('Promoted from' / 'Relegated from')."""
    acc = acc or Acc("club")
    tb = find_tab(page, [kind], heading="Team changes")
    ci = tb.col(kind, regex=True) if False else next(i for i, h in enumerate(tb.hdr) if h.startswith(kind))
    for tx, ln in tb.body:
        for t, a in ln[ci]:
            acc.add(t, a, label)
    return acc


def team_col_clubs(page, heading="Stadiums and locations", col=r"Team|Club", acc=None, label="", stadium=False):
    """Clubs (or their home stadiums) from a season page's 'Stadiums and locations' table."""
    acc = acc or Acc("club")
    tb = find_tab(page, [], heading=heading)
    ci = next(i for i, h in enumerate(tb.hdr) if re.fullmatch(col, h))
    si = next((i for i, h in enumerate(tb.hdr) if re.fullmatch(r"Stadium|Venue|Ground", h)), None) if stadium else None
    for tx, ln in tb.body:
        cell = ln[si] if stadium else ln[ci]
        if cell:
            acc.add(cell[0][0], cell[0][1], label)
    return acc


def league_table_clubs(page):
    """[(title, anchor)] of the clubs in a season page's main league table (first table with Pos + Team columns)."""
    for tb in tabs(page):
        if tb.hdr[:1] == ["Pos"] and any(h.startswith("Team") for h in tb.hdr):
            ti = next(i for i, h in enumerate(tb.hdr) if h.startswith("Team"))
            out = [ln[ti][0] for tx, ln in tb.body if len(ln) > ti and ln[ti]]
            if out:
                return out
    raise LookupError(f"{page}: no league table")


def promoted_relegated(fmt, y0, y1, kind, label=lambda y: ""):
    """Clubs promoted into (kind='promoted': in season y but not y-1) or relegated out of (kind='relegated': in season
    y but not y+1) a league, for seasons y0..y1, by diffing consecutive league tables."""
    acc = Acc("club")
    cache = {}

    def clubs(y):
        if y not in cache:
            cl = league_table_clubs(fmt.format(s=season_label(y), y=y))
            res = resolve([t for t, _ in cl])
            cache[y] = {res[t]["title"]: (t, a) for t, a in cl}
        return cache[y]

    for y in range(y0, y1 + 1):
        cur = clubs(y)
        other = clubs(y - 1 if kind == "promoted" else y + 1)
        for canon, (t, a) in cur.items():
            if canon not in other:
                acc.add(t, a, label(y) or season_label(y))
    return acc


def season_coaches(page, outer=False):
    """Coaches in a season page: 'Manager' column of the personnel table plus outgoing (left during the season) and
    incoming coaches from the managerial-changes table."""
    acc = Acc()
    mname = r"Manager|Head coach|Coach"
    pt = next(tb for tb in tabs(page) if any(re.fullmatch(mname, h) for h in tb.hdr) and
              ("Captain" in tb.hdr or "Kit manufacturer" in tb.hdr or "Kit maker" in tb.hdr))
    mi = next(i for i, h in enumerate(pt.hdr) if re.fullmatch(mname, h))
    for tx, ln in pt.rows[1:]:
        if len(ln) > mi and ln[mi] and not re.fullmatch(mname, tx[mi]):
            for t, a in ln[mi]:
                if not re.search(r"national|Football", t):
                    acc.add(t, a, "in charge")
    for tb in tabs(page):
        if any(h.startswith("Outgoing") for h in tb.hdr) and any(h.startswith("Incoming") for h in tb.hdr):
            oi = next(i for i, h in enumerate(tb.hdr) if h.startswith("Outgoing"))
            ii = next(i for i, h in enumerate(tb.hdr) if h.startswith("Incoming"))
            pos = next((i for i, h in enumerate(tb.hdr) if re.search(r"Position|table", h)), None)
            for tx, ln in tb.rows[1:]:
                if len(ln) <= max(oi, ii) or tx[oi].startswith("Outgoing"):
                    continue
                pre = pos is not None and re.search(r"pre-?season", tx[pos], re.I)
                if not pre:
                    for t, a in ln[oi][:1]:
                        acc.add(t, a, "left during season")
                for t, a in ln[ii][:1]:
                    acc.add(t, a, "appointed")
            break
    return acc


def managers_since(page, year=2000):
    """Managers in a 'List of X managers' page whose tenure touches `year` or later (From/To/Years/Tenure/Season col)."""
    acc = Acc()
    per = re.compile(r"From|To|Years|Tenure|Season|Period|Dates", re.I)
    for tb in tabs(page):
        mi = next((i for i, h in enumerate(tb.hdr) if re.fullmatch(r"Name|Manager|Coach|Head coach", h)), None)
        pcols = [i for i, h in enumerate(tb.hdr) if per.fullmatch(h)]
        if mi is None or not pcols:
            continue
        for tx, ln in tb.body:
            if len(ln) <= max([mi] + pcols) or not ln[mi]:
                continue
            txt = " ".join(tx[i] for i in pcols)
            yrs = [int(y) for y in re.findall(r"\d{4}", txt)]
            if (yrs and max(yrs) >= year) or re.search(r"present|incumbent|current", txt, re.I):
                p = first_person(ln[mi])
                if p:
                    acc.add(p[0], p[1], re.sub(r"\s+", " ", txt)[:40])
    return acc


# ---------------------------------------------------------------- wikidata helpers
def wd_property_label(titles, prop="P17"):
    """{enwiki title -> English label of the item's `prop` value} via Wikidata SPARQL (titles resolved to QIDs first)."""
    from ballion.wikidata import sparql
    res = resolve(titles)
    qid2title = {}
    for t in titles:
        q = res[t]["qid"]
        if q:
            qid2title.setdefault(q, []).append(t)
    out = {}
    qs = list(qid2title)
    for i in range(0, len(qs), 60):
        chunk = qs[i:i + 60]
        vals = " ".join(f"wd:{q}" for q in chunk)
        rows = sparql(f'SELECT ?q ?l WHERE {{ VALUES ?q {{ {vals} }} ?q wdt:{prop} ?c . ?c rdfs:label ?l . FILTER(LANG(?l)="en") }}')
        for r in rows:
            q = r["q"].rsplit("/", 1)[1]
            for t in qid2title.get(q, []):
                out.setdefault(t, r["l"])
    return out


def wd_filter(titles, occupation=None):
    """Subset of enwiki titles that are humans (Wikidata P31=Q5), optionally with occupation `occupation` (e.g. Q937857
    = association football player)."""
    from ballion.wikidata import sparql
    titles = list(dict.fromkeys(titles))
    res = resolve(titles)
    qid2title = {}
    for t in titles:
        q = res[t]["qid"]
        if q:
            qid2title.setdefault(q, []).append(t)
    keep = set()
    qs = list(qid2title)
    for i in range(0, len(qs), 60):
        vals = " ".join(f"wd:{q}" for q in qs[i:i + 60])
        occ = f" ?q wdt:P106 wd:{occupation} ." if occupation else ""
        rows = sparql(f"SELECT DISTINCT ?q WHERE {{ VALUES ?q {{ {vals} }} ?q wdt:P31 wd:Q5 .{occ} }}")
        for r in rows:
            keep.update(qid2title.get(r["q"].rsplit("/", 1)[1], []))
    return keep
