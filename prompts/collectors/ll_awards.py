"""ll024-ll039, ll188: La Liga awards."""
import re

from ballion.registry import prompt
from prompts.collectors.ll_util import NAT_TEAM, clean, dedupe, find, season_label, tables

PM = "La Liga Player of the Month"
AW = "La Liga Awards"
SEASON_LINK = re.compile(r"^\d{4}(–\d{2,4})?\b|^\d{4} ")


def cell_players(text, links):
    """People in a cell shaped 'Name ( Club ) ; Name ( Club )' -> [(title, name)]."""
    out = []
    for seg in re.split(r"\s*;\s*", text):
        seg = seg.strip()
        if not seg or seg.startswith("("):
            continue
        name = re.split(r"\s*\(", seg)[0].strip()
        if not name:
            continue
        for t, a in links:
            if a == name or (len(name) > 3 and (a in name or name in a)):
                if not SEASON_LINK.match(t) and not NAT_TEAM.search(t):
                    out.append((t, name))
                    break
    return out


def col_people(tb, colname, detail_cols=(), pred=None, nth=0):
    """Person links from column `colname` of each data row."""
    h = tb["hdr"]
    ci = [i for i, c in enumerate(h) if colname in c][nth]
    out = []
    for tx, ln in tb["rows"]:
        if len(tx) <= ci or (pred and not pred(tx, h)) or not re.match(r"\d{4}", tx[0]):
            continue
        ppl = cell_players(tx[ci], ln[ci]) if ("(" in tx[ci] or ";" in tx[ci]) else [(l[0], tx[ci]) for l in ln[ci][-1:] if not SEASON_LINK.match(l[0])]
        for t, name in ppl:
            d = tx[0] if not SEASON_LINK.match(tx[0]) or True else ""
            out.append({"answer": clean(re.sub(r"\s*\(\d+\)$", "", name)), "enwiki": t,
                        "detail": ", ".join([x for x in [tx[0]] + [tx[h.index(c)] for c in detail_cols if c in h] if x])})
    return out


def monthly(pid, text, page, role, head="Winners", fam=None, first="Month"):
    @prompt(pid, text, f"en:{page} — Winners", family=fam)
    def fn():
        tb = find(page, first, [role, "Year"], head=head)
        recs = []
        h = tb["hdr"]
        ci = h.index(role)
        for tx, ln in tb["rows"]:
            if len(tx) <= ci or not ln[ci]:
                continue
            t = [l for l in ln[ci] if not SEASON_LINK.match(l[0])]
            if t:
                recs.append({"answer": clean(tx[ci]), "enwiki": t[-1][0], "detail": f"{tx[0]} {tx[1][-4:]}"})
        return dedupe(recs)
    return fn


monthly("ll024", "Name a winner of the La Liga Player of the Month award", PM, "Player", fam="ll-monthly")
monthly("ll025", "Name a winner of the La Liga Manager of the Month award", "La Liga Manager of the Month", "Manager", fam="ll-monthly")
monthly("ll026", "Name a winner of the La Liga U23 Player of the Month award", "La Liga U23 Player of the Month", "Player", fam="ll-monthly")
monthly("ll027", "Name a winner of the La Liga Goal of the Month award", "La Liga Goal of the Month", "Player", fam="ll-monthly")
monthly("ll188", "Name a winner of the Segunda División Player of the Month award", "Segunda División Player of the Month", "Player", fam="ll-monthly")


def _club_table(page, head, pid):
    tb = find(page, "Club", ["Players", "Wins"], head=head)
    recs = []
    for tx, ln in tb["rows"]:
        if ln[0] and tx[1].isdigit():
            recs.append({"answer": clean(tx[0]), "enwiki": ln[0][-1][0], "detail": f"{tx[1]} winner(s), {tx[2]} awards"})
    return dedupe(recs)


@prompt("ll038", "Name a club whose player has won the La Liga Player of the Month award",
        "en:La Liga Player of the Month — Awards won by club", family="ll-monthly-club")
def ll038():
    return _club_table(PM, "club", "ll038")


NATION_TITLE = {"Ivory Coast": "Ivory Coast national football team", "DR Congo": "DR Congo national football team",
                "Republic of Ireland": "Republic of Ireland national football team",
                "United States": "United States men's national soccer team",
                "China": "China national football team"}


@prompt("ll039", "Name a country whose player has won the La Liga Player of the Month award",
        "en:La Liga Player of the Month — Awards won by nationality (national football team articles)", family="ll-monthly-nation")
def ll039():
    tb = find(PM, "Nationality", ["Players", "Wins"], head="nationality")
    recs = []
    for tx, ln in tb["rows"]:
        if tx[1].isdigit():
            n = clean(tx[0])
            recs.append({"answer": n, "enwiki": NATION_TITLE.get(n, f"{n} national football team"),
                         "detail": f"{tx[1]} winner(s), {tx[2]} awards"})
    return dedupe(recs)


# ---------------------------------------------------------------- La Liga Awards page

def _aw(head, role="Recipient"):
    tb = find(AW, "Season", [role], head=head)
    return col_people(tb, role)


@prompt("ll028", "Name a player named in a La Liga Team of the Season (2013–14 onward)",
        "en:La Liga Awards — Team of the season")
def ll028():
    tb = find(AW, "Season", [], head="Team of the season")
    recs = []
    for tx, ln in tb["rows"]:
        if not re.match(r"\d{4}", tx[0]):
            continue
        for i in range(1, len(tx)):
            for t, name in cell_players(tx[i], ln[i]):
                recs.append({"answer": clean(name), "enwiki": t, "detail": tx[0]})
    return dedupe(recs)


