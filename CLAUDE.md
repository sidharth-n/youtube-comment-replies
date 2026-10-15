# YouTube comment replies (Ravichandran channel)

## What this is
Appu's channel "Ravichandran" (AI content creator) asks viewers to comment a keyword to get a link.
YouTube has no auto-DM, so this script watches comments on each configured video, finds ones with
that video's keyword, and replies with the video's link. Replies must read like a human wrote them:
every reply worded differently (assembled from a pre-written phrase bank, never the same text twice), posted at random intervals, with daily caps
so the channel is never flagged as spam.

## Links
- All landing pages live under https://ayurbook.com/vaidyar/ (one page per video, e.g. `/vaidyar/vayar/`).
- Only videos where viewers are asked to comment for a link go in `videos.json`. Compliment-only
  videos are left alone (Appu, 2026-10-16).

## Stack
- Python 3.10+
- YouTube Data API v3 (OAuth as the channel) for reading comments and posting replies
- No LLM at runtime: reply text comes from a phrase bank written in advance
- Runs on GitHub Actions on a schedule (public repo, so Actions minutes are free).
  Google Cloud is used only for the YouTube API login, with no billing or server.

## Commands
- (filled in once built)

## Safety rules
- Auto-reply only when the comment is 3 words or fewer (`replies.MAX_WORDS`). Longer
  comments go to a list for Appu to answer by hand.
- Never post the same reply text twice. Never reply twice to the same person on the same video.
- Random delay (about 2 to 8 min) between replies, quiet hours at night, daily cap 190
  (Appu wants no waiting; 190 is the ceiling of the free 10,000 unit/day API quota).
- If YouTube rejects or hides replies, stop and alert; never retry in a tight loop.
- Secrets (`.env`, `client_secret.json`, `token.json`) are gitignored, chmod 600, never in chat.
  This repo is PUBLIC: on GitHub, secrets live only in encrypted Actions Secrets.

## Conventions
- Micro-commits; never break the previously-working state (see global CLAUDE.md).
- File tangents, ideas and bugs as issues in `issues/`.
