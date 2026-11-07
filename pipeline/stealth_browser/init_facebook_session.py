"""
Interactive Facebook Profile Session Initializer
Launches a visible Chrome window with the persistent facebook_profile.
Allows a one-time human sign-in (or MFA) so the profile preserves the cookies
indefinitely for zero-token headless background group publishing.
"""
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.stealth_browser.stealth_engine import StealthBrowserEngine, human_delay

def main():
    print("=================================================================")
    print("Launching visible Chrome window with persistent Facebook profile...")
    print("Please log in to Facebook once. Once logged in, your session")
    print("will be saved permanently to pipeline/browser_profiles/facebook_profile.")
    print("=================================================================")
    
    with StealthBrowserEngine(profile_name="facebook_profile", headless=False) as engine:
        page = engine.page
        page.goto("https://www.facebook.com", wait_until="domcontentloaded")
        print("\nBrowser is open. Waiting for login completion (checking every 5 seconds)...")
        
        while True:
            human_delay(4.0, 6.0)
            if page.locator('[role="feed"], [aria-label*="Create a post"], div[data-pagelet*="Feed"]').count() > 0:
                print("\n[SUCCESS] Detected active Facebook feed! Session permanently persisted.")
                break
            if page.is_closed():
                print("\n[CLOSED] Browser window closed.")
                break

if __name__ == "__main__":
    main()
