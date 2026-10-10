"""Parsers for 'List of foreign La Liga players' style pages (bullet lists: Player - Club - years)."""
import re
from functools import lru_cache

from ballion.tables import _link_title
from prompts.collectors.ll_util import soup_of


def last_start(text):
    """Latest season start year in the years part of 'Name - clubs - 2006-08, 09-' (open end = still playing)."""
    parts = [x.strip() for x in re.split(r"\s+[–—]\s+", text)]
    yrs = next((x for x in parts[1:] if re.match(r"\d{2,4}\b", x)), None)
    if yrs is None:
        return None
    best, century = None, None
    for tok in yrs.split(","):
        m = re.match(r"\s*(\d{2,4})(?:\s*([–—-])\s*(\d{2,4})?)?", tok)
        if not m:
            continue
        s0 = int(m.group(1))
        if s0 < 100:
            s0 += (century if century is not None else (1900 if s0 > 40 else 2000))
        century = (s0 // 100) * 100
        if m.group(2) and not m.group(3):
            v = 2026 if s0 >= 2010 else s0
        elif m.group(3):
            e = int(m.group(3))
            if e < 100:
                e += century
                if e < s0:
                    e += 100
            v = e - 1 if e > s0 else s0
        else:
            v = s0
        best = v if best is None else max(best, v)
    return best


@lru_cache(None)
def sections(page):
    """{section heading text: [entry]} for every h2/h3/h4 section containing list items."""
    soup = soup_of(page)
    out = {}
    for hd in soup.select("h2, h3, h4"):
        name = hd.get_text(" ", strip=True)
        wrap = hd.parent if hd.parent is not None and hd.parent.name == "div" and "mw-heading" in (hd.parent.get("class") or []) else hd
        ents = []
        n = wrap.find_next_sibling()
        while n is not None:
            if n.name == "div" and "mw-heading" in (n.get("class") or []):
                break
            if n.name in ("h2", "h3", "h4"):
                break
            for li in n.find_all("li") if n.name in ("ul", "ol", "div") else []:
                links = [(t, a.get_text(" ", strip=True), a) for a in li.find_all("a") if (t := _link_title(a))]
                people = [x for x in links if x[2].find_parent("small") is None]
                if not people or "redlink=1" in people[0][2].get("href", ""):
                    continue
                p = people[0]
                txt = li.get_text(" ", strip=True)
                if txt.find(p[1]) > 40:  # the first non-club link is not the player (unlinked name)
                    continue
                clubs = [(t, x) for t, x, a in links if a.find_parent("small") is not None]
                ents.append({"title": p[0], "name": p[1], "clubs": clubs, "text": txt, "last": last_start(txt)})
            n = n.find_next_sibling()
        out[name] = ents
    return out
