from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
for n in ('Medium', 'SemiBold', 'Bold'):
    pdfmetrics.registerFont(TTFont(f'Fredoka-{n}', f'{D}/fonts/Fredoka-{n}.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu', f'{D}/fonts/DejaVuSans.ttf'))
NAVY, RED, GREY = colors.HexColor('#14285C'), colors.HexColor('#B3261E'), colors.HexColor('#555555')
H1 = ParagraphStyle('h1', fontName='Fredoka-Bold', fontSize=22, leading=26, textColor=NAVY, spaceAfter=4)
SUB = ParagraphStyle('s', fontName='DejaVu', fontSize=10, leading=14, textColor=GREY, spaceAfter=10)
H2 = ParagraphStyle('h2', fontName='Fredoka-SemiBold', fontSize=14, leading=18, textColor=RED, spaceBefore=12, spaceAfter=5)
B = ParagraphStyle('b', fontName='DejaVu', fontSize=9.6, leading=13.5)
BUL = ParagraphStyle('bul', parent=B, leftIndent=14, firstLineIndent=-10, spaceAfter=2)
CAP = ParagraphStyle('cap', parent=B, fontSize=9.2, leading=13, backColor=colors.HexColor('#F4F6FB'), borderPadding=6, spaceBefore=4, spaceAfter=8)
T = ParagraphStyle('t', parent=B, fontSize=8.8, leading=12)
TB = ParagraphStyle('tb', parent=T, fontName='Fredoka-SemiBold')

def bl(items): return [Paragraph('• ' + i, BUL) for i in items]
def tbl(rows, widths):
    data = [[Paragraph(c, TB if r == 0 else T) for c in row] for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8ECF7')),
                           ('LINEBELOW', (0, 0), (-1, -1), 0.4, colors.HexColor('#CCCCCC')), ('TOPPADDING', (0, 0), (-1, -1), 4),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]))
    return t

S = []
S += [Paragraph("Pip's Christmas Countdown: $0 Launch Campaign", H1),
      Paragraph('Goal: maximum free reach, Nov 3 to Dec 18, 2026, the window for gifts to arrive by Christmas. Every channel below costs nothing.', SUB)]

S.append(Paragraph('The big idea: give away Day 1, sell the other 49', H2))
S.append(Paragraph('Parents share free printables far more than ads. Every post points to one free 4-page pack '
                   '(countdown tracker + Day 1 and Day 2 pages). Each printed page ends with "the full book is on Amazon", so the free pack '
                   'keeps selling inside homes and classrooms. The hook for every post: <b>"Can you find Little Star?"</b>, '
                   'which turns posts into a comment game, and comments are what the Instagram and Facebook algorithms reward.', B))

S.append(Paragraph('Channels, ranked by free reach for this book', H2))
S.append(tbl([
    ['#', 'Channel', 'Why it works', 'What to post'],
    ['1', 'Pinterest', 'Parents plan Christmas activities on Pinterest. Pins keep getting found for months, not hours. Biggest free channel for printables.', '5 to 10 pins a week from the coloring pages, each linking to the free pack or the Amazon page.'],
    ['2', 'YouTube Shorts / TikTok / Reels', 'Short videos of a page being colored, with the rhyme read aloud, get pushed to strangers for free. You already have the BlobbyWorld video pipeline.', 'One 20-40 second "color with Pip" video per countdown day.'],
    ['3', 'Instagram (feed + Stories)', 'Builds the brand; Stories polls and "find the star" questions get replies.', '3 feed posts a week + daily Story in December.'],
    ['4', 'Facebook parent and homeschool groups', 'Huge, active audiences who ask for "Christmas activities for kids". Only post the FREE pack, and only where group rules allow.', 'The free pack, with a short friendly note. Never a sales link alone.'],
    ['5', 'Teachers / preschools', 'One preschool teacher printing Day 1 for a class puts the book in front of 20 families.', 'Email the free pack to local preschools, libraries and daycares in Wesley Chapel.'],
    ['6', 'Amazon itself (free)', 'Author Central page links all 3 Blobby World books; A+ Content (free) adds big images to the listing.', 'Set up Author Central bio + A+ Content once the book is live.'],
], [0.3 * inch, 1.25 * inch, 2.65 * inch, 2.55 * inch]))

