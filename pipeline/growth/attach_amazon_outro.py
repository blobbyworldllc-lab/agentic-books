"""
Attach Amazon Call-To-Action Outro to All Marketing & Countdown Videos.
Extracts the beautiful holiday card from the official Instagram release
and appends a voiceover: "Check the description to buy our book on Amazon!"
"""

import os
import sys
import asyncio
import subprocess
import logging
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

SHORTS_DIR = REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "output" / "marketing" / "shorts"
OUTRO_VIDEO_PATH = SHORTS_DIR / "pip_amazon_outro.mp4"
TEMP_DIR = SHORTS_DIR / "temp"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

VOICE = "en-US-AnaNeural"
TEXT = "Check the description to buy our book on Amazon!"

def ensure_master_outro():
    """Generates the master outro clip if missing."""
    if OUTRO_VIDEO_PATH.exists() and OUTRO_VIDEO_PATH.stat().st_size > 100000:
        logging.info(f"Master Amazon outro exists: {OUTRO_VIDEO_PATH}")
        return str(OUTRO_VIDEO_PATH)

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    card_img = TEMP_DIR / "outro_card_1080.png"
    audio_path = TEMP_DIR / "outro_audio.mp3"

    # Source frame from scratch or render
    src_frame = Path(r"C:\Users\movov\.gemini\antigravity\brain\c985265e-3960-48cf-b104-dc69ade68dfa\scratch\reel_frames\frame_10.png")
    if src_frame.exists():
        im = Image.open(src_frame).convert("RGB")
        im_resized = im.resize((1080, 1920), Image.Resampling.LANCZOS)
        im_resized.save(card_img, quality=98)
    else:
        # Fallback to launch graphic
        fallback = REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "output" / "marketing" / "ig_1_launch.png"
        im = Image.open(fallback).convert("RGB")
        im_resized = im.resize((1080, 1920), Image.Resampling.LANCZOS)
        im_resized.save(card_img, quality=98)

    # Generate TTS
    import edge_tts
    async def _gen():
        comm = edge_tts.Communicate(TEXT, VOICE, rate="+10%", pitch="+2Hz")
        await comm.save(str(audio_path))

    asyncio.run(_gen())

    # Compile with ffmpeg
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", str(card_img), "-i", str(audio_path),
        "-vf", "scale=1080:1920,fade=t=in:st=0:d=0.3,fade=t=out:st=3.2:d=0.3",
        "-c:v", "libx264", "-tune", "stillimage", "-r", "25",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-pix_fmt", "yuv420p", "-t", "3.5", "-movflags", "+faststart",
        str(OUTRO_VIDEO_PATH)
    ]
    subprocess.run(cmd, check=True)
    logging.info(f"Master Amazon outro generated: {OUTRO_VIDEO_PATH}")
    return str(OUTRO_VIDEO_PATH)

def append_outro_to_video(input_video_path, output_video_path=None):
    """Concatenates input video + Amazon outro."""
    in_path = Path(input_video_path)
    if not in_path.exists():
        logging.error(f"Input video missing: {in_path}")
        return False

    outro_path = ensure_master_outro()
    target_out = Path(output_video_path) if output_video_path else in_path

    temp_out = in_path.parent / f"temp_{in_path.stem}_outro.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(in_path),
        "-i", str(outro_path),
        "-filter_complex",
        "[0:v]scale=1080:1920,setsar=1[v0]; [1:v]scale=1080:1920,setsar=1[v1]; [0:a]aformat=sample_rates=44100:channel_layouts=mono[a0]; [1:a]aformat=sample_rates=44100:channel_layouts=mono[a1]; [v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(temp_out)
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        if target_out.exists():
            target_out.unlink()
        temp_out.rename(target_out)
        logging.info(f"[SUCCESS] Appended Amazon outro to: {target_out.name}")
        return True
    else:
        logging.error(f"Concat failed for {in_path.name}: {res.stderr[-300:]}")
        if temp_out.exists():
            temp_out.unlink()
        return False

def batch_update_all_shorts():
    """Appends Amazon outro to all 25 daily countdown videos."""
    ensure_master_outro()
    videos = sorted(list(SHORTS_DIR.glob("pip_countdown_day_*.mp4")))
    logging.info(f"Found {len(videos)} countdown videos to update.")
    
    updated_count = 0
    for v in videos:
        # Check current duration to avoid double-appending
        dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(v)]
        try:
            dur = float(subprocess.check_output(dur_cmd).decode().strip())
            # If duration is already > 24s, it already has the outro appended
            if dur > 24.0:
                logging.info(f"Skipping {v.name} (already updated, duration: {dur:.1f}s)")
                continue
        except Exception:
            pass

        if append_outro_to_video(v):
            updated_count += 1

    logging.info(f"Batch outro update complete! {updated_count} videos upgraded.")
    return updated_count

if __name__ == "__main__":
    batch_update_all_shorts()
