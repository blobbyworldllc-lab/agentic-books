import os,random
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("B","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("R","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
PAGES=int(os.environ.get("PAGES",94));spine=PAGES*0.002252*inch;bl=.125*inch;tw,th=8.5*inch,11*inch
W=2*tw+spine+2*bl;H=th+2*bl
c=canvas.Canvas(os.path.join(os.path.dirname(__file__),"..","output","kdp","Bug_Safari_Mazes_Cover.pdf"),pagesize=(W,H),initialFontName="R")
c.setFillColorRGB(.78,.93,.62);c.rect(0,0,W,H,fill=1,stroke=0)
fx=bl+tw+spine  # front cover left edge
rng=random.Random(3);c.setStrokeColorRGB(.2,.5,.2);c.setLineWidth(6)
for i in range(14):  # decorative maze-like lines
    x=fx+.5*inch+rng.random()*(tw-1*inch);y=.5*inch+rng.random()*1.6*inch
    c.line(x,y,x+rng.choice([-1,1])*.6*inch,y);c.line(x,y,x,y+.6*inch)
c.setFillColorRGB(.1,.3,.1)
def ct(t,y,f,s):c.setFont(f,s);c.drawCentredString(fx+tw/2,y,t)
ct("BUG SAFARI",H-2.4*inch,"B",64);ct("MAZES",H-3.4*inch,"B",64)
c.setFillColorRGB(.15,.15,.15);ct("80 Backyard Bug Mazes",H-4.4*inch,"R",24);ct("for Kids Ages 5-8",H-4.9*inch,"R",24)
c.setFillColorRGB(.95,.9,.3);c.roundRect(fx+1.4*inch,H-6.6*inch,tw-2.8*inch,.9*inch,12,fill=1,stroke=0)
c.setFillColorRGB(.1,.1,.1);ct("Easy to Tricky  |  Answer Key Included",H-6.25*inch,"B",16)
ct("Blobby World Official",3.2*inch,"B",22)
if spine>=.35*inch:
    c.saveState();c.translate(bl+tw+spine/2,H/2);c.rotate(-90);c.setFont("B",16);c.drawCentredString(0,-5,"BUG SAFARI MAZES  -  Blobby World Official");c.restoreState()
c.setFont("R",13);c.setFillColorRGB(.1,.1,.1)
bx=bl+.8*inch
for i,t in enumerate(["Help Ladybug, Bee, Butterfly and friends","find their way home!","","80 mazes that start small and grow","a little bigger on every page.","","Pencil-friendly pages, big clear paths,","and an answer key at the back."]):
    c.drawString(bx,H-2.5*inch-i*.32*inch,t)
c.save();print(spine/inch,W/inch,H/inch)
