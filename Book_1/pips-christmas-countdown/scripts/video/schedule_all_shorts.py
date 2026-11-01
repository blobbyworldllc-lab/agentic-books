"""
Autonomous YouTube Shorts Scheduler & Publisher for Pip's Christmas Countdown
Channel: BLOBBY WORLD OFFICIAL

Schedules all remaining 24 days (Day 2 to Day 25) to automatically go live 
daily at 09:00 AM EST (14:00 UTC) starting December 2 through December 25.
"""
import os
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

TOKEN_PATH = r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json"
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SHORTS_DIR = BASE_DIR / "output" / "marketing" / "shorts"
LANDING_URL = "https://blobbyworldllc-lab.github.io/agentic-books/"

def get_youtube_client():
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError(f"OAuth token not found at {TOKEN_PATH}")
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube'
    ])
    return build('youtube', 'v3', credentials=creds)

def schedule_short(day: int, publish_date_utc: str = None):
    yt = get_youtube_client()
    video_path = SHORTS_DIR / f"pip_countdown_day_{day:02d}.mp4"
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    title = f"Day {day} of 25! Pip's Christmas Countdown 🐧⭐ #Shorts"
    if len(title) > 100:
        title = title[:97] + "..."

    description = (
        f"Day {day} of 25: Pip's Christmas Countdown! ⭐\n\n"
        f"Can you find Little Star hiding in this picture before the video ends? Tell a grown-up where she is hiding! 👇\n\n"
        f"🎁 Download the FREE 4-page Christmas countdown coloring pack:\n"
        f"{LANDING_URL}\n\n"
        f"Full 110-page paperback on Amazon:\n"
        f"https://www.amazon.com/dp/B0HPZ647J6\n\n"
        f"#BlobbyWorld #ChristmasColoring #ToddlerActivities #ColoringBook #KidsChristmas #ChristmasCountdown #Shorts"
    )

    tags = [
        "Blobby World Official", "Pip's Christmas Countdown", "Christmas coloring",
        "toddler activities", "kids coloring book", "holiday countdown", "find the star",
        "advent activity", "preschool activities", "Shorts"
    ]

    status_dict = {
        'privacyStatus': 'private',
        'selfDeclaredMadeForKids': True
    }
    
    if publish_date_utc:
        status_dict['publishAt'] = publish_date_utc

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '27'
        },
        'status': status_dict
    }

    media = MediaFileUpload(str(video_path), mimetype='video/mp4', resumable=True)
    print(f"Uploading and scheduling Day {day} (Go-live: {publish_date_utc})...")
    req = yt.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = req.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    video_id = response.get('id')
    print(f"[SUCCESS] Scheduled Day {day}! Video ID: {video_id} (Scheduled for: {publish_date_utc})")
    return video_id

def schedule_all_remaining():
    """
    Schedules Day 2 to Day 25 for Dec 2 to Dec 25, 2026 at 14:00 UTC (9:00 AM EST).
    """
    print("Scheduling all remaining countdown days (Day 2 to Day 25)...")
    for day in range(2, 26):
        publish_iso = f"2026-12-{day:02d}T14:00:00Z"
        schedule_short(day, publish_iso)

if __name__ == "__main__":
    schedule_all_remaining()
