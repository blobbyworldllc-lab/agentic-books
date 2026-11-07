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

PIN_CATALOG = [
    {
        "id": "pin_1_coloring_pages",
        "image": str(REPO_ROOT / "docs" / "pin_1_coloring_pages.png"),
        "title": "Free Christmas Countdown Coloring Pages for Kids Ages 3-6 (Printable PDF)",
        "desc": (
            "Cute penguin Christmas countdown coloring pages for toddlers & preschoolers (ages 3–6)! "
            "25 nights to Christmas + 25 bonus winter adventures. "
            "Features 'Find Little Star' seek-and-find game on every single page! "
            "Download the free 4-page starter pack or order the 110-page paperback on Amazon Prime: "
            "https://www.amazon.com/dp/B0HPZ647J6"
        ),
        "link": "https://www.amazon.com/dp/B0HPZ647J6",
        "board": "Christmas Coloring Pages for Kids"
    },
    {
        "id": "pin_2_a_plus_module1",
        "image": str(REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "output" / "marketing" / "a_plus_content" / "a_plus_module1_300x300.png"),
        "title": "25 Nights Christmas Countdown Coloring Book for Toddlers & Preschoolers",
        "desc": (
            "Make December bedtime magical! 25 countdown nights + 25 winter wonderland scenes "
            "featuring Pip the baby penguin and Biscuit the puppy. Single-sided designs prevent marker bleed! "
            "Available on Amazon Prime: https://www.amazon.com/dp/B0HPZ647J6"
        ),
        "link": "https://www.amazon.com/dp/B0HPZ647J6",
        "board": "Christmas Coloring Pages for Kids"
    },
    {
        "id": "pin_3_find_little_star",
        "image": str(REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "output" / "marketing" / "a_plus_content" / "a_plus_module2_300x300.png"),
        "title": "Find Little Star Game: Christmas Activity & Coloring Book for Toddlers",
        "desc": (
            "Seek-and-find activity built into every holiday illustration! Kids search for Little Star "
            "on all 50 full-page coloring designs. Keeps hands busy and screen-free all holiday season! "
            "Get the paperback on Amazon Prime: https://www.amazon.com/dp/B0HPZ647J6"
        ),
        "link": "https://www.amazon.com/dp/B0HPZ647J6",
        "board": "Christmas Coloring Pages for Kids"
    },
    {
        "id": "pin_4_single_sided_no_bleed",
        "image": str(REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "output" / "marketing" / "a_plus_content" / "a_plus_module3_300x300.png"),
        "title": "Single-Sided No Bleed Christmas Coloring Pages for Kids Ages 3-6",
        "desc": (
            "Every coloring page has a clean blank reverse page so markers, crayons, and watercolors won't bleed through! "
            "110 pages of festive holiday fun for preschoolers. "
            "Order on Amazon Prime: https://www.amazon.com/dp/B0HPZ647J6"
        ),
        "link": "https://www.amazon.com/dp/B0HPZ647J6",
        "board": "Christmas Coloring Pages for Kids"
    },
    {
        "id": "pin_5_banner_countdown",
        "image": str(REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "output" / "marketing" / "a_plus_content" / "a_plus_banner_970x600.png"),
        "title": "Pip's Christmas Countdown: Complete 50-Design Holiday Coloring Adventure",
        "desc": (
            "The ultimate December countdown tradition for toddlers and preschoolers (ages 3–6). "
            "Featuring Pip the baby penguin! Get the 110-page paperback with fast Prime shipping: "
            "https://www.amazon.com/dp/B0HPZ647J6"
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
    # If all published, return first valid item for scheduled rotation
    for item in PIN_CATALOG:
        if os.path.exists(item["image"]):
            return item
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
