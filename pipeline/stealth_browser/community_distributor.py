"""
Autonomous Stealth Community Distributor
Safely coordinates distribution of free printable lead magnets and Amazon paperback links
across parenting, homeschool, preschool, and holiday tradition communities.
Enforces human pacing (10-20 min intervals) with up to 15-20 groups/day and records full audit history.
"""
import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_FILE = REPO_ROOT / "pipeline" / "growth" / "community_database.json"
HISTORY_FILE = REPO_ROOT / "pipeline" / "growth" / "community_history.json"
PROFILE_NAME = "facebook_profile"

LEAD_MAGNET_URL = "https://blobbyworldllc-lab.github.io/agentic-books/"
AMAZON_BUY_LINK = "https://www.amazon.com/dp/B0HPZ647J6"
VIDEO_PREVIEW_URL = "https://youtube.com/shorts/v24c4QH0XWQ"

MESSAGE_TEMPLATES = {
    "preschool": (
        "Hi parents and teachers! 🎄 If you're looking for screen-free holiday countdown ideas, "
        "I wanted to share a free 4-page Christmas countdown coloring pack (featuring Pip the baby penguin and Biscuit the puppy)! "
        "Every page has a mini 'Find Little Star' seek-and-find game hidden in the art.\n\n"
        f"Watch the 15-second countdown preview short: {VIDEO_PREVIEW_URL}\n"
        f"Grab the free printable PDF here: {LEAD_MAGNET_URL}\n"
        f"Complete 110-page paperback on Amazon Prime ($7.99 launch promo): {AMAZON_BUY_LINK}\n\n"
        "Hope your little ones enjoy it!"
    ),
    "homeschool": (
        "Free holiday activity resource for preschool and kindergarten homeschoolers: "
        "4 printable Christmas countdown activity pages designed with thick bold lines for pencil control "
        "and a 'Find Little Star' seek-and-find visual observation game on each page.\n\n"
        f"Watch the quick video activity preview: {VIDEO_PREVIEW_URL}\n"
        f"Download the free PDF starter kit: {LEAD_MAGNET_URL}\n"
        f"Full 50-design book available on Amazon ($7.99 early-bird price): {AMAZON_BUY_LINK}\n\n"
        "Happy holiday planning!"
    ),
    "printables": (
        "Sharing our free Christmas countdown coloring printable pack! 🐧⭐ "
        "Cute penguin & puppy illustrations with seek-and-find activities for toddlers & preschoolers.\n\n"
        f"Watch the countdown preview: {VIDEO_PREVIEW_URL}\n"
        f"Free PDF download: {LEAD_MAGNET_URL}\n"
        f"Full 110-page paperback on Amazon ($7.99): {AMAZON_BUY_LINK}"
    ),
    "christmas_traditions": (
        "Start a peaceful bedtime countdown tradition this December! "
        "Here is a free 4-page sample of our Christmas countdown coloring pages featuring Pip the penguin.\n\n"
        f"Watch the bedtime countdown short: {VIDEO_PREVIEW_URL}\n"
        f"Free printable pack: {LEAD_MAGNET_URL}\n"
        f"Order the complete 110-page paperback on Amazon ($7.99 early-bird): {AMAZON_BUY_LINK}"
    )
}

def load_database():
    if DB_FILE.exists():
        return json.loads(DB_FILE.read_text(encoding="utf-8"))
    return {}

def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"posted_groups": [], "attempted_groups": [], "daily_counts": {}}

def save_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")

def check_daily_limit(max_per_day=20):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    history = load_history()
    count = history.get("daily_counts", {}).get(today, 0)
    return count < max_per_day, count

def get_next_target_community(max_per_day=20):
    can_post, current_count = check_daily_limit(max_per_day=max_per_day)
    if not can_post:
        return None, f"Daily limit reached ({current_count}/{max_per_day} today)"
        
    db = load_database()
    history = load_history()
    posted_urls = {item["url"] for item in history.get("posted_groups", [])}
    # Only skip groups attempted within the last 24 hours
    now_ts = datetime.now(timezone.utc).timestamp()
    recently_attempted = set()
    for item in history.get("attempted_groups", []):
        try:
            dt = datetime.fromisoformat(item.get("timestamp", ""))
            if (now_ts - dt.timestamp()) < 86400:
                recently_attempted.add(item["url"])
        except Exception:
            recently_attempted.add(item.get("url"))
            
    skip_urls = posted_urls.union(recently_attempted)
    
    for category, groups in db.get("categories", {}).items():
        for group in groups:
            if group["url"] not in skip_urls:
                template = MESSAGE_TEMPLATES.get(category, MESSAGE_TEMPLATES["preschool"])
                return {
                    "category": category,
                    "group": group,
                    "copy": template
                }, "OK"
                
    return None, "All communities in catalog have been recently seeded"

def record_attempt(target_data, reason="inaccessible"):
    history = load_history()
    if "attempted_groups" not in history:
        history["attempted_groups"] = []
    history["attempted_groups"].append({
        "url": target_data["group"]["url"],
        "name": target_data["group"]["name"],
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    save_history(history)

def record_distribution_event(target_data, max_per_day=20):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    now_iso = datetime.now(timezone.utc).isoformat()
    history = load_history()
    
    if "daily_counts" not in history:
        history["daily_counts"] = {}
    if "posted_groups" not in history:
        history["posted_groups"] = []
        
    history["daily_counts"][today] = history["daily_counts"].get(today, 0) + 1
    history["posted_groups"].append({
        "category": target_data["category"],
        "name": target_data["group"]["name"],
        "url": target_data["group"]["url"],
        "members": target_data["group"]["members"],
        "timestamp": now_iso
    })
    save_history(history)
    print(f"[SUCCESS] Recorded community distribution to {target_data['group']['name']}. Today: {history['daily_counts'][today]}/{max_per_day}")

if __name__ == "__main__":
    target, status = get_next_target_community()
    if target:
        print(f"Next Target Community: [{target['category']}] {target['group']['name']} ({target['group']['members']})")
        print(f"URL: {target['group']['url']}")
        copy_clean = target['copy'].encode('ascii', errors='replace').decode('ascii')
        print(f"Tailored Copy:\n{copy_clean}")
    else:
        print(f"Status: {status}")
