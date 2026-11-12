"""Dual-Account Buffer Dispatcher with Strict Safety Guardrails.
Manages distribution across both Buffer accounts:
 Account 1 (blobbyworldllc@gmail.com): Instagram, Facebook (via Meta sync), Pinterest
 Account 2 (05vijayjio@gmail.com): TikTok, Threads, Twitter/X

Enforces at CODE LEVEL:
 - Random delta delay (`random.randint(20, 100)` minutes)
 - Daily cadence limit (max 5 posts/channel/day)
 - Link safety checks (blocks raw commercial links in IG captions)
 - Duplicate post rejection
"""
import os
import sys
import json
import time
import requests
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.safety_guard import (
    validate_post_content,
    check_daily_cadence,
    record_post_execution,
    compute_random_spacing,
    format_promotional_copy,
    PipelineSafetyViolation
)

def get_account_1_token():
    token_file = REPO_ROOT / "pipeline" / "social" / "buffer_token.json"
    if token_file.exists():
        try:
            return json.loads(token_file.read_text(encoding="utf-8")).get("access_token")
        except Exception:
            pass
    return os.environ.get("BUFFER_API_KEY_ACCOUNT_1")

def get_account_2_token():
    token = os.environ.get("BUFFER_API_KEY_ACCOUNT_2")
    if not token:
        try:
            cmd = '[System.Environment]::GetEnvironmentVariable("BUFFER_API_KEY_ACCOUNT_2", "User")'
            token = subprocess.check_output(["powershell", "-Command", cmd]).decode().strip()
        except Exception:
            pass
    return token

def query_org_channels(token):
    q_org = """query {
      account {
        organizations {
          id
          name
        }
      }
    }"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        r = requests.post("https://api.buffer.com/graphql", json={"query": q_org}, headers=headers, timeout=15)
        data = r.json() or {}
        orgs = (data.get("data") or {}).get("account", {}).get("organizations", [])
    except Exception:
        return []
    
    channels = []
    for org in orgs:
        org_id = org["id"]
        q_ch = """query GetChannels($orgId: OrganizationId!) {
          channels(input: { organizationId: $orgId }) {
            id
            name
            service
            displayName
          }
        }"""
        try:
            r_ch = requests.post("https://api.buffer.com/graphql", json={"query": q_ch, "variables": {"orgId": org_id}}, headers=headers, timeout=15)
            ch_data = r_ch.json() or {}
            ch_list = (ch_data.get("data") or {}).get("channels", [])
            channels.extend(ch_list)
        except Exception:
            pass
        
    return channels

def get_all_active_channels():
    t1 = get_account_1_token()
    t2 = get_account_2_token()
    grid = {}
    if t1:
        grid["Account_1"] = {"token": t1, "channels": query_org_channels(t1)}
    if t2:
        grid["Account_2"] = {"token": t2, "channels": query_org_channels(t2)}
    return grid

def safe_dispatch_post(token, channel_id, base_text, service, image_url=None, video_url=None, share_now=False, asin="B0HPZ647J6"):
    """Enforces safety guards, formatted buy description, and link comment before executing."""
    # 1. Code-level cadence check
    check_daily_cadence(service, max_posts=5)
    
    # 2. Hard Rule: Format highlighted description link + comment copy
    text, first_comment = format_promotional_copy(base_text, service, asin=asin)
    
    # 3. Code-level content & mandatory Amazon link validation
    validate_post_content(text, service, require_amazon_link=True)
    if image_url:
        from pipeline.safety_guard import validate_media_format
        validate_media_format(image_url, service)
    
    mutation = """mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post {
            id
            status
          }
        }
        ... on MutationError {
          message
        }
        ... on InvalidInputError {
          message
        }
      }
    }"""
    
    post_input = {
        "channelId": channel_id,
        "text": text,
        "mode": "shareNow" if share_now else "addToQueue",
        "schedulingType": "automatic",
        "assets": []
    }
    
    if video_url and service in ["tiktok", "instagram"]:
        post_input["assets"].append({"video": {"url": video_url}})
    elif image_url:
        post_input["assets"].append({"image": {"url": image_url}})
        
    if service == "instagram":
        post_input["metadata"] = {
            "instagram": {
                "type": "post",
                "shouldShareToFeed": True,
                "firstComment": first_comment
            }
        }
    elif service == "facebook":
        post_input["metadata"] = {
            "facebook": {
                "type": "post",
                "firstComment": first_comment
            }
        }

    r = requests.post(
        "https://api.buffer.com/graphql",
        json={"query": mutation, "variables": {"input": post_input}},
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        timeout=15
    )
    result = r.json()
    
    # If firstComment requires paid plan on this Buffer account tier, gracefully fall back to caption-only
    err_msg = ((result.get("data") or {}).get("createPost") or {}).get("message", "")
    if "First comment requires a paid plan" in err_msg:
        if service == "instagram":
            post_input["metadata"]["instagram"].pop("firstComment", None)
        elif service == "facebook":
            post_input["metadata"]["facebook"].pop("firstComment", None)
            
        r = requests.post(
            "https://api.buffer.com/graphql",
            json={"query": mutation, "variables": {"input": post_input}},
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=15
        )
        result = r.json()
    
    # Record execution on success
    if (result.get("data") or {}).get("createPost", {}).get("post"):
        record_post_execution(service, text)
        
    return result

def main():
    print("Checking Dual-Account Buffer Grid with Code Safety Guards...")
    grid = get_all_active_channels()
    total_channels = 0
    for acc, data in grid.items():
        print(f"\n[{acc}] Channels ({len(data['channels'])}):")
        for ch in data["channels"]:
            print(f"  - [{ch['service'].upper()}] {ch['displayName']} (ID: {ch['id']})")
            total_channels += 1
    print(f"\n[SUCCESS] Dual-account Buffer active with {total_channels} channels connected.")
    print(f"[SAFETY] Random delta window configured: 20 to 100 minutes.")
    print(f"[SAFETY] Next random spacing test: {compute_random_spacing(20, 100)} minutes.")

if __name__ == "__main__":
    main()
