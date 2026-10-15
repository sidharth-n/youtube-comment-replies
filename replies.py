"""Builds a varied reply from phrases.json. Never returns a text already in `used`."""
import json
import os
import random

from yt import HERE

PHRASES = json.load(open(os.path.join(HERE, "phrases.json"), encoding="utf-8"))


MAX_WORDS = 3  # longer comments are left for Appu to answer by hand


def is_short(text):
    return len(text.split()) <= MAX_WORDS


def make_reply(link, used, recent_lines=(), rng=random):
    """recent_lines: link lines used in the last few replies, avoided so neighbours differ."""
    for _ in range(500):
        opening = rng.choice(PHRASES["openings"])
        line = rng.choice(PHRASES["link_lines"])
        if line in recent_lines:
            continue
        closing = rng.choice(PHRASES["closings"])
        head = f"{opening} {line}".strip() if opening else line
        if closing and rng.random() < 0.5:
            text = f"{head}\n{link}\n{closing}"      # closing after the link
        elif closing:
            text = f"{head} {closing}\n{link}"       # closing before the link
        else:
            text = f"{head}\n{link}"
        if text not in used:
            return text, line
    raise RuntimeError("Phrase bank exhausted: add more phrases to phrases.json")
