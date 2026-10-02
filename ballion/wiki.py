"""Thin Wikipedia / Wikimedia API helpers with on-disk caching."""
import hashlib
import json
import threading
import time
from pathlib import Path

import requests

UA = "Ballion/0.1 (football quiz research prototype; https://github.com/FatsyBear09/Ballion)"
CACHE = Path(__file__).resolve().parent.parent / "data" / "raw" / "cache"
CACHE.mkdir(parents=True, exist_ok=True)

_session = requests.Session()
_session.headers["User-Agent"] = UA

# Shared throttle across threads: at most MAX_RPS uncached requests/second, and a 429
# pauses every thread until its Retry-After has passed.
MAX_RPS = 5
_lock = threading.Lock()
_next_slot = 0.0


def _wait_turn():
    global _next_slot
    with _lock:
        now = time.monotonic()
        slot = max(now, _next_slot)
        _next_slot = slot + 1 / MAX_RPS
    time.sleep(max(0.0, slot - time.monotonic()))


def _back_off(seconds):
    global _next_slot
    with _lock:
        _next_slot = max(_next_slot, time.monotonic() + seconds)


def _get(url, params=None, retries=8):
    key = hashlib.sha1((url + json.dumps(params, sort_keys=True)).encode()).hexdigest()
    path = CACHE / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text())
    for attempt in range(retries):
        _wait_turn()
        r = _session.get(url, params=params, timeout=30)
        if r.status_code == 429 or r.status_code >= 500:
            _back_off(float(r.headers.get("Retry-After", 0) or 0) or min(60, 2 ** attempt))
            continue
        if r.status_code == 404:
            data = None
            break
        r.raise_for_status()
        data = r.json()
        break
    else:
        r.raise_for_status()
    path.write_text(json.dumps(data))
    return data


def api(lang="en", **params):
    params = {"format": "json", "formatversion": 2, **params}
    return _get(f"https://{lang}.wikipedia.org/w/api.php", params)


def page_html(title, lang="en"):
    """Rendered HTML of an article (follows redirects)."""
    return api(lang, action="parse", page=title, prop="text", redirects=1)["parse"]["text"]


def resolve(titles, lang="en"):
    """Map titles -> {canonical title, wikidata qid, {lang: title} langlinks}. Batches of 50."""
    out = {}
    titles = list(dict.fromkeys(titles))
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        cont = {}
        while True:
            d = api(lang, action="query", titles="|".join(chunk), redirects=1,
                    prop="pageprops|langlinks", ppprop="wikibase_item", lllimit="max", **cont)
            q = d["query"]
            alias = {}
            for k in ("normalized", "redirects"):
                for m in q.get(k, []):
                    alias[m["from"]] = m["to"]
            for p in q["pages"]:
                rec = out.setdefault(p["title"], {"title": p["title"], "missing": p.get("missing", False),
                                                  "qid": p.get("pageprops", {}).get("wikibase_item"),
                                                  "langlinks": {}})
                for ll in p.get("langlinks", []):
                    rec["langlinks"][ll["lang"]] = ll["title"]
            for t in chunk:
                c = t
                while c in alias:
                    c = alias[c]
                out[t] = out.get(c, {"title": c, "missing": True, "qid": None, "langlinks": {}})
            if "continue" in d:
                cont = {k: v for k, v in d["continue"].items()}
            else:
                break
    return out


def monthly_views(title, lang, start="20251001", end="20260930"):
    t = title.replace(" ", "_")
    url = (f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{lang}.wikipedia/"
           f"all-access/user/{requests.utils.quote(t, safe='')}/monthly/{start}00/{end}00")
    d = _get(url)
    return sum(i["views"] for i in d["items"]) if d else 0
