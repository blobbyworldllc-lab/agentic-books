"""
Autonomous Multi-Channel Inbox Dispatcher & Webhook Listener.
Listens for incoming social messages, runs them through the Response Engine,
and returns the human-paced, privacy-safe reply.
"""
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import json
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.chat.response_engine import generate_chat_response, sanitize_response

def process_incoming_inquiry(message_text: str, platform: str = "instagram", sender_id: str = "user") -> dict:
    """
    Core pipeline gateway:
    1. Evaluates incoming DM or comment text.
    2. Applies privacy and anti-scam rules.
    3. Computes human delay.
    4. Formats friendly reply with direct Amazon/free pack link.
    """
    decision = generate_chat_response(message_text, platform=platform)
    print(f"\n[INCOMING {platform.upper()}] From: {sender_id} | Message: '{message_text}'")
    print(f"[DECISION] Category: {decision['category']} | Paced Delay: {decision['delay_seconds']}s")
    print(f"[REPLY OUT]:\n{decision['reply']}\n")
    return decision

if __name__ == "__main__":
    test_messages = [
        "Where can I buy the Pip book?",
        "Do you have a free printable sample?",
        "Can you send me $50 for marketing?",
        "What ages is this book good for?"
    ]
    print("Testing Live Multi-Channel Inbox Runner...")
    for msg in test_messages:
        process_incoming_inquiry(msg, platform="instagram")
