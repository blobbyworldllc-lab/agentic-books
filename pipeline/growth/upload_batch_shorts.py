"""
Autonomous YouTube Batch Shorts Uploader
Uploads and syndicates Pip's Christmas Countdown 3D animated shorts with:
1. Master Amazon CTA Outro ("Check the description to buy our book on Amazon!")
2. Direct Amazon Purchase Link (https://www.amazon.com/dp/B0HPZ647J6)
3. Direct Playlist Syndication (PLMfyshV9ONIw & PLQzA_sHOsoXc)
4. High-Intent VSEO keywords
"""
import os
import sys
import json
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

TOKEN_PATH = r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json"
SHORTS_DIR = REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "output" / "marketing" / "shorts"
UPLOAD_HISTORY_FILE = REPO_ROOT / "pipeline" / "growth" / "youtube_upload_history.json"

DAYS_METADATA = {
    5: {
        "title": "Pip Brings Home the Christmas Tree! | Holiday Bedtime Story #Shorts",
        "description": "Pip found a small tree, as green as can be. Can you find Little Star hiding in the branches?\n\nBuy Pip's Christmas Countdown Paperback on Amazon Prime:\nhttps://www.amazon.com/dp/B0HPZ647J6\n\nFree Printable Activity Pack:\nhttps://blobbyworldllc-lab.github.io/agentic-books/\n\n#Shorts #ChristmasColoring #ToddlerActivities #BedtimeStories #PipsChristmasCountdown #KidsAnimation",
        "tags": ["Pips Christmas Countdown", "Christmas Tree", "Toddler Bedtime Story", "Christmas Coloring Book", "Kids Holiday Animation", "Shorts"]
    },
    6: {
        "title": "Shiny Ornaments with Pip! Christmas Tree Decorating #Shorts",
        "description": "Shiny round ornaments went up one by one! Pip hung up the last one. Can you spot Little Star?\n\nBuy Pip's Christmas Countdown Paperback on Amazon Prime:\nhttps://www.amazon.com/dp/B0HPZ647J6\n\nFree Printable Activity Pack:\nhttps://blobbyworldllc-lab.github.io/agentic-books/\n\n#Shorts #ChristmasColoring #ToddlerActivities #BedtimeStories #PipsChristmasCountdown #KidsAnimation",
        "tags": ["Pips Christmas Countdown", "Christmas Ornaments", "Toddler Bedtime Story", "Christmas Coloring Book", "Kids Holiday Animation", "Shorts"]
    },
    7: {
        "title": "Something is Missing on the Treetop! Pip's Mystery #Shorts",
        "description": "Pip looked at the treetop, so empty and bare. Can you find where Little Star went?\n\nBuy Pip's Christmas Countdown Paperback on Amazon Prime:\nhttps://www.amazon.com/dp/B0HPZ647J6\n\nFree Printable Activity Pack:\nhttps://blobbyworldllc-lab.github.io/agentic-books/\n\n#Shorts #ChristmasColoring #ToddlerActivities #BedtimeStories #PipsChristmasCountdown #KidsAnimation",
        "tags": ["Pips Christmas Countdown", "Christmas Tree Top", "Toddler Bedtime Story", "Kids Holiday Animation", "Shorts"]
    },
    8: {
        "title": "Baking Holiday Cookies with Bo the Bear! #Shorts",
        "description": "Bo helped Pip bake cookies, warm, golden and sweet! Did Bo sneak a treat?\n\nBuy Pip's Christmas Countdown Paperback on Amazon Prime:\nhttps://www.amazon.com/dp/B0HPZ647J6\n\nFree Printable Activity Pack:\nhttps://blobbyworldllc-lab.github.io/agentic-books/\n\n#Shorts #ChristmasColoring #ToddlerActivities #BedtimeStories #PipsChristmasCountdown #KidsAnimation",
        "tags": ["Pips Christmas Countdown", "Christmas Cookies", "Toddler Bedtime Story", "Kids Holiday Animation", "Shorts"]
    },
    9: {
        "title": "Pip's Giant Gingerbread House! Holiday Magic #Shorts",
        "description": "Gumdrops and frosting and candy-cane beams! Pip built the gingerbread house of his dreams.\n\nBuy Pip's Christmas Countdown Paperback on Amazon Prime:\nhttps://www.amazon.com/dp/B0HPZ647J6\n\nFree Printable Activity Pack:\nhttps://blobbyworldllc-lab.github.io/agentic-books/\n\n#Shorts #ChristmasColoring #ToddlerActivities #BedtimeStories #PipsChristmasCountdown #KidsAnimation",
        "tags": ["Pips Christmas Countdown", "Gingerbread House", "Toddler Bedtime Story", "Kids Holiday Animation", "Shorts"]
    },
    10: {
        "title": "Tangled in Ribbon! Giant Present Wrapping #Shorts",
        "description": "Pip wrapped a present so giant and wide, he got himself tangled in ribbon inside!\n\nBuy Pip's Christmas Countdown Paperback on Amazon Prime:\nhttps://www.amazon.com/dp/B0HPZ647J6\n\nFree Printable Activity Pack:\nhttps://blobbyworldllc-lab.github.io/agentic-books/\n\n#Shorts #ChristmasColoring #ToddlerActivities #BedtimeStories #PipsChristmasCountdown #KidsAnimation",
        "tags": ["Pips Christmas Countdown", "Gift Wrapping", "Toddler Bedtime Story", "Kids Holiday Animation", "Shorts"]
    }
}

