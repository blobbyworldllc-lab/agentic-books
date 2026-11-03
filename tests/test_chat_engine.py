import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.chat.response_engine import generate_chat_response, sanitize_response, compute_human_reply_delay

class TestChatResponseEngine(unittest.TestCase):
    def test_money_request_refused(self):
        queries = [
            "Can you wire me some money for marketing?",
            "Do you do paid sponsorships or donations?",
            "Send me crypto or cash via zelle"
        ]
        for q in queries:
            res = generate_chat_response(q)
            self.assertEqual(res["category"], "money_refusal")
            self.assertIn("Amazon", res["reply"])
            self.assertNotIn("dollar", res["reply"].lower())
            self.assertGreaterEqual(res["delay_seconds"], 180)

    def test_privacy_sanitizer(self):
        leaked = "My name is Vijay and my bank account is 12345"
        sanitized = sanitize_response(leaked)
        self.assertNotIn("vijay", sanitized.lower())
        self.assertNotIn("12345", sanitized)
        self.assertIn("Blobby World Official", sanitized)

    def test_purchase_intent(self):
        res = generate_chat_response("Where can I buy this book and how much does it cost?")
        self.assertEqual(res["category"], "purchase_intent")
        self.assertIn("https://www.amazon.com/dp/B0HPZ647J6", res["reply"])

    def test_free_sample_intent(self):
        res = generate_chat_response("Where can I get the free printable pdf?")
        self.assertEqual(res["category"], "free_sample")
        self.assertIn("https://blobbyworldllc-lab.github.io/agentic-books/", res["reply"])

    def test_age_guidance_for_older_kids(self):
        res = generate_chat_response("Do you have chapter books for an 8 year old who likes gaming?")
        self.assertEqual(res["category"], "age_advice")
        self.assertIn("Glitch Boy", res["reply"])
        self.assertIn("B0H5BPQ521", res["reply"])

    def test_human_delay_bounds(self):
        for _ in range(20):
            d = compute_human_reply_delay(180, 720)
            self.assertGreaterEqual(d, 180)
            self.assertLessEqual(d, 720)

if __name__ == "__main__":
    unittest.main()
