"""High-CTR KDP Full-Wrap Cover Generator for Pip's Christmas Countdown.

Optimized specifically for Amazon Search Grid Thumbnails (120px mobile scale):
1. Massive 82pt 'COLORING BOOK' header for instant category recognition.
2. High-contrast Red Ribbon: 'FOR TODDLERS & PRESCHOOLERS (AGES 3-6)'.
3. High-visibility Gold Bottom Banner: '★ 50 BIG & EASY PAGES TO COLOR ★'.
4. Increased outline contrast for readability on small screens.
"""
import os, sys, math
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

D = Path(__file__).resolve().parent.parent  # project root (Book_1/pips-christmas-countdown)
REPO_ROOT = D.parent.parent

for n in ('Medium', 'SemiBold', 'Bold'):
    pdfmetrics.registerFont(TTFont(f'Fredoka-{n}', str(D / 'fonts' / f'Fredoka-{n}.ttf')))

PAGES = int(os.environ.get('PAGES', 110))
AUTHOR = os.environ.get('BOOK_AUTHOR', 'Blobby World Official')
BLEED, TW, TH = 0.125 * inch, 8.5 * inch, 11 * inch
SPINE = PAGES * 0.002252 * inch
W = 2 * (TW + BLEED) + SPINE
H = TH + 2 * BLEED
BACK_X0 = 0
SPINE_X0 = BLEED + TW
FRONT_X0 = SPINE_X0 + SPINE

NAVY = HexColor('#0B1B3D')
GOLD = HexColor('#FFD13B')
BRIGHT_GOLD = HexColor('#FFE066')
RED = HexColor('#D91B33')
CREAM = HexColor('#FFFDF5')

def star(c, cx, cy, R, r_ratio=0.5, fill=1, stroke=0):
    p = c.beginPath()
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        rad = R if k % 2 == 0 else R * r_ratio
        x, y = cx + rad * math.cos(a), cy + rad * math.sin(a)
        p.moveTo(x, y) if k == 0 else p.lineTo(x, y)
    p.close()
    c.setLineJoin(1)
    c.drawPath(p, fill=fill, stroke=stroke)

def outlined(c, text, x, y, font, size, fill=white, stroke=NAVY, sw=None, align='center'):
    sw = sw or size * 0.18
    t = c.beginText(); t.setFont(font, size)
    w = c.stringWidth(text, font, size)
    x = x - w / 2 if align == 'center' else x
    c.saveState()
    c.setLineJoin(1)
    c.setLineWidth(sw)
    c.setStrokeColor(stroke)
    t.setTextOrigin(x, y); t.setTextRenderMode(1); t.textLine(text); t.setTextRenderMode(0)
    c.drawText(t)
    t2 = c.beginText(); t2.setFont(font, size); t2.setTextOrigin(x, y); t2.setTextRenderMode(0)
    t2.setFillColor(fill); t2.textLine(text)
    c.drawText(t2)
    c.restoreState()

