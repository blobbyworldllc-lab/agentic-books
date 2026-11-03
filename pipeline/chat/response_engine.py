"""
Lightweight, Zero-Cost Autonomous Community Chat & Response Engine.
Brand: Blobby World Official (Tampa-based)

Core Principles:
 1. 100% Free & Unlimited (Zero API costs, deterministic + local rule evaluation).
 2. Strict Privacy Firewall: Never reveals real names, personal phone numbers, physical home addresses, or financial/banking details.
 3. Ironclad Financial / Anti-Scam Shield: Rejects all money, donation, sponsorship, or investment requests. Directs only to Amazon.
 4. Anti-Bot Dynamic Pacing: Computes human-realistic delay intervals (3 to 12 minutes).
 5. Natural Human Persona: Warm, friendly, helpful indie children's book team member.
"""
import re
import random
from typing import Dict, Any

# Knowledge Base & Verified Facts
PIP_AMAZON_URL = "https://www.amazon.com/dp/B0HPZ647J6"
GLITCH_AMAZON_URL = "https://www.amazon.com/dp/B0H5BPQ521"
FREE_PACK_URL = "https://blobbyworldllc-lab.github.io/agentic-books/"

PROHIBITED_DISCLOSURES = [
    "vijay", "anusha", "movov", "kumar", "home address", "bank account", 
    "credit card", "routing number", "ssn", "tax id", "ein", "wire transfer",
    "zelle", "venmo", "cashapp", "paypal personal"
]

def sanitize_response(text: str) -> str:
    """Verifies that no private personal or financial information ever leaks."""
    lower = text.lower()
    for item in PROHIBITED_DISCLOSURES:
        if item in lower:
            # Overwrite with safe standard brand response
            return (
                "Hi there! Thank you so much for reaching out to Blobby World Official! "
                "We're a small indie children's book team based in Tampa, Florida. "
                f"You can explore all our books securely on Amazon Prime here: {PIP_AMAZON_URL} "
                f"or grab our free printable pack here: {FREE_PACK_URL} 😊 Have a wonderful day!"
            )
    return text

def compute_human_reply_delay(min_seconds: int = 180, max_seconds: int = 720) -> int:
    """Computes a random human-like delay between 3 to 12 minutes to evade bot detection."""
    return random.randint(min_seconds, max_seconds)

