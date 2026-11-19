"""
Generates Amazon KDP A+ Content Graphics & Manifest for Pip's Christmas Countdown.
Brand: Blobby World Official
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
BOOK_DIR = REPO_ROOT / "Book_1" / "pips-christmas-countdown"
OUT_DIR = BOOK_DIR / "output" / "marketing" / "a_plus_content"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ART_COVER = BOOK_DIR / "art" / "cover" / "cover_art_final.jpg"
PAGE_01 = BOOK_DIR / "art" / "pages" / "p01.png"
PAGE_07 = BOOK_DIR / "art" / "pages" / "p07.png"
PAGE_25 = BOOK_DIR / "art" / "pages" / "p25.png"

def get_font(size):
    font_path = BOOK_DIR / "fonts" / "Fredoka-Bold.ttf"
    if font_path.exists():
        try:
            return ImageFont.truetype(str(font_path), size)
        except Exception:
            pass
    return ImageFont.load_default()

import math

def draw_star(draw, x, y, r=7, fill="#FFD166"):
    points = []
    for i in range(10):
        radius = r if i % 2 == 0 else r * 0.45
        angle = i * math.pi / 5 - math.pi / 2
        px = x + radius * math.cos(angle)
        py = y + radius * math.sin(angle)
        points.append((px, py))
    draw.polygon(points, fill=fill)

def create_banner():
    # 970 x 600 px banner (Standard Single Image)
    W, H = 970, 600
    bg = Image.new("RGB", (W, H), "#0b2545")
    draw = ImageDraw.Draw(bg)
    
    # Left side: Cover art preview with crisp white card border
    if ART_COVER.exists():
        cover = Image.open(ART_COVER).convert("RGB")
        cover_h = int(H * 0.86)
        cover_w = int(cover_h * (cover.width / cover.height))
        cover_resized = cover.resize((cover_w, cover_h), Image.Resampling.LANCZOS)
        
        pos_x = 45
        pos_y = (H - cover_h) // 2
        draw.rounded_rectangle([pos_x - 4, pos_y - 4, pos_x + cover_w + 4, pos_y + cover_h + 4], radius=10, fill="#FFFFFF")
        bg.paste(cover_resized, (pos_x, pos_y))
    
    # Right side: Text details
    font_title = get_font(32)
    font_sub = get_font(22)
    font_body = get_font(18)
    
    text_x = 460
    draw.text((text_x, 65), "PIP'S CHRISTMAS COUNTDOWN", font=font_title, fill="#FFD166")
    draw.text((text_x, 115), "A Story Coloring Book for Ages 3–6", font=font_sub, fill="#FFFFFF")
    
    bullets = [
        "25 Nights to Christmas + 25 Bonus Winter Adventures",
        "Hidden 'Find Little Star' Game on Every Page",
        "Gentle 2-Line Rhyming Read-Aloud on Every Night",
        "Big, Bold Outlines Engineered for Toddler Hands",
        "Single-Sided Pages — Never Bleeds Through",
        "Free 25-Star Countdown Tracker + Certificate Inside",
        "Designed with Love in Tampa, FL by Blobby World"
    ]
    
    curr_y = 175
    for b in bullets:
        draw_star(draw, text_x + 10, curr_y + 11, r=7, fill="#FFD166")
        draw.text((text_x + 28, curr_y), b, font=font_body, fill="#E0F2FE")
        curr_y += 48
        
    out_file = OUT_DIR / "a_plus_banner_970x600.png"
    bg.save(out_file, quality=95)
    print(f"Created banner: {out_file}")

FRAMES_DIR = BOOK_DIR / "output" / "marketing" / "3d_frames"

def build_3d_card(src_path, out_file, banner_text, crop_box=(60, 480, 1020, 1440)):
    im = Image.open(src_path)
    cropped = im.crop(crop_box)
    resized = cropped.resize((300, 300), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(resized)
    banner_h = 44
    draw.rectangle([0, 300 - banner_h, 300, 300], fill=(11, 37, 69))
    draw.line([0, 300 - banner_h, 300, 300 - banner_h], fill="#FFD166", width=2)
    font = get_font(15)
    bbox = font.getbbox(banner_text)
    tw = bbox[2] - bbox[0]
    draw.text(((300 - tw) // 2, 300 - banner_h + 12), banner_text, font=font, fill="#FFFFFF")
    draw.rectangle([0, 0, 299, 299], outline="#0b2545", width=2)
    resized.save(out_file, quality=95)

def create_module_1():
    out_file = OUT_DIR / "a_plus_module1_300x300.png"
    master = OUT_DIR / "a_plus_module1_3d_sledding_fullres.jpg"
    if master.exists():
        im = Image.open(master).convert("RGB")
        im.resize((300, 300), Image.Resampling.LANCZOS).save(out_file, quality=95)
    else:
        sled_frame = FRAMES_DIR / "sledding_t2s.png"
        if sled_frame.exists():
            build_3d_card(sled_frame, out_file, "25 NIGHTS OF ADVENTURE")
        else:
            W, H = 300, 300
            im = Image.new("RGB", (W, H), "#134e4a")
            draw = ImageDraw.Draw(im)
            if PAGE_01.exists():
                p1 = Image.open(PAGE_01).convert("L")
                im.paste(p1.resize((180, 200), Image.Resampling.LANCZOS), (60, 20))
            draw.rectangle([0, 240, W, H], fill="#0f766e")
            draw.text((25, 255), "25 NIGHTS TO CHRISTMAS", font=get_font(18), fill="#FFFFFF")
            im.save(out_file, quality=95)
    print(f"Created module 1: {out_file}")

def create_module_2():
    out_file = OUT_DIR / "a_plus_module2_300x300.png"
    master = OUT_DIR / "a_plus_module2_3d_skating_fullres.jpg"
    if master.exists():
        im = Image.open(master).convert("RGB")
        im.resize((300, 300), Image.Resampling.LANCZOS).save(out_file, quality=95)
    else:
        skate_frame = FRAMES_DIR / "skating_t2s.png"
        if skate_frame.exists():
            build_3d_card(skate_frame, out_file, "SCREEN-FREE BEDTIME MAGIC")
        else:
            W, H = 300, 300
            im = Image.new("RGB", (W, H), "#831843")
            draw = ImageDraw.Draw(im)
            if PAGE_25.exists():
                p25 = Image.open(PAGE_25).convert("L")
                im.paste(p25.resize((180, 200), Image.Resampling.LANCZOS), (60, 20))
            draw.rectangle([0, 240, W, H], fill="#be185d")
            draw.text((20, 255), "FIND LITTLE STAR GAME", font=get_font(18), fill="#FFFFFF")
            im.save(out_file, quality=95)
    print(f"Created module 2: {out_file}")

def create_module_3():
    out_file = OUT_DIR / "a_plus_module3_300x300.png"
    master = OUT_DIR / "a_plus_module3_3d_tree_star_fullres.jpg"
    if master.exists():
        im = Image.open(master).convert("RGB")
        im.resize((300, 300), Image.Resampling.LANCZOS).save(out_file, quality=95)
    else:
        tree_frame = FRAMES_DIR / "tree_t2s.png"
        if tree_frame.exists():
            build_3d_card(tree_frame, out_file, "FIND LITTLE STAR GAME")
        else:
            W, H = 300, 300
            im = Image.new("RGB", (W, H), "#1e293b")
            draw = ImageDraw.Draw(im)
            if PAGE_07.exists():
                p7 = Image.open(PAGE_07).convert("L")
                im.paste(p7.resize((180, 200), Image.Resampling.LANCZOS), (60, 20))
            draw.rectangle([0, 240, W, H], fill="#334155")
            draw.text((25, 255), "SINGLE-SIDED NO BLEED", font=get_font(18), fill="#FFFFFF")
            im.save(out_file, quality=95)
    print(f"Created module 3: {out_file}")

def generate_manifest():
    manifest_file = OUT_DIR / "A_PLUS_CONTENT_GUIDE.md"
    guide = f"""# Amazon KDP A+ Content Submission Kit
