# Setting Up a Permanent, Non-Expiring YouTube API Token for Automated Uploads

This guide provides the exact architectural procedure to configure a **permanent, non-expiring OAuth2 token** for automated YouTube Shorts and video publishing (via YouTube Data API v3). Any agent or developer can follow these instructions to reproduce or verify the setup.

---

## 1. Why YouTube Tokens Expire (The Root Cause)

Standard Google OAuth2 `access_token`s expire after **1 hour (3,600 seconds)**. Automated background uploaders rely on a `refresh_token` to automatically renew access without human login.

However, Google enforces two strict rules on `refresh_token`s:
1. **The 7-Day Expiration Trap ("Testing" Mode)**: If the Google Cloud Project's OAuth consent screen Publishing Status is set to **"Testing"**, all issued refresh tokens are hard-capped to **expire in exactly 7 days**, causing automated pipelines to fail with `invalid_grant: Token has been expired or revoked`.
2. **Missing `access_type="offline"` and `prompt="consent"`**: If the initial authorization flow does not explicitly request offline access and force consent prompt, Google does not return a permanent `refresh_token`.

---

## 2. Step-by-Step Procedure to Make the Token Permanent

### Step A: Google Cloud Console Configuration
1. Navigate to [Google Cloud Console](https://console.cloud.google.com/) and select the project (e.g., `blobbyworld-uploader`).
2. Go to **APIs & Services > Enabled APIs & Services** and ensure **YouTube Data API v3** is enabled.
3. Go to **APIs & Services > OAuth consent screen**:
   - Set **User Type**: **External**.
   - Fill in mandatory branding fields: **App Name** (`BlobbyWorld Uploader`), **User Support Email**, and **Developer Contact Email**.
   - **CRITICAL STEP**: Look at **Publishing Status**. If it displays **Testing**, click **"PUBLISH APP"** and confirm.
   - *Note on Verification*: YouTube Data API upload scopes are sensitive. Publishing without verification shows an "unverified app" warning during the initial one-time login screen (click "Advanced > Go to App (unsafe)"), but **it completely removes the 7-day token cap**.
4. Go to **APIs & Services > Credentials**:
   - Create an **OAuth 2.0 Client ID** of type **Desktop App** (or Web Application with `http://localhost:8080/` redirect).
   - Download the JSON credentials as `client_secrets.json`.

---

### Step B: The Permanent Authorization Script (`generate_permanent_token.py`)

Run this Python script once on any local machine with a browser. It forces Google to issue a permanent offline `refresh_token`.

```python
"""
Generate a Permanent, Auto-Renewing YouTube OAuth2 Token.
Requires: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
"""
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import json

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

def generate_token(client_secrets_path="client_secrets.json", output_token_path="token.json"):
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_path,
        scopes=SCOPES
    )
    
    # CRITICAL: access_type='offline' and prompt='consent' guarantee a permanent refresh_token
    creds = flow.run_local_server(
        port=8080,
        access_type="offline",
        prompt="consent"
    )
    
    # Save the authorized user credentials
    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
        "expiry": creds.expiry.isoformat() if creds.expiry else None
    }
    
    Path(output_token_path).write_text(json.dumps(token_data, indent=2), encoding="utf-8")
    print(f"[SUCCESS] Permanent token generated and saved to {output_token_path}")
    print(f"Refresh Token Present: {bool(creds.refresh_token)}")

if __name__ == "__main__":
    generate_token()
```

---

### Step C: Automated Reusable Upload Code (`youtube_uploader.py`)

Any agent or daemon can now upload videos/Shorts autonomously. When the 1-hour `token` expires, the Google client library uses the `refresh_token` to renew it automatically behind the scenes with zero prompts or human intervention:

```python
import os
import json
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def get_authenticated_service(token_path="token.json"):
    token_file = Path(token_path)
    if not token_file.exists():
        raise FileNotFoundError(f"Missing OAuth token: {token_path}")
        
    creds = Credentials.from_authorized_user_file(str(token_file))
    
    # Automatically refresh expired access tokens using the permanent refresh_token
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Update token file with refreshed access token
        token_file.write_text(creds.to_json(), encoding="utf-8")
        
    return build("youtube", "v3", credentials=creds)

def upload_short(video_path, title, description, tags, privacy_status="public"):
    youtube = get_authenticated_service()
    
    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "27"  # Education / Kids
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": True
        }
    }
    
    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded: {int(status.progress() * 100)}%")
            
    video_id = response.get("id")
    print(f"[SUCCESS] YouTube Short Live: https://youtube.com/shorts/{video_id}")
    return video_id
```

---

## 3. GitHub Actions / Cloud Integration (Zero Laptop Dependency)

To run automated uploads in GitHub Actions or any headless cloud worker:
1. Copy the entire contents of the generated `token.json` (as a single JSON string).
2. Go to **GitHub Repository > Settings > Secrets and variables > Actions**.
3. Create a repository secret named **`YOUTUBE_TOKEN_JSON`**.
4. In the GitHub Actions workflow, restore it before uploading:
   ```yaml
   - name: Restore YouTube Token
     env:
       YOUTUBE_TOKEN: ${{ secrets.YOUTUBE_TOKEN_JSON }}
     run: |
       mkdir -p config
       echo "$YOUTUBE_TOKEN" > config/token.json
   ```
This allows scheduled workflows to upload YouTube Shorts 24/7 without requiring the laptop to be powered on.
