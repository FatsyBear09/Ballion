"""Prompt registry. Collector modules in prompts/collectors/ register prompts with @prompt.

A collector returns a list of dicts with keys:
  answer  - display name of the answer
  enwiki  - English Wikipedia article title (used for popularity + dedup)
  detail  - short human-readable evidence string (e.g. "117 goals (1996–2007)")

`family` tags sibling prompts that differ only by season/club/nationality (e.g. every
"<nationality> player in the PL since 2015–16" prompt shares one family); a game never
draws two prompts from the same family. Untagged prompts are their own family.
"""
from ballion.themes import EXISTING_FAMILY

PROMPTS = {}


def prompt(pid, text, source, family=None):
    def deco(fn):
        if pid in PROMPTS:
            raise ValueError(f"duplicate prompt id {pid}")
        fam = family or EXISTING_FAMILY.get(pid, pid)
        PROMPTS[pid] = {"id": pid, "text": text, "source": source, "family": fam, "collect": fn}
        return fn
    return deco
