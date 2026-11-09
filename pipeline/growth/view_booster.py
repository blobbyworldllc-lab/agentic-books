"""
View Booster Engine — Automated Video SEO, Closed-Loop Recommendations,
Playlist Syndication, and Multi-Platform View Acceleration.
"""

import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

VIEW_METRICS_FILE = REPO_ROOT / "pipeline" / "growth" / "view_metrics.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Canonical Videos & Watch Loop Configuration
PIP_VIDEOS = {
    "HfQJeqQ23jg": {
        "title": "Pip Goes Sledding! 🛷 Cutest Christmas Sled Ride #Shorts",
        "action": "zooms down Snowy Hill on his red wooden sled! Can you hear his cheerful giggles as snowflakes swirl all around?",
        "next_videos": [
            ("Pip Goes Ice Skating! ⛸️", "https://youtube.com/shorts/NuFvuM8Q2bg"),
            ("Pip Decorates the Christmas Tree! 🎄", "https://youtube.com/shorts/yxkljv_Y5F4"),
            ("Pip Colors a Snowflake! ❄️", "https://youtube.com/shorts/v24c4QH0XWQ")
        ],
        "tags": [
            "Blobby World Official",
            "Pip the penguin",
            "Pip Goes Sledding",
            "Pip Christmas Countdown",
            "Christmas countdown for toddlers",
            "Christmas bedtime stories",
            "Christmas coloring book for kids",
            "toddler Christmas animation",
            "kids Christmas activities",
            "preschool advent calendar",
            "screen free toddler activities",
            "preschool Christmas crafts",
            "cute penguin cartoon",
            "find little star game"
        ]
    },
    "NuFvuM8Q2bg": {
        "title": "Pip Goes Ice Skating! ⛸️ Toddler Christmas Fun #Shorts",
        "action": "twirls and glides across the frozen pond! Watch his cute little penguin waddle on the slippery ice!",
        "next_videos": [
            ("Pip Decorates the Christmas Tree! 🎄", "https://youtube.com/shorts/yxkljv_Y5F4"),
            ("Pip Goes Sledding! 🛷", "https://youtube.com/shorts/HfQJeqQ23jg"),
            ("Pip Colors a Snowflake! ❄️", "https://youtube.com/shorts/v24c4QH0XWQ")
        ],
        "tags": [
            "Blobby World Official",
            "Pip the penguin",
            "Pip Goes Ice Skating",
            "Pip Christmas Countdown",
            "Christmas countdown for toddlers",
            "Christmas bedtime stories",
            "Christmas coloring book for kids",
            "toddler Christmas animation",
            "kids Christmas activities",
            "preschool advent calendar",
            "screen free toddler activities",
            "preschool Christmas crafts",
            "cute penguin cartoon",
            "find little star game"
        ]
    },
    "yxkljv_Y5F4": {
        "title": "Pip Decorates the Christmas Tree! 🎄 Holiday Bedtime Magic #Shorts",
        "action": "hangs shiny red baubles and glowing stars on the big evergreen Christmas tree with his holiday friends!",
        "next_videos": [
            ("Pip Goes Sledding! 🛷", "https://youtube.com/shorts/HfQJeqQ23jg"),
            ("Pip Goes Ice Skating! ⛸️", "https://youtube.com/shorts/NuFvuM8Q2bg"),
            ("Pip Colors a Snowflake! ❄️", "https://youtube.com/shorts/v24c4QH0XWQ")
        ],
        "tags": [
            "Blobby World Official",
            "Pip the penguin",
            "Pip Decorates the Christmas Tree",
            "Pip Christmas Countdown",
            "Christmas countdown for toddlers",
            "Christmas bedtime stories",
            "Christmas coloring book for kids",
            "toddler Christmas animation",
            "kids Christmas activities",
            "preschool advent calendar",
            "screen free toddler activities",
            "preschool Christmas crafts",
            "cute penguin cartoon",
            "find little star game"
        ]
    }
}

PRIMARY_PLAYLIST_ID = "PLMfyshV9ONIw"
AMAZON_BUY_URL = "https://www.amazon.com/dp/B0HPZ647J6"
FREE_STARTER_URL = "https://blobbyworldllc-lab.github.io/agentic-books/"

