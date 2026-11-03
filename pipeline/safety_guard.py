"""Pipeline Safety & Timing Guard (Source of Truth Code Barrier).

Hard rules enforced at the code execution level:
 1. Random Non-Uniform Spacing: Enforces `random.randint(20, 100)` minute deltas.
 2. Mandatory Amazon Links (Zero Exceptions): Every post across EVERY platform (Instagram, Facebook, Pinterest, Threads, X, YouTube, TikTok) MUST include the direct Amazon purchase link in the post description/caption AND in the first comment.
 3. Daily Cadence Throttle: Limits max 5 posts per channel per 24-hour rolling window.
 4. Zero Copy Duplication: Cryptographic hash comparison ensures no duplicate post text within 7 days.
 5. Content Policy Filter: Rejects trademarked/copyrighted terms, violence, or non-kid-safe keywords.

Any violating action raises `PipelineSafetyViolation` and stops execution immediately.
"""
import hashlib
import json
import random
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

class PipelineSafetyViolation(Exception):
    """Raised when an automated action violates account safety, policy, or rate standards."""
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent
HISTORY_FILE = REPO_ROOT / "pipeline" / "social_history.json"

# Prohibited keywords (Copyright, Adult, Violence, Brand Infringement)
PROHIBITED_TERMS = [
    "disney", "marvel", "pokemon", "mickey", "peppa", "paw patrol",
    "cocomelon", "bluey", "star wars", "lego", "barbie", "nintendo",
    "kill", "blood", "weapon", "scary", "death", "hate", "fight"
]

def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"posts": []}

def save_history(history):
    # Keep last 100 records
    history["posts"] = history["posts"][-100:]
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")

def compute_random_spacing(min_minutes=20, max_minutes=100):
    """Generates a non-uniform random delta to defeat pattern detection."""
    return random.randint(min_minutes, max_minutes)

def validate_post_content(text, platform, require_amazon_link=False):
    """Enforces content safety and platform link rules at code level."""
    lower_text = text.lower()
    
    # 1. Prohibited terms check with word boundaries (avoids false positives like 'skills' matching 'kill')
    for term in PROHIBITED_TERMS:
        if re.search(r"\b" + re.escape(term) + r"\b", lower_text):
            raise PipelineSafetyViolation(f"[CODE REJECT] Prohibited term '{term}' detected. Violates IP/Safety gate.")

    # 2. Mandatory Amazon link check if enforced
    if require_amazon_link:
        if "amazon.com/dp/" not in lower_text and "amzn.to/" not in lower_text and "amazon.com/gp/" not in lower_text:
            raise PipelineSafetyViolation(
                f"[CODE REJECT] Missing mandatory Amazon purchase link on {platform}. "
                "Hard Rule: Every post must include the Amazon purchase link in post copy."
            )

    # 3. Duplicate text check (rolling 7-day window)
    history = load_history()
    text_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
    now_utc = datetime.now(timezone.utc)
    
    for item in history.get("posts", []):
        if item.get("hash") == text_hash and item.get("platform") == platform.lower():
            ts = datetime.fromisoformat(item["timestamp"])
            if (now_utc - ts).total_seconds() < (7 * 86400):
                raise PipelineSafetyViolation(
                    f"[CODE REJECT] Duplicate post copy detected within 7 days on {platform}. "
                    "All posts must carry unique day rhymes and copy."
                )

    return True

def record_post_execution(platform, text):
    """Records executed post to prevent cadence flooding and duplicate copy."""
    history = load_history()
    now_utc = datetime.now(timezone.utc)
    text_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
    
    history["posts"].append({
        "timestamp": now_utc.isoformat(),
        "platform": platform.lower(),
        "hash": text_hash
    })
    save_history(history)

def check_daily_cadence(platform, max_posts=5):
    """Enforces maximum daily limit at the code level."""
    history = load_history()
    now_utc = datetime.now(timezone.utc)
    day_ago = now_utc - timedelta(hours=24)
    
    recent_count = sum(
        1 for p in history.get("posts", [])
        if p.get("platform") == platform.lower()
        and datetime.fromisoformat(p["timestamp"]) >= day_ago
    )
    
    if recent_count >= max_posts:
        raise PipelineSafetyViolation(
            f"[CODE REJECT] Cadence limit reached for {platform} ({recent_count}/{max_posts} in last 24h). "
            "Pacing enforced to prevent account suspension."
        )
    return True


def format_promotional_copy(base_caption, platform, asin="B0HPZ647J6"):
    """
    Hard Rule (Zero Exceptions, Any Book):
    Formats post description/caption and generates dedicated first comment.
    Both MUST carry the direct Amazon purchase link with high-visibility modern 2026 icons.
    Returns: (formatted_caption, first_comment)
    """
    amazon_url = f"https://www.amazon.com/dp/{asin}"
    landing_url = "https://blobbyworldllc-lab.github.io/agentic-books/"
    divider = "━━━━━━━━━━━━━━━━━━━━"
    
    # 1. Instagram / IG formatting:
    # High-contrast 2026 header block with clean directional icons,
    # screen-free & fine-motor developmental benefits, Tampa/Made in USA geotags,
    # and dedicated first comment.
    if platform.lower() in ["instagram", "ig"]:
        header = (
            f"✨ AVAILABLE NOW ON AMAZON PRIME ✨\n"
            f"🛒 TAP TO ORDER HERE ➔ {amazon_url}\n"
            f"{divider}"
        )
        footer = (
            f"{divider}\n"
            f"📵 100% SCREEN-FREE • MOTOR SKILLS & BEDTIME FOCUS\n"
            f"📍 Tampa, Florida • 🇺🇸 Printed in USA with Prime Delivery\n"
            f"📦 FAST PRIME SHIPPING ➔ {amazon_url}\n"
            f"🎁 FREE ACTIVITY PACK ➔ {landing_url}\n"
            f"👉 Also available via bio: @blobbyworldofficial"
        )
        caption = f"{header}\n\n{base_caption}\n\n{footer}"
        comment = (
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🛒 DIRECT AMAZON PURCHASE LINK:\n"
            f"👉 {amazon_url}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📵 100% Screen-Free Motor Skills | 🇺🇸 Made in USA\n"
            f"✨ Prime Fast Delivery | 🎁 Free Printable Pack: {landing_url}"
        )
        return caption, comment

    # 2. All other platforms (Threads, Facebook, X, Pinterest, YouTube, TikTok)
    header = (
        f"✨ AVAILABLE NOW ON AMAZON PRIME ✨\n"
        f"🛒 ORDER HERE ➔ {amazon_url}\n"
        f"{divider}"
    )
    footer = (
        f"{divider}\n"
        f"📵 100% Screen-Free • Builds Motor Skills & Focus\n"
        f"📍 Tampa, Florida • 🇺🇸 Printed in USA with Prime\n"
        f"📦 FAST PRIME DELIVERY: {amazon_url}\n"
        f"🎁 FREE ACTIVITY PACK: {landing_url}"
    )
    caption = f"{header}\n\n{base_caption}\n\n{footer}"
    comment = (
        f"🛒 Direct Amazon Purchase Link: {amazon_url}\n"
        f"📵 100% Screen-Free Motor Skills Development | 🇺🇸 Printed in USA with Fast Prime delivery!"
    )
    return caption, comment
