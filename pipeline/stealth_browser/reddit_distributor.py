"""
Stealth Reddit Community Distributor
Autonomously shares holiday countdown activity resources, video short previews,
and Amazon Prime purchase links into targeted parenting and homeschool subreddits.
Uses persistent profiles and human-mimicked interaction to avoid bot triggers.
"""
import json
import logging
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from .stealth_engine import StealthBrowserEngine, human_delay, human_type, human_click

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
HISTORY_FILE = REPO_ROOT / "pipeline" / "growth" / "reddit_history.json"
PROFILE_NAME = "reddit_profile"

LEAD_MAGNET_URL = "https://blobbyworldllc-lab.github.io/agentic-books/"
AMAZON_BUY_LINK = "https://www.amazon.com/dp/B0HPZ647J6"
FEATURED_VIDEO_URL = "https://youtube.com/shorts/HfQJeqQ23jg"

REDDIT_COMMUNITIES = [
    {
        "subreddit": "toddlers",
        "url": "https://www.reddit.com/r/toddlers/submit",
        "title": "Free 25-Day Christmas Countdown Coloring Sampler (with 'Find Little Star' seek & find game!)",
        "body": (
            "Hi everyone! If you're looking for screen-free holiday quiet time ideas for December mornings or bedtime, "
            "I wanted to share a free 4-page Christmas countdown coloring pack featuring Pip the baby penguin and Biscuit the puppy!\n\n"
            "Each illustration has a mini 'Find Little Star' seek-and-find observation game hidden in the art.\n\n"
            f"🎬 Quick 15-second countdown video preview: {FEATURED_VIDEO_URL}\n\n"
            f"🎁 Download the free 4-page starter PDF: {LEAD_MAGNET_URL}\n\n"
            f"📖 The full 110-page paperback (50 designs + single-sided pages) is also available on Amazon Prime: {AMAZON_BUY_LINK}\n\n"
            "Hope this brings some peaceful bedtime fun to your little ones!"
        )
    },
    {
        "subreddit": "preschoolers",
        "url": "https://www.reddit.com/r/preschoolers/submit",
        "title": "Preschool Screen-Free Activity: Free 4-Page Christmas Countdown Sampler + Bedtime Rhymes",
        "body": (
            "Sharing a free holiday fine-motor activity resource for 3-6 year olds:\n\n"
            "We put together a cute Christmas countdown coloring pack with bold outlines for pencil grip, "
            "rhyming read-aloud captions, and a hidden Little Star puzzle on every page.\n\n"
            f"🎬 Watch the short preview: {FEATURED_VIDEO_URL}\n\n"
            f"🎁 Free PDF download: {LEAD_MAGNET_URL}\n\n"
            f"📖 Complete 110-page paperback on Amazon Prime: {AMAZON_BUY_LINK}\n\n"
            "Happy holiday planning!"
        )
    },
    {
        "subreddit": "homeschool",
        "url": "https://www.reddit.com/r/homeschool/submit",
        "title": "Free Holiday Unit Resource: 4-Page Christmas Countdown Activity Pack (Ages 3-6)",
        "body": (
            "For anyone doing preschool or kindergarten holiday unit studies, here is a free printable Christmas countdown pack:\n\n"
            "- 25-star number recognition countdown chart\n"
            "- Rhyming story captions for early reading\n"
            "- Visual observation 'Find Little Star' puzzle on each page\n\n"
            f"🎬 Video preview: {FEATURED_VIDEO_URL}\n\n"
            f"🎁 Free instant PDF: {LEAD_MAGNET_URL}\n\n"
            f"📖 Full 50-design paperback on Amazon Prime: {AMAZON_BUY_LINK}"
        )
    },
    {
        "subreddit": "coloring",
        "url": "https://www.reddit.com/r/coloring/submit",
        "title": "Pip's Christmas Countdown: Single-Sided Holiday Coloring Book with Hidden Star Game",
        "body": (
            "Wanted to share a preview of our new holiday coloring project for little ones: 'Pip's Christmas Countdown'!\n\n"
            "50 festive illustrations featuring Pip the baby penguin and Biscuit the puppy, all printed single-sided to prevent bleed-through.\n\n"
            f"🎬 Watch the coloring countdown short: {FEATURED_VIDEO_URL}\n\n"
            f"🎁 Free 4-page starter PDF: {LEAD_MAGNET_URL}\n\n"
            f"📖 Available in paperback on Amazon Prime: {AMAZON_BUY_LINK}"
        )
    },
    {
        "subreddit": "CraftsWithKids",
        "url": "https://www.reddit.com/r/CraftsWithKids/submit",
        "title": "Christmas Countdown Craft & Coloring Activity: Free Printable Starter Pack",
        "body": (
            "Fun holiday quiet time activity for toddlers and preschoolers: color one star each night until Christmas Eve!\n\n"
            f"🎬 Quick video peek: {FEATURED_VIDEO_URL}\n\n"
            f"🎁 Free PDF download: {LEAD_MAGNET_URL}\n\n"
            f"📖 Complete 110-page book on Amazon: {AMAZON_BUY_LINK}"
        )
    }
]

