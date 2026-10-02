"""Prompt registry. Collector modules in prompts/collectors/ register prompts with @prompt.

A collector returns a list of dicts with keys:
  answer  - display name of the answer
  enwiki  - English Wikipedia article title (used for popularity + dedup)
  detail  - short human-readable evidence string (e.g. "117 goals (1996–2007)")
"""
PROMPTS = {}


def prompt(pid, text, source):
    def deco(fn):
        if pid in PROMPTS:
            raise ValueError(f"duplicate prompt id {pid}")
        PROMPTS[pid] = {"id": pid, "text": text, "source": source, "collect": fn}
        return fn
    return deco
