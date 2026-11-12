"""
Autonomous Stealth Pinterest Publisher
Posts promotional pins using persistent browser profiles and natural human typing/clicking.
Ensures zero bot triggers by mimicking human interaction speed and adhering to safe daily limits.
"""
import json
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from .stealth_engine import StealthBrowserEngine, human_delay, human_type, human_click

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
HISTORY_FILE = REPO_ROOT / "pipeline" / "growth" / "pinterest_history.json"
PROFILE_NAME = "pinterest_profile"

SHORTS_DIR = REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "output" / "marketing" / "shorts"

PIN_CATALOG = [
    {
        "id": "video_pin_1_sledding",
        "image": str(SHORTS_DIR / "pip_sledding_amazon_short.mp4"),
        "title": "Pip Goes Sledding! Cute Christmas Countdown Coloring Adventure (Ages 3-6)",
        "desc": (
            "Watch Pip the baby penguin zoom through the snow on his winter sled! "
            "From the 110-page paperback 'Pip's Christmas Countdown' featuring 25 bedtime countdown nights "
            "and a 'Find Little Star' seek-and-find game on every page. "
            "Available on Amazon Prime: https://www.amazon.com/dp/B0HPZ647J6"
        ),
        "link": "https://www.amazon.com/dp/B0HPZ647J6",
        "board": "Christmas Coloring Pages for Kids"
    },
    {
        "id": "video_pin_2_skating",
        "image": str(SHORTS_DIR / "pip_skating_amazon_short.mp4"),
        "title": "Pip Goes Ice Skating! Toddler Bedtime Christmas Coloring Book",
        "desc": (
            "Pip the little penguin glides across the frozen pond! "
            "Screen-free bedtime coloring countdown with single-sided pages preventing marker bleed. "
            "Order on Amazon Prime: https://www.amazon.com/dp/B0HPZ647J6"
        ),
        "link": "https://www.amazon.com/dp/B0HPZ647J6",
        "board": "Christmas Coloring Pages for Kids"
    },
    {
        "id": "video_pin_3_tree",
        "image": str(SHORTS_DIR / "pip_tree_amazon_short.mp4"),
        "title": "Pip Decorates the Tree! 25-Night Christmas Countdown for Toddlers",
        "desc": (
            "Pip decorates the holiday Christmas tree with sparkling ornaments! "
            "Complete 50-design coloring adventure with seek-and-find star game for ages 3-6. "
            "Available on Amazon Prime: https://www.amazon.com/dp/B0HPZ647J6"
        ),
        "link": "https://www.amazon.com/dp/B0HPZ647J6",
        "board": "Christmas Coloring Pages for Kids"
    },
    {
        "id": "video_pin_4_snowflake",
        "image": str(SHORTS_DIR / "pip_3d_coloring_amazon_pure_soothing.mp4"),
        "title": "Soothing Christmas Coloring: Pip's Winter Wonderland Activity Book",
        "desc": (
            "Peaceful, soothing bedtime coloring with pure music box chimes. "
            "Give the gift of creative, screen-free holiday joy for toddlers and preschoolers! "
            "Get the paperback on Amazon Prime: https://www.amazon.com/dp/B0HPZ647J6"
        ),
        "link": "https://www.amazon.com/dp/B0HPZ647J6",
        "board": "Christmas Coloring Pages for Kids"
    }
]

def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"published_pins": [], "daily_counts": {}}

def save_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")

def check_can_publish(max_daily=4):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    history = load_history()
    count = history["daily_counts"].get(today, 0)
    return count < max_daily, count

def get_next_pin_to_publish():
    history = load_history()
    published_ids = {p.get("pin_id") for p in history.get("published_pins", [])}
    for item in PIN_CATALOG:
        if item["id"] not in published_ids and os.path.exists(item["image"]):
            return item
    # If all published, do NOT repeat/repost duplicates
    return None

def publish_pin(pin_data=None, headless=True):
    can_publish, daily_count = check_can_publish()
    if not can_publish:
        print(f"[LIMIT REACHED] Daily Pinterest limit reached ({daily_count} pins published today).")
        return False, "Daily limit reached"

    if not pin_data:
        pin_data = get_next_pin_to_publish()
        
    if not pin_data or not os.path.exists(pin_data["image"]):
        print("[ERROR] No valid pin assets available for publishing.")
        return False, "Asset missing"

    print(f"[START] Publishing pin '{pin_data['id']}' to board '{pin_data['board']}'...")
    
    with StealthBrowserEngine(profile_name=PROFILE_NAME, headless=headless) as engine:
        page = engine.page
        
        # Navigate to pin creator
        page.goto("https://www.pinterest.com/pin-creation-tool/", wait_until="domcontentloaded", timeout=25000)
        human_delay(2.5, 4.0)
        
        # Check login state
        if "login" in page.url.lower():
            print("[AUTH ERROR] Profile not logged into Pinterest.")
            return False, "Not logged in"
            
        # Upload image
        file_input = page.locator('input[type="file"]').first
        file_input.set_input_files(pin_data["image"])
        print("[OK] Uploaded pin image.")
        human_delay(2.0, 3.5)
        
        # Title
        title_loc = page.locator('input[placeholder*="title"], textarea[placeholder*="title"], [data-test-id*="title"] input')
        if title_loc.count() > 0:
            human_type(page, 'input[placeholder*="title"], textarea[placeholder*="title"], [data-test-id*="title"] input', pin_data["title"])
            print("[OK] Title entered.")
            
        # Description
        desc_loc = page.locator('div[contenteditable="true"], textarea[placeholder*="description"]')
        if desc_loc.count() > 0:
            human_type(page, 'div[contenteditable="true"], textarea[placeholder*="description"]', pin_data["desc"])
            print("[OK] Description entered.")
            
        # Destination Link
        link_loc = page.locator('input[placeholder*="link"], input[id*="WebsiteField"]')
        if link_loc.count() > 0:
            human_type(page, 'input[placeholder*="link"], input[id*="WebsiteField"]', pin_data["link"])
            print("[OK] Destination Amazon link entered.")
            
        human_delay(1.5, 2.5)
        
        # Board selection
        board_btn = page.locator('[data-test-id="board-dropdown-select-button"], button:has-text("Choose a board")')
        if board_btn.count() > 0:
            board_btn.first.click()
            human_delay(1.5, 2.5)
            board_choice = page.locator(f'text="{pin_data["board"]}"')
            if board_choice.count() > 0:
                board_choice.first.click()
                print(f"[OK] Selected board '{pin_data['board']}'.")
                human_delay(2.0, 3.0)
                
        # Click Publish button
        pub_btn = page.locator('[data-test-id="board-dropdown-save-button"], button:has-text("Publish"), button:has-text("Save")')
        if pub_btn.count() > 0:
            pub_btn.first.click()
            print("[OK] Clicked Publish button.")
            human_delay(5.0, 7.0)
            
            # Record in history
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            now_iso = datetime.now(timezone.utc).isoformat()
            history = load_history()
            history["daily_counts"][today] = history["daily_counts"].get(today, 0) + 1
            history["published_pins"].append({
                "pin_id": pin_data["id"],
                "title": pin_data["title"],
                "board": pin_data["board"],
                "url": page.url,
                "timestamp": now_iso
            })
            save_history(history)
            print(f"[SUCCESS] Pin '{pin_data['id']}' published live! Daily count: {history['daily_counts'][today]}")
            return True, page.url

    return False, "Failed to locate publish button"

if __name__ == "__main__":
    publish_pin()
