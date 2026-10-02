"""Cached Wikidata SPARQL queries."""
from ballion.wiki import _get

ENDPOINT = "https://query.wikidata.org/sparql"


def sparql(query):
    """Return result bindings as a list of {var: value} dicts."""
    d = _get(ENDPOINT, {"query": query, "format": "json"})
    return [{k: v["value"] for k, v in b.items()} for b in d["results"]["bindings"]]


def enwiki_title(url):
    """https://en.wikipedia.org/wiki/Foo_Bar -> 'Foo Bar'."""
    from urllib.parse import unquote
    return unquote(url.rsplit("/wiki/", 1)[1]).replace("_", " ")
