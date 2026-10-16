# Learning

- 2026-10-16: A Google API client kept across a multi-minute sleep times out on the next call (stale
  HTTPS connection). Build a fresh service right before each write after a long wait.
- 2026-10-16: When a background script's output goes through `grep | tee`, lines can show up late even
  with -u. Don't treat a missing line as a hang; confirm against YouTube itself before acting.
- 2026-10-16: OAuth login must happen in the Chrome profile already signed in to the channel. A fresh
  profile hits a Google CAPTCHA, and the Chrome extension cannot drive accounts.google.com.
- 2026-10-16: Replies to viewer comments give only the link. No health advice in any reply (remedies,
  diet, ingredients, doctor referrals) unless Appu asks for it and it has been researched first, even
  when the landing page itself contains the answer.
