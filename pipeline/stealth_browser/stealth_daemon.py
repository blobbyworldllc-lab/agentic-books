"""
Autonomous Stealth Distribution Daemon
Executes continuous, randomized marketing pushes across Pinterest,
parenting/homeschool Facebook communities, and group boards.
Dynamically picks a random interval between 5 to 20 minutes after each post.
Enforces strict daily caps (up to 20/day), anti-bot human cadence,
and uses 100% video/animation and free lead magnets (zero static page exposures).
"""
import argparse
import datetime
import logging
import os
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
    record_attempt,
    check_daily_limit
)
from pipeline.stealth_browser.fb_group_poster import post_to_facebook_group

LOG_FILE = REPO_ROOT / "pipeline" / "growth" / "stealth_daemon.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
LOCK_FILE = REPO_ROOT / "pipeline" / "growth" / "stealth_daemon.lock"

# Setup logging with stream and optional file handler
handlers = [logging.StreamHandler(sys.stdout)]
try:
    handlers.append(logging.FileHandler(str(LOG_FILE), encoding="utf-8"))
except Exception:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=handlers
)

def run_distribution_cycle():
    logging.info("=== Starting Stealth Distribution Cycle ===")
    
    # 1. Check & Execute Pinterest Pin (Up to 20 per day)
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

def acquire_lock():
    if LOCK_FILE.exists():
        try:
            pid = int(LOCK_FILE.read_text().strip())
            # Check if process is still alive on Windows
            import ctypes
            kernel32 = ctypes.windll.kernel32
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            h_proc = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if h_proc:
                kernel32.CloseHandle(h_proc)
                logging.warning(f"Stealth daemon already running (PID {pid}). Exiting.")
                return False
        except Exception:
            pass
    LOCK_FILE.write_text(str(os.getpid()))
    return True

def release_lock():
    try:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="Stealth Distribution Daemon")
    parser.add_argument("--once", action="store_true", help="Run a single distribution cycle and exit")
    parser.add_argument("--min-gap-minutes", type=float, default=5.0, help="Minimum gap in minutes (default: 5.0)")
    parser.add_argument("--max-gap-minutes", type=float, default=20.0, help="Maximum gap in minutes (default: 20.0)")
    args = parser.parse_args()
    
    if args.once:
        run_distribution_cycle()
        return

    if not acquire_lock():
        sys.exit(0)

    try:
        logging.info(f"Starting Stealth Distribution Daemon loop (random gaps: {args.min_gap_minutes:.1f} to {args.max_gap_minutes:.1f} mins)...")
        while True:
            # Check if both daily limits reached
            can_post_comm, comm_count = check_daily_limit(max_per_day=20)
            can_post_pin, pin_count = can_pin(max_daily=20)
            
            if not can_post_comm and not can_post_pin:
                logging.info(f"Daily cap of 20 reached for both Facebook ({comm_count}/20) and Pinterest ({pin_count}/20). Pausing until tomorrow...")
                time.sleep(3600)  # Check again in 1 hour
                continue
                
            try:
                run_distribution_cycle()
            except Exception as e:
                logging.error(f"Unexpected error in daemon cycle: {e}", exc_info=True)
                
            # Pick a random number between 5 to 20 minutes
            gap_minutes = round(random.uniform(args.min_gap_minutes, args.max_gap_minutes), 1)
            sleep_seconds = gap_minutes * 60
            next_time = (datetime.datetime.now() + datetime.timedelta(seconds=sleep_seconds)).strftime("%H:%M:%S")
            logging.info(f"[RANDOM INTERVAL] Picked {gap_minutes} minutes gap. Sleeping until {next_time}...")
            time.sleep(sleep_seconds)
    finally:
        release_lock()

if __name__ == "__main__":
    main()
