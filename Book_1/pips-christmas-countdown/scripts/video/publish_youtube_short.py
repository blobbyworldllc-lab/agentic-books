"""
Automated YouTube Shorts Publisher for Pip's Christmas Countdown
Channel: BLOBBY WORLD OFFICIAL
"""
import os
import sys
import argparse
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

DEFAULT_TOKEN_PATH = r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json"
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SHORTS_DIR = BASE_DIR / "output" / "marketing" / "shorts"
LANDING_URL = "https://blobbyworldllc-lab.github.io/agentic-books/"

def get_youtube_client(custom_token_path=None):
    token_path = custom_token_path or os.environ.get("YOUTUBE_TOKEN_PATH") or DEFAULT_TOKEN_PATH
    if not os.path.exists(token_path):
        raise FileNotFoundError(f"OAuth token not found at {token_path}. In GitHub Actions, ensure YOUTUBE_TOKEN_PATH points to restored secret.")
    creds = Credentials.from_authorized_user_file(token_path, [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube'
    ])
    return build('youtube', 'v3', credentials=creds)

def upload_short(day: int, privacy: str = "public"):
    yt = get_youtube_client()
    video_path = SHORTS_DIR / f"pip_countdown_day_{day:02d}.mp4"
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    title = f"Day {day} of 25! Pip's Christmas Countdown 🐧⭐ #Shorts"
    # Ensure title length complies
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

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '27' # Education / Kids
        },
        'status': {
            'privacyStatus': privacy,
            'selfDeclaredMadeForKids': True
        }
    }

    media = MediaFileUpload(str(video_path), mimetype='video/mp4', resumable=True)
    print(f"Uploading Day {day} Short to BLOBBY WORLD OFFICIAL...")
    req = yt.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = req.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    video_id = response.get('id')
    print(f"[SUCCESS] Uploaded Day {day}! Video URL: https://youtube.com/shorts/{video_id}")
    return video_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", type=int, default=1, help="Day number (1-25)")
    parser.add_argument("--privacy", type=str, default="public", choices=["public", "unlisted", "private"])
    args = parser.parse_args()

    upload_short(args.day, args.privacy)
