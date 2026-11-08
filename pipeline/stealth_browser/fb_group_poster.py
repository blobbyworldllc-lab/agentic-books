"""
Stealth Facebook Group Publisher
Handles automated navigation, membership verification, and slow-paced human posting
into targeted parenting and homeschool Facebook communities.
"""
import json
import logging
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from .stealth_engine import StealthBrowserEngine, human_delay, human_type, human_click

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
HISTORY_FILE = REPO_ROOT / "pipeline" / "growth" / "community_history.json"
PROFILE_NAME = "facebook_profile"

def is_facebook_logged_in(headless=True):
    """Verifies whether the persistent Facebook browser profile is actively authenticated."""
    with StealthBrowserEngine(profile_name=PROFILE_NAME, headless=headless) as engine:
        page = engine.page
        page.goto("https://www.facebook.com", wait_until="domcontentloaded", timeout=25000)
        human_delay(2.0, 3.5)
        
        # If email input or login button is prominent, not logged in
        has_login = page.locator('input[name="email"], input[id="email"]').count() > 0
        return not has_login

def post_to_facebook_group(group_url, copy_text, group_name="Unknown Group", headless=True):
    """
    Navigates to Facebook group, checks membership/posting box, types with human delays,
    and publishes the discussion post.
    """
    print(f"[START] Navigating to Facebook Group: {group_name} ({group_url})...")
    with StealthBrowserEngine(profile_name=PROFILE_NAME, headless=headless) as engine:
        page = engine.page
        page.goto(group_url, wait_until="domcontentloaded", timeout=30000)
        human_delay(3.0, 5.0)
        
        # Check login gate
        if "login" in page.url.lower() or page.locator('input[name="email"]').count() > 0:
            print(f"[AUTH REQUIRED] Facebook profile is not logged in. Need session initialization.")
            return False, "Not logged in"
            
        # Check if Join group needed
        join_btn = page.locator('text="Join group", [aria-label*="Join group"]')
        if join_btn.count() > 0:
            print("[INFO] Clicking Join group button...")
            join_btn.first.click()
            human_delay(2.0, 4.0)
            
        # Locate post composer
        composer = page.locator(
            '[aria-label*="Write something"], [aria-label*="Create a public post"], div[role="button"]:has-text("Write something...")'
        )
        if composer.count() == 0:
            print("[NOTICE] Composer not immediately visible (group may require admin approval or manual answer questions).")
            return False, "Composer not accessible"
            
        print("[OK] Opening post composer modal...")
        composer.first.click()
        human_delay(2.0, 3.5)
        
        # Active text area (scope to modal dialog if present to avoid background comments)
        dialog = page.locator('div[role="dialog"]')
        if dialog.count() > 0:
            target_input = 'div[role="dialog"] div[contenteditable="true"][role="textbox"]'
            target_btn = 'div[role="dialog"] div[aria-label="Post"][role="button"], div[role="dialog"] div[role="button"]:has-text("Post")'
        else:
            target_input = 'div[contenteditable="true"][role="textbox"], div[aria-label*="What\'s on your mind"]'
            target_btn = 'div[aria-label="Post"][role="button"], button:has-text("Post")'

        print("[OK] Human-typing promotional copy into modal...")
        human_type(page, target_input, copy_text)
        human_delay(2.5, 4.0)
        
        # Post button
        post_btn = page.locator(target_btn)
        if post_btn.count() > 0:
            print("[OK] Submitting post to group...")
            post_btn.first.click()
            human_delay(6.0, 9.0)
            print(f"[SUCCESS] Successfully published live post to {group_name}!")
            return True, "Published"
                
        return False, "Post button not found"

if __name__ == "__main__":
    logged_in = is_facebook_logged_in()
    print("Facebook Profile Authenticated?:", logged_in)
