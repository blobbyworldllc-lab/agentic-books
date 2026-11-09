import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.growth.youtube_comment_poster import ACTIVE_SHORTS, BUY_COMMENT_TEXT

def test_comment_text_contains_amazon_link():
    assert "https://www.amazon.com/dp/B0HPZ647J6" in BUY_COMMENT_TEXT
    assert "Pip's Christmas Countdown" in BUY_COMMENT_TEXT

def test_active_shorts_structure():
    assert len(ACTIVE_SHORTS) == 4
    ids = {s["id"] for s in ACTIVE_SHORTS}
    assert "HfQJeqQ23jg" in ids
    assert "NuFvuM8Q2bg" in ids
    assert "yxkljv_Y5F4" in ids
    assert "v24c4QH0XWQ" in ids
