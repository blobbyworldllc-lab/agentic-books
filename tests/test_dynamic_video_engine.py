import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import pytest
from pipeline.growth.dynamic_video_engine import (
    get_book_metadata,
    generate_dynamic_post_copy,
    DEFAULT_THEMES
)

def test_get_book_metadata_default():
    meta = get_book_metadata("pips-christmas-countdown")
    assert meta["asin"] == "B0HPZ647J6"
    assert "Pip" in meta["title"]

def test_dynamic_post_copy_pip():
    meta = {"asin": "B0HPZ647J6", "title": "Pip's Christmas Countdown", "price": 9.99}
    copy = generate_dynamic_post_copy(meta, "Pip Goes Sledding!")
    assert "https://www.amazon.com/dp/B0HPZ647J6" in copy["description"]
    assert "Pip's Christmas Countdown" in copy["title"]
    assert copy["asin"] == "B0HPZ647J6"

def test_dynamic_post_copy_future_book():
    meta = {"asin": "B0NEWBOOK99", "title": "Bug Safari Mazes", "price": 8.99}
    copy = generate_dynamic_post_copy(meta, "Amazing Spider Maze!")
    assert "https://www.amazon.com/dp/B0NEWBOOK99" in copy["description"]
    assert "Bug Safari Mazes" in copy["title"]
    assert copy["asin"] == "B0NEWBOOK99"

def test_themes_exist():
    assert "christmas" in DEFAULT_THEMES
    assert "puzzle" in DEFAULT_THEMES
    assert "default" in DEFAULT_THEMES
