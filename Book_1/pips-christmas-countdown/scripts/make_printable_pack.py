"""Free 4-page printable lead magnet: promo page + countdown tracker + Day 1 + Day 2 (interior PDF pages 5, 9, 11)."""
import os, io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for n in ('Medium', 'SemiBold', 'Bold'):
    pdfmetrics.registerFont(TTFont(f'Fredoka-{n}', f'{ROOT}/fonts/Fredoka-{n}.ttf'))
b = io.BytesIO(); c = canvas.Canvas(b, pagesize=(612, 792), initialFontName='Fredoka-Medium')
c.setFont('Fredoka-Bold', 34); c.drawCentredString(306, 700, "Free Printable Pack")
c.setFont('Fredoka-SemiBold', 22); c.drawCentredString(306, 660, "from Pip's Christmas Countdown")
c.setFont('Fredoka-Medium', 15)
lines = ["Inside: the Countdown Tracker + Day 1 and Day 2 story pages.",
         "Print them, read the rhyme together, and find Little Star!", "",
         "Loved it? The full book has 25 countdown nights,",
         "25 bonus winter adventures, a Letter to Santa page",
         "and a Coloring Champion certificate.", "",
         "Search \"Pip's Christmas Countdown\" on Amazon.", "",
         "Free for personal and classroom use. Please do not resell."]
for i, l in enumerate(lines): c.drawCentredString(306, 590 - i * 24, l)
c.save(); b.seek(0)
r = PdfReader(f'{ROOT}/output/kdp/Pips_Christmas_Countdown_Interior.pdf'); w = PdfWriter()
w.add_page(PdfReader(b).pages[0])
for p in (4, 8, 10): w.add_page(r.pages[p])   # tracker, Day 1, Day 2 (0-based)
w.write(f'{ROOT}/output/marketing/Pip_Free_Printable_Pack.pdf'); print('ok')
