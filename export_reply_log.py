"""Writes data/reply_log.csv: every reply the channel has posted, with the comment it answered.

Read-only. Rebuilt from YouTube each time, so it always matches what is actually posted.
data/ is gitignored, so viewers' names and comments never reach the public repo.

  python export_reply_log.py
"""
import csv
import datetime as dt
import json
import os

from replies import is_short
from yt import HERE, author_id, comment_threads, get_service, my_channel

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
OUT = os.path.join(HERE, "data", "reply_log.csv")


def ist(stamp):
    return dt.datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone(IST).strftime("%Y-%m-%d %H:%M")


def main():
    yt = get_service()
    my_id = my_channel(yt)["id"]
    rows = []
    for v in json.load(open(os.path.join(HERE, "videos.json"))):
        for t in comment_threads(yt, v["video_id"]):
            top = t["snippet"]["topLevelComment"]["snippet"]
            for r in t["all_replies"]:
                if author_id(r) != my_id:
                    continue
                rows.append({
                    "posted_ist": ist(r["snippet"]["publishedAt"]),
                    "video": v["title"],
                    "commenter": top["authorDisplayName"],
                    "comment": top["textDisplay"],
                    "comment_ist": ist(top["publishedAt"]),
                    "our_reply": r["snippet"]["textOriginal"],
                    "type": "auto" if is_short(top["textDisplay"]) else "hand-written",
                    "link": f"https://www.youtube.com/watch?v={v['video_id']}&lc={r['id']}",
                })
    rows.sort(key=lambda x: x["posted_ist"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:  # utf-8-sig so Excel shows Malayalam
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["posted_ist"])
        w.writeheader()
        w.writerows(rows)
    by_type = {k: sum(r["type"] == k for r in rows) for k in ("auto", "hand-written")}
    print(f"Wrote {len(rows)} replies to {OUT} ({by_type['auto']} auto, {by_type['hand-written']} hand-written)")


if __name__ == "__main__":
    main()
