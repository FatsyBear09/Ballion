"""Shared helpers for the nat* (national football) collectors."""
import re
from urllib.parse import unquote

from bs4 import BeautifulSoup

from ballion.tables import _link_title
from ballion.wiki import page_html, resolve

# ------------------------------------------------------------------ generic


def dedupe(recs):
    """Merge records whose enwiki titles resolve to the same canonical article; drop red links."""
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
            out[key] = dict(r, answer=clean_name(r["answer"]))
    return list(out.values())


def clean_name(s):
    """Strip footnote marks and squad annotations such as (c), (vc), ( vice-captain ), (captain)."""
    s = re.sub(r"\[.*?\]", "", s)
    s = re.sub(r"\s*\(\s*(?:c|vc|gk|(?:[\w-]+\s+)?(?:vice[- ]?)?captain)\s*\)", "", s, flags=re.I)
    s = re.sub(r"[*†‡§#]+", "", s)
    return re.sub(r"\s+", " ", s).strip(" ,")


_soups = {}


def soup(title, lang="en"):
    """Parsed article with footnote markers removed (cached per process)."""
    key = (title, lang)
    if key not in _soups:
        s = BeautifulSoup(page_html(title, lang), "lxml")
        for sup in s.select("sup.reference, span.mw-editsection, style"):
            sup.decompose()
        _soups[key] = s
    return _soups[key]


def soup_noflags(title, lang="en"):
    """Like soup() but with flag icons removed (so table name cells only hold the name's own links)."""
    key = ("nf", title, lang)
    if key not in _soups:
        s = BeautifulSoup(str(soup(title, lang)), "lxml")
        for f in s.select(".flagicon"):
            f.decompose()
        _soups[key] = s
    return _soups[key]


def links_in(node, skip_flags=True):
    out = []
    for a in node.find_all("a"):
        if skip_flags and a.find_parent(class_="flagicon"):
            continue
        t = _link_title(a)
        if t and not t.startswith(("Captain", "List of")) and "(association football)" not in t:
            out.append((a.get_text(" ", strip=True), t))
    return out


def heading_text(h):
    return h.get_text(" ", strip=True).replace("[edit]", "").strip()


# ------------------------------------------------------------------ national team articles
_TEAM_CACHE = {}
TEAM_OVERRIDE = {
    "United States": "United States men's national soccer team",
    "USA": "United States men's national soccer team",
    "Ivory Coast": "Ivory Coast national football team",
    "Côte d'Ivoire": "Ivory Coast national football team",
    "DR Congo": "DR Congo national football team",
    "Congo DR": "DR Congo national football team",
    "Republic of Ireland": "Republic of Ireland national football team",
    "Ireland": "Republic of Ireland national football team",
    "Türkiye": "Turkey national football team",
    "Turkey": "Turkey national football team",
    "China": "China national football team",
    "China PR": "China national football team",
    "Korea Republic": "South Korea national football team",
    "IR Iran": "Iran national football team",
    "Cabo Verde": "Cape Verde national football team",
    "Czechia": "Czech Republic national football team",
    "West Germany": "Germany national football team",
}
SUFFIXES = [" national football team", " men's national soccer team", " national soccer team"]


def team_titles(names):
    """Resolve country names -> national-team article titles (batched)."""
    need = [n for n in dict.fromkeys(names) if n not in _TEAM_CACHE]
    if need:
        cands = {}
        for n in need:
            cands[n] = [TEAM_OVERRIDE[n]] if n in TEAM_OVERRIDE else [n + s for s in SUFFIXES]
        res = resolve([c for v in cands.values() for c in v])
        for n in need:
            for c in cands[n]:
                if not res[c]["missing"]:
                    _TEAM_CACHE[n] = res[c]["title"]
                    break
            else:
                raise LookupError(f"no national team article for {n!r}")
    return {n: _TEAM_CACHE[n] for n in names}


def country_recs(pairs):
    """[(display, detail)] -> deduped country answers linked to the men's national team article."""
    tt = team_titles([p[0] for p in pairs])
    return dedupe([{"answer": n, "enwiki": tt[n], "detail": d} for n, d in pairs])