S.append(Paragraph('Launch schedule', H2))
S.append(tbl([
    ['When', 'Action'],
    ['Nov 3-4 (book goes live)', 'Launch post (graphic 1). Pin graphic 5. Set up Amazon Author Central + A+ Content. Put the free pack link in the Instagram bio.'],
    ['Nov 5-14', 'Posts: "Find Little Star" (graphic 2), Free page (graphic 3), What\'s inside (graphic 4). 1 pin a day. Share free pack in 3-5 Facebook groups that allow freebies.'],
    ['Nov 15-30 (peak gift shopping)', '"Christmas Eve box" and "stocking stuffer" angle posts. Email preschools/libraries. Black Friday (Nov 27) and Cyber Monday (Nov 30) "perfect stocking stuffer" posts.'],
    ['Dec 1-24', 'Daily "Day X with Pip" Story or Short: color that day\'s page, read the rhyme, ask kids to find Little Star. This is the countdown, live.'],
    ['Dec 10-18', 'Last-chance posts: "Order by Dec 18 for Christmas delivery." After Dec 18, push the free pack only.'],
], [1.7 * inch, 5.05 * inch]))

S.append(Paragraph('Ready-to-post captions', H2))
caps = [
    ('Post 1: Launch (ig_1_launch.png)',
     "NEW for Christmas!  Meet Pip, a little penguin with a big countdown. A tiny star lands on his nose and plays hide-and-seek every night until Christmas. "
     "Read one rhyme, color one page, find Little Star. 25 nights + 25 bonus adventures for ages 3-6. Search \"Pip's Christmas Countdown\" on Amazon. "
     "Free Day 1 printable: link in bio."),
    ('Post 2: Find Little Star (ig_2_find_little_star.png)',
     "Pip got SPLATTED in a snowball fight  ...but Little Star is hiding somewhere on this page. Can your little one find her? "
     "Comment where she's hiding! (Every page of Pip's Christmas Countdown has a hidden star.)"),
    ('Post 3: Free page (ig_3_free_page.png)',
     "FREE coloring page! Day 1 of Pip's Christmas Countdown: \"A little star tumbled right onto Pip's nose...\" "
     "Grab the free printable pack (countdown tracker + 2 pages) from the link in bio. Print it tonight and start the countdown together."),
    ('Post 4: What\'s inside (ig_4_whats_inside.png)',
     "What's inside Pip's Christmas Countdown: a short rhyme every night, a countdown tracker to color, a Letter to Santa page, "
     "and a Coloring Champion certificate at the end. One picture per sheet, so markers don't bleed. The perfect Christmas Eve box filler!"),
    ('Pinterest pin (pin_1_coloring_pages.png): title + description',
     "Title: Free Christmas Coloring Pages for Kids Ages 3-6 (Printable). "
     "Description: Cute penguin Christmas coloring pages for toddlers and preschoolers. Free printable countdown tracker + 2 story pages "
     "from Pip's Christmas Countdown, a 25-night advent story coloring book. Easy, bold designs and a find-the-star game on every page."),
]
for t, c in caps:
    S.append(KeepTogether([Paragraph('<b>' + t + '</b>', B), Paragraph(c, CAP)]))
S.append(Paragraph('<b>Hashtags (paste under each Instagram post):</b>', B))
S.append(Paragraph('#christmascoloringpages #coloringbookforkids #toddleractivities #preschoolactivities #advent #adventcalendar '
                   '#christmascountdown #christmasactivitiesforkids #christmaseveboxideas #stockingstuffers #freeprintables #momlife '
                   '#homeschoolmom #kidsbooks #penguin #colouringpages #kidsactivities #christmas2026', CAP))

S.append(Paragraph('Short-video script (20-40 seconds, one per countdown day)', H2))
S += bl(['0-3s: close-up of the page with the hook text on screen: "Day 7. Can you find Little Star?"',
         '3-20s: time-lapse of the page being colored (crayon or a coloring app), with the day\'s rhyme read aloud.',
         '20-30s: zoom onto Little Star\'s hiding spot. "Found her!" Then the cover for 2 seconds with "Pip\'s Christmas Countdown on Amazon".',
         'Your BlobbyWorld pipeline (storyboard, narration, MP4 assembly) can render all 25 of these automatically from the page art and captions.'])

S.append(Paragraph('Rules that protect the book', H2))
S += bl(['Never offer anything (free copies, gift cards, refunds) in exchange for an Amazon review. Amazon removes those reviews and can penalize the account. '
         'Just ask real buyers: "If Pip made your countdown cozier, a quick review helps other parents find him."',
         'In Facebook groups, follow each group\'s self-promotion rules; share the free pack, not just a sales link.',
         'Use only the book\'s own art. No trending songs with copyrighted lyrics in videos; use the platform\'s free music library.'])

S.append(Paragraph('If you later want paid help', H2))
S.append(Paragraph('The single best paid add-on is an Amazon Sponsored Products ad capped at $5 a day, keyword-targeted to '
                   '"christmas coloring book for toddlers", "advent activity book for kids" and "penguin coloring book". It is optional; nothing above depends on it.', B))

SimpleDocTemplate(f'{D}/output/marketing/Pip_Free_Launch_Campaign.pdf', pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                  topMargin=0.75 * inch, bottomMargin=0.75 * inch, title="Pip's Christmas Countdown: $0 Launch Campaign").build(S)