**Book:** Pip's Christmas Countdown (ASIN: `B0HPZ647J6`)
**Publisher:** Blobby World Official

---

## How to Submit on Amazon KDP (Takes 3 Minutes):
1. Sign in to **Amazon KDP** -> click **Marketing** tab.
2. Scroll to **A+ Content** -> Click **Manage A+ Content** -> Click **Start creating A+ content**.
3. **Content Name:** `Pips Christmas Countdown Launch A+` (Language: English).
4. Click **Add Module**:

---

### Module 1: Standard Image & Dark Header (or Standard Single Image)
* **Upload Image:** `a_plus_banner_970x600.png`
* **Image Alt Text:** `Pip's Christmas Countdown Story Coloring Book for Ages 3-6 by Blobby World`
* **Headline:** `The Magical 25-Night Bedtime Coloring Countdown for Toddlers & Preschoolers`
* **Body Text:**
  Make bedtime special every night in December! Each evening features a sweet rhyming read-aloud story page, big simple coloring shapes, and the joyful 'Find Little Star' seek-and-find game. Printed on pure white paper with blank backs so markers and crayons never bleed through.

---

### Module 2: Standard 3 Images & Text
* **Image 1 (Column 1):** `a_plus_module1_300x300.png`
  - **Alt Text:** `Pip the baby penguin joyfully riding a red holiday sled with golden bells down a snowy hill`
  - **Headline:** `25 Nights of Adventure`
  - **Body:** Follow Pip the penguin across 25 nightly adventures as he sleds, bakes cookies, and counts down to Christmas.
* **Image 2 (Column 2):** `a_plus_module2_300x300.png`
  - **Alt Text:** `Pip the baby penguin ice skating across a glowing frozen pond under twilight fairy lights`
  - **Headline:** `Screen-Free Bedtime Magic`
  - **Body:** Gentle rhyming stories and soothing holiday scenes designed specifically for calming evening wind-downs.
* **Image 3 (Column 3):** `a_plus_module3_300x300.png`
  - **Alt Text:** `Pip the baby penguin sitting by a glowing Christmas tree with presents as Little Star floats happily`
  - **Headline:** `Find Little Star Game`
  - **Body:** A smiling star hides on every page. Builds observational focus and visual tracking before bed.

---

5. Click **Apply ASINs** -> Enter `B0HPZ647J6` -> Click **Apply content**.
6. Click **Review & Submit** -> Click **Submit for approval**.
Amazon typically approves KDP A+ Content within 24 to 48 hours.
"""
    manifest_file.write_text(guide, encoding="utf-8")
    print(f"Created guide: {manifest_file}")

if __name__ == "__main__":
    create_banner()
    create_module_1()
    create_module_2()
    create_module_3()
    generate_manifest()
