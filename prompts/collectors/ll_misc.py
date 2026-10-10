"""ll088, ll090, ll091, ll099, ll100, ll105, ll135, ll181-ll185, ll187: assorted lists."""
import re

from ballion.registry import prompt
from ballion.wiki import resolve
from prompts.collectors.ll_foreign import sections
from prompts.collectors.ll_util import clean, dedupe, find, season_label, season_top, tables
from prompts.collectors.ll_awards import monthly

CONTINENTS = ("Africa", "Asia", "Europe", "North", "South America", "Oceania")


def continent(S, prefix):
    keys = list(S)
    i = next(i for i, k in enumerate(keys) if k.startswith(prefix))
    j = next((j for j, k in enumerate(keys) if j > i and re.search(r"\((AFC|CAF|UEFA|CONMEBOL|CONCACAF|OFC)\)$", k)), len(keys))
    out = []
    for k in keys[i + 1:j]:
        out += S[k]
    return out


# ---------------------------------------------------------------- Segunda / promotion

@prompt("ll088", "Name a club that has taken part in the Segunda División promotion play-offs since 2011",
        "en:La Liga play-offs — 2011–present (promoted, finalist, semi-finalists)")
def ll088():
    tb = find("La Liga play-offs", "Season", ["Promoted", "Finalist"], head="2011")
    out = []
    for tx, ln in tb["rows"]:
        for c in range(1, len(ln)):
            for t, a in ln[c]:
                out.append({"answer": clean(a), "enwiki": t, "detail": f"{tx[0]}"})
    return dedupe(out)


@prompt("ll090", "Name a club that has won the Segunda División title since 2000",
        "en:Segunda División — Segunda División seasons (champions, 2000 onward)")
def ll090():
    tb = find("Segunda División", "Season", ["Champions", "Runners-up"], head="seasons")
    out = []
    for tx, ln in tb["rows"]:
        m = re.match(r"\d{4}", tx[0])
        if m and int(m.group()) >= 2000 and len(ln) > 1 and ln[1]:
            out.append({"answer": clean(tx[1]), "enwiki": ln[1][0][0], "detail": f"champions {tx[0]}"})
    return dedupe(out)


@prompt("ll091", "Name a former La Liga club that has played in the third tier (Primera Federación) since 2021–22",
        "en:2021–22 Primera División RFEF … 2025–26 Primera Federación — teams, intersected with En:List of La Liga clubs")
def ll091():
    ll = find("List of La Liga clubs", "Pos", ["Club", "Pts"], head="All-time table")
    ci = ll["hdr"].index("Club")
    names = [r[1][ci][0][0] for r in ll["rows"] if len(r[1]) > ci and r[1][ci]]
    pages = ["2021–22 Primera División RFEF", "2022–23 Primera Federación", "2023–24 Primera Federación",
             "2024–25 Primera Federación", "2025–26 Primera Federación"]
    seen = {}
    for pg in pages:
        for tb in tables(pg):
            h = tb["hdr"]
            if h[:1] == ["Team"] and "Stadium" in h:
                for tx, ln in tb["rows"]:
                    if ln and ln[0]:
                        seen.setdefault(ln[0][0][0], (clean(tx[0]), pg[:7]))
    res = resolve(names + list(seen))
    top = {res[n]["title"] for n in names}
    out = []
    for t, (n, s) in seen.items():
        if res[t]["title"] in top:
            out.append({"answer": n, "enwiki": t, "detail": f"third tier, {s}"})
    return dedupe(out)


# ---------------------------------------------------------------- stadiums, presidents, transfers

@prompt("ll099", "Name a football stadium in Spain with a capacity of 20,000 or more",
        "en:List of football stadiums in Spain — Current stadiums (capacity >= 20,000)")
def ll099():
    tb = find("List of football stadiums in Spain", "No.", ["Stadium", "Capacity"], head="Current stadiums")
    h = tb["hdr"]
    si, ci = h.index("Stadium"), h.index("Capacity")
    out = []
    for tx, ln in tb["rows"]:
        m = re.match(r"[\d,]+", tx[ci])
        if m and int(m.group().replace(",", "")) >= 20000 and ln[si]:
            out.append({"answer": clean(tx[si]), "enwiki": ln[si][0][0], "detail": f"capacity {m.group()}"})
    return dedupe(out)


@prompt("ll100", "Name a stadium that has hosted a Copa del Rey final",
        "en:List of Copa del Rey finals — List of finals (venue column)")
def ll100():
    tb = find("List of Copa del Rey finals", "Season", ["Winners", "Venue"], head="List of finals")
    vi = tb["hdr"].index("Venue")
    out = []
    for tx, ln in tb["rows"]:
        if len(tx) > vi and ln[vi]:
            t, a = ln[vi][0]
            if t.startswith(("Spanish Civil", "Spain")):
                continue
            out.append({"answer": clean(a), "enwiki": t, "detail": tx[0]})
    return dedupe(out)


@prompt("ll105", "Name a president of Real Madrid or Barcelona",
        "en:List of Real Madrid CF presidents; List of FC Barcelona presidents")
