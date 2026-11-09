"""
Autonomous YouTube Comment & Pinned Link Poster
Pins the official Amazon Prime purchase link to every live promotional Short:
- HfQJeqQ23jg (Pip Goes Sledding!)
- NuFvuM8Q2bg (Pip Goes Ice Skating!)
- yxkljv_Y5F4 (Pip Decorates the Tree!)
- v24c4QH0XWQ (Pip Colors a Christmas Snowflake!)
"""
import os
import sys
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOKEN_PATH = r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json"

ACTIVE_SHORTS = [
    {"id": "HfQJeqQ23jg", "title": "Pip Goes Sledding!"},
    {"id": "NuFvuM8Q2bg", "title": "Pip Goes Ice Skating!"},
    {"id": "yxkljv_Y5F4", "title": "Pip Decorates the Tree!"},
    {"id": "v24c4QH0XWQ", "title": "Pip Colors a Snowflake!"}
]

BUY_COMMENT_TEXT = (
    "🛒 DIRECT AMAZON PRIME PURCHASE LINK:\n"
    "👉 https://www.amazon.com/dp/B0HPZ647J6\n\n"
    "📖 Order 'Pip's Christmas Countdown' Paperback on Amazon Prime!\n"
    "✨ 50 Big & Easy Designs | Bedtime Rhyming Stories | Find Little Star Game on Every Page!\n"
    "🎁 Free Printable 4-Page Activity Pack: https://blobbyworldllc-lab.github.io/agentic-books/"
)

def post_all_comments():
    if not os.path.exists(TOKEN_PATH):
        print(f"Token file {TOKEN_PATH} not found.")
        return False

    with open(TOKEN_PATH, "r") as f:
        d = json.load(f)
    scopes = d.get("scopes", [])

    creds = Credentials.from_authorized_user_file(TOKEN_PATH, scopes)
    yt = build('youtube', 'v3', credentials=creds)

    results = {}
    for short in ACTIVE_SHORTS:
        vid_id = short["id"]
        title = short["title"]
        print(f"\n[POSTING] Posting first comment on '{title}' ({vid_id})...")
        body = {
            'snippet': {
                'videoId': vid_id,
                'topLevelComment': {
                    'snippet': {
                        'textOriginal': BUY_COMMENT_TEXT
                    }
                }
            }
        }
        try:
            res = yt.commentThreads().insert(part='snippet', body=body).execute()
            c_id = res.get('id')
            print(f"[SUCCESS] Comment posted on {vid_id}! ID: {c_id}")
            results[vid_id] = {"status": "success", "comment_id": c_id}
        except Exception as e:
            err = str(e)
            print(f"[ERROR] Failed on {vid_id}: {err}")
            results[vid_id] = {"status": "error", "error": err}

    return results

if __name__ == "__main__":
    post_all_comments()
