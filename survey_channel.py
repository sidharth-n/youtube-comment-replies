"""Read-only: ranks every channel video by comments still waiting for a reply."""
import collections
import json
import os

from replies import is_short
from yt import HERE, author_id, comment_threads, get_service, my_channel

yt = get_service()
me = my_channel(yt)
my_id, uploads = me["id"], me["contentDetails"]["relatedPlaylists"]["uploads"]

vids, token = [], None
while True:
    r = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50, pageToken=token).execute()
    vids += [i["contentDetails"]["videoId"] for i in r["items"]]
    token = r.get("nextPageToken")
    if not token:
        break

info = {}
for i in range(0, len(vids), 50):
    for v in yt.videos().list(part="snippet,statistics", id=",".join(vids[i:i + 50])).execute()["items"]:
        info[v["id"]] = v

configured = {v["video_id"] for v in json.load(open(os.path.join(HERE, "videos.json")))}
rows = []
for vid in vids:
    v = info[vid]
    total = int(v["statistics"].get("commentCount", 0))
    row = {"video_id": vid, "title": v["snippet"]["title"], "published": v["snippet"]["publishedAt"][:10],
           "views": int(v["statistics"].get("viewCount", 0)), "comments": total,
           "waiting_short": 0, "waiting_long": 0, "replied": 0, "top_words": [], "my_link": None,
           "configured": vid in configured}
    if total:
        words = collections.Counter()
        try:
            for t in comment_threads(yt, vid):
                top = t["snippet"]["topLevelComment"]
                if author_id(top) == my_id:
                    continue
                mine = [r for r in t["all_replies"] if author_id(r) == my_id]
                for r in mine:
                    for w in r["snippet"]["textOriginal"].split():
                        if w.startswith("http"):
                            row["my_link"] = w
                text = top["snippet"]["textDisplay"]
                if mine:
                    row["replied"] += 1
                elif is_short(text):
                    row["waiting_short"] += 1
                else:
                    row["waiting_long"] += 1
                if is_short(text):
                    words[text.strip().lower()[:20]] += 1
            row["top_words"] = words.most_common(4)
        except Exception as e:
            row["error"] = type(e).__name__
    rows.append(row)

rows.sort(key=lambda r: r["waiting_short"], reverse=True)
os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
json.dump(rows, open(os.path.join(HERE, "data", "channel_survey.json"), "w"), ensure_ascii=False, indent=2)
print(f"{len(rows)} videos on the channel\n")
for r in rows:
    print(f"{r['waiting_short']:4} waiting short | {r['waiting_long']:3} long | {r['replied']:3} replied | "
          f"{r['comments']:4} total | {r['views']:7} views | {r['published']} | {r['video_id']}"
          f"{' [ACTIVE]' if r['configured'] else ''}\n      {r['title'][:90]}\n      words: {r['top_words']}"
          f"{'  link: ' + r['my_link'] if r['my_link'] else ''}{'  ERR ' + r['error'] if r.get('error') else ''}")
