# Learning

- 2026-10-16: A Google API client kept across a multi-minute sleep times out on the next call (stale
  HTTPS connection). Build a fresh service right before each write after a long wait.
- 2026-10-16: When a background script's output goes through `grep | tee`, lines can show up late even
  with -u. Don't treat a missing line as a hang; confirm against YouTube itself before acting.
- 2026-10-16: OAuth login must happen in the Chrome profile already signed in to the channel. A fresh
  profile hits a Google CAPTCHA, and the Chrome extension cannot drive accounts.google.com.
