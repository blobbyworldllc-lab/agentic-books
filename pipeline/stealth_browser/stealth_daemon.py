"""
Autonomous Stealth Distribution Daemon
Executes continuous, slow-and-steady marketing pushes across Pinterest,
parenting/homeschool communities, and social channels.
Adheres strictly to human pacing, daily caps, and anti-spam heuristics.
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
from pipeline.stealth_browser.community_distributor import get_next_target_community, record_distribution_event

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
    
    # 1. Check & Execute Pinterest Pin
    can_post_pin, pin_count = can_pin()
    logging.info(f"Pinterest status: {pin_count}/4 published today. Can publish?: {can_post_pin}")
    if can_post_pin:
        try:
            success, result = publish_pin(headless=True)
            if success:
                logging.info(f"[PINTEREST OK] Published pin successfully: {result}")
            else:
                logging.warning(f"[PINTEREST SKIP] {result}")
        except Exception as e:
            logging.error(f"[PINTEREST ERROR] Exception during Pinterest run: {e}", exc_info=True)
            
    # 2. Check & Seed Community Lead Magnet
    target, status = get_next_target_community()
    logging.info(f"Community distribution target status: {status}")
    if target:
        group = target["group"]
        logging.info(f"[COMMUNITY SEED] Next candidate: [{target['category']}] {group['name']} ({group['members']}) -> {group['url']}")
        # When running in full automation, record staging and schedule safe delivery
        record_distribution_event(target)
        logging.info(f"[COMMUNITY OK] Recorded seeding cycle for {group['name']}")
    else:
        logging.info(f"[COMMUNITY SKIP] {status}")
        
    logging.info("=== Completed Stealth Distribution Cycle ===")

def main():
    parser = argparse.ArgumentParser(description="Stealth Distribution Daemon")
    parser.add_argument("--once", action="store_true", help="Run a single distribution cycle and exit")
    parser.add_argument("--interval-hours", type=float, default=2.0, help="Interval between runs in hours (default: 2.0)")
    args = parser.parse_args()
    
    if args.once:
        run_distribution_cycle()
        return

    logging.info(f"Starting Stealth Distribution Daemon loop (interval: {args.interval_hours}h)...")
    while True:
        try:
            run_distribution_cycle()
        except Exception as e:
            logging.error(f"Unexpected error in daemon cycle: {e}", exc_info=True)
            
        # Add jitter to avoid exact interval detection (±15 min)
        base_seconds = args.interval_hours * 3600
        jitter = random.uniform(-900, 900)
        sleep_duration = max(1800, base_seconds + jitter)
        logging.info(f"Sleeping for {sleep_duration / 60:.1f} minutes until next stealth cycle...")
        time.sleep(sleep_duration)

if __name__ == "__main__":
    main()
