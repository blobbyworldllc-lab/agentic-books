"""
Direct Meta Graph API Publisher for Facebook Page
Page URL: https://www.facebook.com/share/1DtG7fTPNu/
Brand: Blobby World Official

Features:
- Publishes launch posts, free printable announcements, and images directly to your Facebook Page feed.
- Uses Meta Graph API (POST https://graph.facebook.com/v21.0/{page_id}/feed)
"""
import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = BASE_DIR / "pipeline" / "social" / "fb_config.json"
LANDING_URL = "https://blobbyworldllc-lab.github.io/agentic-books/"
AMAZON_ASIN_URL = "https://www.amazon.com/dp/B0HPZ647J6"
IMAGE_URL = "https://raw.githubusercontent.com/blobbyworldllc-lab/agentic-books/main/docs/ig_1_launch.png"

def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return {}

def publish_to_page(message=None, link=None, image_url=None):
    cfg = load_config()
    page_id = cfg.get("page_id")
    page_access_token = cfg.get("page_access_token")

    if not page_id or not page_access_token:
        print("[!] Facebook Page API Token not configured yet.")
        print(f"Please save Page ID and Page Access Token into: {CONFIG_FILE}")
        return False

    if not message:
        message = (
            "NEW for Christmas! Pip's Christmas Countdown is now LIVE on Amazon! 🐧🎄\n\n"
            "A 25-night story coloring book for kids ages 3-6: read one gentle rhyme, color one big easy picture, "
            "and help Pip find Little Star on every single page!\n\n"
            f"🎁 Free 4-page starter printable pack: {LANDING_URL}\n"
            f"📕 Full 110-page paperback on Amazon: {AMAZON_ASIN_URL}"
        )

    # If posting a photo directly
    if image_url:
        endpoint = f"https://graph.facebook.com/v21.0/{page_id}/photos"
        payload = {
            "url": image_url,
            "caption": message,
            "access_token": page_access_token
        }
    else:
        endpoint = f"https://graph.facebook.com/v21.0/{page_id}/feed"
        payload = {
            "message": message,
            "link": link or LANDING_URL,
            "access_token": page_access_token
        }

    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(endpoint, data=data, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            print(f"[SUCCESS] Published to Facebook Page! Post ID: {res.get('id') or res.get('post_id')}")
            return res
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        print(f"[ERROR] Meta Graph API Error ({e.code}): {err}")
        return False

if __name__ == "__main__":
    publish_to_page(image_url=IMAGE_URL)