def ll105():
    out = []
    for page, club in (("List of Real Madrid CF presidents", "Real Madrid"), ("List of FC Barcelona presidents", "Barcelona")):
        tb = find(page, "Name", ["From", "To"], head="presidents")
        for tx, ln in tb["rows"]:
            if ln and ln[0] and ln[0][0][0] != "Mr Twin Sister":  # a wrong link in the Barcelona list (Eric Cardona)
                out.append({"answer": clean(tx[0]), "enwiki": ln[0][0][0], "detail": f"{club} president {tx[1][:20]}"})
    return dedupe(out)


@prompt("ll135", "Name a player whose move to or from a Spanish club is among football's 50 most expensive transfers of all time",
        "en:List of most expensive association football transfers — highest transfer records (From/To a La Liga-era Spanish club)")
def ll135():
    tb = find("List of most expensive association football transfers", "Rank", ["Player", "From", "To"], head="Highest transfer")
    h = tb["hdr"]
    pi, fi, ti = h.index("Player"), h.index("From"), h.index("To")
    ll = find("List of La Liga clubs", "Pos", ["Club", "Pts"], head="All-time table")
    ci = ll["hdr"].index("Club")
    names = [r[1][ci][0][0] for r in ll["rows"] if len(r[1]) > ci and r[1][ci]]
    club_links = {t for r in tb["rows"] for c in (fi, ti) for t, _ in r[1][c]}
    res = resolve(names + list(club_links))
    spanish = {res[n]["title"] for n in names}
    out = []
    for tx, ln in tb["rows"]:
        if not ln[pi] or not tx[0].strip().isdigit():
            continue
        spain = [(t, side) for side, c in (("from", fi), ("to", ti)) for t, _ in ln[c] if res[t]["title"] in spanish]
        if spain:
            out.append({"answer": clean(re.sub(r"\s*\(\d+\)$", "", tx[pi])), "enwiki": ln[pi][0][0],
                        "detail": f"#{tx[0]}, {tx[fi]} to {tx[ti]}"})
    return dedupe(out)


# ---------------------------------------------------------------- Copa del Rey semi-finals

@prompt("ll187", "Name a player who has scored in a Copa del Rey semi-final since 2019–20 (to 2025–26; own goals excluded)",
        "en:2019–20 Copa del Rey … 2025–26 Copa del Rey — semi-final goalscorers")
def ll187():
    from prompts.collectors.ll_util import soup_of
    from ballion.tables import _link_title
    out = []
    for y in range(2019, 2026):
        s = season_label(y)
        soup = soup_of(f"{s} Copa del Rey")
        for sp in soup.select("span.fb-goal"):
            h = None
            for hd in sp.find_all_previous(["h2", "h3"]):
                h = hd.get_text(" ", strip=True)
                if hd.name == "h2":
                    break
            if h != "Semi-finals":
                continue
            a = sp.find_previous("a")
            t = _link_title(a) if a is not None else None
            if not t:
                continue
            txt = sp.get_text(" ", strip=True)
            for sib in sp.next_siblings:
                if getattr(sib, "name", None) in ("a", "br"):
                    break
                txt += " " + (sib.get_text(" ", strip=True) if hasattr(sib, "get_text") else str(sib))
            if re.search(r"o\.\s?g|own goal", txt, re.I):
                continue
            out.append({"answer": re.sub(r"\s*\([^)]*\)$", "", t), "enwiki": t, "detail": s})
    return dedupe(out)


# ---------------------------------------------------------------- women's football

@prompt("ll181", "Name a player listed among Barcelona Femení's notable players",
        "en:List of FC Barcelona Femení players — Players", family="ll-women")
def ll181():
    tb = find("List of FC Barcelona Femení players", "Name", ["Barcelona career"], head="Players")
    out = []
    for tx, ln in tb["rows"]:
        if ln and ln[0]:
            out.append({"answer": clean(tx[0]), "enwiki": ln[0][0][0], "detail": tx[3]})
    return dedupe(out)


@prompt("ll182", "Name a player who finished in Liga F's top scorers table in a season from 2022–23 to 2025–26",
        "en:2022–23 Liga F … 2025–26 Liga F — Goalscorers", family="ll-women")
def ll182():
    out = []
    for y in range(2022, 2026):
        s = season_label(y)
        for name, title, club, val in season_top(f"{s} Liga F"):
            out.append({"answer": name, "enwiki": title, "detail": f"{val} goals, {s}"})
    return dedupe(out)


monthly("ll183", "Name a winner of the Liga F Player of the Month award", "Liga F Player of the Month", "Player", fam="ll-women")


FL = "List of foreign Liga F players"


@prompt("ll184", "Name a South American player who has played in Spain's top women's division (Liga F or its predecessor)",
        "en:List of foreign Liga F players — South America (CONMEBOL)", family="ll-women")
def ll184():
    ents = continent(sections(FL), "South America")
    return dedupe([{"answer": clean(e["name"]), "enwiki": e["title"], "detail": re.sub(r"^.*? – ", "", e["text"])[:80]} for e in ents])


@prompt("ll185", "Name an African player who has played in Spain's top women's division (Liga F or its predecessor)",
        "en:List of foreign Liga F players — Africa (CAF)", family="ll-women")
def ll185():
    ents = continent(sections(FL), "Africa")
    return dedupe([{"answer": clean(e["name"]), "enwiki": e["title"], "detail": re.sub(r"^.*? – ", "", e["text"])[:80]} for e in ents])
