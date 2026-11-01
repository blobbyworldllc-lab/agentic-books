"""Render the cover + sample interior pages to build/ (needed by make_social.py). Requires poppler (pdftoppm)."""
import os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B, K = f'{ROOT}/build', f'{ROOT}/output/kdp'
os.makedirs(B, exist_ok=True)
subprocess.run(['pdftoppm', '-r', '150', '-png', f'{K}/Pips_Christmas_Countdown_Cover.pdf', f'{B}/cov'], check=True)
for page, name in ((5, 'tracker'), (7, 'santa'), (109, 'cert'), (33, 'day13')):
    subprocess.run(['pdftoppm', '-r', '100', '-png', '-f', str(page), '-l', str(page), f'{K}/Pips_Christmas_Countdown_Interior.pdf', f'{B}/{name}'], check=True)
print('previews in', B)
