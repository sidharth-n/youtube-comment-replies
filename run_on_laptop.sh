#!/usr/bin/env bash
# Posts replies from this laptop in a loop, instead of GitHub Actions.
# Pause the GitHub workflow first (gh workflow disable reply.yml) so the two never reply to the same comment.
# Start:  nohup setsid ./run_on_laptop.sh >> /tmp/laptop_replies.log 2>&1 &
# Stop:   pkill -f run_on_laptop.sh
cd "$(dirname "$0")"
while true; do
  if [ "$(gh api repos/sidharth-n/youtube-comment-replies/actions/workflows/reply.yml --jq .state 2>/dev/null)" = "active" ]; then
    echo "$(date '+%F %H:%M') GitHub workflow is active again. Stopping so the two don't overlap."; exit 0
  fi
  .venv/bin/python -W ignore -u post_replies.py --max 5 --min-gap 2 --max-gap 8
  if [ $? -ne 0 ]; then echo "$(date '+%F %H:%M') Poster reported rejections. Stopping."; exit 1; fi
  wait=$(( 180 + RANDOM % 300 ))   # 3 to 8 min between rounds
  echo "$(date '+%F %H:%M') next round in $((wait / 60)) min"; sleep $wait
done
