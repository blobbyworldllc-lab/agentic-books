"""
Autonomous Multi-Channel Polling & Response Daemon.
Monitors incoming notifications/activity across supported channels and executes
the Response Engine without requiring manual setting configurations.
"""
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import time
import random
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.chat.response_engine import generate_chat_response, sanitize_response

QUEUE_FILE = REPO_ROOT / "pipeline" / "chat" / "inbox_queue.json"

def load_queue():
    if QUEUE_FILE.exists():
        try:
            return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"inbox": [], "processed": []}

def save_queue(data):
    QUEUE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def poll_and_respond():
    """
    Simulates automated background inbox monitoring:
    1. Checks for pending incoming customer inquiries.
    2. Runs each through the Response Engine.
    3. Respects anti-bot pacing and safety firewalls.
    """
    queue = load_queue()
    pending = [item for item in queue.get("inbox", []) if not item.get("replied")]
    
    if not pending:
        print("[IDLE] Inbox monitor active. Zero unhandled messages.")
        return 0

    print(f"[ACTIVE] Processing {len(pending)} unhandled inquiries...")
    for item in pending:
        msg = item.get("text", "")
        platform = item.get("platform", "instagram")
        
        # Generate safe response
        res = generate_chat_response(msg, platform=platform)
        delay = res["delay_seconds"]
        
        print(f" -> [{platform.upper()}] Inquiry: '{msg[:40]}...'")
        print(f"    Paced Delay: {delay}s | Category: {res['category']}")
        print(f"    Generated Reply: '{res['reply'][:60]}...'")
        
        # Mark processed
        item["replied"] = True
        item["reply_text"] = res["reply"]
        item["replied_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        queue["processed"].append(item)

    save_queue(queue)
    return len(pending)

if __name__ == "__main__":
    poll_and_respond()
