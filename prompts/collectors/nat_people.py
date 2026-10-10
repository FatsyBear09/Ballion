"""nat: manager / captain / record-holder lists for individual national teams."""
import re

from ballion.registry import prompt
from ballion.tables import rows
from prompts.collectors.nat_tournaments import name_from_title
from prompts.collectors.nat_util import dedupe, links_in, soup, soup_noflags
from prompts.collectors.nat_tournaments import section_nodes


def _first_year(s):
    m = re.search(r"\b(1[89]\d\d|20\d\d)\b", s)
    return int(m.group()) if m else None


def _hdr_clean(h):
    return [re.sub(r"\s+", " ", c).strip() for c in h]


def manager_rows(page, name_col, date_col, since):
    """Rows of every table in `page` having both columns; keep appointments starting in or after `since`."""
    s = soup_noflags(page)
    recs = []
    for t in s.find_all("table"):
        rs = list(rows(t))
        if not rs:
            continue
        # header may sit in row 0 or row 1 (spanning headers)
        for hi in (0, 1):
            if hi >= len(rs):
                break
            h = _hdr_clean(rs[hi][0])
            if name_col in h and date_col in h:
                ni, di = h.index(name_col), h.index(date_col)
                for tx, ln in rs[hi + 1:]:
                    if len(tx) <= max(ni, di):
                        continue
                    y = _first_year(tx[di])
                    ls = [x for x in ln[ni] if not x.startswith("Caretaker")]
                    if y and y >= since and ls:
                        recs.append({"answer": name_from_title(ls[0]), "enwiki": ls[0], "detail": f"from {y}"})
                break
    return recs


def _mgr(page, name_col, date_col, since):
    return lambda: dedupe(manager_rows(page, name_col, date_col, since))


@prompt("nat087", "Name a manager of Brazil or Argentina since 1990 (caretakers included)",
        "en:List of Brazil national football team managers, List of Argentina national football team managers — appointments from 1990",
        family="nat-manager-of-country")
def _nat087():
    return dedupe(manager_rows("List of Brazil national football team managers", "Name", "From", 1990)
                  + manager_rows("List of Argentina national football team managers", "Manager", "Tenure", 1990))


prompt("nat088", "Name a manager of the Italy national team since 1990 (caretakers included)",
       "en:List of Italy national football team managers — appointments from 1990",
       family="nat-manager-of-country")(_mgr("List of Italy national football team managers", "Name", "Date", 1990))
prompt("nat089", "Name a manager of the Mexico national team since 2000 (caretakers included)",
       "en:List of Mexico national football team managers — career column from 2000",
       family="nat-manager-of-country")(_mgr("List of Mexico national football team managers", "Manager", "Career", 2000))
prompt("nat090", "Name a manager of the South Korea national team since 2000 (caretakers included)",
       "en:List of South Korea national football team managers — appointments from 2000",
       family="nat-manager-of-country")(_mgr("List of South Korea national football team managers", "Manager", "From", 2000))
prompt("nat091", "Name a head coach of Saudi Arabia since 2000 (caretakers included)",
       "en:Saudi Arabia national football team — Coaching history table, first match from 2000",
       family="nat-manager-of-country")(_mgr("Saudi Arabia national football team", "Coach", "First match", 2000))


@prompt("nat092", "Name a head coach of Nigeria since 2000 (caretakers included)",
        "en:Nigeria national football team — Coaching history list (tenure years from 2000)",
        family="nat-manager-of-country")
def _nat092():
    s = soup("Nigeria national football team")
    recs = []
    for n in section_nodes(s, "Coaching history"):
        for li in ([n] if n.name == "li" else n.find_all("li")):
            txt = li.get_text(" ", strip=True)
            m = re.search(r"\(([^)]*)\)", txt)
            ls = links_in(li)
            if not m or not ls:
                continue
            ys = [int(x) for x in re.findall(r"(?:^|,\s*)(\d{4})", m.group(1))]
            if any(y >= 2000 for y in ys):
                recs.append({"answer": name_from_title(ls[0][1]), "enwiki": ls[0][1], "detail": m.group(1)})
    return dedupe(recs)


@prompt("nat095", "Name a player who first captained the England men's team in 2000 or later (one-off captains included)",
        "en:List of England national football team captains — men's captain chronology + captains by appearances (first captaincy 2000+)",
        family="nat-captain-list")
def _nat095():
    s = soup_noflags("List of England national football team captains")
    men = set()
    for n in section_nodes(s, "Captain chronology"):
        for t in ([n] if n.name == "table" else n.find_all("table")):
            for tx, ln in rows(t):
                men.update(x for cell in ln for x in cell)
        if men:
            break
    recs = []
    for t in s.find_all("table"):
        rs = list(rows(t))
        if rs and _hdr_clean(rs[0][0])[:3] == ["#", "Player", "England career"]:
            h = _hdr_clean(rs[0][0])
            fi = h.index("First captaincy")
            for tx, ln in rs[1:]:
                y = _first_year(tx[fi])
                if y and y >= 2000 and ln[1] and ln[1][-1] in men:
                    recs.append({"answer": name_from_title(ln[1][-1]), "enwiki": ln[1][-1],
                                 "detail": f"first captaincy {tx[fi]}"})
            break
    return dedupe(recs)
