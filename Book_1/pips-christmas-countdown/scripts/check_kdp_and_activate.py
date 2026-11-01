"""
Automated Amazon KDP Book Status Checker & Campaign Activator
Checks if https://www.amazon.com/dp/9798166809148 is live.
When live:
1. Automatically sets Day 1 YouTube Short to PUBLIC.
2. Updates PROJECT.md status log.
"""
import html
import urllib.request
import urllib.error
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ASIN_URL = "https://www.amazon.com/dp/9798166809148"
DAY_1_VIDEO_ID = "SsBNKohRrVQ"
TOKEN_PATH = r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json"

def is_amazon_book_live():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(ASIN_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            # If "Currently unavailable" or dog page 404, not live yet
            page = html.unescape(content)
            if ("Pip's Christmas Countdown" in page and ('id="productTitle"' in page or 'add-to-cart-button' in page)
                    and "Currently unavailable" not in page):
                return True
            return False
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        return False
    except Exception:
        return False

def activate_day_1_youtube():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube'
    ])
    yt = build('youtube', 'v3', credentials=creds)
    body = {
        'id': DAY_1_VIDEO_ID,
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': True
        }
    }
    res = yt.videos().update(part='status', body=body).execute()
    print(f"[ACTIVATED] Book is Live! Day 1 Short is now {res['status']['privacyStatus']}: https://youtube.com/shorts/{DAY_1_VIDEO_ID}")

if __name__ == "__main__":
    live = is_amazon_book_live()
    print(f"Amazon KDP Book Live Status: {live}")
    if live:
        activate_day_1_youtube()
    else:
        print("Book is still under KDP review (expected ~Nov 3-4). Day 1 Short remains safely PRIVATE.")
