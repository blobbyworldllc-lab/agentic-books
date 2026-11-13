import pytest
from pipeline.social.daily_video_syndicator import get_next_video, ROTATING_VIDEOS, ASIN

def test_rotating_videos_structure():
    assert len(ROTATING_VIDEOS) == 3
    for v in ROTATING_VIDEOS:
        assert "id" in v
        assert "title" in v
        assert "filename" in v
        assert "caption" in v
        assert ASIN in v["caption"]
        assert "https://www.amazon.com/dp/" in v["caption"]

def test_get_next_video():
    video, history = get_next_video()
    assert video["id"] in ["sledding", "skating", "tree"]
