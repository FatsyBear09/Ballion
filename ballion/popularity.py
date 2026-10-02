"""Popularity proxy: Wikipedia user pageviews over the last 60 days, summed across major language editions.

Uses the batched action-API `prop=pageviews` (50 titles/request) rather than the per-article REST
endpoint: ~50x fewer requests. On p002/p003 the 60-day ranking matched the 12-month one with
Spearman 0.98-0.99 and no answer moved more than one tier.
"""
from ballion.wiki import api, resolve

LANGS = ["en", "es", "de", "it", "fr", "pt", "nl", "ru", "pl", "tr", "ar", "ja", "zh", "id"]


def batch_views(titles, lang):
    """title -> summed daily views over the last 60 days (follows API continuation)."""
    out = {}
    titles = sorted(set(titles))
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        alias, cont = {}, {}
        while True:
            d = api(lang, action="query", prop="pageviews", titles="|".join(chunk), redirects=1, **cont)
            q = d["query"]
            for k in ("normalized", "redirects"):
                for m in q.get(k, []):
                    alias[m["from"]] = m["to"]
            for p in q["pages"]:
                if "pageviews" in p:
                    out[p["title"]] = out.get(p["title"], 0) + sum(v or 0 for v in p["pageviews"].values())
            if "continue" not in d:
                break
            cont = d["continue"]
        for t in chunk:
            c = t
            while c in alias:
                c = alias[c]
            if t != c:
                out[t] = out.get(c, 0)
    return out


def popularity(en_titles):
    """en title -> {title, qid, views, views_en, n_langs}."""
    info = resolve(en_titles)
    out = {t: {"title": info[t]["title"], "qid": info[t]["qid"], "views": 0, "views_en": 0, "n_langs": 0}
           for t in en_titles}
    for lang in LANGS:
        local = {}
        for t in en_titles:
            rec = info[t]
            if rec["missing"]:
                continue
            lt = rec["title"] if lang == "en" else rec["langlinks"].get(lang)
            if lt:
                local[t] = lt
        views = batch_views(local.values(), lang)
        for t, lt in local.items():
            v = views.get(lt, 0)
            out[t]["views"] += v
            out[t]["n_langs"] += 1
            if lang == "en":
                out[t]["views_en"] = v
    return out
