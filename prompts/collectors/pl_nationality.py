"""pl100-pl119: players of a given nationality who have played in the Premier League.

Source: en:List of foreign Premier League players. Each country section is a bulleted list
"Player - Club - seasons". A span "2007–12" means the seasons 2007–08 .. 2011–12; "2018–" is ongoing;
"1992–95" means 1992–93 .. 1994–95.  A player counts for "since 2015–16" if the last season of any
span ends in 2016 or later.
"""
import re

from bs4 import BeautifulSoup

from ballion.registry import prompt
from ballion.tables import _link_title
from ballion.wiki import page_html
from prompts.collectors.pl_util import Acc

PAGE = "List of foreign Premier League players"
_cache = {}


def _end_year(m):
    s, e = m.group(1), m.group(2)
    s = int(s)
    if e is None:  # open-ended "2018–"
        return 9999
    if e == "":
        return 9999
    e = int(e)
    if e < 100:
        e += s - s % 100
        if e < s:
            e += 100
    return e


def _span_end(text):
    best = 0
    for m in re.finditer(r"(\d{4})\s*[–-]\s*(\d{2,4})?", text):
        best = max(best, _end_year(m))
    return best


def countries():
    """{country heading: [(player name, article title, last season end year, text)]}"""
    if _cache:
        return _cache
    soup = BeautifulSoup(page_html(PAGE), "lxml")
    for h in soup.find_all(["h3", "h4"]):
        name = h.get_text(" ", strip=True)
        div = h.parent if h.parent and "mw-heading" in (h.parent.get("class") or []) else h
        rows = []
        n = div.find_next_sibling()
        while n is not None and not (n.name == "div" and "mw-heading" in (n.get("class") or [])):
            if n.name == "ul":
                for li in n.find_all("li", recursive=False):
                    a = next((x for x in li.find_all("a") if _link_title(x)), None)
                    if a is None:
                        continue
                    txt = li.get_text(" ", strip=True)
                    rows.append((a.get_text(" ", strip=True), _link_title(a), _span_end(txt), txt))
            n = n.find_next_sibling()
        if rows:
            _cache[name] = rows
    return _cache


def by_country(country, since_end=0):
    rows = countries()[country]
    acc = Acc()
    for name, title, end, txt in rows:
        if end >= since_end:
            acc.add(title, name, txt.split(" – ", 1)[-1][:80])
    return acc.out()


# (pid, nationality adjective article, section heading, since-season-start, article word)
NATS = [
    ("pl100", "a Brazilian", "Brazil", 2015), ("pl101", "a Spanish player", "Spain", 2015),
    ("pl102", "a French player", "France", 2020), ("pl103", "a Portuguese player", "Portugal", 2015),
    ("pl104", "a Dutch player", "Netherlands", 2015), ("pl105", "a German player", "Germany", 2015),
    ("pl106", "a Belgian player", "Belgium", 2015), ("pl107", "an Argentine player", "Argentina", 2015),
    ("pl108", "a Danish player", "Denmark", 2015), ("pl109", "a Norwegian player", "Norway", 2015),
    ("pl110", "an Ivorian player", "Ivory Coast", 2015), ("pl111", "a Nigerian player", "Nigeria", 2015),
    ("pl112", "a Senegalese player", "Senegal", 2015), ("pl113", "a Ghanaian player", "Ghana", 2015),
    ("pl114", "an American player", "United States", 2015), ("pl115", "a Colombian player", "Colombia", 2015),
    ("pl116", "a Moroccan player", "Morocco", 2015), ("pl117", "a Japanese player", "Japan", None),
    ("pl118", "a South Korean player", "Korea Republic", None), ("pl119", "an Egyptian player", "Egypt", None),
]


def _mk(pid, who, heading, since):
    who = who.replace("a Brazilian", "a Brazilian player")
    if since:
        text = f"Name {who} who has played in the Premier League since {since}–{(since + 1) % 100:02d}"
        src = f"en:{PAGE} — {heading} section, last season in 2015–16 or later" if since == 2015 else \
            f"en:{PAGE} — {heading} section, last season in {since}–{(since + 1) % 100:02d} or later"
        end = since + 1
    else:
        text = f"Name {who} who has played in the Premier League"
        src = f"en:{PAGE} — {heading} section"
        end = 0

    @prompt(pid, text, src, family="pl-nationality")
    def f():
        return by_country(heading, end)
    return f


for _n in NATS:
    _mk(*_n)
