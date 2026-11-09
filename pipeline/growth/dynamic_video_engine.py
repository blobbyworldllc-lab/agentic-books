"""
Dynamic Universal Video & Outro Engine
Generates dynamic, book-agnostic promotional shorts and Amazon CTA outro cards for ANY book
launched across the pipeline (Pip's Christmas Countdown, Bug Safari Mazes, Glitch Boy, etc.).

Standards Enforced:
1. Pure soothing, enchanting background music (zero spoken voiceover interruption).
2. Dynamic Amazon Outro Card reading live ASIN, Title, Age Group, and Key Bullets.
3. Golden 'BUY NOW ON AMAZON' button + direct amazon.com/dp/{asin} URL.
4. Seamless 0.5s visual crossfade dissolve from 3D animation to Outro Card.
5. Dynamic description and tag generation with prominent Amazon buy links.
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FONTS_DIR = REPO_ROOT / "Book_1" / "pips-christmas-countdown" / "fonts"
CATALOG_PATH = REPO_ROOT / "pipeline" / "catalog.json"

DEFAULT_THEMES = {
    "christmas": {
        "primary": "#1A362B",
        "accent": "#B3261E",
        "badge_bg": "#B3261E",
        "badge_text": "#FFEB3B",
        "card_bg": (255, 255, 255, 240),
        "card_border": (179, 38, 30, 255)
    },
    "puzzle": {
        "primary": "#1B3A4B",
        "accent": "#2E7D32",
        "badge_bg": "#2E7D32",
        "badge_text": "#FFFFFF",
        "card_bg": (255, 255, 255, 240),
        "card_border": (46, 125, 50, 255)
    },
    "default": {
        "primary": "#1A202C",
        "accent": "#3182CE",
        "badge_bg": "#3182CE",
        "badge_text": "#FFFFFF",
        "card_bg": (255, 255, 255, 240),
        "card_border": (49, 130, 206, 255)
    }
}

def get_book_metadata(slug_or_asin: str) -> dict:
    """Dynamically retrieve book specifications from pipeline catalog."""
    if CATALOG_PATH.exists():
        try:
            data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
            for b in data.get("books", []):
                if b.get("slug") == slug_or_asin or b.get("asin") == slug_or_asin:
                    return b
        except Exception:
            pass
    # Fallback default for Book 1
    return {
        "slug": "pips-christmas-countdown",
        "title": "Pip's Christmas Countdown",
        "asin": "B0HPZ647J6",
        "type": "seasonal",
        "price": 9.99
    }

def generate_dynamic_amazon_outro(
    book_meta: dict,
    output_img_path: str,
    output_video_path: str,
    music_wav_path: str,
    duration_s: float = 3.5,
    custom_badge: str = None,
    custom_bullets: list = None
):
    """
    Renders 1080x1920 dynamic Amazon CTA Outro card and compiles a 3.5s video
    with pure soothing music (zero spoken voiceover interruption).
    """
    W, H = 1080, 1920
    b_type = book_meta.get("type", "default")
    theme = DEFAULT_THEMES.get(b_type, DEFAULT_THEMES["default"])
    asin = book_meta.get("asin", "B0HPZ647J6")
    title = book_meta.get("title", "Pip's Christmas Countdown")

    # Determine theme background
    im = Image.new("RGBA", (W, H), theme["primary"])
    # Gradient overlay
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_over = ImageDraw.Draw(overlay)
    
    # White content card
    card_x0, card_y0, card_x1, card_y1 = 80, 320, W - 80, 1600
    d_over.rounded_rectangle(
        [(card_x0, card_y0), (card_x1, card_y1)],
        radius=45,
        fill=theme["card_bg"],
        outline=theme["card_border"],
        width=8
    )
    im = Image.alpha_composite(im, overlay).convert("RGB")
    draw = ImageDraw.Draw(im)

    f_bold = str(FONTS_DIR / "Fredoka-Bold.ttf")
    f_semi = str(FONTS_DIR / "Fredoka-SemiBold.ttf")

    font_badge = ImageFont.truetype(f_bold, 42)
    font_title = ImageFont.truetype(f_bold, 74)
    font_sub = ImageFont.truetype(f_semi, 44)
    font_bullet = ImageFont.truetype(f_semi, 38)
    font_btn = ImageFont.truetype(f_bold, 54)
    font_url = ImageFont.truetype(f_bold, 44)

    # 1. Badge
    badge_text = custom_badge or ("CHRISTMAS GIFT GUIDE" if b_type == "seasonal" else "ACTIVITY & STORY BOOK")
    draw.rounded_rectangle([(W//2 - 270, 380), (W//2 + 270, 460)], radius=25, fill=theme["badge_bg"])
    draw.text((W // 2, 420), badge_text, fill=theme["badge_text"], font=font_badge, anchor="mm")

    # 2. Dynamic Title
    title_lines = [title] if len(title) <= 24 else [title[:22], title[22:].strip()]
    y_title = 540 if len(title_lines) == 1 else 520
    for tl in title_lines:
        draw.text((W // 2, y_title), tl, fill=theme["primary"], font=font_title, anchor="mm")
        y_title += 80

    # 3. Subtitle / Details
    sub_text = "50 Big & Easy Designs | Ages 3-6" if "pip" in title.lower() else "Perfect Screen-Free Learning Activity"
    draw.text((W // 2, y_title + 20), sub_text, fill="#4A5568", font=font_sub, anchor="mm")

    # 4. Bullet Points
    bullets = custom_bullets or [
        "Bedtime Stories & Beautiful Illustrations",
        "Big Simple Designs (Zero Marker Bleed)",
        "Fun Seek-and-Find Activity on Every Page",
        "Perfect Gift for Toddlers & Preschoolers"
    ]
    y_bullet = y_title + 110
    for b in bullets[:4]:
        draw.text((W // 2, y_bullet), f"• {b}", fill="#2D3748", font=font_bullet, anchor="mm")
        y_bullet += 65

    # 5. Golden Amazon "BUY NOW" Button
    btn_x0, btn_y0, btn_x1, btn_y1 = 150, 1200, W - 150, 1340
    draw.rounded_rectangle([(btn_x0, btn_y0), (btn_x1, btn_y1)], radius=40, fill="#FF9900", outline="#E68A00", width=4)
    draw.text((W // 2, 1270), "BUY NOW ON AMAZON", fill="#111111", font=font_btn, anchor="mm")

    # 6. Prominent Direct Amazon URL
    draw.rounded_rectangle([(180, 1380), (W - 180, 1470)], radius=25, fill="#EDF2F7")
    draw.text((W // 2, 1425), f"amazon.com/dp/{asin}", fill=theme["primary"], font=font_url, anchor="mm")

    # 7. Sub-Note
    draw.text((W // 2, 1530), "Click description link to order on Amazon Prime!", fill=theme["accent"], font=ImageFont.truetype(f_bold, 34), anchor="mm")

    # 8. Branding
    draw.text((W // 2, 1720), "Blobby World Official", fill="#FFFFFF", font=ImageFont.truetype(f_bold, 48), anchor="mm")

    os.makedirs(os.path.dirname(output_img_path), exist_ok=True)
    im.save(output_img_path, quality=95)

    # Compile Outro Video with pure soothing music
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", output_img_path,
        "-i", music_wav_path,
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-shortest", "-t", str(duration_s),
        output_video_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_video_path

def assemble_dynamic_short(
    animation_clip_path: str,
    outro_card_img_path: str,
    music_wav_path: str,
    output_short_path: str,
    anim_duration_s: float = 6.5,
    outro_duration_s: float = 3.5,
    crossfade_s: float = 0.5
):
    """
    Assembles a master short:
    Part 1: Real 3D Moving Animation (0.0 to 6.5s)
    Transition: 0.5s visual dissolve (xfade)
    Part 2: Dynamic Amazon Buy Card (6.5s to 9.5s)
    Audio: 100% pure continuous soothing music box (no spoken voiceover).
    """
    scratch_dir = Path(output_short_path).parent / "temp_render"
    scratch_dir.mkdir(parents=True, exist_ok=True)

    part1 = scratch_dir / "temp_anim.mp4"
    part2 = scratch_dir / "temp_card.mp4"
    video_xfaded = scratch_dir / "temp_xfaded.mp4"

    # 1. Scale animation to 1080x1920 25fps
    subprocess.run([
        "ffmpeg", "-y", "-ss", "0", "-t", str(anim_duration_s),
        "-i", str(animation_clip_path),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25", "-an",
        str(part1)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Render Card to video
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(outro_card_img_path),
        "-c:v", "libx264", "-t", str(outro_duration_s), "-pix_fmt", "yuv420p", "-r", "25", "-an",
        str(part2)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. Apply smooth visual crossfade
    offset = anim_duration_s - crossfade_s
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(part1), "-i", str(part2),
        "-filter_complex", f"[0:v][1:v]xfade=transition=fade:duration={crossfade_s}:offset={offset}[v]",
        "-map", "[v]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25",
        str(video_xfaded)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 4. Mux with continuous soothing music
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(video_xfaded),
        "-i", str(music_wav_path),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output_short_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return output_short_path

def generate_dynamic_post_copy(book_meta: dict, hook_title: str) -> dict:
    """Generate dynamic title, description, and tags for any social video."""
    asin = book_meta.get("asin", "B0HPZ647J6")
    title = book_meta.get("title", "Pip's Christmas Countdown")
    price = book_meta.get("price", 9.99)
    amazon_url = f"https://www.amazon.com/dp/{asin}"

    description = f"""{hook_title} ✨

📖 Order {title} Paperback on Amazon Prime:
{amazon_url}

🎁 Free Printable Activity Pack:
https://blobbyworldllc-lab.github.io/agentic-books/

Full collection by Blobby World Official. Clean, single-sided pages designed for kids!

#Shorts #ChildrensBooks #ActivityBooks #AmazonBooks #{title.replace(" ", "").replace("'", "")} #KidsAnimation
"""
    return {
        "title": f"{hook_title} | {title} #Shorts",
        "description": description.strip(),
        "amazon_url": amazon_url,
        "asin": asin,
        "tags": [
            title,
            "Kids Books",
            "Coloring Book",
            "Storybook",
            "Amazon Books",
            "Blobby World Official",
            "Shorts"
        ]
    }
