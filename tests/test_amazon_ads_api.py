import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import pytest
from unittest.mock import patch
from pipeline.growth.amazon_ads_api import (
    load_live_metrics,
    save_live_metrics,
    get_live_summary
)

def test_load_live_metrics():
    metrics = load_live_metrics()
    assert isinstance(metrics, dict)
    assert "aggregate_metrics" in metrics
    assert metrics["aggregate_metrics"]["purchases"] == 1
    assert metrics["aggregate_metrics"]["roas"] == 2.46

def test_get_live_summary():
    summary = get_live_summary()
    assert summary["purchases"] == 1
    assert summary["spend"] == "$3.25"
    assert summary["sales"] == "$7.99"
    assert summary["cvr"] == "16.7%"
    assert summary["active_campaign_id"] == "A0257914GQM1ZCK9OORJ"