@prompt("ll029", "Name a winner of a La Liga season award (Player, Manager, African Player, U23 Player, Goal or Save of the Season)",
        "en:La Liga Awards — Player / Manager / African player / U23 player / Goal / Save of the season")
def ll029():
    recs = []
    for head in ("Player of the season", "Manager of the season", "African player of the season",
                 "U23 Player of the season", "Goal of the season", "Save of the season"):
        for r in _aw(head):
            r["detail"] = f"{head} {r['detail']}"
            recs.append(r)
    return dedupe(recs)


@prompt("ll030", "Name a winner of a discontinued La Liga award (Best Forward, Midfielder, Attacking Midfielder, Defender, Goalkeeper, Breakthrough or Best American Player)",
        "en:La Liga Awards — discontinued LFP awards (2008–09 to 2014–15)")
def ll030():
    recs = []
    for head in ("Best Forward", "Goalkeeper of the season", "Best Attacking Midfielder", "Best Midfielder",
                 "Best Defender", "Breakthrough Player", "Best American Player"):
        for r in _aw(head):
            r["detail"] = f"{head} {r['detail']}"
            recs.append(r)
    return dedupe(recs)


# ---------------------------------------------------------------- Zamora / Zarra / MARCA / Don Balon / EFE

@prompt("ll031", "Name a winner of the Ricardo Zamora Trophy in La Liga (best goalkeeper by goals-against average)",
        "en:Ricardo Zamora Trophy — Winners (Primera División)")
def ll031():
    tb = find("Ricardo Zamora Trophy", "Season", ["Player", "Goals conceded"], head="Winners")
    return dedupe(col_people(tb, "Player"))


# ll032 dropped: the season pages have no parseable Zamora standings table.
def ll032():
    recs = []
    for y in range(2015, 2026):
        s = season_label(y)
        tb = find(f"{s} La Liga", "Rank", ["Player", "Club"], head="Zamora")
        for r in col_people(tb, "Player"):
            r["detail"] = s
            recs.append(r)
    return dedupe(recs)


@prompt("ll033", "Name a winner of the Zarra Trophy (top Spanish scorer in La Liga or the Segunda División)",
        "en:Zarra Trophy — La Liga and Segunda División winners")
def ll033():
    recs = []
    for head in ("La Liga", "Segunda División"):
        tb = find("Zarra Trophy", "Season", ["Goals"], head=head)
        h = tb["hdr"]
        pi = [i for i, c in enumerate(h) if "Player" in c][0]
        for tx, ln in tb["rows"]:
            for t, a in ln[pi]:
                if not SEASON_LINK.match(t):
                    recs.append({"answer": clean(a), "enwiki": t, "detail": f"{head} {tx[0]}"})
    return dedupe(recs)


@prompt("ll034", "Name a winner of MARCA's Miguel Muñoz Trophy for La Liga coach of the season",
        "en:Miguel Muñoz Trophy — La Liga")
def ll034():
    tb = find("Miguel Muñoz Trophy", "Season", ["Score"], head="La Liga")
    return dedupe(col_people(tb, "Manager"))


@prompt("ll035", "Name a player who finished in the top three of MARCA's Alfredo Di Stéfano Trophy (La Liga player of the season)",
        "en:Trofeo Alfredo Di Stéfano — Winners table (ranks 1st to 3rd)")
def ll035():
    tb = find("Trofeo Alfredo Di Stéfano", None, ["Rank", "Player"], head="Winners")
    h = tb["hdr"]
    ri, pi = h.index("Rank"), h.index("Player")
    recs = []
    for tx, ln in tb["rows"]:
        if len(tx) > pi and re.match(r"[123](st|nd|rd)", tx[ri]) and ln[pi]:
            recs.append({"answer": clean(tx[pi]), "enwiki": ln[pi][-1][0], "detail": tx[0].split(";")[0].strip()})
    return dedupe(recs)


@prompt("ll036", "Name a player or coach who won a Don Balón Award (best Spanish player, best foreign player, best breakthrough or best coach)",
        "en:Don Balón Award — Winners (referees excluded)")
def ll036():
    tb = find("Don Balón Award", "Season", ["Best coach"], head="Winners")
    recs = []
    h = tb["hdr"]
    for c in ("Best Spanish", "Best foreign", "Best breakthrough", "Best coach"):
        ci = [i for i, x in enumerate(h) if x.startswith(c)][0]
        for tx, ln in tb["rows"]:
            if len(tx) <= ci or tx[ci] in ("–", "-", ""):
                continue
            for t, name in cell_players(tx[ci], ln[ci]):
                recs.append({"answer": clean(name), "enwiki": t, "detail": f"{c} {tx[0]}"})
    return dedupe(recs)


@prompt("ll037", "Name a winner of the Trofeo EFE (best Ibero-American player in La Liga)",
        "en:Trofeo EFE — Winners (men's La Liga seasons)")
def ll037():
    tb = find("Trofeo EFE", "Season", ["Player", "Club"], head="Winners")
    recs = []
    for tx, ln in tb["rows"]:
        if len(tx) < 3 or not ln[1] or not ln[0] or "La Liga" not in ln[0][0][0] or "Special" in tx[2]:
            continue
        txt = tx[1]
        m = re.match(r"(.*?)\s*\(Men\)", txt)
        name = clean(m.group(1)) if m else clean(txt)
        link = [l for l in ln[1] if l[1] == name]
        if not link:
            continue
        recs.append({"answer": name, "enwiki": link[0][0], "detail": tx[0]})
    return dedupe(recs)
