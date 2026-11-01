import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from captions import *
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from xml.sax.saxutils import escape
H=ParagraphStyle('h',fontName='Helvetica-Bold',fontSize=20,leading=24,spaceAfter=4)
S=ParagraphStyle('s',fontName='Helvetica',fontSize=10.5,leading=14,textColor=colors.HexColor('#555555'),spaceAfter=12)
H2=ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=14,leading=18,spaceBefore=10,spaceAfter=6,textColor=colors.HexColor('#B3261E'))
B=ParagraphStyle('b',fontName='Helvetica',fontSize=10.5,leading=14.5)
C=ParagraphStyle('c',fontName='Helvetica',fontSize=11,leading=15)
N=ParagraphStyle('n',fontName='Helvetica-Bold',fontSize=11,leading=15,textColor=colors.HexColor('#1E5631'))
def cap(t): return Paragraph(escape(t).replace(' / ','<br/>'),C)
def table(rows,label):
    data=[[Paragraph(f"{label} {n}",N),cap(t)] for n,t in rows]
    tb=Table(data,colWidths=[0.95*inch,5.55*inch])
    tb.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),0.4,colors.HexColor('#DDDDDD')),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),6),('LEFTPADDING',(0,0),(-1,-1),0)]))
    return tb
st=[Paragraph(TITLE,H),Paragraph(escape(SUBTITLE),S)]
st.append(Paragraph("The story",H2))
st.append(Paragraph("A tiny star falls onto Pip's nose and plays hide-and-seek with him every night until Christmas. Kids hunt for Little Star on every page; on Christmas morning she appears on top of Pip's tree. In the bonus pages the friends keep playing through winter, until Little Star flies home and promises to come back next Christmas (sequel hook). Each caption is read aloud by a parent; every page ends with: <b>Can you find Little Star?</b>",B))
st.append(Paragraph("Characters (all original)",H2))
st.append(Paragraph("<br/>".join(f"<b>{n}</b>: {escape(d)}" for n,d in CAST),B))
st.append(Paragraph("Front and back pages",H2))
st.append(Paragraph("<b>This book belongs to</b> page &nbsp;|&nbsp; <b>My Countdown Tracker</b>: 25 stars, color one each night &nbsp;|&nbsp; <b>Letter to Santa</b> page &nbsp;|&nbsp; <b>Christmas Coloring Champion</b> certificate (last page)",B))
st.append(PageBreak())
st.append(Paragraph("Part 1: 25 Nights to Christmas",H2)); st.append(table(COUNTDOWN,"Day"))
st.append(PageBreak())
st.append(Paragraph("Part 2: Winter Adventures with Pip & Little Star",H2)); st.append(table(BONUS,"Page"))
st.append(Paragraph("Gemini prompt changes to match the story",H2))
st.append(Paragraph("<b>Setup message</b>: replace the hidden-star rule with: <i>Hide Little Star, a small five-point star with a tiny smiling face, somewhere on every page (medium size, easy for a child to find).</i><br/>"
 "<b>Page 1</b>: Pip looks cross-eyed and smiling at Little Star, a small smiling star sitting on the tip of his beak, snowflakes falling<br/>"
 "<b>Page 7</b>: Pip on tiptoes looking up at a decorated Christmas tree with an empty top, a puzzled smile<br/>"
 "<b>Page 25</b>: Pip and all his friends opening presents by the tree, Little Star big and smiling on top of the tree (not hidden on this page)<br/>"
 "<b>Page 50</b>: Pip waving goodbye from in front of a cozy snowy house as Little Star flies up into the night sky",B))
SimpleDocTemplate(f'{ROOT}/docs/Pips_Christmas_Countdown_Story.pdf',pagesize=letter,leftMargin=0.9*inch,rightMargin=0.9*inch,topMargin=0.8*inch,bottomMargin=0.8*inch,title=TITLE).build(st)