# ------------------------------------------------------------------ squads pages
_FLAG_RE = re.compile(r"Flag_of_(?:the_)?([^./]+?)(?:_\(.*)?\.(?:svg|png)", re.I)


def _flag_country(node):
    img = node.find("img") if node else None
    if not img:
        return None
    m = _FLAG_RE.search(unquote(img.get("src", "")))
    return m.group(1).replace("_", " ") if m else img.get("alt")


def _int(s):
    m = re.search(r"\d+", s.replace(",", ""))
    return int(m.group()) if m else None


_squad_cache = {}


def _col_int(tr, cells, name):
    t = tr.find_parent("table")
    first = t.find("tr")
    hdr = [c.get_text(" ", strip=True) for c in first.find_all(["th", "td"], recursive=False)]
    if name in hdr and hdr.index(name) < len(cells):
        return _int(cells[hdr.index(name)].get_text())
    return None


def _plain_player_row(tr):
    """Squad rows written without the nat-fs-player class (older/hand-made tables)."""
    cells = tr.find_all(["td", "th"], recursive=False)
    return (len(cells) >= 5 and cells[2].name == "th" and cells[2].get("scope") == "row"
            and cells[1].name == "td" and tr.find_parent("table") is not None
            and "Pos" in tr.find_parent("table").get_text(" ")[:300])


def squads(title):
    """Parse a '<tournament> squads' article -> {team: {"coach": [(name, link)], "players": [...]}}.
    Each player: no, pos, name, link, born (year), caps, goals, club, clubtxt, clubnat, captain."""
    if title in _squad_cache:
        return _squad_cache[title]
    s = soup(title)
    teams = {}
    cur = None
    root = s.find("div", class_="mw-parser-output") or s
    for el in root.descendants:
        nm = getattr(el, "name", None)
        if nm in ("h2", "h3", "h4"):
            cur = heading_text(el)
            continue
        if cur is None:
            continue
        if nm == "p" and re.match(r"\s*(Head\s+)?([Cc]oach|[Mm]anager|[Tt]rainer)(es)?\s*:", el.get_text()):
            tm = teams.setdefault(cur, {"coach": [], "players": []})
            flag = False  # a flag icon before the name marks a coach of another nationality
            for ch in el.descendants:
                cls = ch.get("class") or [] if hasattr(ch, "get") else []
                if getattr(ch, "name", None) == "span" and "flagicon" in cls:
                    flag = True
                elif getattr(ch, "name", None) == "a" and not ch.find_parent(class_="flagicon"):
                    t = _link_title(ch)
                    if t:
                        tm["coach"].append((ch.get_text(" ", strip=True), t, flag))
                        flag = False
        elif nm == "tr" and ("nat-fs-player" in (el.get("class") or []) or _plain_player_row(el)):
            cells = el.find_all(["td", "th"], recursive=False)
            if len(cells) < 4:
                continue
            tm = teams.setdefault(cur, {"coach": [], "players": []})
            ptxt = el.find("th") or cells[2]
            pls = links_in(ptxt)
            txt = ptxt.get_text(" ", strip=True)
            cap = bool(re.search(r"\(\s*(c|captain)\s*\)|\bcaptain\b", txt, re.I))
            bd = el.find(class_="bday")
            born = int(bd.get_text()[:4]) if bd else None
            club_cell = cells[-1]
            clubs = [t for _, t in links_in(club_cell)]
            pos_cell = cells[1].get_text(" ", strip=True)
            tm["players"].append({
                "no": cells[0].get_text(strip=True), "pos": re.sub(r"[^A-Z]", "", pos_cell.upper()),
                "name": clean_name(txt), "link": pls[-1][1] if pls else None, "born": born,
                "caps": _col_int(el, cells, "Caps"), "goals": _col_int(el, cells, "Goals"),
                "club": clubs[0] if clubs else None, "clubtxt": club_cell.get_text(" ", strip=True),
                "clubnat": _flag_country(club_cell), "captain": cap})
    teams = {k: v for k, v in teams.items() if v["players"]}
    _squad_cache[title] = teams
    return teams


def player_recs(plist, detail_fn):
    return dedupe([{"answer": p["name"], "enwiki": p["link"], "detail": detail_fn(p)} for p in plist if p["link"]])
