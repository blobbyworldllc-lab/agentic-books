"""
Community Seeding Tracker & Safe Dispatch Coordinator
Manages distribution of the Free Lead Magnet across hundreds of parenting/homeschool communities.
Ensures zero spam flagging by enforcing strict daily caps (max 5 groups/day) and tracking history.
"""
import json
import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_FILE = REPO_ROOT / "pipeline" / "growth" / "community_database.json"
HISTORY_FILE = REPO_ROOT / "pipeline" / "growth" / "community_history.json"

def load_database():
    if DB_FILE.exists():
        return json.loads(DB_FILE.read_text(encoding="utf-8"))
    return {}

def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"posted_groups": [], "daily_counts": {}}

def save_history(history):
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")

def check_daily_limit(max_per_day=5):
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    history = load_history()
    count = history["daily_counts"].get(today, 0)
    return count < max_per_day, count

def record_group_posted(group_name, group_url):
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    history = load_history()
    
    history["daily_counts"][today] = history["daily_counts"].get(today, 0) + 1
    history["posted_groups"].append({
        "name": group_name,
        "url": group_url,
        "timestamp": now_iso
    })
    save_history(history)
    print(f"[SUCCESS] Recorded post to {group_name}. Today's total: {history['daily_counts'][today]}")

def get_next_recommended_groups(limit=5):
    db = load_database()
    history = load_history()
    posted_urls = {item["url"] for item in history["posted_groups"]}
    
    candidates = []
    for category, groups in db.get("categories", {}).items():
        for g in groups:
            if g["url"] not in posted_urls:
                candidates.append((category, g))
                if len(candidates) >= limit:
                    return candidates
    return candidates

if __name__ == "__main__":
    can_post, current_count = check_daily_limit()
    print(f"Community Tracker Status: {current_count}/5 posted today. Can post more?: {can_post}")
    next_up = get_next_recommended_groups(5)
    print(f"\nNext {len(next_up)} recommended communities:")
    for cat, g in next_up:
        print(f" - [{cat.upper()}] {g['name']} ({g['members']}) -> {g['url']}")
