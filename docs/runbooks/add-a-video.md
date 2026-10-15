# Add a new video (from phone or laptop)

1. Open https://github.com/sidharth-n/youtube-comment-replies/blob/master/videos.json
2. Tap the pencil (Edit) icon.
3. Copy one existing block and paste it before the last `]`, adding a comma after the previous `}`:

```json
  {
    "video_id": "PASTE_ID",
    "title": "Short name, any text",
    "link": "https://ayurbook.com/vaidyar/PAGE/"
  }
```

   The video ID is the part after `/shorts/` or `watch?v=` in the YouTube link, without `?si=...`.
   Example: `https://youtube.com/shorts/r8-xJkmGneA?si=abc` → `r8-xJkmGneA`.
4. Tap **Commit changes**. The next run (within 15 minutes, 7am to 11pm IST) picks it up.

Only add videos where viewers are asked to comment for a link. Leave compliment-only videos out.

# Check it is working
- Runs: https://github.com/sidharth-n/youtube-comment-replies/actions (green tick = fine, red = look).
- Long comments to answer by hand: YouTube Studio → Comments → filter "I haven't responded".

# If YouTube login stops working (red runs saying invalid_grant)
On the laptop: delete token.json, run `.venv/bin/python list_comments.py`, log in as Ravichandran
in the Ravichandran Chrome profile, then `gh secret set YT_TOKEN_JSON < token.json`.
