"""
Amazon Video & Visual Listing Automation Engine
Handles:
1. Continuous monitoring of Amazon Product Page (B0HPZ647J6) for Videos & A+ Content.
2. Autonomous Creator / Influencer Seeding for "Videos for this product" placement.
3. Automated multi-platform video promotion syndication linking directly to Amazon.
"""
import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

ASIN = "B0HPZ647J6"
AMAZON_URL = f"https://www.amazon.com/dp/{ASIN}"
FREE_PACK_URL = "https://blobbyworldllc-lab.github.io/agentic-books/"
HISTORY_FILE = REPO_ROOT / "pipeline" / "growth" / "amazon_video_history.json"

CREATOR_TARGETS = [
    {
        "platform": "YouTube / Shorts",
        "niche": "Toddler Bedtime Stories & Coloring",
        "action": "Syndicate 3D animated trailer with Amazon purchase outro",
        "status": "active"
    },
    {
        "platform": "Pinterest Video Pins",
        "niche": "Preschool Christmas Activities",
        "action": "Distribute video pins pointing directly to Amazon ASIN B0HPZ647J6",
        "status": "active"
    },
    {
        "platform": "Amazon Influencer / Reviewer Seeding",
        "niche": "Children's Book Reviewers",
        "action": "Seed review copies & printable packs for customer video placement",
        "status": "staged"
    }
]

def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"last_checked": None, "video_count": 0, "aplus_live": False, "events": []}

def save_history(data):
    HISTORY_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def check_listing_visuals():
    """Check Amazon listing for live videos and A+ content."""
    from pipeline.stealth_browser.stealth_engine import StealthBrowserEngine, human_delay
    
    print(f"[{datetime.now().isoformat()}] Scanning {AMAZON_URL} for live videos and A+ Content...")
    history = load_history()
    
    with StealthBrowserEngine(profile_name="amazon_monitor", headless=True) as engine:
        page = engine.page
        page.goto(AMAZON_URL, wait_until="domcontentloaded", timeout=45000)
        human_delay(2.0, 3.5)
        
        # Check for videos
        vids = page.locator("#video-block, #vse-video, .vse-player-container, [data-action='video-player']").count()
        has_video_text = page.locator("text='Videos for this product'").count() > 0
        
        # Check for A+ Content
        has_aplus = page.locator("#aplus, #aplus_feature_div .aplus-v2").count() > 0
        
        print(f"-> Video elements: {vids}")
        print(f"-> 'Videos for this product' section: {has_video_text}")
        print(f"-> A+ Content live: {has_aplus}")
        
        history["last_checked"] = datetime.now().isoformat()
        history["video_count"] = vids
        history["has_video_section"] = has_video_text
        history["aplus_live"] = has_aplus
        
        save_history(history)
        return history

if __name__ == "__main__":
    check_listing_visuals()
