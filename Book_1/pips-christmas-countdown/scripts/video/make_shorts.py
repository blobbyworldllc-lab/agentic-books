"""
Batch generator for 25 vertical daily countdown videos (YouTube Shorts / TikTok / Reels)
Format: 9:16 (1080x1920)
Channel Branding: Blobby World Official
"""
import os
import asyncio
import edge_tts
from PIL import Image, ImageDraw, ImageFont

# Directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(SCRIPT_DIR)
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
ART_PAGES = os.path.join(BASE_DIR, "art", "pages")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
OUTPUT_VIDEOS = os.path.join(BASE_DIR, "output", "marketing", "shorts")

os.makedirs(OUTPUT_VIDEOS, exist_ok=True)
TEMP_DIR = os.path.join(OUTPUT_VIDEOS, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# Import captions
import sys
sys.path.insert(0, SCRIPTS_DIR)
from captions import COUNTDOWN, BONUS

def get_caption(day_num: int):
    for p, text in COUNTDOWN:
        if p == day_num:
            parts = text.split(" / ")
            return parts[0], parts[1]
    return "", ""

# Voice configuration for friendly storytelling
VOICE = "en-US-AnaNeural"  # Cheerful, warm female child/young adult voice

async def generate_narration(text: str, audio_path: str):
    communicate = edge_tts.Communicate(text, VOICE, rate="+0%", pitch="+2Hz")
    await communicate.save(audio_path)

def render_vertical_frame(page_idx: int, day_num: int, line1: str, line2: str, out_img_path: str):
    """
    Renders 1080x1920 vertical canvas:
    - Top header: "Day X of 25: Christmas Countdown"
    - Center: Art page with clean border
    - Bottom: The 2-line rhyming caption + "Can you find Little Star?"
    - Channel footer: Blobby World Official
    """
    W, H = 1080, 1920
    im = Image.new("RGB", (W, H), "#F7FAFC")
    draw = ImageDraw.Draw(im)

    # Load fonts
    f_bold = os.path.join(FONTS_DIR, "Fredoka-Bold.ttf")
    f_semi = os.path.join(FONTS_DIR, "Fredoka-SemiBold.ttf")
    f_med = os.path.join(FONTS_DIR, "Fredoka-Medium.ttf")

    font_title = ImageFont.truetype(f_bold, 54)
    font_day = ImageFont.truetype(f_bold, 76)
    font_text = ImageFont.truetype(f_semi, 44)
    font_sub = ImageFont.truetype(f_bold, 40)
    font_footer = ImageFont.truetype(f_med, 30)

    # Top Header banner
    draw.rectangle([(0, 0), (W, 260)], fill="#B3261E")
    draw.text((W // 2, 80), f"DAY {day_num} OF 25", fill="#FFEB3B", font=font_day, anchor="mm")
    draw.text((W // 2, 175), "Pip's Christmas Countdown", fill="#FFFFFF", font=font_title, anchor="mm")

    # Center Art Page
    art_path = os.path.join(ART_PAGES, f"p{page_idx:02d}.png")
    if os.path.exists(art_path):
        art_im = Image.open(art_path).convert("RGB")
        # Target size for art: ~920 x 1100
        art_im.thumbnail((920, 1100), Image.Resampling.LANCZOS)
        aw, ah = art_im.size
        ax = (W - aw) // 2
        ay = 290 + (1120 - ah) // 2
        
        # Shadow / Border
        draw.rectangle([(ax - 10, ay - 10), (ax + aw + 10, ay + ah + 10)], fill="#E2E8F0")
        draw.rectangle([(ax - 4, ay - 4), (ax + aw + 4, ay + ah + 4)], fill="#CBD5E1")
        im.paste(art_im, (ax, ay))

    # Bottom caption box
    draw.rectangle([(50, 1450), (W - 50, 1750)], fill="#FFFFFF", outline="#E2E8F0", width=3)
    draw.text((W // 2, 1515), f'"{line1}', fill="#14285C", font=font_text, anchor="mm")
    draw.text((W // 2, 1575), f'{line2}"', fill="#14285C", font=font_text, anchor="mm")

    # Hook line
    draw.text((W // 2, 1680), "⭐ Can YOU find Little Star? ⭐", fill="#B3261E", font=font_sub, anchor="mm")

    # Footer attribution
    draw.text((W // 2, 1835), "Blobby World Official • Free Printables in Bio", fill="#718096", font=font_footer, anchor="mm")

    im.save(out_img_path, quality=95)

def build_single_video(day_num: int):
    page_idx = day_num
    line1, line2 = get_caption(day_num)
    spoken_text = (
        f"Day {day_num} of Pip's Christmas Countdown! "
        f"{line1} {line2} "
        f"Can you find Little Star hiding on this page? Comment below when you spot her!"
    )

    frame_png = os.path.join(TEMP_DIR, f"frame_{day_num:02d}.png")
    audio_mp3 = os.path.join(TEMP_DIR, f"audio_{day_num:02d}.mp3")
    final_mp4 = os.path.join(OUTPUT_VIDEOS, f"pip_countdown_day_{day_num:02d}.mp4")

    print(f"Generating Day {day_num} frame...")
    render_vertical_frame(page_idx, day_num, line1, line2, frame_png)

    print(f"Generating TTS narration for Day {day_num}...")
    asyncio.run(generate_narration(spoken_text, audio_mp3))

    # Compile with ffmpeg
    cmd = (
        f'ffmpeg -y -loop 1 -i "{frame_png}" -i "{audio_mp3}" '
        f'-c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p '
        f'-shortest -movflags +faststart "{final_mp4}"'
    )
    res = os.system(cmd)
    if res == 0:
        print(f"[OK] Video ready: {final_mp4}")
    else:
        print(f"[ERROR] Failed to compile Day {day_num}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", type=int, default=1, help="Day to build (1-25) or 0 for all")
    args = parser.parse_args()

    if args.day == 0:
        print("Generating all 25 daily countdown videos...")
        for d in range(1, 26):
            build_single_video(d)
    else:
        build_single_video(args.day)
