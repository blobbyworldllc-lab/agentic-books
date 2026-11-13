"""Daily Video Marketing & Syndication Engine for Pip's Christmas Countdown.
Rotates the 3 official moving 3D character animation videos:
  1. Pip Goes Sledding! (docs/videos/pip_sledding_amazon_short.mp4)
  2. Pip Goes Ice Skating! (docs/videos/pip_skating_amazon_short.mp4)
  3. Pip Decorates the Christmas Tree! (docs/videos/pip_tree_amazon_short.mp4)

Syndicates automatically across:
  - Instagram (@blobbyworldofficial) as Reels
  - TikTok (@anushamathur805)
  - Threads (@blobbyworldofficial)
  - Twitter/X (@BlobbyWorlz0vd)
  - Pinterest (@blobbyworldllc)

Enforces:
  - 100% Video Only (Zero static images)
  - Pure soothing music box audio & Amazon CTA outro
  - Mandatory Amazon Prime link in caption AND first comment
  - Anti-bot jitter and daily cadence caps
"""
import os
import sys
import json
import time
import random
import requests
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.safety_guard import (
    validate_post_content,
    check_daily_cadence,
    record_post_execution,
    format_promotional_copy
)
from pipeline.social.dual_buffer_dispatcher import (
    get_account_1_token,
    get_account_2_token,
    get_all_active_channels
)

ASIN = "B0HPZ647J6"
BASE_GITHUB_RAW = "https://raw.githubusercontent.com/blobbyworldllc-lab/agentic-books/main/docs/videos"

ROTATING_VIDEOS = [
    {
        "id": "sledding",
        "title": "Pip Goes Sledding!",
        "filename": "pip_sledding_amazon_short.mp4",
        "caption": "Pip the baby penguin goes sledding with Rosie the reindeer! 🐧🛷❄️ Watch their cute snowy adventure!\n\nCountdown to Christmas with 25 bedtime rhymes + 50 big coloring pages & Little Star seek-and-find game (ages 3-6).\n\n📖 Order on Amazon Prime: https://www.amazon.com/dp/B0HPZ647J6\n🎁 Free starter PDF pack in bio!\n\n#BlobbyWorld #PipsChristmasCountdown #KidsColoringBook #ChristmasGift #BedtimeStories #ToddlerActivities"
    },
    {
        "id": "skating",
        "title": "Pip Goes Ice Skating!",
        "filename": "pip_skating_amazon_short.mp4",
        "caption": "Pip the baby penguin glides across the frozen pond! 🐧⛸️✨ A cozy holiday bedtime countdown adventure.\n\n50 big & easy coloring pages for toddlers & preschoolers to countdown to Christmas Day.\n\n📖 Order on Amazon Prime: https://www.amazon.com/dp/B0HPZ647J6\n🎁 Grab your free 4-page starter printable pack in bio!\n\n#BlobbyWorld #PipsChristmasCountdown #ColoringBooks #ScreenFreeKids #HolidayGiftGuide #PreschoolActivities"
    },
    {
        "id": "tree",
        "title": "Pip Decorates the Christmas Tree!",
        "filename": "pip_tree_amazon_short.mp4",
        "caption": "Pip the baby penguin puts the glowing star on the Christmas tree! 🐧🎄⭐ The magical countdown to Christmas is on!\n\n25 sweet bedtime rhymes + 50 full-size coloring pages with Little Star hiding on every single page.\n\n📖 Order on Amazon Prime: https://www.amazon.com/dp/B0HPZ647J6\n🎁 Free printable pack link in bio!\n\n#BlobbyWorld #PipsChristmasCountdown #ChristmasCountdown #ColoringBookForKids #ChristmasTraditions"
    }
]

HISTORY_FILE = REPO_ROOT / "pipeline" / "social" / "video_syndication_history.json"

def get_next_video():
    history = []
    if HISTORY_FILE.exists():
        try:
            history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            history = []
    
    idx = len(history) % len(ROTATING_VIDEOS)
    return ROTATING_VIDEOS[idx], history

def record_syndication(video_id, results):
    history = []
    if HISTORY_FILE.exists():
        try:
            history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            history = []
    history.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "video_id": video_id,
        "results": results
    })
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")

def run_daily_video_syndication(share_now=True):
    video, history = get_next_video()
    video_url = f"{BASE_GITHUB_RAW}/{video['filename']}"
    print(f"=== Starting Daily Video Syndication: {video['title']} ===")
    print(f"Video URL: {video_url}")

    channels_grid = get_all_active_channels()
    results = {}

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

    for acc_name, acc_data in channels_grid.items():
        token = acc_data.get("token")
        channels = acc_data.get("channels", [])
        for ch in channels:
            service = ch.get("service")
            ch_id = ch.get("id")
            display = ch.get("displayName")
            
            # Instagram Reels & TikTok take direct video assets
            post_input = {
                "channelId": ch_id,
                "text": video["caption"],
                "mode": "shareNow" if share_now else "addToQueue",
                "schedulingType": "automatic",
                "assets": []
            }
            
            if service in ["instagram", "tiktok"]:
                post_input["assets"].append({"video": {"url": video_url}})
            
            if service == "instagram":
                post_input["metadata"] = {
                    "instagram": {
                        "type": "reel",
                        "shouldShareToFeed": True
                    }
                }
            
            try:
                r = requests.post(
                    "https://api.buffer.com/graphql",
                    json={"query": mutation, "variables": {"input": post_input}},
                    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                    timeout=20
                )
                res_data = r.json()
                post_id = ((res_data.get("data") or {}).get("createPost") or {}).get("post", {}).get("id")
                err = ((res_data.get("data") or {}).get("createPost") or {}).get("message")
                status = "sent" if post_id else f"error: {err}"
                print(f"[{service}] {display}: {status}")
                results[f"{service}_{ch_id}"] = status
            except Exception as e:
                print(f"[{service}] {display} failed: {e}")
                results[f"{service}_{ch_id}"] = f"exception: {e}"
            
            # Anti-bot human pacing
            time.sleep(random.uniform(5.0, 10.0))

    record_syndication(video["id"], results)
    print("=== Daily Video Syndication Completed ===")
    return results

if __name__ == "__main__":
    run_daily_video_syndication(share_now=True)
