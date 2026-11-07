"""
Interactive Facebook Profile Session Initializer
Launches a visible Chrome window with the persistent facebook_profile.
Allows a one-time human sign-in (or MFA) so the profile preserves the cookies
indefinitely for zero-token headless background group publishing.
"""
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.stealth_browser.stealth_engine import StealthBrowserEngine, human_delay

def main():
    print("=================================================================", flush=True)
    print("Launching visible Chrome window with persistent Facebook profile...", flush=True)
    print("Please log in to Facebook once. Once logged in, your session", flush=True)
    print("will be saved permanently to pipeline/browser_profiles/facebook_profile.", flush=True)
    print("=================================================================", flush=True)
    
    with StealthBrowserEngine(profile_name="facebook_profile", headless=False) as engine:
        page = engine.page
        context = engine.context
        page.goto("https://www.facebook.com", wait_until="domcontentloaded")
        print("\nBrowser is open on your screen. Waiting for login completion...", flush=True)
        
        while True:
            time.sleep(3)
            try:
                if page.is_closed():
                    print("\n[CLOSED] Browser window closed.", flush=True)
                    break
                    
                # Check for standard Facebook authenticated cookie 'c_user'
                cookies = context.cookies()
                has_c_user = any(c.get("name") == "c_user" for c in cookies)
                
                # Check for logged-in DOM indicators
                has_feed = page.locator('[role="feed"], [aria-label*="Create a post"], div[data-pagelet*="Feed"]').count() > 0
                
                if has_c_user or has_feed:
                    print("\n[SUCCESS] Active Facebook authentication session detected!", flush=True)
                    print("[SUCCESS] Session saved permanently to pipeline/browser_profiles/facebook_profile.", flush=True)
                    time.sleep(3)
                    break
            except Exception as e:
                # If page is navigating or closed
                pass

if __name__ == "__main__":
    main()
