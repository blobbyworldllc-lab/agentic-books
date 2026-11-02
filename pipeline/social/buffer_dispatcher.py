"""
Buffer Autonomous Publisher for Pip's Christmas Countdown & Catalog Books
Brand: Blobby World Official

Fully autonomous publishing across all connected channels:
- Instagram: Scheduled & Queued
- X (Twitter): Scheduled & Queued
- Pinterest: Injected directly into Buffer drafts/queue with full asset and copy
"""
import os
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SOCIAL_DIR = BASE_DIR / "pipeline" / "social"
TOKEN_FILE = SOCIAL_DIR / "buffer_token.json"

LANDING_URL = "https://blobbyworldllc-lab.github.io/agentic-books/"
AMAZON_ASIN_URL = "https://www.amazon.com/dp/B0HPZ647J6"
CDN_BASE = "https://raw.githubusercontent.com/blobbyworldllc-lab/agentic-books/main/docs"

BUFFER_GQL = "https://api.buffer.com/graphql"

def get_token():
    if os.environ.get("BUFFER_ACCESS_TOKEN"):
        return os.environ.get("BUFFER_ACCESS_TOKEN").strip()
    if TOKEN_FILE.exists():
        data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
        return data.get("access_token", "").strip()
    return None

def gql_request(query, variables=None):
    token = get_token()
    if not token:
        raise ValueError("Buffer access token missing.")
    
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    req = urllib.request.Request(
        BUFFER_GQL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def get_channels():
    acc_res = gql_request("query { account { id email organizations { id name } } }")
    orgs = acc_res.get("data", {}).get("account", {}).get("organizations", [])
    if not orgs:
        return []
    org_id = orgs[0]["id"]
    
    query = """
    query GetChannels($orgId: OrganizationId!) {
        channels(input: { organizationId: $orgId }) {
            id
            name
            service
            displayName
            metadata {
                ... on PinterestMetadata {
                    boards {
                        id
                        name
                    }
                }
            }
        }
    }
    """
    ch_res = gql_request(query, {"orgId": org_id})
    return ch_res.get("data", {}).get("channels", [])

def create_post(channel_id, text, image_url=None, service="instagram", board_id=None, save_as_draft=False):
    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
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
        }
    }
    """
    post_input = {
        "channelId": channel_id,
        "text": text,
        "mode": "addToQueue",
        "schedulingType": "automatic",
        "needsApproval": False,
        "saveToDraft": save_as_draft,
        "assets": []
    }
    if image_url:
        post_input["assets"].append({
            "image": {
                "url": image_url
            }
        })
    
    if service == "instagram":
        post_input["metadata"] = {
            "instagram": {
                "type": "post",
                "shouldShareToFeed": True
            }
        }
    elif service == "pinterest" and board_id:
        post_input["metadata"] = {
            "pinterest": {
                "boardServiceId": board_id,
                "title": "Free Christmas Countdown Coloring Pages for Kids (Printable PDF)",
                "url": LANDING_URL
            }
        }
    
    return gql_request(mutation, {"input": post_input})

def dispatch_all():
    channels = get_channels()
    if not channels:
        print("[!] No social channels currently connected in Buffer.")
        return False

    print(f"Connected channels found ({len(channels)}):")
    for ch in channels:
        print(f" - [{ch['service'].upper()}] {ch.get('displayName') or ch.get('name')} (ID: {ch['id']})")

    dispatched = 0
    for ch in channels:
        service = ch["service"].lower()
        cid = ch["id"]
        
        if service == "pinterest":
            boards = ch.get("metadata", {}).get("boards", [])
            board_id = boards[0]["id"] if boards else None
            
            pin_text = (
                "Free Christmas Countdown Coloring Pages for Kids Ages 3-6 (Printable PDF)! 🐧⭐\n\n"
                "Cute penguin Christmas coloring pages for toddlers and preschoolers. "
                "Free printable countdown tracker + Day 1 & Day 2 story pages featuring Pip and Little Star.\n\n"
                f"Instant free download: {LANDING_URL}\n"
                f"Full 110-page paperback on Amazon: {AMAZON_ASIN_URL}"
            )
            pin_img = f"{CDN_BASE}/pin_1_coloring_pages.png"
            
            # If board not yet synced in metadata, inject directly into Buffer drafts/queue with full assets
            save_draft = (board_id is None)
            res = create_post(cid, pin_text, pin_img, service="pinterest", board_id=board_id, save_as_draft=save_draft)
            print(f"[OK] Pinterest Pin created in Buffer: {res}")
            dispatched += 1

        elif service == "instagram":
            text = (
                "NEW for Christmas! Pip's Christmas Countdown is now LIVE on Amazon! 🐧🎄\n\n"
                "A tiny star lands on his nose and plays hide-and-seek every night until Christmas. "
                "Read one rhyme, color one page, find Little Star! 25 nights + 25 bonus winter adventures for ages 3-6.\n\n"
                f"Full paperback now live on Amazon: {AMAZON_ASIN_URL}\n"
                f"Grab the FREE 4-page starter printable pack from the link in bio!\n\n"
                "#BlobbyWorld #ChristmasColoring #ToddlerActivities #ColoringBook #KidsChristmas #ChristmasCountdown"
            )
            img = f"{CDN_BASE}/ig_1_launch.png"
            res = create_post(cid, text, img, service="instagram")
            print(f"[OK] Instagram Post queued: {res}")
            dispatched += 1

        elif service in ["twitter", "x"]:
            x_text = (
                "Pip's Christmas Countdown is LIVE on Amazon! 🐧🎄\n\n"
                "A 25-night story coloring book for kids ages 3-6 with rhyming read-alouds & hidden star game!\n\n"
                f"Amazon: {AMAZON_ASIN_URL}\n"
                f"Free Printables: {LANDING_URL}"
            )
            img = f"{CDN_BASE}/ig_1_launch.png"
            res = create_post(cid, x_text, img, service="twitter")
            print(f"[OK] X/Twitter Post queued: {res}")
            dispatched += 1

    return dispatched > 0

if __name__ == "__main__":
    import sys
    if "--book1-repost" not in sys.argv:
        print("This dispatcher carries the hardcoded Book 1 payload (Pip's Christmas Countdown) and already ran. "
              "Pass --book1-repost only to deliberately queue it again. New books need their own payload.")
        sys.exit(0)
    dispatch_all()
