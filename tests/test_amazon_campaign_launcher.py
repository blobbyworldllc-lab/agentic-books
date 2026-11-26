import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import pytest
from unittest.mock import MagicMock, patch
from pipeline.growth.amazon_campaign_launcher import (
    load_campaign_history,
    record_campaign_status,
    AmazonAdsAutomationEngine,
    DEFAULT_CAMPAIGN
)

def test_record_campaign_status(tmp_path):
    with patch("pipeline.growth.amazon_campaign_launcher.CAMPAIGN_HISTORY_FILE", tmp_path / "test_campaigns.json"):
        entry = record_campaign_status(DEFAULT_CAMPAIGN, "APPROVED_BY_USER", "Test approval")
        assert entry["status"] == "APPROVED_BY_USER"
        assert entry["daily_budget"] == 5.00
        assert entry["end_date"] == "2026-12-05"
        
        history = load_campaign_history()
        assert len(history) == 1
        assert history[0]["campaign_name"] == DEFAULT_CAMPAIGN["name"]

def test_amazon_ads_automation_engine_init():
    engine = AmazonAdsAutomationEngine(DEFAULT_CAMPAIGN, headless=True)
    assert engine.config["asin"] == "B0HPZ647J6"
    assert len(engine.config["keywords"]) == 3
    assert engine.config["keywords"][0]["bid"] == 0.65

def test_set_end_date_in_dom():
    engine = AmazonAdsAutomationEngine(DEFAULT_CAMPAIGN, headless=True)
    mock_page = MagicMock()
    mock_page.evaluate.return_value = True
    
    success = engine.set_end_date_in_dom(mock_page, "12/05/2026")
    assert success is True
    mock_page.evaluate.assert_called_once()
