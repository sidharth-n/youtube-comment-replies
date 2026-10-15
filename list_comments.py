"""Step 2 read-only test. Lists comments and which ones still need a reply. Posts nothing."""
import json
import os

from yt import HERE, author_id, comment_threads, get_service, my_channel

yt = get_service()
me = my_channel(yt)
my_id = me["id"]
print(f"Logged in as channel: {me['snippet']['title']} ({my_id})\n")

out = {"channel": me["snippet"]["title"], "videos": [], "recent_titles": [], "my_past_replies": []}

# Recent uploads and the channel's own past replies, to learn the tone.
uploads = me["contentDetails"]["relatedPlaylists"]["uploads"]
items = yt.playlistItems().list(part="snippet", playlistId=uploads, maxResults=15).execute()["items"]
for it in items:
    vid = it["snippet"]["resourceId"]["videoId"]
    out["recent_titles"].append({"video_id": vid, "title": it["snippet"]["title"],
                                 "description": it["snippet"]["description"][:500]})
    try:
        for t in comment_threads(yt, vid):
            for r in t["all_replies"]:
                if author_id(r) == my_id:
                    out["my_past_replies"].append(r["snippet"]["textDisplay"])
    except Exception as e:  # comments disabled on some videos
        print(f"  (skipped comments on {vid}: {type(e).__name__})")

# The configured test videos.
for v in json.load(open(os.path.join(HERE, "videos.json"))):
    rows = []
    for t in comment_threads(yt, v["video_id"]):
        top = t["snippet"]["topLevelComment"]
        mine = author_id(top) == my_id
        replied = any(author_id(r) == my_id for r in t["all_replies"])
        rows.append({"author": top["snippet"]["authorDisplayName"],
                     "text": top["snippet"]["textDisplay"],
                     "published": top["snippet"]["publishedAt"],
                     "own_comment": mine, "already_replied": replied,
                     "would_reply": not mine and not replied})
    out["videos"].append({"video_id": v["video_id"], "comments": rows})
    todo = sum(r["would_reply"] for r in rows)
    print(f"Video {v['video_id']}: {len(rows)} comments, {todo} would get a reply\n")
    for r in rows:
        flag = "REPLY" if r["would_reply"] else ("own" if r["own_comment"] else "done")
        print(f"  [{flag:5}] {r['author']}: {r['text'][:80]!r}")

print(f"\nRecent videos read: {len(out['recent_titles'])}, past replies by you found: {len(out['my_past_replies'])}")
os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
path = os.path.join(HERE, "data", "step2_readonly.json")
json.dump(out, open(path, "w"), ensure_ascii=False, indent=2)
print(f"Full results saved to {path}")
