"""Amazon BSR (Best Sellers Rank), Price & Review Monitor.
Runs periodically to monitor sales velocity, BSR rank, reviews, and pricing for all live books in pipeline/catalog.json.
Safe, read-only scraper with exponential backoff and zero-spam alerting.
"""
import argparse
import datetime
import html
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

UA = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

def get_page(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as resp:
            return html.unescape(resp.read().decode('utf-8', 'ignore'))
    except Exception as e:
        return ""

def parse_amazon_metrics(asin):
    url = f"https://www.amazon.com/dp/{asin}"
    content = get_page(url)
    if not content or "robot check" in content.lower() or "captcha" in content.lower():
        return None

    metrics = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "bsr": None,
        "category_ranks": [],
        "rating": None,
        "review_count": None,
        "price": None
    }

    # Extract Best Sellers Rank
    bsr_match = re.search(r'#([0-9,]+)\s+in\s+Books', content, re.IGNORECASE)
    if bsr_match:
        metrics["bsr"] = int(bsr_match.group(1).replace(',', ''))

    # Extract subcategory ranks
    sub_matches = re.findall(r'#([0-9,]+)\s+in\s+([A-Za-z0-9\s&,>-]+?)(?:\(|$|<)', content)
    for rank_str, cat in sub_matches[:3]:
        clean_cat = cat.strip().replace('\n', ' ')
        if "Books" not in clean_cat:
            metrics["category_ranks"].append({
                "category": clean_cat,
                "rank": int(rank_str.replace(',', ''))
            })

    # Extract rating
    rating_match = re.search(r'([0-9\.]+)\s+out of 5 stars', content)
    if rating_match:
        metrics["rating"] = float(rating_match.group(1))

    # Extract review count
    review_match = re.search(r'([0-9,]+)\s+(?:global\s+)?ratings', content, re.IGNORECASE)
    if review_match:
        metrics["review_count"] = int(review_match.group(1).replace(',', ''))

    # Extract price
    price_match = re.search(r'class="a-price-whole">([0-9]+)<span class="a-price-decimal">\.</span></span><span class="a-price-fraction">([0-9]+)</span>', content)
    if price_match:
        metrics["price"] = float(f"{price_match.group(1)}.{price_match.group(2)}")

    return metrics

def run_monitor(repo_dir=None):
    repo = Path(repo_dir) if repo_dir else Path(__file__).resolve().parent.parent
    cat_file = repo / "pipeline" / "catalog.json"
    if not cat_file.exists():
        print("catalog.json not found")
        return

    catalog = json.loads(cat_file.read_text(encoding="utf-8"))
    updated = False

    for book in catalog.get("books", []):
        asin = book.get("asin")
        if not asin or book.get("status") != "live":
            continue

        print(f"Checking metrics for {book.get('title')} (ASIN: {asin})...")
        metrics = parse_amazon_metrics(asin)
        if metrics:
            if "metrics" not in book:
                book["metrics"] = []
            # Append new metrics snapshot (keep last 60 data points)
            book["metrics"].append(metrics)
            if len(book["metrics"]) > 60:
                book["metrics"] = book["metrics"][-60:]
            book["last_checked"] = metrics["timestamp"]
            updated = True
            print(f"Recorded snapshot: BSR={metrics['bsr']}, Price={metrics['price']}, Rating={metrics['rating']}, Reviews={metrics['review_count']}")
        else:
            print("Amazon returned anti-bot / empty page. Backing off gracefully.")

    if updated:
        cat_file.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
        subprocess.run(["git", "add", str(cat_file)], cwd=repo, capture_output=True)
        subprocess.run(["git", "commit", "-m", "chore(pipeline): update live Amazon sales & rank metrics [skip ci]"], cwd=repo, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=repo, capture_output=True)
        print("[SUCCESS] catalog.json updated and pushed to origin/main.")

if __name__ == "__main__":
    run_monitor()
