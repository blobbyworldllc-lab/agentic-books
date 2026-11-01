"""KDP full-wrap paperback cover: 8.5x11 trim, white paper, bleed 0.125"."""
import os, sys, math
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageOps

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
for n in ('Medium', 'SemiBold', 'Bold'):
    pdfmetrics.registerFont(TTFont(f'Fredoka-{n}', f'{D}/fonts/Fredoka-{n}.ttf'))
PAGES = int(os.environ.get('PAGES', 110))
AUTHOR = os.environ.get('BOOK_AUTHOR', 'Blobby World Official')
BLEED, TW, TH = 0.125 * inch, 8.5 * inch, 11 * inch
SPINE = PAGES * 0.002252 * inch
W = 2 * (TW + BLEED) + SPINE
H = TH + 2 * BLEED
BACK_X0 = 0; SPINE_X0 = BLEED + TW; FRONT_X0 = SPINE_X0 + SPINE
NAVY, GOLD, RED, CREAM = HexColor('#14285C'), HexColor('#FFC93C'), HexColor('#D7263D'), HexColor('#FFF8E7')

def star(c, cx, cy, R, r_ratio=0.5, fill=1, stroke=0):
    p = c.beginPath()
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5; rad = R if k % 2 == 0 else R * r_ratio
        x, y = cx + rad * math.cos(a), cy + rad * math.sin(a)
        p.moveTo(x, y) if k == 0 else p.lineTo(x, y)
    p.close(); c.setLineJoin(1); c.drawPath(p, fill=fill, stroke=stroke)

def outlined(c, text, x, y, font, size, fill=white, stroke=NAVY, sw=None, align='center'):
    sw = sw or size * 0.16
    t = c.beginText(); t.setFont(font, size)
    w = c.stringWidth(text, font, size)
    x = x - w / 2 if align == 'center' else x
    c.saveState(); c.setLineJoin(1); c.setLineWidth(sw); c.setStrokeColor(stroke)
    t.setTextOrigin(x, y); t.setTextRenderMode(1); t.textLine(text); t.setTextRenderMode(0); c.drawText(t)
    t2 = c.beginText(); t2.setFont(font, size); t2.setTextOrigin(x, y); t2.setTextRenderMode(0)
    t2.setFillColor(fill); t2.textLine(text); c.drawText(t2); c.restoreState()

