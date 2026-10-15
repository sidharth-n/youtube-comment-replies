"""Step 3 preview: shows sample replies for real waiting comments. Posts nothing."""
import json
import os
import sys

from replies import PHRASES, is_short, make_reply
from yt import HERE

n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
data = json.load(open(os.path.join(HERE, "data", "step2_readonly.json"), encoding="utf-8"))
link = json.load(open(os.path.join(HERE, "videos.json")))[0]["link"]
waiting = [c for c in data["videos"][0]["comments"] if c["would_reply"]]
todo = [c for c in waiting if is_short(c["text"])]
manual = [c for c in waiting if not is_short(c["text"])]
print(f"Waiting: {len(waiting)} | auto-reply: {len(todo)} | left for you: {len(manual)}\n")
for c in manual:
    print(f"  FOR YOU  {c['author']}: {c['text'][:90]!r}")
print()
todo.sort(key=lambda c: c["published"], reverse=True)  # newest first

used = set(data["my_past_replies"])
recent = []
for c in todo[:n]:
    text, line = make_reply(link, used, recent)
    used.add(text)
    recent = (recent + [line])[-3:]
    print(f"COMMENT  {c['author']}: {c['text'][:70]!r}\nREPLY    " + text.replace("\n", "\n         ") + "\n")

# How many distinct replies the bank can produce (2 positions for a non-empty closing).
o, l, cl = (len(set(PHRASES[k])) for k in ("openings", "link_lines", "closings"))
print(f"Distinct replies possible: about {o * l * (2 * (cl - 1) + 1)}")
