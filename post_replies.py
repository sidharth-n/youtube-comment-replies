"""Posts link replies to short comments on the videos in videos.json.

Stateless on purpose (GitHub Actions keeps no files between runs): who has been replied to, which
texts were used and how many replies went out today are all worked out from YouTube itself.

  python post_replies.py --max 5 --dry-run   # show what would be posted
  python post_replies.py --max 5             # post for real
"""
import argparse
import datetime as dt
import json
import os
import random
import sys
import time

from googleapiclient.errors import HttpError

from replies import is_short, make_reply
from yt import HERE, author_id, comment_threads, get_service, my_channel

DAILY_CAP = 190                      # free API quota is 10,000 units/day, a reply costs 50
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
QUIET_START, QUIET_END = 23, 7       # no replies 11pm to 7am India time
MAX_FAILURES = 2                     # stop the run after this many rejected replies


def now_ist():
    return dt.datetime.now(IST)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=5, help="most replies this run")
    ap.add_argument("--min-gap", type=float, default=2, help="minutes")
    ap.add_argument("--max-gap", type=float, default=8, help="minutes")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ignore-quiet-hours", action="store_true")
    a = ap.parse_args()

    if not a.ignore_quiet_hours and (now_ist().hour >= QUIET_START or now_ist().hour < QUIET_END):
        print(f"Quiet hours ({now_ist():%H:%M} IST). Nothing to do.")
        return 0

    yt = get_service()
    my_id = my_channel(yt)["id"]
    today = now_ist().date()

    used, todo, manual, sent_today = set(), [], [], 0
    for v in json.load(open(os.path.join(HERE, "videos.json"))):
        for t in comment_threads(yt, v["video_id"]):
            top = t["snippet"]["topLevelComment"]
            mine = [r for r in t["all_replies"] if author_id(r) == my_id]
            for r in mine:
                used.add(r["snippet"]["textOriginal"])
                published = dt.datetime.fromisoformat(r["snippet"]["publishedAt"].replace("Z", "+00:00"))
                if published.astimezone(IST).date() == today:
                    sent_today += 1
            if author_id(top) == my_id or mine:
                continue
            text = top["snippet"]["textDisplay"]
            item = {"thread": t["id"], "author": top["snippet"]["authorDisplayName"], "text": text,
                    "published": top["snippet"]["publishedAt"], "link": v["link"]}
            (todo if is_short(text) else manual).append(item)

    todo.sort(key=lambda c: c["published"], reverse=True)  # newest first
    budget = max(0, min(a.max, DAILY_CAP - sent_today))
    print(f"{now_ist():%Y-%m-%d %H:%M} IST | waiting: {len(todo)} short, {len(manual)} long (for Appu) | "
          f"sent today: {sent_today}/{DAILY_CAP} | this run: {min(budget, len(todo))}")
    if manual:
        print("Long comments for Appu to answer:")
        for c in manual:
            print(f"  {c['author']}: {c['text'][:100]!r}")

    recent, failures, posted = [], 0, 0
    for c in todo[:budget]:
        text, line = make_reply(c["link"], used, recent)
        recent = (recent + [line])[-3:]
        print(f"\n-> {c['author']}: {c['text']!r}\n   " + text.replace("\n", "\n   "))
        if a.dry_run:
            used.add(text)
            continue
        try:
            yt.comments().insert(part="snippet", body={
                "snippet": {"parentId": c["thread"], "textOriginal": text}}).execute()
            used.add(text)
            posted += 1
            print(f"   POSTED {now_ist():%H:%M:%S}")
        except HttpError as e:
            failures += 1
            print(f"   REJECTED by YouTube: {e.status_code} {e.reason}")
            if failures >= MAX_FAILURES:
                print("Too many rejections. Stopping so the channel is not flagged.")
                return 1
        if posted < budget and c is not todo[:budget][-1]:
            gap = random.uniform(a.min_gap, a.max_gap)
            print(f"   waiting {gap:.1f} min")
            time.sleep(gap * 60)

    print(f"\nDone. Posted {posted}{' (dry run)' if a.dry_run else ''}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
