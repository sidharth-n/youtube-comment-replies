# State

## Now
Step 1 of 5 DONE: repo (public), Google Cloud project youtube-comment-replies-511718, YouTube Data API v3 enabled, OAuth app published (In production), Desktop client_secret.json in place (gitignored, chmod 600).

## Next
Step 2: read-only test that lists keyword-matching comments on one video.

## Blockers
- Need from Appu for step 2: test video link + keyword + landing page link, 2 to 3 sample replies in his own tone.

## Latest handoff
2026-10-15: plan approved (API route, Haiku replies, random timing, Google Cloud e2-micro). Scaffold done.
2026-10-15: dropped Claude Haiku. Appu: most comments are a single prompted word; he replies to long ones by hand. Replies come from a phrase bank.
2026-10-15: dropped the Google Cloud server (needs a card, bill risk after trial). Runs on GitHub Actions; repo made public for unlimited free minutes.
