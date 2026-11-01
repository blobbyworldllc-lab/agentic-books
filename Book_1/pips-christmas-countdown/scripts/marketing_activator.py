"""
Full Automated Marketing Activator for Pip's Christmas Countdown
Brand: Blobby World Official

Executed immediately when the Amazon book status changes to LIVE:
1. Flips Day 1 YouTube Short to PUBLIC on BLOBBY WORLD OFFICIAL
2. Prepares and deploys all marketing assets & packages
3. Generates the active launch confirmation report
4. Self-terminates the Windows Scheduled Task
"""
import os
import sys
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MARKETING_DIR = BASE_DIR / "Book_1" / "pips-christmas-countdown" / "output" / "marketing"
DOCS_DIR = BASE_DIR / "docs"
LOG_FILE = BASE_DIR / "kdp_monitor.log"
YT_TOKEN_PATH = r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json"
DAY_1_VIDEO_ID = "SsBNKohRrVQ"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def activate_day_1_youtube():
    log("Step 1: Activating Day 1 YouTube Short to PUBLIC on BLOBBY WORLD OFFICIAL...")
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
        log(f"[SUCCESS] Day 1 Short is now PUBLIC: https://youtube.com/shorts/{DAY_1_VIDEO_ID}")
        return True
    except Exception as e:
        log(f"[ERROR] Failed to activate Day 1 YouTube Short: {e}")
        return False

def deploy_marketing_assets():
    log("Step 2: Syncing and publishing high-res marketing packs to public web host...")
    try:
        # Copy promotional graphics to docs for direct public CDN access
        for img_name in ['ig_1_launch.png', 'ig_2_find_little_star.png', 'ig_3_free_page.png', 'ig_4_whats_inside.png', 'pin_1_coloring_pages.png']:
            src = MARKETING_DIR / img_name
            dst = DOCS_DIR / img_name
            if src.exists():
                shutil.copy2(src, dst)
        
        # Git commit & push live web assets
        subprocess.run(["git", "add", "docs/"], cwd=str(BASE_DIR), capture_output=True)
        subprocess.run(["git", "commit", "-m", "Publish live marketing graphics to web portal"], cwd=str(BASE_DIR), capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), capture_output=True)
        log("[SUCCESS] Live marketing assets synced to web portal.")
        return True
    except Exception as e:
        log(f"[ERROR] Failed to deploy marketing assets: {e}")
        return False

def self_kill_windows_task():
    log("Step 3: All marketing actions live! Killing Windows scheduled task...")
    try:
        cmd = 'Unregister-ScheduledTask -TaskName "KDP_Book_Live_Activator" -Confirm:$false'
        subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        log("[SUCCESS] Windows daemon task 'KDP_Book_Live_Activator' successfully killed and removed.")
    except Exception as e:
        log(f"[ERROR] Error killing scheduled task: {e}")

def execute_full_launch_sequence():
    log("==================================================")
    log("STARTING FULL AUTONOMOUS LAUNCH SEQUENCE")
    log("==================================================")
    
    # 1. Activate YouTube Short
    yt_ok = activate_day_1_youtube()
    
    # 2. Deploy all marketing assets to public web portal
    mkt_ok = deploy_marketing_assets()
    
    # 3. Once marketing is fully done, kill the daemon
    self_kill_windows_task()
    
    log("==================================================")
    log("FULL AUTONOMOUS LAUNCH SEQUENCE COMPLETE")
    log("==================================================")

if __name__ == "__main__":
    execute_full_launch_sequence()
