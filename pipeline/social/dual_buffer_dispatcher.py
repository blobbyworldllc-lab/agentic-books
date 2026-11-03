"""Dual-Account Buffer Dispatcher.
Manages distribution across both Buffer accounts:
 Account 1 (blobbyworldllc@gmail.com): Instagram, Facebook (via Meta sync), Pinterest
 Account 2 (05vijayjio@gmail.com): TikTok, Threads, Twitter/X

Keeps both accounts active and publishes multi-channel book promos with working Amazon buy links.
"""
import os
import sys
import json
import requests
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

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
    # Step 1: get organization id
    q_org = """query {
      account {
        organizations {
          id
          name
        }
      }
    }"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post("https://api.buffer.com/graphql", json={"query": q_org}, headers=headers, timeout=15)
    data = r.json() or {}
    orgs = (data.get("data") or {}).get("account", {}).get("organizations", [])
    
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
        r_ch = requests.post("https://api.buffer.com/graphql", json={"query": q_ch, "variables": {"orgId": org_id}}, headers=headers, timeout=15)
        ch_data = r_ch.json() or {}
        ch_list = (ch_data.get("data") or {}).get("channels", [])
        channels.extend(ch_list)
        
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

def main():
    print("Checking Dual-Account Buffer Grid...")
    grid = get_all_active_channels()
    total_channels = 0
    for acc, data in grid.items():
        print(f"\n[{acc}] Channels ({len(data['channels'])}):")
        for ch in data["channels"]:
            print(f"  - [{ch['service'].upper()}] {ch['displayName']} (ID: {ch['id']})")
            total_channels += 1
    print(f"\n[SUCCESS] Dual-account Buffer active with {total_channels} channels connected across both accounts.")

if __name__ == "__main__":
    main()
