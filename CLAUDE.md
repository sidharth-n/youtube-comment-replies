# YouTube comment replies (Ravichandran channel)

## What this is
Appu's channel "Ravichandran" (AI content creator) asks viewers to comment a keyword to get a link.
YouTube has no auto-DM, so this script watches comments on each configured video, finds ones with
that video's keyword, and replies with the video's link. Replies must read like a human wrote them:
every reply worded differently (assembled from a pre-written phrase bank, never the same text twice), posted at random intervals, with daily caps
so the channel is never flagged as spam.

## Stack
- Python 3.10+
- YouTube Data API v3 (OAuth as the channel) for reading comments and posting replies
- No LLM at runtime: reply text comes from a phrase bank written in advance
- Runs on a Google Cloud free-tier e2-micro server

## Commands
- (filled in once built)

## Safety rules
- Auto-reply only when the comment is basically just the keyword (a few words at most). Longer
  comments go to a list for Appu to answer by hand.
- Never post the same reply text twice. Never reply twice to the same person on the same video.
- Random delay between replies, quiet hours at night, daily cap (start at 25).
- If YouTube rejects or hides replies, stop and alert; never retry in a tight loop.
- Secrets (`.env`, `client_secret.json`, `token.json`) are gitignored, chmod 600, never in chat.

## Conventions
- Micro-commits; never break the previously-working state (see global CLAUDE.md).
- File tangents, ideas and bugs as issues in `issues/`.
