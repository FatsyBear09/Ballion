"""Export scored prompts + answer aliases to web/data/ for the game.

  web/data/index.js     every prompt's id, theme, family, text and answer count (loaded up front)
  web/data/p/<id>.js    one prompt's answers + aliases (loaded on demand, 7 per game)
  web/data/names.js     every alias in the game, for the "different real entity" check

  python prompts/export_web.py

Aliases per answer (all later normalised in the browser the same way):
  - display name, enwiki title (minus "(footballer, born 1988)"-style qualifiers), both halves of "X (Y)"
  - Wikidata English label + aliases, plus labels in a few big football languages
  - people: surname (with particles, e.g. "van Basten"); clubs: name without FC/CF/AFC-style affixes
Ambiguity (one alias -> several answers in the same prompt) is resolved in the browser.
"""
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from ballion.scoring import TIERS  # noqa: E402
from ballion.themes import EXISTING_FAMILY, THEMES, theme_of  # noqa: E402
from ballion.wiki import _get  # noqa: E402
from ballion.wikidata import sparql  # noqa: E402

LABEL_LANGS = ["en", "es", "de", "it", "fr", "pt", "nl"]
PARTICLES = {"van", "von", "de", "da", "di", "der", "den", "del", "dos", "das", "do", "le", "la", "mac", "ten", "ter"}
CLUB_AFFIXES = r"\b(f\.?\s?c\.?|a\.?\s?f\.?\s?c\.?|c\.?\s?f\.?|s\.?\s?c\.?|s\.?\s?s\.?\s?c\.?|a\.?\s?c\.?|a\.?\s?s\.?|u\.?\s?s\.?|s\.?\s?s\.?|calcio|club|cfc|fk|sk|sv|vfb|vfl|tsv|bsc|1\.|\d{4})\b"


TRANSLIT = str.maketrans({"ø": "o", "Ø": "o", "æ": "ae", "Æ": "ae", "œ": "oe", "Œ": "oe", "ß": "ss", "ł": "l",
                          "Ł": "l", "đ": "d", "Đ": "d", "ð": "d", "þ": "th", "ı": "i", "’": "'"})
NATIONAL_TEAM = re.compile(r"\b(men'?s )?national (association )?(football|soccer) team\b", re.I)
# Common alternative names for countries that Wikidata's national-team items don't carry.
COUNTRY_ALIASES = {
    "Ivory Coast": ["Cote d'Ivoire", "Côte d'Ivoire"], "United States": ["USA", "US", "America", "USMNT"],
    "South Korea": ["Korea Republic", "Korea"], "North Korea": ["Korea DPR", "DPR Korea"],
    "DR Congo": ["Congo DR", "Zaire", "Democratic Republic of the Congo"], "Czech Republic": ["Czechia"],
    "Netherlands": ["Holland"], "Republic of Ireland": ["Ireland", "Eire"], "Turkey": ["Turkiye", "Türkiye"],
    "Iran": ["IR Iran"], "China": ["China PR"], "Cape Verde": ["Cabo Verde"], "Eswatini": ["Swaziland"],
    "Soviet Union": ["USSR", "CCCP"], "CIS": ["Commonwealth of Independent States"],
    "Serbia and Montenegro": ["FR Yugoslavia"], "United Arab Emirates": ["UAE"], "Bosnia and Herzegovina": ["Bosnia"],
    "Trinidad and Tobago": ["Trinidad"], "East Germany": ["GDR", "DDR"], "Germany": ["West Germany"],
}


def norm(s):
    s = unicodedata.normalize("NFKD", s.translate(TRANSLIT)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s.replace("&", " and "))
    return re.sub(r"\s+", " ", s).strip()


def wikidata_names(qids):
    out = {}
    qids = [q for q in qids if isinstance(q, str)]
    for i in range(0, len(qids), 50):
        d = _get("https://www.wikidata.org/w/api.php", {
            "action": "wbgetentities", "ids": "|".join(qids[i:i + 50]), "props": "labels|aliases",
            "languages": "|".join(LABEL_LANGS), "format": "json"})
        for q, e in d.get("entities", {}).items():
            names = {v["value"] for v in e.get("labels", {}).values()}
            names |= {a["value"] for a in e.get("aliases", {}).get("en", [])}
            out[q] = names
    return out


def humans(qids):
    qids = sorted({q for q in qids if isinstance(q, str)})
    out = set()
    for i in range(0, len(qids), 250):
        vals = " ".join(f"wd:{q}" for q in qids[i:i + 250])
        for b in sparql(f"SELECT ?item WHERE {{ VALUES ?item {{ {vals} }} ?item wdt:P31 wd:Q5 }}"):
            out.add(b["item"].rsplit("/", 1)[1])
    return out


def surname(name):
    toks = norm(re.sub(r"\(.*?\)", "", name)).split()
    if len(toks) < 2:
        return []
    out = [toks[-1]]
    j = len(toks) - 1
    while j > 1 and toks[j - 1] in PARTICLES:
        j -= 1
    if j < len(toks) - 1:
        out.append(" ".join(toks[j:]))
    return out


