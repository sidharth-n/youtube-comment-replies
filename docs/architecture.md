# Architecture

Poll loop: YouTube commentThreads.list per configured video -> keyword match -> skip already-replied
-> Claude Haiku writes reply -> comments.insert -> random sleep -> repeat. State in data/ (who got a
reply, daily count). Quota: comments.insert = 50 units, 10,000 units/day free.

Hosting: GitHub Actions cron (public repo). Each run handles a small batch with random gaps, then exits.
