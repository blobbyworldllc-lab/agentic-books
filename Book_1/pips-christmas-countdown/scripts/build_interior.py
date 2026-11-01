"""Build the KDP interior PDF: 8.5x11, no bleed, art one-sided (blank backs)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from captions import TITLE, COUNTDOWN, BONUS
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
for n in ('Medium', 'SemiBold', 'Bold'):
    pdfmetrics.registerFont(TTFont(f'Fredoka-{n}', f'{D}/fonts/Fredoka-{n}.ttf'))
W, H = 8.5 * inch, 11 * inch
IN, OUT, TOP, BOT = 0.7 * inch, 0.55 * inch, 0.55 * inch, 0.55 * inch   # recto margins
AUTHOR = os.environ.get('BOOK_AUTHOR', 'Blobby World Official')

def star(c, cx, cy, R, fill=0, lw=2.2, r_ratio=0.5, rounded=True):
    pts = []
    for k in range(10):
        ang = math.pi / 2 + k * math.pi / 5
        rad = R if k % 2 == 0 else R * r_ratio
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close()
    c.setLineJoin(1); c.setLineWidth(lw)
    c.drawPath(p, stroke=1, fill=fill)

def x_range(recto=True):
    return (IN, W - OUT) if recto else (OUT, W - IN)

def fit_text(c, text, font, maxsize, maxw):
    s = maxsize
    while s > 8 and c.stringWidth(text, font, s) > maxw: s -= 0.5
    return s

def center(c, text, y, font, size, maxw=None):
    x0, x1 = x_range()
    if maxw: size = fit_text(c, text, font, size, maxw)
    c.setFont(font, size); c.drawCentredString((x0 + x1) / 2, y, text)
    return size

def art(c, path, x, y, w, h):
    im = Image.open(path); iw, ih = im.size
    s = min(w / iw, h / ih); dw, dh = iw * s, ih * s
    px = (round(dw / 72 * 300), round(dh / 72 * 300))          # exactly 300 DPI at print size
    if px[0] < iw:
        im = im.convert('L').resize(px, Image.LANCZOS).point(lambda v: 0 if v < 140 else 255).convert('1')
    c.drawImage(ImageReader(im), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh)

def blank(c): c.showPage()

def badge(c, text, cx, cy):
    c.setFont('Fredoka-Bold', 15); tw = c.stringWidth(text, 'Fredoka-Bold', 15)
    w, h = tw + 34, 26
    c.setLineWidth(2); c.roundRect(cx - w / 2, cy - h / 2, w, h, 13, stroke=1, fill=0)
    star(c, cx - w / 2 + 14, cy, 6.5, lw=1.4)
    c.drawCentredString(cx + 7, cy - 5, text)

def coloring_page(c, n, caption, label):
    x0, x1 = x_range(); cx = (x0 + x1) / 2
    y = H - TOP - 14
    badge(c, label, cx, y)
    lines = caption.split(' / ')
    size = min(fit_text(c, l, 'Fredoka-SemiBold', 17, x1 - x0) for l in lines)
    c.setFont('Fredoka-SemiBold', size)
    ly = y - 34
    for l in lines:
        c.drawCentredString(cx, ly, l); ly -= size * 1.25
    art_top = ly - 2
    foot = BOT + 6
    if n == 25:
        ftxt = 'Little Star found her spot on top of the tree!'
    else:
        ftxt = 'Can you find Little Star?'
    c.setFont('Fredoka-Medium', 12); fw = c.stringWidth(ftxt, 'Fredoka-Medium', 12)
    c.drawCentredString(cx, foot, ftxt)
    star(c, cx - fw / 2 - 13, foot + 4, 6, lw=1.2); star(c, cx + fw / 2 + 13, foot + 4, 6, lw=1.2)
    art_bot = foot + 20
    path = f'{D}/art/pages/p{n:02d}.png'
    if os.path.exists(path):
        art(c, path, x0, art_bot, x1 - x0, art_top - art_bot)
    else:
        c.setDash(6, 6); c.rect(x0, art_bot, x1 - x0, art_top - art_bot); c.setDash()
        center(c, f'[art for page {n} pending]', (art_top + art_bot) / 2, 'Fredoka-Medium', 14)
    c.showPage()

def title_page(c):
    x0, x1 = x_range(); cx = (x0 + x1) / 2
    center(c, "Pip's Christmas", H - 1.6 * inch, 'Fredoka-Bold', 46)
    center(c, 'Countdown', H - 2.3 * inch, 'Fredoka-Bold', 46)
    center(c, 'A Story Coloring Book', H - 2.85 * inch, 'Fredoka-SemiBold', 20)
    center(c, '25 Nights to Christmas + 25 Bonus Winter Adventures', H - 3.2 * inch, 'Fredoka-Medium', 14, x1 - x0)
    art(c, f'{D}/art/pages/p01.png', x0 + 0.6 * inch, 1.6 * inch, x1 - x0 - 1.2 * inch, H - 5.0 * inch)
    center(c, AUTHOR, 1.0 * inch, 'Fredoka-SemiBold', 16)
    c.showPage()

def copyright_page(c):
    x0, x1 = x_range(False)
    c.setFont('Fredoka-Medium', 10.5)
    lines = [f"Pip's Christmas Countdown: A Story Coloring Book",
             f"Copyright © 2026 {AUTHOR}. All rights reserved.",
             "No part of this book may be reproduced or shared without written permission,",
             "except that the buyer may photocopy pages for personal, non-commercial use.",
             "Story text and line art created with AI assistance, selected and edited by the author.",
             "Pip, Little Star and friends are original characters.",
             "Coloring tip: place a sheet of card behind the page when using markers."]
    y = 2.6 * inch
    for l in lines:
        c.drawString(x0, y, l); y -= 16
    c.showPage()

def belongs_page(c):
    x0, x1 = x_range(); cx = (x0 + x1) / 2
    center(c, 'This Book Belongs To', H - 1.5 * inch, 'Fredoka-Bold', 38)
    c.setLineWidth(2.5); c.roundRect(x0 + 0.3 * inch, H - 3.0 * inch, x1 - x0 - 0.6 * inch, 0.95 * inch, 22)
    for k, sx in enumerate((x0 + 0.1 * inch, x1 - 0.1 * inch)):
        star(c, sx, H - 2.52 * inch, 16, lw=2.2)
    art(c, f'{D}/art/pages/p18.png', x0 + 0.5 * inch, 0.9 * inch, x1 - x0 - 1.0 * inch, H - 4.3 * inch)
    c.showPage()

def tracker_page(c):
    x0, x1 = x_range(); cx = (x0 + x1) / 2
    center(c, 'My Christmas Countdown', H - 1.2 * inch, 'Fredoka-Bold', 36, x1 - x0)
    center(c, 'Each night, read the story, color the page,', H - 1.7 * inch, 'Fredoka-Medium', 16)
    center(c, 'then color one star!', H - 1.98 * inch, 'Fredoka-Medium', 16)
    gw = x1 - x0; cell = gw / 5; top = H - 2.5 * inch
    for i in range(25):
        r, col = divmod(i, 5)
        sx = x0 + cell * (col + 0.5); sy = top - cell * (r + 0.5)
        star(c, sx, sy, cell * 0.46, lw=2.6, r_ratio=0.52)
        c.setFont('Fredoka-Bold', 20); c.drawCentredString(sx, sy - 9, str(i + 1))
    center(c, 'Day 25 is CHRISTMAS!', top - cell * 5 - 0.35 * inch, 'Fredoka-SemiBold', 18)
    c.showPage()

def santa_page(c):
    x0, x1 = x_range(); cx = (x0 + x1) / 2
    center(c, 'My Letter to Santa', H - 1.2 * inch, 'Fredoka-Bold', 38)
    c.setFont('Fredoka-SemiBold', 20); c.drawString(x0 + 0.2 * inch, H - 2.0 * inch, 'Dear Santa,')
    c.setLineWidth(1.4); y = H - 2.6 * inch
    for _ in range(8):
        c.line(x0 + 0.2 * inch, y, x1 - 0.2 * inch, y); y -= 0.5 * inch
    c.drawString(x0 + 0.2 * inch, y - 0.05 * inch, 'Love,')
    c.line(x0 + 1.0 * inch, y - 0.05 * inch, x0 + 3.6 * inch, y - 0.05 * inch)
    art(c, f'{D}/art/pages/p03.png', cx - 1.5 * inch, BOT, 3.0 * inch, y - BOT - 0.4 * inch)
    c.showPage()

def certificate_page(c):
    x0, x1 = x_range(); cx = (x0 + x1) / 2
    c.setLineWidth(4); c.roundRect(x0, BOT, x1 - x0, H - TOP - BOT, 26)
    c.setLineWidth(1.5); c.roundRect(x0 + 10, BOT + 10, x1 - x0 - 20, H - TOP - BOT - 20, 20)
    for sx, sy in ((x0 + 34, H - TOP - 34), (x1 - 34, H - TOP - 34), (x0 + 34, BOT + 34), (x1 - 34, BOT + 34)):
        star(c, sx, sy, 14)
    center(c, 'Christmas Coloring', H - 1.6 * inch, 'Fredoka-Bold', 40)
    center(c, 'CHAMPION', H - 2.3 * inch, 'Fredoka-Bold', 48)
    center(c, 'This certificate is proudly awarded to', H - 3.0 * inch, 'Fredoka-Medium', 17)
    c.setLineWidth(1.6); c.line(x0 + 1.0 * inch, H - 3.75 * inch, x1 - 1.0 * inch, H - 3.75 * inch)
    center(c, 'for coloring all 50 pages', H - 4.3 * inch, 'Fredoka-Medium', 17)
    center(c, 'and finding Little Star every single time!', H - 4.62 * inch, 'Fredoka-Medium', 17)
    art(c, f'{D}/art/pages/p44.png', cx - 2.0 * inch, 2.0 * inch, 4.0 * inch, H - 6.85 * inch)
    c.setFont('Fredoka-Medium', 14); ly = 1.5 * inch
    c.drawString(x0 + 0.7 * inch, ly, 'Date:'); c.line(x0 + 1.25 * inch, ly - 2, x0 + 3.1 * inch, ly - 2)
    c.drawString(x1 - 3.3 * inch, ly, 'Signed:'); c.line(x1 - 2.55 * inch, ly - 2, x1 - 0.7 * inch, ly - 2)
    c.showPage()

def build(out):
    c = canvas.Canvas(out, pagesize=(W, H), initialFontName='Fredoka-Medium'); c.setTitle(TITLE); c.setAuthor(AUTHOR)
    title_page(c); copyright_page(c)
    belongs_page(c); blank(c)
    tracker_page(c); blank(c)
    santa_page(c); blank(c)
    for n, t in COUNTDOWN:
        coloring_page(c, n, t, f'Day {n}'); blank(c)
    for n, t in BONUS:
        coloring_page(c, n, t, 'Winter Fun'); blank(c)
    certificate_page(c); blank(c)
    c.save()

if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else f'{D}/output/kdp/Pips_Christmas_Countdown_Interior.pdf')
