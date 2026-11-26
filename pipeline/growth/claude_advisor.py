"""Autonomous Claude Strategy & Campaign Advisory Engine.

Provides an automated programmatic bridge to Anthropic Claude for reviewing,
validating, and optimizing marketing campaigns, keywords, bids, and book strategies.
"""
import os
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
import anthropic

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
HISTORY_DIR = REPO_ROOT / "pipeline" / "growth"
HISTORY_FILE = HISTORY_DIR / "claude_advisory_history.json"

# Preferred Anthropic models in priority order
MODELS = [
    "claude-sonnet-5",
    "claude-sonnet-4-5-20250929",
    "claude-haiku-4-5-20251001",
    "claude-3-5-sonnet-latest"
]

def get_anthropic_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        env_paths = [
            Path(r"C:\Users\movov\Projects\.env"),
            Path(r"C:\Users\movov\.gemini\.env")
        ]
        for p in env_paths:
            if p.exists():
                for line in p.read_text(encoding="utf-8").splitlines():
                    if line.startswith("ANTHROPIC_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
            if api_key:
                break
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment or central vault.")
    return anthropic.Anthropic(api_key=api_key)

def consult_claude_strategy(prompt: str, max_tokens: int = 600) -> str:
    """Queries Claude with automatic model fallback."""
    client = get_anthropic_client()
    last_err = None
    for model in MODELS:
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            text = resp.content[0].text
            _record_consultation(model, prompt, text)
            return text
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f"All Claude models failed. Last error: {last_err}")

def review_ad_campaign_plan(asin: str, book_title: str, daily_budget: float, end_date: str, keywords: list, bid: float) -> dict:
    """Asks Claude to evaluate and approve an Amazon Ads campaign plan."""
    prompt = f"""You are the master advertising strategist for kids' books on Amazon KDP.
Review and validate the following Amazon Sponsored Products campaign:
- Book: {book_title} (ASIN: {asin})
- Daily Budget: ${daily_budget:.2f}
- End Date: {end_date}
- Target Keywords: {json.dumps(keywords)}
- Default Bid: ${bid:.2f}

Provide your structured assessment:
1. Verdict: APPROVED or NEEDS_ADJUSTMENT
2. Evaluation of keywords for intent and conversion
3. Daily click & spend estimate
4. Tactical guidance for Black Friday / Cyber Monday / Holiday window.
Keep response concise and actionable."""

    evaluation_text = consult_claude_strategy(prompt, max_tokens=500)
    verdict = "APPROVED" if "APPROVED" in evaluation_text.upper() else "REVIEW"
    return {
        "verdict": verdict,
        "evaluation": evaluation_text,
        "asin": asin,
        "daily_budget": daily_budget,
        "end_date": end_date,
        "keywords": keywords,
        "bid": bid,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def _record_consultation(model: str, prompt: str, response: str):
    history = []
    if HISTORY_FILE.exists():
        try:
            history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            history = []
    history.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "prompt": prompt[:200] + "...",
        "response": response
    })
    # Keep last 50 entries
    HISTORY_FILE.write_text(json.dumps(history[-50:], indent=2), encoding="utf-8")

if __name__ == "__main__":
    result = review_ad_campaign_plan(
        asin="B0HPZ647J6",
        book_title="Pip's Christmas Countdown",
        daily_budget=5.00,
        end_date="2026-12-05",
        keywords=[
            "toddler christmas coloring book",
            "christmas countdown book kids",
            "advent calendar coloring book"
        ],
        bid=0.65
    )
    print(f"Verdict: {result['verdict']}")
    print(result['evaluation'])
