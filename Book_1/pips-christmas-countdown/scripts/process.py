"""Stitch a two-column Gemini capture back into one image, then clean it to
print-ready 1-bit line art at 300 DPI.
usage: python3 process.py <screenshot.jpg> <page_no> [w h col vh]"""
import sys, os, cv2, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image

def stitch(path, w=765, h=1024, col=768, vh=730):
    shot = np.array(Image.open(path).convert('L'))
    out = np.full((h, w), 255, np.uint8)
    y = x = 0
    while y < h:
        rows = min(vh, h - y)
        out[y:y+rows] = shot[0:rows, x:x+w]
        y += rows; x += col
    return out

def clean(gray, scale=3.2):
    big = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    big = cv2.GaussianBlur(big, (0, 0), 1.6)
    bw = np.where(big < 150, 0, 255).astype(np.uint8)
    # remove specks
    n, lab, stats, _ = cv2.connectedComponentsWithStats(255 - bw, 8)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] < 40:
            bw[lab == i] = 255
    # trim to content
    ys, xs = np.where(bw == 0)
    pad = 10
    bw = bw[max(ys.min()-pad, 0):ys.max()+pad, max(xs.min()-pad, 0):xs.max()+pad]
    return bw

if __name__ == '__main__':
    src, page = sys.argv[1], int(sys.argv[2])
    dims = list(map(int, sys.argv[3:7])) if len(sys.argv) > 3 else []
    g = stitch(src, *dims)
    Image.fromarray(g).save(f'{ROOT}/art/raw_captures/raw_{page:02d}.png')
    bw = clean(g)
    Image.fromarray(bw).convert('1').save(f'{ROOT}/art/pages/p{page:02d}.png', dpi=(300, 300))
    print(page, bw.shape)
