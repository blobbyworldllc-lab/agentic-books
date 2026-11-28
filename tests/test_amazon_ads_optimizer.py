import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import pytest
from pipeline.growth.amazon_ads_optimizer import (
    generate_negative_exclusions,
    run_campaign_optimization,
    HIGH_INTENT_TARGETS
)

def test_generate_negative_exclusions():
    exclusions = generate_negative_exclusions()
    assert len(exclusions) > 10
    terms = [e["term"] for e in exclusions]
    assert any("toy" in t for t in terms)
    assert any("lego" in t for t in terms)

def test_run_campaign_optimization():
    plan = run_campaign_optimization()
    assert plan["asin"] == "B0HPZ647J6"
    assert plan["current_roas"] == 2.46
    assert len(plan["optimized_targets"]) == 3
