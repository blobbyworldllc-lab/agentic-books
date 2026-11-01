import os,re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for n in ('SemiBold','Bold'): pdfmetrics.registerFont(TTFont(f'F-{n}',f'{D}/fonts/Fredoka-{n}.ttf'))
pdfmetrics.registerFont(TTFont('DV',f'{D}/fonts/DejaVuSans.ttf'))
NAVY,RED=colors.HexColor('#14285C'),colors.HexColor('#B3261E')
H1=ParagraphStyle('1',fontName='F-Bold',fontSize=20,leading=24,textColor=NAVY,spaceAfter=6)
H2=ParagraphStyle('2',fontName='F-SemiBold',fontSize=14,leading=18,textColor=RED,spaceBefore=12,spaceAfter=4)
H3=ParagraphStyle('3',fontName='F-SemiBold',fontSize=11,leading=14,textColor=NAVY,spaceBefore=6,spaceAfter=2)
B=ParagraphStyle('b',fontName='DV',fontSize=9.2,leading=13)
BUL=ParagraphStyle('u',parent=B,leftIndent=14,firstLineIndent=-10,spaceAfter=2)
def fmt(t):
    t=t.replace('&','&amp;').replace('<','&lt;')
    return re.sub(r'`([^`]+)`',r'\1',t)
S=[]
for l in open(f'{D}/docs/WEEKLY_PLAYBOOK.md').read().splitlines():
    if not l.strip(): continue
    if l.startswith('# '): S.append(Paragraph(fmt(l[2:]),H1))
    elif l.startswith('## '): S.append(Paragraph(fmt(l[3:]),H2))
    elif l.startswith('### '): S.append(Paragraph(fmt(l[4:]),H3))
    elif l.startswith('- '): S.append(Paragraph('• '+fmt(l[2:]),BUL))
    elif re.match(r'\d+\. ',l): S.append(Paragraph(fmt(l),BUL))
    else: S.append(Paragraph(fmt(l),B))
os.makedirs(f'{D}/output/marketing',exist_ok=True)
SimpleDocTemplate(f'{D}/output/Blobby_World_Catalog_Strategy_and_Weekly_Plan.pdf',pagesize=letter,leftMargin=.85*inch,rightMargin=.85*inch,topMargin=.75*inch,bottomMargin=.75*inch,title='Catalog Strategy and Weekly Plan').build(S)
