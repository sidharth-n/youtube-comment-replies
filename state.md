# YouTube comment replies State

_Last updated: 2026-10-16_

## Now
LIVE. GitHub Actions workflow "Reply to comments" (`.github/workflows/reply.yml`, branch master) runs
every 15 min, posts up to 3 replies/run with 1.5 to 5 min gaps, cap 190/day, quiet 11pm to 7am IST.
Videos in `videos.json`: r8-xJkmGneA (Bloated Belly, /vaidyar/vayar/), DFd4RXSJuSc (Stretch Marks,
/vaidyar/paadukal/). Last verified 2026-10-16 00:47 IST: manual run 38792642033 green, posted 1 reply.
6 replies posted in total; Appu confirmed the first is visible logged out. Queue then: 400 short, 12 long.

## Next
1. After 7am IST 2026-10-16: check the Actions page for green scheduled runs and spot-check 2 replies
   in incognito. Confirm the daily count climbs (runs log "sent today: N/190").
2. Add new videos as Appu sends them (video ID + landing page under https://ayurbook.com/vaidyar/).
3. If the phrase bank starts feeling repetitive, add phrases to `phrases.json` (about 1,350 combos now).

## Blockers
- None.

## Latest handoff, 2026-10-16
What shipped (all committed and pushed, last commit before this handoff a28f2fa):
- `yt.py` login helper (scope youtube.force-ssl, token.json), `list_comments.py` read-only test,
  `survey_channel.py` ranks all channel videos by waiting comments.
- `phrases.json` Malayalam phrase bank (Appu approved) + `replies.py` (unique text, no repeat of the
  middle line within 3 replies, MAX_WORDS = 3 → longer comments left for Appu).
- `post_replies.py`: stateless (reads replied-to people, used texts and today's count from YouTube),
  newest first, fresh API connection before each reply, stops after 2 failures.
- GitHub secret `YT_TOKEN_JSON` = token.json (contains refresh token + client id/secret).
- Google Cloud project youtube-comment-replies-511718, OAuth app published (In production), no billing.
Key decisions: no Claude API (phrase bank), no Google server (GitHub Actions, public repo), reply to
every short comment, skip compliment-only videos (Pimple, Dark Circles, Dandruff), 190/day cap.
Useful commands: `.venv/bin/python -W ignore post_replies.py --max 5 --dry-run --ignore-quiet-hours`,
`gh workflow run reply.yml -f max=1 -f ignore_quiet_hours=true`, `gh run list --workflow reply.yml`.
Login lives in the Ravichandran Chrome profile (extension "Browser 1"); re-login steps in
docs/runbooks/add-a-video.md. Open issue: 0001 (schedule pauses after 60 days with no commit).
