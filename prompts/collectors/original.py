"""p001-p003: the user's original prompts."""
import re

from ballion.registry import prompt
from ballion.tables import rows, wikitables


def apps(s):
    """'33 (3)' -> 36, '(1)' -> 1, '0' -> 0."""
    return sum(int(n) for n in re.findall(r"\d+", s))


@prompt("p001", "Name a player who was part of Arsenal's Invincibles Premier League season (2003–04)",
        "en:2003–04 Arsenal F.C. season — Player statistics (≥1 Premier League appearance)")
def arsenal_invincibles():
    t = [t for t in wikitables("2003–04 Arsenal F.C. season")
         if "Name" in t.find("tr").get_text() and "Premier League" in t.find("tr").get_text()][0]
    out = []
    for tx, ln in rows(t):
        if len(tx) < 5 or not tx[0].isdigit() or not ln[3]:
            continue
        n = apps(tx[4])
        if n > 0:
            out.append({"answer": tx[3], "enwiki": ln[3][0], "detail": f"{tx[1]}, {n} PL apps"})
    return out


@prompt("p002", "Name a player who has scored over 100 goals in La Liga",
        "en:List of La Liga top scorers — La Liga players with 100 or more goals")
def laliga_100():
    t = wikitables("List of La Liga top scorers")[0]
    out = []
    for tx, ln in rows(t):
        if not tx[0].isdigit() or int(tx[2]) <= 100:  # 'over 100' -> strictly more than 100
            continue
        out.append({"answer": tx[1], "enwiki": ln[1][-1], "detail": f"{tx[2]} goals ({tx[5]}–{tx[6]})"})
    return out


TOP5 = [  # (country, page, table selector by header text, club col)
    ("England", "List of English football champions", ["Rank", "Club", "Winners"]),
    ("Spain", "List of Spanish football champions", ["Club", "Winners", "Runners-up"]),
    ("Germany", "List of German football champions", ["Club", "Winners", "Runners-up", "Winning seasons"]),
    ("Italy", "List of Italian football champions", ["Club", "Champions", "Runners-up"]),
    ("France", "List of French football champions", ["Rank", "Club", "Winners"]),  # amateur + pro era
]
FR_PRO_HDR = ["Club", "Winners", "Runners-up", "Winning seasons"]


@prompt("p003", "Name a club that has won the top-flight league title in one of Europe's top 5 leagues",
        "en:List of {English,Spanish,German,Italian,French} football champions — by-club tables")
def top5_champions():
    out = {}
    for country, page, hdr in TOP5:
        tables = wikitables(page)
        def header(t):
            return [c for c in next(rows(t))[0]]
        t = next(t for t in tables if header(t)[:len(hdr)] == hdr)
        ci = header(t).index("Club")
        wi = ci + 1
        pro = set()
        if country == "France":
            tp = next(t for t in tables if header(t)[:len(FR_PRO_HDR)] == FR_PRO_HDR)
            pro = {ln[0][-1] for tx, ln in list(rows(tp))[1:] if ln[0] and tx[1].isdigit()}
        for tx, ln in list(rows(t))[1:]:
            if not tx[wi].isdigit() or int(tx[wi]) == 0 or not ln[ci]:
                continue
            title = ln[ci][-1]  # last link skips flag icons (e.g. Rapid Wien's Austria flag)
            era = ""
            if country == "France":
                era = "pro" if title in pro or tx[ci] in {"RC Paris"} else "amateur-only"
            rec = out.setdefault(title, {"answer": re.sub(r"\s*†$", "", tx[ci]), "enwiki": title, "detail": []})
            rec["detail"].append(f"{country} ×{tx[wi]}" + (f" [{era}]" if era else ""))
    return [{**r, "detail": "; ".join(r["detail"])} for r in out.values()]