def build(out):
    c = canvas.Canvas(out, pagesize=(W, H), initialFontName='Fredoka-Medium'); c.setTitle("Pip's Christmas Countdown - Cover")
    # ---------- FRONT ----------
    art = Image.open(f'{D}/art/cover/cover_art_x4.png').convert('RGB')
    fw, fh = TW + BLEED, H
    s = fw / art.width; dh = art.height * s
    art.save(f'{D}/art/cover/cover_art_final.jpg', quality=92)
    # anchor art to top (keep sky for title); crop bottom
    c.drawImage(f'{D}/art/cover/cover_art_final.jpg', FRONT_X0, H - dh, fw, dh)
    cx = FRONT_X0 + TW / 2
    # title
    c.setFillColor(GOLD); star(c, cx - 3.05 * inch, H - 1.25 * inch, 16)
    star(c, cx + 3.05 * inch, H - 1.25 * inch, 16)
    outlined(c, "Pip's Christmas", cx, H - 1.45 * inch, 'Fredoka-Bold', 60)
    outlined(c, 'Countdown', cx, H - 2.3 * inch, 'Fredoka-Bold', 74, fill=GOLD)
    # subtitle ribbon
    rw, rh, ry = 6.5 * inch, 0.5 * inch, H - 3.0 * inch
    c.setFillColor(RED); c.setStrokeColor(white); c.setLineWidth(3)
    c.roundRect(cx - rw / 2, ry, rw, rh, rh / 2, fill=1, stroke=1)
    c.setFillColor(white); c.setFont('Fredoka-SemiBold', 22)
    c.drawCentredString(cx, ry + 0.155 * inch, 'A Story Coloring Book for Kids Ages 3-6')
    # bottom banner
    bw, bh, by = 7.4 * inch, 0.95 * inch, BLEED + 0.38 * inch
    c.setFillColor(CREAM); c.setStrokeColor(NAVY); c.setLineWidth(3)
    c.roundRect(cx - bw / 2, by, bw, bh, 22, fill=1, stroke=1)
    c.setFillColor(NAVY); c.setFont('Fredoka-Bold', 23)
    c.drawCentredString(cx, by + 0.53 * inch, '50 Big & Easy Pages to Color')
    c.setFont('Fredoka-Medium', 15); c.setFillColor(RED)
    c.drawCentredString(cx, by + 0.2 * inch, '25 Nights to Christmas  +  25 Bonus Winter Adventures')
    # burst badge: hide and seek
    bx, byy = FRONT_X0 + TW - 1.15 * inch, H - 4.25 * inch
    c.setFillColor(GOLD); c.setStrokeColor(NAVY); c.setLineWidth(2.5)
    star(c, bx, byy, 0.95 * inch, r_ratio=0.62, fill=1, stroke=1)
    c.setFillColor(NAVY)
    for i, (t, sz) in enumerate((('Find', 13), ('Little Star', 13), ('on every', 13), ('page!', 13))):
        c.setFont('Fredoka-Bold', sz); c.drawCentredString(bx, byy + 0.24 * inch - i * 0.17 * inch, t)
    # author
    c.setFillColor(white); c.setFont('Fredoka-SemiBold', 14)
    outlined(c, AUTHOR, cx, by + bh + 0.12 * inch, 'Fredoka-SemiBold', 15, sw=2.5)

    # ---------- SPINE ----------
    c.setFillColor(NAVY); c.rect(SPINE_X0, 0, SPINE, H, fill=1, stroke=0)
    if PAGES >= 80:
        c.saveState(); c.translate(SPINE_X0 + SPINE / 2, H / 2); c.rotate(-90)
        c.setFillColor(white); c.setFont('Fredoka-SemiBold', 8.5)
        c.drawCentredString(0, -3, f"PIP'S CHRISTMAS COUNTDOWN   •   {AUTHOR.upper()}")
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
    blurb = ["A tiny star lands - plip! - right on Pip's nose,",
             "and a magical game of hide-and-seek begins.",
             "Each night, read one rhyming line together, color",
             "Pip's adventure, and find Little Star hiding on every page!"]
    y = H - 1.85 * inch
    for l in blurb: c.drawCentredString(bcx, y, l); y -= 0.27 * inch
    # sample page thumbnails
    tw_, th_ = 1.95 * inch, 2.5 * inch; gap = (bx1 - bx0 - 3 * tw_) / 2; ty = y - 0.25 * inch - th_
    for i, p in enumerate((8, 21, 41)):
        x = bx0 + i * (tw_ + gap)
        c.setFillColor(white); c.setStrokeColor(GOLD); c.setLineWidth(3)
        c.roundRect(x, ty, tw_, th_, 12, fill=1, stroke=1)
        im = Image.open(f'{D}/art/pages/p{p:02d}.png'); s2 = min((tw_ - 16) / im.width, (th_ - 16) / im.height)
        c.drawImage(ImageReader(im.convert('L')), x + (tw_ - im.width * s2) / 2, ty + (th_ - im.height * s2) / 2, im.width * s2, im.height * s2)
    # features
    feats = ['25 countdown story pages for December 1-25, plus 25 bonus winter adventures',
             'Big, bold, easy-to-color designs made for little hands',
             'A short read-aloud rhyme on every page',
             'Find-Little-Star game on every page',
             'Countdown tracker, Letter to Santa & Coloring Champion certificate',
             'One design per sheet - no marker bleed-through, easy to tear out and hang']
    y = ty - 0.42 * inch
    for f in feats:
        c.setFillColor(GOLD); star(c, bx0 + 8, y + 5, 7)
        c.setFillColor(white); c.setFont('Fredoka-Medium', 13.5); c.drawString(bx0 + 24, y, f); y -= 0.3 * inch
    c.setFillColor(GOLD); c.setFont('Fredoka-SemiBold', 15)
    c.drawString(bx0, BLEED + 0.75 * inch, 'A perfect stocking stuffer')
    c.drawString(bx0, BLEED + 0.48 * inch, 'and Christmas Eve box gift!')
    # barcode clear zone (KDP prints barcode here): bottom-right 2" x 1.2", 0.25" in from trim
    c.setFillColor(white); c.rect(SPINE_X0 - 0.25 * inch - 2.0 * inch, BLEED + 0.25 * inch, 2.0 * inch, 1.2 * inch, fill=1, stroke=0)
    c.showPage(); c.save()
    print(f'cover {W/inch:.4f} x {H/inch:.4f} in, spine {SPINE/inch:.4f} in')

if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else f'{D}/output/kdp/Pips_Christmas_Countdown_Cover.pdf')
