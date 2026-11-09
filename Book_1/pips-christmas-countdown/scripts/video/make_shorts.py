"""
Universal Dynamic Video Generator for Pip's Christmas Countdown & Catalog Books
Standards Enforced:
1. Moving 3D character animation / active drawing & coloring motion ONLY (Zero static book page exposures).
2. 100% Pure soothing, enchanting background music box chimes with ZERO spoken voiceover intrusion.
3. Seamless 0.5s visual crossfade (dissolve) into the dynamic Amazon Call-to-Action Outro card.
4. Golden 'BUY NOW ON AMAZON' button and prominent direct URL amazon.com/dp/{asin} on the outro card.
5. Code-level dynamic binding to pipeline catalog and live ASIN.
"""
import os
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.growth.dynamic_video_engine import (
    get_book_metadata,
    generate_dynamic_amazon_outro,
    assemble_dynamic_short,
    generate_dynamic_post_copy
)
from pipeline.safety_guard import validate_video_asset

OUTPUT_DIR = REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "output" / "marketing" / "shorts"
FONTS_DIR = REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "fonts"
MUSIC_PATH = REPO_ROOT / "pipeline" / "assets" / "audio" / "soothing_music_box.wav"
DEFAULT_3D_ANIM = OUTPUT_DIR / "pip_3d_coloring_amazon_pure_soothing.mp4"

def build_dynamic_promo_video(
    slug_or_asin: str = "B0HPZ647J6",
    animation_clip: str = None,
    output_path: str = None,
    anim_duration_s: float = 6.5,
    outro_duration_s: float = 3.5
):
    """
    Builds a fully compliant, dynamic Amazon promotional short using the central video engine.
    Guarantees zero static page exposures, pure soothing audio, and live ASIN call-to-action.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    meta = get_book_metadata(slug_or_asin)
    
    anim_file = Path(animation_clip) if animation_clip else DEFAULT_3D_ANIM
    out_file = Path(output_path) if output_path else OUTPUT_DIR / f"{meta['slug']}_dynamic_short.mp4"
    
    # Generate Outro Card & Video
    outro_img = OUTPUT_DIR / "temp" / f"outro_{meta['asin']}.png"
    outro_vid = OUTPUT_DIR / "temp" / f"outro_{meta['asin']}.mp4"
    outro_img.parent.mkdir(parents=True, exist_ok=True)
    
    # If soothing music file does not exist, synthesize one
    music_file = Path(MUSIC_PATH)
    if not music_file.exists():
        music_file = OUTPUT_DIR / "temp" / "soothing_music_box.wav"
        if not music_file.exists():
            import numpy as np
            import wave
            sr = 44100
            t = np.linspace(0, 10, int(sr * 10), False)
            audio = np.zeros_like(t)
            notes = [523.25, 659.25, 783.99, 1046.50, 783.99, 659.25]
            for i, f in enumerate(notes * 4):
                start = int(i * 0.4 * sr)
                dur = int(1.2 * sr)
                if start + dur < len(t):
                    decay = np.exp(-3.0 * np.linspace(0, 1.2, dur))
                    tone = np.sin(2 * np.pi * f * np.linspace(0, 1.2, dur)) * decay
                    audio[start:start+dur] += tone * 0.15
            audio = np.clip(audio, -0.9, 0.9)
            data = (audio * 32767).astype(np.int16)
            with wave.open(str(music_file), "w") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sr)
                wf.writeframes(data.tobytes())
    
    print(f"[ENGINE] Generating dynamic Amazon outro for: {meta['title']} (ASIN: {meta['asin']})...")
    generate_dynamic_amazon_outro(
        book_meta=meta,
        output_img_path=str(outro_img),
        output_video_path=str(outro_vid),
        music_wav_path=str(music_file),
        duration_s=outro_duration_s
    )
    
    print(f"[ENGINE] Assembling dynamic short with 0.5s visual dissolve: {out_file}...")
    assemble_dynamic_short(
        animation_clip_path=str(anim_file),
        outro_card_img_path=str(outro_img),
        music_wav_path=str(music_file),
        output_short_path=str(out_file),
        anim_duration_s=anim_duration_s,
        outro_duration_s=outro_duration_s,
        crossfade_s=0.5
    )
    
    # Validate result
    validate_video_asset(str(out_file), allow_static_pages=False)
    print(f"[SUCCESS] Dynamic short built and verified compliant: {out_file}")
    return str(out_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build dynamic promotional short")
    parser.add_argument("--asin", type=str, default="B0HPZ647J6", help="Book ASIN or slug")
    args = parser.parse_args()
    build_dynamic_promo_video(slug_or_asin=args.asin)
