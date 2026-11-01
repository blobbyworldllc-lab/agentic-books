"""Ready-to-post social graphics for Pip's Christmas Countdown (IG 1080x1350, Pinterest 1000x1500)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, math
import os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
OUT = f'{D}/output/marketing'
os.makedirs(f'{D}/build', exist_ok=True)
NAVY, GOLD, RED, CREAM, WHITE = (20, 40, 92), (255, 201, 60), (215, 38, 61), (255, 248, 231), (255, 255, 255)
F = lambda w, s: ImageFont.truetype(f'{D}/fonts/Fredoka-{w}.ttf', s)

cov = Image.open(f'{D}/build/cov-1.png').convert('RGB')
W_, H_ = cov.size
# front panel: right of spine. full width 17.4977in @150dpi
front = cov.crop((int(W_ - (8.5 + 0.125) * 150) + int(0.125 * 150) - 19, 19, W_ - 19, H_ - 19))

def bg(w, h, seed=1):
    im = Image.new('RGB', (w, h), NAVY); d = ImageDraw.Draw(im); random.seed(seed)
    for _ in range(140):
        x, y, r = random.randint(0, w), random.randint(0, h), random.randint(2, 7)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(60, 85, 150))
    return im

def star(d, cx, cy, R, fill=GOLD, outline=None, width=0):
    pts = [(cx + (R if k % 2 == 0 else R * .5) * math.cos(math.pi / 2 + k * math.pi / 5),
            cy - (R if k % 2 == 0 else R * .5) * math.sin(math.pi / 2 + k * math.pi / 5)) for k in range(10)]
    d.polygon(pts, fill=fill, outline=outline, width=width)

def ctext(d, y, text, font, fill=WHITE, w=1080, stroke=0, sfill=NAVY):
    tw = d.textlength(text, font=font)
    d.text(((w - tw) / 2, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=sfill)

def card(img, w, pad=14, radius=28, border=GOLD):
    im = img.copy(); im.thumbnail((w, 10000))
    c = Image.new('RGB', (im.width + 2 * pad, im.height + 2 * pad), WHITE)
    c.paste(im, (pad, pad))
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), radius, fill=255)
    out = Image.new('RGBA', (c.width + 12, c.height + 12), (0, 0, 0, 0))
    b = Image.new('RGB', out.size, border)
    bm = Image.new('L', out.size, 0); ImageDraw.Draw(bm).rounded_rectangle((0, 0, out.width - 1, out.height - 1), radius + 6, fill=255)
    out.paste(b, (0, 0), bm); out.paste(c, (6, 6), m)
    return out

def page_art(n):
    return Image.open(f'{D}/art/pages/p{n:02d}.png').convert('RGB')

out = []
# 1. Launch post
im = bg(1080, 1350, 3); d = ImageDraw.Draw(im)
ctext(d, 40, 'NEW for Christmas!', F('Bold', 74), GOLD)
cv = front.copy(); cv.thumbnail((700, 900)); c = card(cv, 700, pad=0, radius=18)
im.paste(c, ((1080 - c.width) // 2, 150), c)
ctext(d, 150 + c.height + 26, '25 nights of stories + 50 pages to color', F('SemiBold', 40))
ctext(d, 150 + c.height + 80, 'Search "Pip\'s Christmas Countdown" on Amazon', F('Medium', 34), GOLD)
out.append(('ig_1_launch.png', im))

# 2. Find Little Star game
im = bg(1080, 1350, 5); d = ImageDraw.Draw(im)
ctext(d, 34, 'Can YOU find', F('Bold', 80), WHITE)
ctext(d, 120, 'Little Star?', F('Bold', 96), GOLD)
c = card(page_art(12), 690); im.paste(c, ((1080 - c.width) // 2, 250), c)
ctext(d, 250 + c.height + 22, 'Comment where she\'s hiding!', F('SemiBold', 44))
out.append(('ig_2_find_little_star.png', im))

# 3. Free coloring page
im = bg(1080, 1350, 7); d = ImageDraw.Draw(im)
d.rounded_rectangle((300, 36, 780, 120), 42, fill=RED); ctext(d, 46, 'FREE PAGE', F('Bold', 58))
ctext(d, 140, 'Day 1 of Pip\'s Christmas Countdown', F('SemiBold', 44), GOLD)
c = card(page_art(1), 720); im.paste(c, ((1080 - c.width) // 2, 220), c)
ctext(d, 220 + c.height + 22, 'Free printable: link in bio', F('SemiBold', 44))
out.append(('ig_3_free_page.png', im))

# 4. What's inside collage
im = bg(1080, 1350, 9); d = ImageDraw.Draw(im)
ctext(d, 34, 'What\'s inside', F('Bold', 84), GOLD)
tiles = [Image.open(f'{D}/build/{f}').convert('RGB') for f in ('day13-033.png', 'tracker-005.png', 'santa-007.png', 'cert-109.png')]
labels = ['A rhyme a night', 'Countdown tracker', 'Letter to Santa', 'Champion certificate']
for i, (t, lab) in enumerate(zip(tiles, labels)):
    c = card(t, 380, pad=8, radius=20); x = 110 + (i % 2) * 470; y = 150 + (i // 2) * 575
    im.paste(c, (x, y), c)
    tw = d.textlength(lab, font=F('SemiBold', 36)); d.text((x + (c.width - tw) / 2, y + c.height + 8), lab, font=F('SemiBold', 36), fill=WHITE)
out.append(('ig_4_whats_inside.png', im))

# 5. Pinterest pin (1000x1500)
im = bg(1000, 1500, 11); d = ImageDraw.Draw(im)
ctext(d, 40, 'Christmas Coloring Pages', F('Bold', 66), GOLD, w=1000)
ctext(d, 120, 'for Kids Ages 3-6', F('SemiBold', 52), WHITE, w=1000)
for i, n in enumerate((4, 14, 21, 44)):
    c = card(page_art(n), 400, pad=8, radius=18); x = 70 + (i % 2) * 460; y = 220 + (i // 2) * 560
    im.paste(c, (x, y), c)
ctext(d, 1380, '50 pages + a 25-night story  |  on Amazon', F('SemiBold', 40), GOLD, w=1000)
out.append(('pin_1_coloring_pages.png', im))

for name, im in out:
    im.convert('RGB').save(f'{OUT}/{name}')
print([n for n, _ in out])