def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"posted_subreddits": [], "daily_counts": {}}

def save_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")

def is_reddit_logged_in(headless=True):
    """Verifies whether the persistent Reddit profile is logged in."""
    with StealthBrowserEngine(profile_name=PROFILE_NAME, headless=headless) as engine:
        page = engine.page
        page.goto("https://www.reddit.com", wait_until="domcontentloaded", timeout=25000)
        human_delay(2.5, 4.0)
        has_login_btn = page.locator('a[href*="login"], button:has-text("Log In")').count() > 0
        return not has_login_btn

def post_next_reddit_thread(headless=True):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    history = load_history()
    posted = {item["subreddit"] for item in history.get("posted_subreddits", [])}
    
    # Safe limit: 1-2 per day on Reddit
    if history["daily_counts"].get(today, 0) >= 2:
        print("[LIMIT] Daily Reddit post limit reached (2/day).")
        return False, "Daily limit reached"
        
    target = None
    for item in REDDIT_COMMUNITIES:
        if item["subreddit"] not in posted:
            target = item
            break
            
    if not target:
        print("[INFO] All cataloged subreddits have been posted.")
        return False, "Catalog fully seeded"
        
    print(f"[START] Navigating to r/{target['subreddit']} submit page...")
    with StealthBrowserEngine(profile_name=PROFILE_NAME, headless=headless) as engine:
        page = engine.page
        page.goto(target["url"], wait_until="domcontentloaded", timeout=30000)
        human_delay(3.0, 5.0)
        
        if "login" in page.url.lower() or page.locator('a[href*="login"]').count() > 0:
            print("[AUTH REQUIRED] Reddit profile is not logged in.")
            return False, "Not logged in"
            
        # Post Title
        title_box = page.locator('textarea[placeholder*="Title"], input[placeholder*="Title"]')
        if title_box.count() > 0:
            human_type(page, 'textarea[placeholder*="Title"], input[placeholder*="Title"]', target["title"])
            print(f"[OK] Title entered for r/{target['subreddit']}.")
            human_delay(2.0, 3.5)
            
        # Post Body
        body_box = page.locator('div[contenteditable="true"][role="textbox"], textarea[placeholder*="Text"]')
        if body_box.count() > 0:
            human_type(page, 'div[contenteditable="true"][role="textbox"], textarea[placeholder*="Text"]', target["body"])
            print("[OK] Body text entered with video and buy links.")
            human_delay(2.5, 4.0)
            
        # Submit button
        submit_btn = page.locator('button:has-text("Post"), button[type="submit"]:has-text("Post")')
        if submit_btn.count() > 0 and submit_btn.first.is_enabled():
            submit_btn.first.click()
            print(f"[OK] Submitted post to r/{target['subreddit']}!")
            human_delay(5.0, 7.0)
            
            history["daily_counts"][today] = history["daily_counts"].get(today, 0) + 1
            history["posted_subreddits"].append({
                "subreddit": target["subreddit"],
                "title": target["title"],
                "url": page.url,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            save_history(history)
            return True, f"Posted to r/{target['subreddit']}"
            
        return False, "Submit button not clickable"

if __name__ == "__main__":
    success, msg = post_next_reddit_thread(headless=True)
    print(f"Result: {success} - {msg}")
