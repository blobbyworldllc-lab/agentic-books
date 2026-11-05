# Existing Live YouTube Setup in `agentic-books`

This document details the exact, already-configured YouTube infrastructure in this repository so any AI agent or automated workflow can immediately publish and manage YouTube Shorts without re-authenticating or asking for setup steps.

---

## 1. Where the Active Token Lives

The verified, permanent, non-expiring OAuth2 token is already configured and live in two places:

### A. Local Machine Path (Laptop / Local Agent)
- **Path**: `C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json`
- **Client Secrets**: `C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\client_secrets.json`
- **Target Channel**: `BLOBBY WORLD OFFICIAL` (Channel ID: `UC4jKRU8Con3dPSC1rGkzySg`)
- **Status**: **LIVE & VERIFIED**. Auto-renews silently using its permanent `refresh_token`.
- **Scopes Configured**:
  - `https://www.googleapis.com/auth/youtube.upload`
  - `https://www.googleapis.com/auth/youtube`
  - `https://www.googleapis.com/auth/yt-analytics.readonly`

### B. Cloud / GitHub Actions Path (Zero Laptop Dependency)
- **GitHub Secret Name**: `YOUTUBE_TOKEN_JSON` (configured under repo secrets).
- Contains the exact JSON payload of the authorized `token.json`.

---

## 2. Existing Publishing Script in `agentic-books`

The repository already has the complete publishing script built and ready at:
`Book_1/pips-christmas-countdown/scripts/video/publish_youtube_short.py`

### How It Connects to YouTube
```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

TOKEN_PATH = r"C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json"

def get_youtube_client():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube'
    ])
    return build('youtube', 'v3', credentials=creds)
```

---

## 3. How Any AI / Background Job Can Publish a Short Right Now

### Command-Line Execution
To publish any countdown day video directly to **BLOBBY WORLD OFFICIAL**:
```bash
python Book_1/pips-christmas-countdown/scripts/video/publish_youtube_short.py --day 1 --privacy public
```

### Video Assets Directory
Prepared MP4 shorts are located at:
`Book_1/pips-christmas-countdown/output/marketing/shorts/pip_countdown_day_XX.mp4`

### Automatic Description Formatting
Every uploaded short automatically formats the title, hashtags, and Amazon purchase link:
- **Title**: `Day {X} of 25! Pip's Christmas Countdown 🐧⭐ #Shorts`
- **Top of Description**: Features the direct Amazon paperback purchase link (`https://www.amazon.com/dp/B0HPZ647J6`) and the free printable activity pack link (`https://blobbyworldllc-lab.github.io/agentic-books/`).
- **Category**: `27` (Education / Kids) with `selfDeclaredMadeForKids=True`.

---

## 4. Universal Instructions for Future AI Agents
1. **Never ask the user to log in or create a token**: The token already exists at `C:\Users\movov\Videos\BlobbyWorld\blobby_pipeline\token.json`.
2. **Never overwrite or re-authenticate**: The existing `token.json` has `refresh_token` configured under Google Cloud project `blobbyworld-uploader` in **Production** mode, which never expires.
3. **In GitHub Actions**: Always read from `${{ secrets.YOUTUBE_TOKEN_JSON }}` and write it to `token.json` before executing any upload script.
