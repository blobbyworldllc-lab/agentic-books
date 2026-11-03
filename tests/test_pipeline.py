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

    def test_instagram_link_protection(self):
        # Raw amazon links must be blocked on IG
        with self.assertRaises(PipelineSafetyViolation):
            validate_post_content("Buy on Amazon now: https://www.amazon.com/dp/B0HPZ647J6", "instagram")

        with self.assertRaises(PipelineSafetyViolation):
            validate_post_content("Grab it here: https://amzn.to/3xyz", "ig")

        # Compliant bio link CTA must pass
        valid = validate_post_content("Day 2: Pip finds warm mittens! Tap @blobbyworldofficial for link in bio.", "instagram")
        self.assertTrue(valid)

    def test_non_ig_direct_links_allowed(self):
        # Direct links allowed on Twitter, Facebook, YouTube
        self.assertTrue(validate_post_content("Buy on Amazon: https://www.amazon.com/dp/B0HPZ647J6", "twitter"))
        self.assertTrue(validate_post_content("Buy on Amazon: https://www.amazon.com/dp/B0HPZ647J6", "facebook"))

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
