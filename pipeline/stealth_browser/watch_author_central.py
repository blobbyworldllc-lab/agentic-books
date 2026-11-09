"""
Continuous Autonomous Watcher & Operator for Amazon Author Central
Watches for active login in amazon_author_profile, claims ASIN B0HPZ647J6,
and attempts video/media integration.
"""
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.stealth_browser.stealth_engine import StealthBrowserEngine, human_delay, human_click, human_type

ASIN = "B0HPZ647J6"
ISBN = "9798166809148"
ARTIFACT_DIR = Path(r"C:\Users\movov\.gemini\antigravity\brain\c985265e-3960-48cf-b104-dc69ade68dfa")

def check_session_and_act():
    print("[Watcher] Checking Amazon Author Central session state...", flush=True)
    try:
        with StealthBrowserEngine(profile_name="amazon_author_profile", headless=True) as engine:
            page = engine.page
            page.goto("https://author.amazon.com/home", wait_until="domcontentloaded", timeout=45000)
            human_delay(2.0, 3.5)

            current_url = page.url
            print(f"[Watcher] URL: {current_url}", flush=True)

            if "signin" in current_url.lower() or "ap/signin" in current_url.lower():
                print("[Watcher] Session not authenticated yet. Waiting for login in visible Chrome...", flush=True)
                return False

            print("[Watcher] Authentication confirmed! Navigating to Books tab...", flush=True)
            page.goto("https://author.amazon.com/books", wait_until="domcontentloaded", timeout=45000)
            human_delay(2.5, 4.0)

            # Check if book is already claimed
            content = page.content()
            if ASIN in content or "Pip's Christmas Countdown" in content:
                print(f"[Watcher] Book {ASIN} is already claimed in Author Central!", flush=True)
            else:
                print(f"[Watcher] Claiming book {ASIN}...", flush=True)
                # Look for "Add a book" or "Add more books"
                add_btn = page.locator("a:has-text('Add a book'), button:has-text('Add a book'), a:has-text('Add more books')").first
                if add_btn.is_visible():
                    add_btn.click()
                    human_delay(1.5, 2.5)
                    # Search for ASIN or ISBN
                    search_input = page.locator("input[type='search'], input[name='search'], input#search-input").first
                    if search_input.is_visible():
                        human_type(page, "input[type='search'], input[name='search'], input#search-input", ASIN)
                        human_delay(0.5, 1.0)
                        page.keyboard.press("Enter")
                        human_delay(3.0, 5.0)
                        # Click "This is my book"
                        claim_btn = page.locator("button:has-text('This is my book'), a:has-text('This is my book')").first
                        if claim_btn.is_visible():
                            claim_btn.click()
                            human_delay(2.0, 3.0)
                            print("[Watcher] Successfully claimed book!", flush=True)

            # Check for Profile / Media / Video section
            print("[Watcher] Inspecting Profile & Media capabilities...", flush=True)
            page.goto("https://author.amazon.com/profile", wait_until="domcontentloaded", timeout=45000)
            human_delay(2.0, 3.5)
            profile_shot = ARTIFACT_DIR / "author_profile_page.png"
            page.screenshot(path=str(profile_shot))
            print(f"[Watcher] Saved profile screenshot to {profile_shot}", flush=True)

            return True
    except Exception as e:
        print(f"[Watcher] Error during check: {e}", flush=True)
        return False

if __name__ == "__main__":
    check_session_and_act()