def load_upload_history():
    if UPLOAD_HISTORY_FILE.exists():
        try:
            return json.loads(UPLOAD_HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"uploaded_days": [1, 2, 3], "videos": {}}

def save_upload_history(data):
    UPLOAD_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    UPLOAD_HISTORY_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def upload_day(day_num):
    history = load_upload_history()
    if day_num in history.get("uploaded_days", []):
        print(f"Day {day_num} already uploaded. Skipping.")
        return history["videos"].get(str(day_num))

    video_file = SHORTS_DIR / f"pip_countdown_day_{day_num:02d}.mp4"
    if not video_file.exists():
        print(f"Video file {video_file} not found!")
        return None

    meta = DAYS_METADATA.get(day_num)
    if not meta:
        print(f"No metadata for day {day_num}")
        return None

    creds = Credentials.from_authorized_user_file(TOKEN_PATH, [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube'
    ])
    yt = build('youtube', 'v3', credentials=creds)

    body = {
        'snippet': {
            'title': meta['title'],
            'description': meta['description'],
            'tags': meta['tags'],
            'categoryId': '24'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': True
        }
    }

    print(f"Uploading Day {day_num}: {meta['title']}...")
    media = MediaFileUpload(str(video_file), mimetype='video/mp4', resumable=True)
    req = yt.videos().insert(part='snippet,status', body=body, media_body=media)
    resp = req.execute()

    vid_id = resp.get('id')
    print(f"SUCCESS! Day {day_num} Uploaded: https://youtube.com/shorts/{vid_id}")

    # Add to public playlists
    for pl_id in ["PLMfyshV9ONIw", "PLQzA_sHOsoXc"]:
        try:
            yt.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': pl_id,
                        'resourceId': {'kind': 'youtube#video', 'videoId': vid_id}
                    }
                }
            ).execute()
            print(f"Added Day {day_num} to playlist {pl_id}")
        except Exception as e:
            print(f"Playlist insertion error: {e}")

    history["uploaded_days"].append(day_num)
    history["videos"][str(day_num)] = vid_id
    save_upload_history(history)
    return vid_id

def upload_next_available():
    history = load_upload_history()
    uploaded = set(history.get("uploaded_days", []))
    for d in sorted(DAYS_METADATA.keys()):
        if d not in uploaded:
            return upload_day(d)
    return None

if __name__ == "__main__":
    upload_next_available()
