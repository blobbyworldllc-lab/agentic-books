"""Comprehensive Test Suite for Agentic-Books Pipeline.
Verifies all core modules:
 1. safety_guard: Link validation, IP protection, random spacing, cadence tracking.
 2. growth_engine: Analysis of catalog.json and adaptive strategy output.
 3. sales_monitor: Amazon listing health and metric extraction.
 4. dual_buffer_dispatcher: Multi-account token handling and channel parsing.
"""
import sys
import os
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.safety_guard import (
    validate_post_content,
    check_daily_cadence,
    compute_random_spacing,
    record_post_execution,
    PipelineSafetyViolation
)
from pipeline.growth_engine import analyze_catalog_momentum, get_next_campaign_angle
from pipeline.sales_monitor import parse_amazon_metrics
from pipeline.social.dual_buffer_dispatcher import get_account_1_token, get_account_2_token

class TestPipelineSafety(unittest.TestCase):
    def test_random_spacing_bounds(self):
        for _ in range(50):
            val = compute_random_spacing(20, 100)
            self.assertGreaterEqual(val, 20)
            self.assertLessEqual(val, 100)

    def test_prohibited_terms(self):
        with self.assertRaises(PipelineSafetyViolation):
            validate_post_content("Pip plays with Mickey Mouse in winter!", "twitter")
            
        with self.assertRaises(PipelineSafetyViolation):
            validate_post_content("Pip goes on a fight adventure with weapons", "instagram")

    def test_mandatory_amazon_links_all_platforms(self):
        # Hard Rule: Amazon purchase links MUST be included and valid across all platforms, including Instagram
        from pipeline.safety_guard import format_promotional_copy
        
        for platform in ["instagram", "ig", "threads", "facebook", "twitter", "pinterest", "tiktok"]:
            caption, comment = format_promotional_copy("Day 2: Pip finds warm mittens!", platform, asin="B0HPZ647J6")
            # Verify Amazon link is in caption
            self.assertIn("https://www.amazon.com/dp/B0HPZ647J6", caption, f"Missing Amazon link in caption on {platform}")
            # Verify Amazon link is in comment
            self.assertIn("https://www.amazon.com/dp/B0HPZ647J6", comment, f"Missing Amazon link in comment on {platform}")
            # Verify caption passes code-level safety validation with require_amazon_link=True
            self.assertTrue(validate_post_content(caption, platform, require_amazon_link=True))

    def test_missing_amazon_link_rejected_when_enforced(self):
        # Posts missing the Amazon link must be rejected when require_amazon_link is enforced
        with self.assertRaises(PipelineSafetyViolation):
            validate_post_content("Just a cute day rhyme with no purchase link!", "instagram", require_amazon_link=True)
            
        with self.assertRaises(PipelineSafetyViolation):
            validate_post_content("Just a cute day rhyme with no purchase link!", "threads", require_amazon_link=True)

class TestGrowthEngine(unittest.TestCase):
    def test_momentum_analysis(self):
        res = analyze_catalog_momentum(REPO_ROOT)
        self.assertIn("insights", res)
        self.assertGreater(len(res["insights"]), 0)
        book = res["insights"][0]
        self.assertEqual(book["asin"], "B0HPZ647J6")
        self.assertTrue(len(book["recommended_strategy"]) > 0)

    def test_campaign_angles(self):
        angle = get_next_campaign_angle(0)
        self.assertIn("theme", angle)
        self.assertIn("hook", angle)

class TestSalesMonitor(unittest.TestCase):
    def test_amazon_parser_structure(self):
        res = parse_amazon_metrics("B0HPZ647J6")
        if res is not None:
            self.assertIn("price", res)
            self.assertIn("bsr", res)
            self.assertEqual(res["price"], 9.99)

class TestDualBufferTokens(unittest.TestCase):
    def test_token_loading(self):
        t1 = get_account_1_token()
        t2 = get_account_2_token()
        self.assertIsNotNone(t1, "Account 1 token should load from file or env")
        self.assertIsNotNone(t2, "Account 2 token should load from env")
        self.assertTrue(len(t1) > 20)
        self.assertTrue(len(t2) > 20)

if __name__ == "__main__":
    unittest.main()
