import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import pytest
from unittest.mock import MagicMock, patch
from pipeline.growth.claude_advisor import (
    consult_claude_strategy,
    review_ad_campaign_plan,
    _record_consultation
)

def test_review_ad_campaign_plan_approved():
    mock_response = "Verdict: APPROVED. Excellent targeted keywords for holiday season."
    with patch("pipeline.growth.claude_advisor.consult_claude_strategy", return_value=mock_response):
        res = review_ad_campaign_plan(
            asin="B0HPZ647J6",
            book_title="Pip's Christmas Countdown",
            daily_budget=5.00,
            end_date="2026-12-05",
            keywords=["toddler christmas coloring book"],
            bid=0.65
        )
        assert res["verdict"] == "APPROVED"
        assert res["asin"] == "B0HPZ647J6"
        assert res["daily_budget"] == 5.00
        assert res["bid"] == 0.65

def test_record_consultation(tmp_path):
    with patch("pipeline.growth.claude_advisor.HISTORY_FILE", tmp_path / "test_advisory.json"):
        _record_consultation("claude-sonnet-5", "Test prompt", "Test response")
        assert (tmp_path / "test_advisory.json").exists()
