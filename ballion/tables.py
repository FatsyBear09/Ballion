"""Turn rendered Wikipedia tables into rows of cells, keeping each cell's article links."""
import re
from urllib.parse import unquote

from bs4 import BeautifulSoup

from ballion.wiki import page_html


def _link_title(a):
    href = a.get("href", "")
    if not href.startswith("/wiki/") or ":" in href[6:]:
        return None  # skip files, categories, external links
    return unquote(href[6:].split("#")[0]).replace("_", " ")


def _int_attr(cell, name):
    """Parse colspan/rowspan leniently: wikitext like rowspan="2"" renders as '2"'."""
    m = re.match(r"\d+", str(cell.get(name, "1")))
    return max(1, int(m.group())) if m else 1


def wikitables(title, lang="en"):
    soup = BeautifulSoup(page_html(title, lang), "lxml")
    for sup in soup.select("sup.reference"):
        sup.decompose()
    return soup.select("table.wikitable")


def rows(table):
    """Yield (texts, links) per row; links[i] is the list of article titles linked in cell i.
    Rowspan cells are repeated down so every row has full width."""
    pending = {}  # col index -> [remaining rows, text, links]
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
            t = c.get_text(" ", strip=True)
            ls = [x for x in (_link_title(a) for a in c.find_all("a")) if x]
            span = _int_attr(c, "colspan")
            rs = _int_attr(c, "rowspan")
            for _ in range(span):
                if rs > 1:
                    pending[col] = [rs - 1, t, ls]
                texts.append(t); links.append(ls)
                col += 1
        yield texts, links
