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

def create_banner():
    # 970 x 600 px banner (Standard Single Image)
    W, H = 970, 600
    bg = Image.new("RGB", (W, H), "#0b2545")
    draw = ImageDraw.Draw(bg)
    
    # Left side: Cover art preview
    if ART_COVER.exists():
        cover = Image.open(ART_COVER).convert("RGB")
        cover_w = int(H * 0.85 * (cover.width / cover.height))
        cover_h = int(H * 0.85)
        cover_resized = cover.resize((cover_w, cover_h), Image.Resampling.LANCZOS)
        
        # Paste cover with slight border
        pos_x = 50
        pos_y = (H - cover_h) // 2
        bg.paste(cover_resized, (pos_x, pos_y))
    
    # Right side: Text details
    font_title = get_font(44)
    font_sub = get_font(26)
    font_body = get_font(20)
    
    text_x = 480
    draw.text((text_x, 90), "PIP'S CHRISTMAS COUNTDOWN", font=font_title, fill="#FFD166")
    draw.text((text_x, 155), "A Story Coloring Book for Ages 3–6", font=font_sub, fill="#FFFFFF")
    
    bullets = [
        "✨ 25 Nights to Christmas + 25 Bonus Winter Adventures",
        "⭐ 'Can You Find Little Star?' Hidden Game on Every Page",
        "📖 Gentle 2-Line Rhyming Read-Aloud on Every Night",
        "🖍️ Big, Bold Outlines Engineered for Toddler Hands",
        "📄 Single-Sided Pages — Never Bleeds Through to Next Art",
        "🎁 Free 25-Star Countdown Tracker + Certificate Inside",
        "📍 Designed with Love in Tampa, FL by Blobby World"
    ]
    
    curr_y = 220
    for b in bullets:
        draw.text((text_x, curr_y), b, font=font_body, fill="#E0F2FE")
        curr_y += 45
        
    out_file = OUT_DIR / "a_plus_banner_970x600.png"
    bg.save(out_file, quality=95)
    print(f"Created banner: {out_file}")

def create_module_1():
    # 300 x 300 px: Story & Countdown
    W, H = 300, 300
    im = Image.new("RGB", (W, H), "#134e4a")
    draw = ImageDraw.Draw(im)
    
    if PAGE_01.exists():
        p1 = Image.open(PAGE_01).convert("L")
        p1_thumb = p1.resize((180, 200), Image.Resampling.LANCZOS)
        im.paste(p1_thumb, (60, 20))
        
    draw.rectangle([0, 240, W, H], fill="#0f766e")
    font = get_font(18)
    draw.text((25, 255), "25 NIGHTS TO CHRISTMAS", font=font, fill="#FFFFFF")
    
    out_file = OUT_DIR / "a_plus_module1_300x300.png"
    im.save(out_file, quality=95)
    print(f"Created module 1: {out_file}")

def create_module_2():
    # 300 x 300 px: Find Little Star Game
    W, H = 300, 300
    im = Image.new("RGB", (W, H), "#831843")
    draw = ImageDraw.Draw(im)
    
    if PAGE_25.exists():
        p25 = Image.open(PAGE_25).convert("L")
        p25_thumb = p25.resize((180, 200), Image.Resampling.LANCZOS)
        im.paste(p25_thumb, (60, 20))
        
    draw.rectangle([0, 240, W, H], fill="#be185d")
    font = get_font(18)
    draw.text((20, 255), "FIND LITTLE STAR GAME", font=font, fill="#FFFFFF")
    
    out_file = OUT_DIR / "a_plus_module2_300x300.png"
    im.save(out_file, quality=95)
    print(f"Created module 2: {out_file}")

def create_module_3():
    # 300 x 300 px: Single Sided Quality
    W, H = 300, 300
    im = Image.new("RGB", (W, H), "#1e293b")
    draw = ImageDraw.Draw(im)
    
    if PAGE_07.exists():
        p7 = Image.open(PAGE_07).convert("L")
        p7_thumb = p7.resize((180, 200), Image.Resampling.LANCZOS)
        im.paste(p7_thumb, (60, 20))
        
    draw.rectangle([0, 240, W, H], fill="#334155")
    font = get_font(18)
    draw.text((25, 255), "SINGLE-SIDED NO BLEED", font=font, fill="#FFFFFF")
    
    out_file = OUT_DIR / "a_plus_module3_300x300.png"
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
* **Image 1:** `a_plus_module1_300x300.png`
  - **Headline:** `25 Nights to Christmas`
  - **Body:** Follow Pip the penguin across 25 nightly adventures as he prepares for Christmas morning.
* **Image 2:** `a_plus_module2_300x300.png`
  - **Headline:** `Hidden Little Star Game`
  - **Body:** A smiling star hides on every page. Builds observational skills and visual tracking before bed.
* **Image 3:** `a_plus_module3_300x300.png`
  - **Headline:** `Zero Marker Bleed-Through`
  - **Body:** All 50 designs are printed single-sided on high-quality white paper with clean blank backs.

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
