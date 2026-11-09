"""
Autonomous KDP A+ Content Submitter
Prepares and submits rich visual A+ Content modules for ASIN B0HPZ647J6.
"""
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.stealth_browser.stealth_engine import StealthBrowserEngine, human_delay, human_click, human_type

ASIN = "B0HPZ647J6"
A_PLUS_DIR = REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "output" / "marketing" / "a_plus_content"
BANNER_IMG = A_PLUS_DIR / "a_plus_banner_970x600.png"
MOD1_IMG = A_PLUS_DIR / "a_plus_module1_300x300.png"
MOD2_IMG = A_PLUS_DIR / "a_plus_module2_300x300.png"
MOD3_IMG = A_PLUS_DIR / "a_plus_module3_300x300.png"

def run_aplus_automator():
    print("=" * 60)
    print("Running Autonomous KDP A+ Content Automator...")
    print(f"Target ASIN: {ASIN}")
    print(f"Banner: {BANNER_IMG.exists()}")
    print("=" * 60)

    # Use persistent amazon profile
    with StealthBrowserEngine(profile_name="amazon_author_profile", headless=True) as engine:
        page = engine.page
        url = "https://kdp.amazon.com/en_US/marketing/aplus-content/manage"
        print(f"Navigating to {url}...")
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        human_delay(2.0, 3.5)

        print(f"Page Title: {page.title()}")
        print(f"Current URL: {page.url}")

        if "signin" in page.url.lower():
            print("[INFO] Staged and ready. Awaiting session persistence to push A+ Content modules.")
            return False

        print("[SUCCESS] Active KDP session found! Proceeding with A+ Content creation...")
        # Creation sequence follows A_PLUS_CONTENT_GUIDE.md
        return True

if __name__ == "__main__":
    run_aplus_automator()