def club_core(name):
    core = norm(re.sub(CLUB_AFFIXES, " ", name, flags=re.I))
    return [core] if core and core != norm(name) and len(core) >= 3 else []


def useful(alias):
    """Drop junk like 'i m' / 'f c i m': keep compact codes (cr7, mufc) or anything with a 3+ letter word."""
    toks = alias.split()
    return len(alias) >= 2 and (len(toks) == 1 or any(len(t) >= 3 for t in toks))


def split_title(text):
    """'Name a X (fine print)' -> ('Name a X', 'fine print'); keeps short parentheticals inline."""
    m = re.match(r"^(.*?)\s*\((.{12,})\)\s*$", text)
    return (m.group(1), m.group(2)) if m else (text, "")


def main():
    prompts = [p for p in json.load(open(ROOT / "data" / "prompts.json", encoding="utf8"))
               if (ROOT / "data" / "answers" / f"{p['id']}.csv").exists()]
    frames = {p["id"]: pd.read_csv(ROOT / "data" / "answers" / f"{p['id']}.csv") for p in prompts}
    all_q = pd.concat(frames.values())["qid"].dropna().unique().tolist()
    print(f"fetching names for {len(all_q)} entities")
    wd = wikidata_names(all_q)
    people = humans(all_q)

    out_dir = ROOT / "web" / "data"
    pdir = out_dir / "p"
    pdir.mkdir(parents=True, exist_ok=True)
    index, global_names, written = [], set(), set()
    digest = hashlib.sha1()  # content version, appended to data URLs so browsers never mix stale files
    for p in prompts:
        df = frames[p["id"]]
        title, fine = split_title(p["text"])
        answers = []
        for r in df.itertuples():
            names = {r.answer, re.sub(r"\s*\(.*?\)\s*$", "", r.enwiki)}
            for part in re.findall(r"^(.*?)\s*\((.*?)\)$", r.answer):
                names |= set(part)
            names |= wd.get(r.qid, set())
            names |= set(COUNTRY_ALIASES.get(r.answer, []))
            names |= {NATIONAL_TEAM.sub(" ", n) for n in names}
            aliases = {norm(n) for n in names if n}
            if r.qid in people:
                aliases |= set(surname(r.answer)) | set(surname(r.enwiki))
            else:
                for n in list(names):
                    aliases |= set(club_core(n))
            aliases = sorted(a for a in aliases if useful(a))
            global_names.update(aliases)
            global_names.add(norm(r.answer))
            rec = {"n": r.answer, "t": [t[0] for t in TIERS].index(r.tier), "a": aliases}
            first = norm(r.answer).split()
            if r.qid in people and len(first) >= 2 and len(first[0]) >= 4:
                rec["fn"] = first[0]  # first name: only accepted when unique within the prompt
            answers.append(rec)
        # One small file per prompt, so a game only downloads the 7 prompts it plays.
        body = json.dumps({"id": p["id"], "ans": answers}, ensure_ascii=False, separators=(",", ":"))
        (pdir / f"{p['id']}.js").write_text(f"BallionData.add({body});\n", encoding="utf8")
        written.add(f"{p['id']}.js")
        digest.update(body.encode())
        index.append({"id": p["id"], "th": p.get("theme") or theme_of(p["id"]),
                      "g": p.get("family") or EXISTING_FAMILY.get(p["id"], p["id"]), "q": title, "f": fine, "n": len(answers)})
    for stale in pdir.glob("*.js"):
        if stale.name not in written:
            stale.unlink()

    tiers = [{"name": n, "pts": pts} for n, pts in TIERS]
    themes = [{"key": k, "name": name, "n": sum(1 for i in index if i["th"] == k)} for k, _, name in THEMES]
    js = "window.BALLION_INDEX = " + json.dumps({"v": digest.hexdigest()[:10], "tiers": tiers, "themes": themes, "prompts": index},
                                                 ensure_ascii=False, separators=(",", ":")) + ";\n"
    (out_dir / "index.js").write_text(js, encoding="utf8")
    # Every alias of every answer, so a correctly spelled name of some *other* entity is never
    # autocorrected into this prompt's answers. Loaded in the background; only typo handling uses it.
    names = "BallionData.names(" + json.dumps(sorted(global_names), ensure_ascii=False, separators=(",", ":")) + ");\n"
    (out_dir / "names.js").write_text(names, encoding="utf8")
    total = sum(f.stat().st_size for f in pdir.glob("*.js"))
    print(f"wrote {out_dir}: index {len(js) / 1e3:.0f} kB, names {len(names) / 1e3:.0f} kB, "
          f"{len(index)} prompt files {total / 1e6:.2f} MB, {sum(i['n'] for i in index)} answers")


if __name__ == "__main__":
    main()
