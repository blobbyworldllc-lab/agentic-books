"""
Autonomous YouTube OAuth & Comment Poster Runner
Starts a local OAuth flow on port 8095 for 600s with youtube.force-ssl scope.
Once approved, updates token.json and automatically posts first comments
with direct Amazon Prime purchase links to all live YouTube Shorts.
"""
import os
import sys
import webbrowser
import subprocess
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
        scopes=SCOPES,
        redirect_uri="http://localhost:8095/"
    )

    auth_url, _ = flow.authorization_url(prompt="consent")
    print(f"\n[OAUTH] Authorization URL generated:\n{auth_url}\n", flush=True)

    # Launch in default system browser
    try:
        os.startfile(auth_url)
        print("[OAUTH] Launched authorization URL in system browser via ShellExecute.", flush=True)
    except Exception as e:
        print(f"[OAUTH] Could not launch browser automatically: {e}", flush=True)

    print("[OAUTH] Waiting for approval on http://localhost:8095/ (timeout: 600s)...", flush=True)
    try:
        creds = flow.run_local_server(
            port=8095,
            prompt="consent",
            timeout_seconds=600,
            open_browser=False,
            success_message="YouTube comment authorization successful! You can now close this tab."
        )

        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print(f"\n[SUCCESS] Token updated with youtube.force-ssl at {TOKEN_FILE}!", flush=True)

        # Automatically post comments to all live shorts
        print("\n[POSTING] Triggering automated comment posting across all live Shorts...", flush=True)
        from pipeline.growth.youtube_comment_poster import post_all_comments
        results = post_all_comments()
        print(f"[COMPLETE] Comment posting results: {results}", flush=True)
        return True
    except Exception as e:
        print(f"[ERROR] OAuth or posting failed: {e}", flush=True)
        return False

if __name__ == "__main__":
    run_auth_and_post()
