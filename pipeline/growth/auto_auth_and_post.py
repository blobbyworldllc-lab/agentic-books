"""
Autonomous YouTube OAuth & Comment Poster Runner
"""
import os
import sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CLIENT_SECRETS_FILE = Path(r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\client_secrets.json")
TOKEN_FILE = Path(r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json")

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]

def run_auth_and_post():
    if not CLIENT_SECRETS_FILE.exists():
        print(f"[ERROR] Client secrets not found at: {CLIENT_SECRETS_FILE}", flush=True)
        return False

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE),
        scopes=SCOPES
    )

    print("[OAUTH] Starting local server on http://localhost:8095/ and opening system browser...", flush=True)
    try:
        creds = flow.run_local_server(
            port=8095,
            prompt="consent",
            open_browser=True,
            timeout_seconds=600,
            success_message="YouTube comment authorization successful! You can now close this tab."
        )

        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print(f"\n[SUCCESS] Token updated with youtube.force-ssl at {TOKEN_FILE}!", flush=True)

        # Automatically post comments to all live shorts
        print("\n[POSTING] Triggering automated comment posting across all live Shorts...", flush=True)
        sys.path.insert(0, str(REPO_ROOT))
        from pipeline.growth.youtube_comment_poster import post_all_comments
        results = post_all_comments()
        print(f"[COMPLETE] Comment posting results: {results}", flush=True)
        return True
    except Exception as e:
        print(f"[ERROR] OAuth or posting failed: {e}", flush=True)
        return False

if __name__ == "__main__":
    run_auth_and_post()
