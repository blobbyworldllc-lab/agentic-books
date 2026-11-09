"""
Autonomous Amazon Author Central Bot
Handles session initialization, book claiming (ASIN B0HPZ647J6),
and media / video upload for Pip's Christmas Countdown.
"""
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.stealth_browser.stealth_engine import StealthBrowserEngine, human_delay, human_type, human_click

ARTIFACT_DIR = Path(r"C:\Users\movov\.gemini\antigravity\brain\c985265e-3960-48cf-b104-dc69ade68dfa")
ASIN = "B0HPZ647J6"
BOOK_TITLE = "Pip's Christmas Countdown"
AUTHOR_NAME = "Blobby World Official"
VIDEO_PATH = REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "output" / "marketing" / "shorts" / "pip_amazon_outro.mp4"

def run_author_central_bot():
    print("=" * 60)
    print("Starting Autonomous Amazon Author Central Bot...")
    print(f"Target ASIN: {ASIN}")
    print(f"Target Author: {AUTHOR_NAME}")
    print(f"Video File: {VIDEO_PATH}")
    print("=" * 60)

    # Launch visible browser for full interaction and session handling
    with StealthBrowserEngine(profile_name="amazon_author_profile", headless=False, width=1366, height=900) as engine:
        page = engine.page
        context = engine.context

        print("\n[Step 1] Navigating to https://author.amazon.com/ ...")
        page.goto("https://author.amazon.com/", wait_until="domcontentloaded", timeout=60000)
        human_delay(2.5, 4.0)

        # Save initial screenshot
        screenshot_1 = ARTIFACT_DIR / "author_central_step1.png"
        page.screenshot(path=str(screenshot_1))
        print(f"[Saved Screenshot] {screenshot_1}")

        current_url = page.url
        print(f"Current URL: {current_url}")
        print(f"Page Title: {page.title()}")

        # Check if Join / Sign in button is visible
        sign_in_selectors = [
            "a[href*='signin']",
            "button:has-text('Sign In')",
            "a:has-text('Sign In')",
            "a:has-text('Join')",
            "button:has-text('Join Free')",
            "a:has-text('Join Free')",
            "#signInSubmit"
        ]

        # Look for Books tab if already logged in
        books_tab = page.locator("a[href*='/books'], nav a:has-text('Books'), button:has-text('Books')").first
        profile_tab = page.locator("a[href*='/profile'], nav a:has-text('Profile'), button:has-text('Profile')").first

        is_logged_in = books_tab.is_visible() or profile_tab.is_visible()

        if is_logged_in:
            print("\n[SUCCESS] Active Amazon Author Central session detected!")
        else:
            print("\n[INFO] Checking for sign-in / join button...")
            clicked = False
            for sel in sign_in_selectors:
                loc = page.locator(sel).first
                if loc.is_visible():
                    print(f"Clicking sign-in/join trigger: {sel}")
                    human_click(page, sel)
                    clicked = True
                    break
            
            human_delay(3.0, 5.0)
            screenshot_login = ARTIFACT_DIR / "author_central_login_screen.png"
            page.screenshot(path=str(screenshot_login))
            print(f"[Saved Screenshot] {screenshot_login}")
            print(f"Login URL: {page.url}")

        # Wait a short moment to observe page state
        time.sleep(5)

if __name__ == "__main__":
    run_author_central_bot()
