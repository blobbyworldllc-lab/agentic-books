import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import pytest
from pipeline.growth.amazon_video_promoter import load_history, save_history, CREATOR_TARGETS

def test_amazon_video_promoter_config():
    assert len(CREATOR_TARGETS) >= 3
    platforms = [t["platform"] for t in CREATOR_TARGETS]
    assert any("YouTube" in p for p in platforms)
    assert any("Pinterest" in p for p in platforms)
    assert any("Amazon" in p for p in platforms)

def test_amazon_video_history(tmp_path, monkeypatch):
    test_hist_file = tmp_path / "test_hist.json"
    monkeypatch.setattr("pipeline.growth.amazon_video_promoter.HISTORY_FILE", test_hist_file)
    data = load_history()
    assert data["video_count"] == 0
    assert data["aplus_live"] is False
    data["video_count"] = 1
    data["aplus_live"] = True
    save_history(data)
    loaded = load_history()
    assert loaded["video_count"] == 1
    assert loaded["aplus_live"] is True
