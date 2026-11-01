"""
Buffer API Dispatcher for Pip's Christmas Countdown & Future Catalog Books
Brand: Blobby World Official

Automates scheduling of Pinterest Pins, Instagram Posts, and Facebook Posts
across all connected channels using the Buffer API.

Documentation / Setup:
1. Connect your Pinterest, Instagram, and Facebook profiles to Buffer (https://buffer.com).
2. Generate an Access Token at: https://buffer.com/developers/api
3. Place your token in `pipeline/social/buffer_token.json` or env `BUFFER_ACCESS_TOKEN`.
"""
import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SOCIAL_DIR = BASE_DIR / "pipeline" / "social"
CONFIG_FILE = SOCIAL_DIR / "buffer_config.json"
TOKEN_FILE = SOCIAL_DIR / "buffer_token.json"

LANDING_URL = "https://blobbyworldllc-lab.github.io/agentic-books/"
AMAZON_ASIN_URL = "https://www.amazon.com/dp/B0HPZ647J6"
CDN_BASE = "https://blobbyworldllc-lab.github.io/agentic-books"

BUFFER_API = "https://api.bufferapp.com/1"

def get_access_token():
    if os.environ.get("BUFFER_ACCESS_TOKEN"):
        return os.environ.get("BUFFER_ACCESS_TOKEN").strip()
    if TOKEN_FILE.exists():
        data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
        return data.get("access_token", "").strip()
    return None

def buffer_request(endpoint, post_data=None):
    token = get_access_token()
    if not token:
        raise ValueError(f"No Buffer access token found. Put token in {TOKEN_FILE} or set BUFFER_ACCESS_TOKEN.")
    
    url = f"{BUFFER_API}/{endpoint}.json?access_token={token}"
    req = urllib.request.Request(url)
    if post_data is not None:
        req.data = urllib.parse.urlencode(post_data).encode("utf-8")
        req.method = "POST"
    
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        raise RuntimeError(f"Buffer API Error ({e.code}): {err_msg}")

def list_profiles():
    """Lists all connected profiles (Pinterest, Instagram, Facebook)."""
    profiles = buffer_request("profiles")
    print(f"Found {len(profiles)} connected Buffer profile(s):")
    profiles_summary = []
    for p in profiles:
        summary = {
            "id": p["id"],
            "service": p.get("service"),
            "formatted_username": p.get("formatted_username") or p.get("service_username")
        }
        profiles_summary.append(summary)
        print(f" - [{summary['service'].upper()}] ID: {summary['id']} (@{summary['formatted_username']})")
    
    CONFIG_FILE.write_text(json.dumps({"profiles": profiles_summary}, indent=2), encoding="utf-8")
    return profiles_summary

def queue_post(profile_ids, text, media_url=None, link_url=None, now=False):
    """Queues a post to the specified profiles."""
    payload = {
        "text": text,
        "now": "true" if now else "false",
        "shorten": "false"
    }
    for idx, pid in enumerate(profile_ids):
        payload[f"profile_ids[{idx}]"] = pid
    
    if media_url:
        payload["media[photo]"] = media_url
    if link_url:
        payload["media[link]"] = link_url
        
    res = buffer_request("updates/create", post_data=payload)
    return res

def queue_launch_campaign():
    """Queues the complete launch campaign across Pinterest, Instagram, and Facebook."""
    token = get_access_token()
    if not token:
        print(f"[ACTION REQUIRED] Please add your Buffer access token to:\n{TOKEN_FILE}\n")
        print("Steps:")
        print("1. Log in to Buffer (https://buffer.com) and link your Pinterest, Instagram & Facebook.")
        print("2. Create an App token at https://buffer.com/developers/api")
        print('3. Save as: {"access_token": "YOUR_TOKEN"}')
        return False

    profiles = list_profiles()
    if not profiles:
        print("[!] No profiles connected in Buffer.")
        return False

    pin_ids = [p["id"] for p in profiles if p["service"] == "pinterest"]
    ig_ids = [p["id"] for p in profiles if p["service"] == "instagram"]
    fb_ids = [p["id"] for p in profiles if p["service"] == "facebook"]

    # 1. Post to Pinterest
    if pin_ids:
        pin_text = (
            "Free Christmas Countdown Coloring Pages for Kids Ages 3-6 (Printable PDF)! 🐧⭐\n\n"
            "Cute penguin Christmas coloring pages for toddlers and preschoolers. "
            "Free printable countdown tracker + Day 1 & Day 2 story pages featuring Pip and Little Star. "
            f"Instant free download: {LANDING_URL}"
        )
        pin_img = f"{CDN_BASE}/pin_1_coloring_pages.png"
        print("Queueing Pinterest pin...")
        queue_post(pin_ids, pin_text, media_url=pin_img, link_url=LANDING_URL)
        print("✓ Pinterest pin queued successfully!")

    # 2. Post to Instagram
    if ig_ids:
        ig_text = (
            "NEW for Christmas! 🐧🎄 Meet Pip, a little penguin with a big countdown!\n\n"
            "A tiny star lands on his nose and plays hide-and-seek every night until Christmas. "
            "Read one rhyme, color one page, find Little Star! 25 nights + 25 bonus winter adventures for ages 3-6.\n\n"
            f"Full paperback now live on Amazon: {AMAZON_ASIN_URL}\n"
            f"Grab the FREE 4-page starter printable pack from the link in bio!\n\n"
            "#BlobbyWorld #ChristmasColoring #ToddlerActivities #ColoringBook #KidsChristmas #ChristmasCountdown"
        )
        ig_img = f"{CDN_BASE}/ig_1_launch.png"
        print("Queueing Instagram launch post...")
        queue_post(ig_ids, ig_text, media_url=ig_img, link_url=LANDING_URL)
        print("✓ Instagram post queued successfully!")

    # 3. Post to Facebook
    if fb_ids:
        fb_text = (
            "Free 25-Day Christmas Countdown Coloring Tracker for Little Ones! 🐧⭐\n\n"
            "We put together a free 4-page Christmas Countdown printable pack for toddlers and preschoolers (ages 3–6) "
            "to make December quiet time fun.\n\n"
            "• 25-night Star Countdown Chart\n"
            "• Day 1 & Day 2 rhyming story coloring pages\n"
            "• 'Find Little Star' seek-and-find game on every page\n\n"
            f"Free printable PDF download: {LANDING_URL}\n"
            f"Full 110-page paperback on Amazon: {AMAZON_ASIN_URL}"
        )
        fb_img = f"{CDN_BASE}/ig_3_free_page.png"
        print("Queueing Facebook post...")
        queue_post(fb_ids, fb_text, media_url=fb_img, link_url=LANDING_URL)
        print("✓ Facebook post queued successfully!")

    return True

if __name__ == "__main__":
    if "--profiles" in sys.argv:
        list_profiles()
    else:
        queue_launch_campaign()