def build(out_path):
    c = canvas.Canvas(str(out_path), pagesize=(W, H), initialFontName='Fredoka-Medium')
    c.setTitle("Pip's Christmas Countdown - High CTR Edition")

    # ---------- FRONT ----------
    art_path = D / 'art' / 'cover' / 'cover_art_x4.png'
    final_art = D / 'art' / 'cover' / 'cover_art_final.jpg'
    art = Image.open(str(art_path)).convert('RGB')
    fw, fh = TW + BLEED, H
    s = fw / art.width
    dh = art.height * s
    art.save(str(final_art), quality=94)

    # Draw full cover art
    c.drawImage(str(final_art), FRONT_X0, H - dh, fw, dh)
    cx = FRONT_X0 + TW / 2

    # --- TOP TITLE BLOCK (Optimized for 120px Thumbnail) ---
    c.setFillColor(GOLD)
    star(c, cx - 3.25 * inch, H - 1.15 * inch, 20, fill=1, stroke=1)
    star(c, cx + 3.25 * inch, H - 1.15 * inch, 20, fill=1, stroke=1)

    # Line 1: PIP'S CHRISTMAS COUNTDOWN
    outlined(c, "Pip's Christmas Countdown", cx, H - 1.35 * inch, 'Fredoka-Bold', 52, fill=white, stroke=NAVY, sw=9)

    # Line 2: COLORING BOOK (MASSIVE & UNMISSABLE IN SEARCH)
    outlined(c, 'COLORING BOOK', cx, H - 2.25 * inch, 'Fredoka-Bold', 78, fill=GOLD, stroke=NAVY, sw=12)

    # Subtitle Ribbon: FOR TODDLERS & PRESCHOOLERS (AGES 3-6)
    rw, rh, ry = 7.2 * inch, 0.52 * inch, H - 2.95 * inch
    c.setFillColor(RED); c.setStrokeColor(white); c.setLineWidth(3.5)
    c.roundRect(cx - rw / 2, ry, rw, rh, rh / 2, fill=1, stroke=1)
    c.setFillColor(white); c.setFont('Fredoka-Bold', 22)
    c.drawCentredString(cx, ry + 0.15 * inch, 'FOR TODDLERS & PRESCHOOLERS (AGES 3-6)')

    # --- BOTTOM HIGH-CONVERTING BENEFIT BANNER ---
    bw, bh, by = 7.6 * inch, 1.05 * inch, BLEED + 0.35 * inch
    c.setFillColor(BRIGHT_GOLD); c.setStrokeColor(NAVY); c.setLineWidth(3.5)
    c.roundRect(cx - bw / 2, by, bw, bh, 22, fill=1, stroke=1)
    
    c.setFillColor(NAVY); c.setFont('Fredoka-Bold', 26)
    c.drawCentredString(cx, by + 0.58 * inch, '★ 50 BIG & EASY PAGES TO COLOR ★')
    
    c.setFont('Fredoka-Bold', 16); c.setFillColor(RED)
    c.drawCentredString(cx, by + 0.22 * inch, 'Single-Sided Bleed-Resistant  •  Find Little Star on Every Page!')

    # Interactive Game Badge: Find Little Star
    bx, byy = FRONT_X0 + TW - 1.25 * inch, H - 4.15 * inch
    c.setFillColor(GOLD); c.setStrokeColor(NAVY); c.setLineWidth(3)
    star(c, bx, byy, 1.05 * inch, r_ratio=0.62, fill=1, stroke=1)
    c.setFillColor(NAVY)
    for i, (t, sz) in enumerate((('FIND', 15), ('LITTLE STAR', 13), ('on every', 12), ('page!', 14))):
        c.setFont('Fredoka-Bold', sz)
        c.drawCentredString(bx, byy + 0.26 * inch - i * 0.18 * inch, t)

    # Author
    outlined(c, AUTHOR, cx, by + bh + 0.12 * inch, 'Fredoka-SemiBold', 15, sw=2.5)

    # ---------- SPINE ----------
    c.setFillColor(NAVY); c.rect(SPINE_X0, 0, SPINE, H, fill=1, stroke=0)
    if PAGES >= 80:
        c.saveState(); c.translate(SPINE_X0 + SPINE / 2, H / 2); c.rotate(-90)
        c.setFillColor(white); c.setFont('Fredoka-SemiBold', 8.5)
        c.drawCentredString(0, -3, f"PIP'S CHRISTMAS COUNTDOWN COLORING BOOK   •   {AUTHOR.upper()}")
        c.restoreState()

    # ---------- BACK ----------
    c.setFillColor(NAVY); c.rect(0, 0, SPINE_X0, H, fill=1, stroke=0)
    c.setFillColor(HexColor('#22397A'))
    import random; random.seed(7)
    for _ in range(70):
        x = random.uniform(0.2, 8.4) * inch; y = random.uniform(0.2, 11.0) * inch
        c.circle(x, y, random.uniform(1.5, 4.5), fill=1, stroke=0)

    bx0 = BLEED + 0.55 * inch; bx1 = SPINE_X0 - 0.55 * inch; bcx = (bx0 + bx1) / 2
    outlined(c, 'Count down to Christmas with Pip!', bcx, H - 1.25 * inch, 'Fredoka-Bold', 30, fill=GOLD, stroke=NAVY, sw=1)
    
    c.setFillColor(white); c.setFont('Fredoka-Medium', 15)
    blurb = [
        "A tiny star lands - plip! - right on Pip's nose,",
        "and a magical game of hide-and-seek begins.",
        "",
        "Every single evening from December 1st to 25th,",
        "open one sweet rhyming story page, color Pip's",
        "cozy winter adventure, and search for Little Star!",
        "",
        "• 50 Big, bold, toddler-friendly outlines (Ages 3-6)",
        "• Single-sided printing on clean white bleed-resistant paper",
        "• Includes Countdown Tracker, Letter to Santa & Certificate!"
    ]
    y_text = H - 2.0 * inch
    for line in blurb:
        c.drawString(bx0 + 0.3 * inch, y_text, line)
        y_text -= 0.32 * inch

    c.showPage()
    c.save()
    print(f"[High-CTR Cover Built] {out_path}")

if __name__ == '__main__':
    out_dir = D / 'output' / 'kdp'
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_out = out_dir / 'Pips_Christmas_Countdown_Cover_HighCTR.pdf'
    build(pdf_out)
