"""
Autonomous Dual-Checker Daemon for Pip's Christmas Countdown
Monitors:
1. Direct Amazon Product Page (https://www.amazon.com/dp/9798166809148)
2. Gmail inbox (if token_blobby_gmail.json is provided)

When the book is confirmed LIVE:
- Automatically activates Day 1 YouTube Short to PUBLIC on BLOBBY WORLD OFFICIAL
- Logs the confirmation
- Self-terminates
"""
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ASIN_URL = "https://www.amazon.com/dp/9798166809148"
DAY_1_VIDEO_ID = "SsBNKohRrVQ"
YT_TOKEN_PATH = r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json"
GMAIL_TOKEN_PATH = r"C:\Users\movov\Projects\agentic-books\token_blobby_gmail.json"
LOG_FILE = r"C:\Users\movov\Projects\agentic-books\kdp_monitor.log"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def check_amazon_product():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    req = urllib.request.Request(ASIN_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            if "Pip's Christmas Countdown" in content and "Currently unavailable" not in content and "Dog of Amazon" not in content:
                return True
    except Exception as e:
        pass
    return False

def check_gmail_notification():
    if not os.path.exists(GMAIL_TOKEN_PATH):
        return False
    try:
        creds = Credentials.from_authorized_user_file(GMAIL_TOKEN_PATH, ['https://www.googleapis.com/auth/gmail.readonly'])
        service = build('gmail', 'v1', credentials=creds)
        # Search for recent KDP live approval emails
        query = 'from:(kdp-support@amazon.com OR "Kindle Direct Publishing") ("Pip\'s Christmas Countdown" OR "is now available" OR "is live")'
        results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
        messages = results.get('messages', [])
        return len(messages) > 0
    except Exception as e:
        log(f"Gmail check error: {e}")
        return False

def activate_day_1_youtube():
    try:
        creds = Credentials.from_authorized_user_file(YT_TOKEN_PATH, [
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
        log(f"SUCCESS: Day 1 Short is now PUBLIC: https://youtube.com/shorts/{DAY_1_VIDEO_ID}")
        return True
    except Exception as e:
        log(f"Failed to activate YouTube Short: {e}")
        return False

from marketing_activator import execute_full_launch_sequence

def run_once():
    log("Running 24-hour check for KDP book status...")
    amazon_live = check_amazon_product()
    gmail_live = check_gmail_notification()

    if amazon_live or gmail_live:
        reason = "Amazon direct listing confirmed" if amazon_live else "KDP approval email detected in Gmail"
        log(f"BOOK IS CONFIRMED LIVE ({reason})! Starting full marketing rollout...")
        # Step 1 & 2: Launch all marketing & YouTube public
        # Step 3: Self-kill daemon
        execute_full_launch_sequence()
        return True
    else:
        log("Book is not live yet. Will continue daily 24-hour monitoring.")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        log("Starting daemon loop (checking every 15 minutes)...")
        while True:
            done = run_once()
            if done:
                log("All tasks complete. Exiting daemon.")
                break
            time.sleep(900)  # Check every 15 minutes
    else:
        run_once()