def get_youtube_service():
    """Locate and return authenticated YouTube API client."""
    candidate_tokens = [
        Path(r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json"),
        REPO_ROOT / "pipeline" / "social" / "token.json",
        Path.home() / "Videos" / "BlobbyWorld" / "blobby_pipeline" / "token.json"
    ]
    for token_path in candidate_tokens:
        if token_path.exists():
            try:
                from googleapiclient.discovery import build
                from google.oauth2.credentials import Credentials
                creds = Credentials.from_authorized_user_file(str(token_path), [
                    'https://www.googleapis.com/auth/youtube.upload',
                    'https://www.googleapis.com/auth/youtube'
                ])
                return build('youtube', 'v3', credentials=creds)
            except Exception as e:
                logging.warning(f"Failed to load credentials from {token_path}: {e}")
    return None

def build_optimized_description(vid_id, config):
    """Build high-converting description with watch loop, links, and hashtags."""
    next_links_str = "\n".join([f"👉 {label} {url}" for label, url in config["next_videos"]])
    
    desc = f"""Pip the baby penguin {config['action']}

🎄 WATCH FULL CHRISTMAS COUNTDOWN PLAYLIST:
👉 https://www.youtube.com/playlist?list={PRIMARY_PLAYLIST_ID}

❄️ WATCH NEXT (CONTINUE THE HOLIDAY FUN!):
{next_links_str}

📖 ORDER THE 110-PAGE PAPERBACK (Amazon Prime):
👉 {AMAZON_BUY_URL}
(25 Daily Rhymes + 25 Large Coloring Pages + "Find Little Star" Game on Every Page!)

🎨 DOWNLOAD FREE 4-PAGE STARTER PACK:
👉 {FREE_STARTER_URL}

#Shorts #ChristmasForKids #ToddlerActivities #PipThePenguin #ChristmasCountdown #ColoringBook #PreschoolActivities #BedtimeStories #ToddlerBooks #ScreenFreeKids #BlobbyWorld"""
    return desc

def optimize_youtube_vseo(yt=None):
    """
    Applies 500-char search-intent tags and closed-loop recommendations to all Pip videos.
    """
    if not yt:
        yt = get_youtube_service()
    if not yt:
        logging.error("YouTube service unavailable for VSEO optimization.")
        return False, "No YouTube credentials found"

    results = {}
    for vid, cfg in PIP_VIDEOS.items():
        try:
            v_res = yt.videos().list(part="snippet", id=vid).execute()
            if not v_res.get("items"):
                results[vid] = "Not found"
                continue
            
            snippet = v_res["items"][0]["snippet"]
            new_desc = build_optimized_description(vid, cfg)
            
            snippet["tags"] = cfg["tags"]
            snippet["description"] = new_desc
            
            update_body = {
                "id": vid,
                "snippet": snippet
            }
            yt.videos().update(part="snippet", body=update_body).execute()
            logging.info(f"[VSEO BOOST] Optimized {cfg['title']} (ID: {vid}) with {len(cfg['tags'])} tags & watch loop.")
            results[vid] = "Optimized"
        except Exception as e:
            logging.error(f"[VSEO BOOST] Failed for {vid}: {e}")
            results[vid] = f"Error: {e}"
            
    return True, results

def ensure_secondary_holiday_playlist(yt=None):
    """
    Ensures a second high-intent activity playlist exists for extra search indexing:
    'Christmas Coloring Pages & Holiday Activities for Kids | Blobby World'
    """
    if not yt:
        yt = get_youtube_service()
    if not yt:
        return False, "No YouTube client"

    try:
        # Check if secondary playlist already exists
        pl_res = yt.playlists().list(mine=True, part='snippet', maxResults=50).execute()
        existing = pl_res.get('items', [])
        sec_title = "Christmas Coloring & Holiday Activities for Kids 🎨 | Pip & Blobby World"
        
        target_pl_id = None
        for p in existing:
            if "Christmas Coloring & Holiday Activities" in p["snippet"]["title"]:
                target_pl_id = p["id"]
                break
                
        if not target_pl_id:
            body = {
                "snippet": {
                    "title": sec_title,
                    "description": "Fun Christmas coloring activities, bedtime stories, and holiday countdowns for toddlers and preschoolers!\n\nGrab the 110-page paperback on Amazon: https://www.amazon.com/dp/B0HPZ647J6\nFree Printable Pack: https://blobbyworldllc-lab.github.io/agentic-books/",
                    "tags": ["christmas coloring pages", "toddler christmas", "preschool activities", "pip penguin"]
                },
                "status": {"privacyStatus": "public"}
            }
            create_res = yt.playlists().insert(part="snippet,status", body=body).execute()
            target_pl_id = create_res["id"]
            logging.info(f"[PLAYLIST CREATED] Secondary activity playlist: {target_pl_id}")
            
            # Add videos to secondary playlist with retry
            import time
            for vid in PIP_VIDEOS.keys():
                for attempt in range(3):
                    try:
                        time.sleep(1.0)
                        yt.playlistItems().insert(
                            part="snippet",
                            body={
                                "snippet": {
                                    "playlistId": target_pl_id,
                                    "resourceId": {"kind": "youtube#video", "videoId": vid}
                                }
                            }
                        ).execute()
                        break
                    except Exception as err:
                        if attempt == 2:
                            logging.warning(f"Failed to add {vid} to secondary playlist: {err}")
                        time.sleep(2.0)
            logging.info(f"[PLAYLIST SEEDED] Added all Pip animated videos to {target_pl_id}")
        else:
            logging.info(f"[PLAYLIST EXISTS] Secondary playlist active: {target_pl_id}")
            
        return True, target_pl_id
    except Exception as e:
        logging.error(f"Error ensuring secondary playlist: {e}")
        return False, str(e)

def audit_and_record_views(yt=None):
    """Fetch live view counts and append to historical view metrics."""
    if not yt:
        yt = get_youtube_service()
    if not yt:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    record = {
        "timestamp": now_iso,
        "videos": {}
    }
    
    total_pip_views = 0
    for vid, cfg in PIP_VIDEOS.items():
        try:
            v_res = yt.videos().list(part="statistics", id=vid).execute()
            if v_res.get("items"):
                stats = v_res["items"][0]["statistics"]
                views = int(stats.get("viewCount", 0))
                likes = int(stats.get("likeCount", 0))
                comments = int(stats.get("commentCount", 0))
                record["videos"][vid] = {
                    "title": cfg["title"],
                    "views": views,
                    "likes": likes,
                    "comments": comments
                }
                total_pip_views += views
        except Exception as e:
            logging.error(f"Failed to fetch stats for {vid}: {e}")
            
    record["total_pip_views"] = total_pip_views
    
    # Save to file
    history = []
    if VIEW_METRICS_FILE.exists():
        try:
            history = json.loads(VIEW_METRICS_FILE.read_text(encoding="utf-8"))
        except Exception:
            history = []
            
    history.append(record)
    history = history[-100:]  # Keep last 100 audits
    VIEW_METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    VIEW_METRICS_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")
    logging.info(f"[VIEW AUDIT] Recorded views snapshot: {total_pip_views} total Pip views.")
    return record

def run_view_booster():
    """Master routine to trigger all view boosting mechanisms."""
    logging.info("=== Running View Booster Automation ===")
    yt = get_youtube_service()
    actions = []
    
    if yt:
        # 1. Update Video SEO & Watch Loops
        ok, res = optimize_youtube_vseo(yt)
        actions.append(f"VSEO Optimization: {ok}")
        
        # 2. Ensure Secondary Activity Playlist
        pl_ok, pl_res = ensure_secondary_holiday_playlist(yt)
        actions.append(f"Activity Playlist: {pl_res}")
        
        # 3. Audit & Record Velocity
        stats = audit_and_record_views(yt)
        if stats:
            actions.append(f"Current Views Recorded: {stats['total_pip_views']}")
    else:
        actions.append("YouTube service unavailable")
        
    logging.info("=== View Booster Automation Finished ===")
    return actions

if __name__ == "__main__":
    run_view_booster()
