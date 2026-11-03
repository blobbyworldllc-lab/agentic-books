import os
import json
import requests
import subprocess
from pathlib import Path

# Get Account 2 token from environment
cmd = '[System.Environment]::GetEnvironmentVariable("BUFFER_API_KEY_ACCOUNT_2", "User")'
token = subprocess.check_output(["powershell", "-Command", cmd]).decode().strip()

# Target channels on Account 2:
tiktok_channel_id = "6ae93063e29c69a1714262e1"
twitter_channel_id = "6ae92fcae29c69a171425f5b"

# Public video asset for TikTok
video_url = "https://raw.githubusercontent.com/blobbyworldllc-lab/agentic-books/main/Book_1/pips-christmas-countdown/output/marketing/shorts/pip_countdown_day_01.mp4"
cover_url = "https://blobbyworldllc-lab.github.io/agentic-books/cover.jpg"

mutation = """mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess {
      post {
        id
        status
      }
    }
    ... on MutationError {
      message
    }
    ... on InvalidInputError {
      message
    }
  }
}"""

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 1. Post to TikTok
print("Queueing to TikTok...")
tiktok_text = """Pip's Christmas Countdown is LIVE on Amazon! 🎄⭐

Day 1 of 25: Can you find Little Star hiding in this picture?
Follow Pip the puppy across 25 daily rhyming holiday coloring pages!

👉 Grab the paperback on Amazon: https://www.amazon.com/dp/B0HPZ647J6
🎁 Download the FREE 4-page coloring pack: https://blobbyworldllc-lab.github.io/agentic-books/

#PipsChristmasCountdown #KidsColoringBook #ChristmasForKids #ToddlerBooks #ChristmasCountdown #HolidayActivities"""

var_tiktok = {
    'input': {
        'channelId': tiktok_channel_id,
        'text': tiktok_text,
        'mode': 'addToQueue',
        'schedulingType': 'automatic',
        'assets': [
            {
                'video': {
                    'url': video_url
                }
            }
        ]
    }
}
r_tt = requests.post("https://api.buffer.com/graphql", json={"query": mutation, "variables": var_tiktok}, headers=headers)
print("TikTok Dispatch Result:", json.dumps(r_tt.json(), indent=2))