def generate_chat_response(incoming_message: str, platform: str = "general") -> Dict[str, Any]:
    """
    Evaluates incoming inquiry and generates a friendly, natural response.
    Returns:
      {
        "reply": str,
        "delay_seconds": int,
        "category": str
      }
    """
    text = (incoming_message or "").lower().strip()
    delay = compute_human_reply_delay()
    
    # 1. Money, Scam, Sponsorship, Paid Promo Requests (Strict Refusal)
    money_triggers = [
        "money", "pay", "payment", "paid", "donate", "donation", "donations", "fund", "funding",
        "sponsor", "sponsors", "sponsorship", "sponsorships", "wire", "crypto", "bitcoin",
        "paid collab", "cash", "venmo", "zelle", "bank", "send me", "invest", "investment"
    ]
    if any(re.search(r"\b" + re.escape(w) + r"\b", text) for w in money_triggers):
        reply = random.choice([
            "Hi there! Thanks so much for reaching out! We don't handle any financial transactions, paid sponsorships, or donations directly over DMs. All of our books are published and fulfilled securely through Amazon Prime for everyone's safety! 😊 Wishing you a wonderful week!",
            "Hello! Appreciate your message! As an independent children's book team, we keep all purchases and transactions strictly through Amazon Prime so readers get fast, verified shipping and complete security. Thanks for understanding! ✨",
            "Hey! Thanks for thinking of us. We don't do any direct payment handling, sponsorships, or outside transactions over social media. Everything we make is hosted right on Amazon Prime! Hope you have a lovely holiday season! 🎄"
        ])
        return {"reply": sanitize_response(reply), "delay_seconds": delay, "category": "money_refusal"}

    # 2. Personal Identity / Location / Who are you?
    personal_triggers = ["who are you", "what is your name", "where do you live", "owner", "real name", "address", "phone number"]
    if any(p in text for p in personal_triggers):
        reply = random.choice([
            "Hello! We're the creative team behind Blobby World Official, a small indie children's book studio based right here in sunny Tampa, Florida! 🌴 We make story coloring books and adventure chapter books for kids. So glad to connect!",
            "Hi there! We are Blobby World Official, an independent children's book team based out of Tampa, FL. We design calming, screen-free story adventures and books for families and little learners. Let us know if we can help with anything! ⭐",
            "Hey! Thanks for stopping by! We're a Tampa-based creator team sharing Pip the penguin and Glitch Boy stories with families worldwide through Amazon Prime. Nice to meet you!"
        ])
        return {"reply": sanitize_response(reply), "delay_seconds": delay, "category": "identity_safe"}

    # 3. Where to buy / Price / Ordering
    buy_triggers = ["where to buy", "how much", "price", "buy", "order", "cost", "link", "amazon", "purchase", "hardcover", "paperback"]
    if any(re.search(r"\b" + re.escape(w) + r"\b", text) for w in buy_triggers):
        reply = random.choice([
            f"Hi! You can grab Pip's Christmas Countdown right on Amazon for $9.99 with fast Amazon Prime delivery! 📦 Here's the direct link: {PIP_AMAZON_URL}\n\nIt has 50 big coloring designs (25 countdown nights + 25 bonus winter adventures) with thick outlines so markers don't bleed through! Let us know if you need anything else! 🐧✨",
            f"Hello! Yes, it's available directly on Amazon for $9.99 with fast Prime shipping: {PIP_AMAZON_URL}\n\nEvery page has a cozy rhyming story and a hidden 'Find Little Star' game that kids love. Perfect screen-free holiday tradition!",
            f"Hey there! It's available on Amazon here: {PIP_AMAZON_URL} for $9.99. If you want to check out the style first, you can also download our free 4-page printable sample pack here: {FREE_PACK_URL} 😊"
        ])
        return {"reply": sanitize_response(reply), "delay_seconds": delay, "category": "purchase_intent"}

    # 4. Free printable / Sample / Activity Pack
    sample_triggers = ["free", "printable", "sample", "pdf", "activity", "download", "tracker", "worksheet"]
    if any(re.search(r"\b" + re.escape(w) + r"\b", text) for w in sample_triggers):
        reply = random.choice([
            f"Hi! Absolutely! We have a 100% free 4-page starter printable pack that includes the Countdown Tracker + Day 1 & Day 2 coloring stories! You can download it instantly right here: {FREE_PACK_URL} 🎁 Enjoy coloring with your little one!",
            f"Hello! Yes, you can grab the free holiday printable pack directly from our site here: {FREE_PACK_URL} - no catch, just pure screen-free fun for your kids or classroom! Have a blast coloring! 🐧⭐",
            f"Hey! Here is the free printable pack link: {FREE_PACK_URL} 🎨 It has the full 25-day countdown tracker and sample pages. If they love it, the complete 110-page paperback is on Amazon here: {PIP_AMAZON_URL}!"
        ])
        return {"reply": sanitize_response(reply), "delay_seconds": delay, "category": "free_sample"}

    # 5. Age appropriateness / Developmental / Toddler / Older chapter book questions
    age_triggers = [
        "age", "ages", "year old", "years old", "toddler", "preschool", "kindergarten", 
        "motor skills", "older", "chapter", "chapter book", "middle grade", "gaming", "game",
        "7", "8", "9", "10", "11", "12"
    ]
    if any(re.search(r"\b" + re.escape(w) + r"\b", text) for w in age_triggers):
        if any(w in text for w in ["older", "7", "8", "9", "10", "11", "12", "chapter", "gaming", "glitch"]):
            reply = (
                f"Hi! For older readers (ages 7–11), we have our exciting 'Glitch Boy' adventure gaming series! "
                f"It's an action-packed chapter book about gaming, teamwork, and managing big emotions. "
                f"You can check it out on Amazon here: {GLITCH_AMAZON_URL} 🎮👾"
            )
        else:
            reply = (
                f"Hi! Pip's Christmas Countdown is specially designed for kids ages 3 to 6! 🐧 "
                "The outlines are extra thick and bold to build pencil grip and motor control without frustration, "
                "and every page is single-sided so markers never bleed through. Plus the 'Find Little Star' game keeps them super engaged! "
                f"You can see details on Amazon here: {PIP_AMAZON_URL} 😊"
            )
        return {"reply": sanitize_response(reply), "delay_seconds": delay, "category": "age_advice"}

    # 6. General Friendly Greeting / Compliment
    reply = random.choice([
        f"Hi! Thank you so much for reaching out to Blobby World! 🐧✨ We hope you and your family have a wonderful holiday season! If you're looking for fun screen-free holiday coloring, check out Pip on Amazon: {PIP_AMAZON_URL} or grab our free printable pack here: {FREE_PACK_URL} 😊 Let us know if you have any questions!",
        f"Hello! Thanks so much for connecting with us! We're always here to share the holiday cheer. Feel free to download our free Christmas countdown activity pages here: {FREE_PACK_URL} or explore our full paperback on Amazon: {PIP_AMAZON_URL} ⭐ Have a magical day!",
        f"Hey there! Appreciate your message! We're a small indie children's book team based in Tampa, FL sharing cozy stories for little ones. You can find our Christmas countdown book on Amazon Prime here: {PIP_AMAZON_URL} 🎄✨"
    ])
    return {"reply": sanitize_response(reply), "delay_seconds": delay, "category": "general_greeting"}
