"""
Autonomous Stealth Distribution Daemon
Executes continuous, gapped-out marketing pushes across Pinterest,
parenting/homeschool Facebook communities, and group boards.
Adheres strictly to human pacing (10-20 min intervals), daily caps (up to 20/day),
and anti-spam heuristics with 100% video/animation and free lead magnets.
"""
import argparse
import datetime
import logging
import random
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.stealth_browser.pinterest_publisher import publish_pin, check_can_publish as can_pin
from pipeline.stealth_browser.community_distributor import (
    get_next_target_community,
    record_distribution_event,
    record_attempt
)
from pipeline.stealth_browser.fb_group_poster import post_to_facebook_group

LOG_FILE = REPO_ROOT / "pipeline" / "growth" / "stealth_daemon.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(str(LOG_FILE), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_distribution_cycle():
    logging.info("=== Starting Stealth Distribution Cycle ===")
    
    # 1. Check & Execute Pinterest Pin (Up to 15-20 per day)
    can_post_pin, pin_count = can_pin(max_daily=20)
    logging.info(f"Pinterest status: {pin_count}/20 published today. Can publish?: {can_post_pin}")
    if can_post_pin:
        try:
            success, result = publish_pin(headless=True)
            if success:
                logging.info(f"[PINTEREST OK] Published pin successfully: {result}")
            else:
                logging.warning(f"[PINTEREST SKIP] {result}")
        except Exception as e:
            logging.error(f"[PINTEREST ERROR] Exception during Pinterest run: {e}", exc_info=True)
            
    # 2. Check & Seed Community Lead Magnet (Up to 20 per day)
    target, status = get_next_target_community(max_per_day=20)
    logging.info(f"Community distribution target status: {status}")
    if target:
        group = target["group"]
        group_url = group["url"]
        group_name = group["name"]
        copy_text = target["copy"]
        
        logging.info(f"[COMMUNITY SEED] Navigating to: [{target['category']}] {group_name} ({group['members']}) -> {group_url}")
        try:
            success, msg = post_to_facebook_group(
                group_url=group_url,
                copy_text=copy_text,
                group_name=group_name,
                headless=True
            )
            if success:
                record_distribution_event(target)
                logging.info(f"[COMMUNITY OK] Successfully published post to {group_name}")
            else:
                record_attempt(target, reason=msg)
                logging.warning(f"[COMMUNITY SKIP] Could not post to {group_name}: {msg}")
        except Exception as e:
            logging.error(f"[COMMUNITY ERROR] Failed posting to {group_name}: {e}", exc_info=True)
            record_attempt(target, reason=str(e))
    else:
        logging.info(f"[COMMUNITY SKIP] {status}")
        
    logging.info("=== Completed Stealth Distribution Cycle ===")

def main():
    parser = argparse.ArgumentParser(description="Stealth Distribution Daemon")
    parser.add_argument("--once", action="store_true", help="Run a single distribution cycle and exit")
    parser.add_argument("--min-gap-minutes", type=float, default=10.0, help="Minimum gap between posts in minutes (default: 10.0)")
    parser.add_argument("--max-gap-minutes", type=float, default=20.0, help="Maximum gap between posts in minutes (default: 20.0)")
    args = parser.parse_args()
    
    if args.once:
        run_distribution_cycle()
        return

    logging.info(f"Starting Stealth Distribution Daemon loop (intervals: {args.min_gap-minutes} to {args.max_gap_minutes} mins)...")
    while True:
        try:
            run_distribution_cycle()
        except Exception as e:
            logging.error(f"Unexpected error in daemon cycle: {e}", exc_info=True)
            
        # Gapped-out intervals: 10, 13, 15, 18, 20 minutes (e.g. 600s - 1200s)
        sleep_seconds = random.uniform(args.min_gap_minutes * 60, args.max_gap_minutes * 60)
        logging.info(f"Sleeping for {sleep_seconds / 60:.1f} minutes until next cycle...")
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    main()
