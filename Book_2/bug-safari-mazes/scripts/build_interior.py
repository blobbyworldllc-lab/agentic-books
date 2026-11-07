"""Bug Safari Mazes interior. Every maze generated, solved and de-duplicated by code."""
import random, hashlib, sys, json, os
from collections import deque
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("B","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("R","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
OUT=os.path.join(os.path.dirname(__file__),"..","output","kdp")
W,H=8.5*inch,11*inch
BUGS=[("Ladybug","a juicy green leaf"),("Bee","the honey hive"),("Butterfly","the pink flower"),("Ant","the picnic crumbs"),
("Beetle","a cozy log home"),("Dragonfly","the pond lily pad"),("Caterpillar","a tasty apple"),("Grasshopper","the tall grass hill"),
("Snail","the dewy cabbage"),("Firefly","the evening lantern tree"),("Cricket","the moonlit rock"),("Spider","her silky web"),
("Worm","the soft garden soil"),("Moth","the glowing porch light"),("Ladybug Family","the sunflower"),("Bumblebee","the clover patch")]
def gen(n,m,rng):
    # grid n cols x m rows; walls[(x,y)] = set of open neighbours
    open_={(x,y):set() for x in range(n) for y in range(m)}
    st=[(0,0)];seen={(0,0)}
    while st:
        x,y=st[-1];nb=[(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if 0<=x+dx<n and 0<=y+dy<m and (x+dx,y+dy) not in seen]
        if nb:
            c=rng.choice(nb);open_[(x,y)].add(c);open_[c].add((x,y));seen.add(c);st.append(c)
        else: st.pop()
    return open_
def solve(op,s,e):
    q=deque([s]);p={s:None}
    while q:
        c=q.popleft()
        if c==e:break
        for nb in op[c]:
            if nb not in p:p[nb]=c;q.append(nb)
    if e not in p:return None
    path=[];c=e
    while c:path.append(c);c=p[c]
    return path[::-1]
def draw(c,op,n,m,x0,y0,cs,path=None,lw=2.2):
    c.setLineWidth(lw);c.setLineCap(1)
    for (x,y),nbs in op.items():
        px,py=x0+x*cs,y0+(m-1-y)*cs
        if y==0 and (x,y)!=(0,0): c.line(px,py+cs,px+cs,py+cs)
        if y==m-1 and (x,y)!=(n-1,m-1): c.line(px,py,px+cs,py)
        if x==0: c.line(px,py,px,py+cs)
        if x==n-1: c.line(px+cs,py,px+cs,py+cs)
        if (x+1,y) in op and (x+1,y) not in nbs: c.line(px+cs,py,px+cs,py+cs)
        if (x,y+1) in op and (x,y+1) not in nbs: c.line(px,py,px+cs,py)
    if path:
        c.setStrokeColorRGB(.45,.45,.45);c.setLineWidth(3)
        pts=[(x0+(x+.5)*cs,y0+(m-1-y+.5)*cs) for x,y in path]
        for a,b in zip(pts,pts[1:]):c.line(*a,*b)
        c.setStrokeColorRGB(0,0,0)
def main(count=80,seed=20261107):
    rng=random.Random(seed);mazes=[];hashes=set()
    for i in range(count):
        t=i/count;n=int(6+t*8);m=int(8+t*10)   # 6x8 up to 14x18
        while True:
            op=gen(n,m,rng);h=hashlib.md5(repr(sorted((k,sorted(v)) for k,v in op.items())).encode()).hexdigest()
            if h in hashes: continue
            path=solve(op,(0,0),(n-1,m-1))
            assert path and len(path)>=n+m-1
            hashes.add(h);break
        b=BUGS[i%len(BUGS)];mazes.append((n,m,op,path,b))
    assert len(hashes)==count
    c=canvas.Canvas(os.path.join(OUT,"Bug_Safari_Mazes_Interior.pdf"),pagesize=(W,H),initialFontName="R")
    c.setTitle("Bug Safari Mazes");c.setAuthor("Blobby World Official")
    def center(t,y,f="B",s=24):c.setFont(f,s);c.drawCentredString(W/2,y,t)
    center("BUG SAFARI MAZES",H-3*inch,s=40);center("80 Backyard Bug Mazes for Kids Ages 5-8",H-3.7*inch,"R",20)
    center("Easy to Tricky, with Answer Key",H-4.2*inch,"R",16);center("Blobby World Official",1.5*inch,"R",16);c.showPage()
    c.setFont("R",11)
    for i,t in enumerate(["Copyright 2026 Bizatree LLC. All rights reserved.","Published under the pen name Blobby World Official.",
      "Text created with Claude (Anthropic). All mazes generated and verified by computer code.","Tampa, Florida, USA."]):
        c.drawCentredString(W/2,H-2*inch-i*20,t)
    c.showPage()
    center("How to Play",H-2*inch,s=30);c.setFont("R",16)
    for i,t in enumerate(["1. Find the bug at START (top left corner).","2. Draw a path to the FINISH (bottom right corner).",
      "3. Use a pencil so you can try again!","4. Mazes get a little bigger as you go.","5. Stuck? Answers are at the back."]):
        c.drawString(1.2*inch,H-3.2*inch-i*40,t)
    c.showPage()
    for k,(n,m,op,path,b) in enumerate(mazes,1):
        center(f"Maze {k}",H-0.9*inch,s=22);center(f"Help {b[0]} get to {b[1]}!",H-1.3*inch,"R",14)
        cs=min(6.8*inch/n,8.3*inch/m);x0=(W-n*cs)/2;y0=0.9*inch+(8.3*inch-m*cs)/2
        draw(c,op,n,m,x0,y0,cs)
        c.setFont("B",11);c.drawString(x0,y0+m*cs+4,"START");c.drawRightString(x0+n*cs,y0-14,"FINISH")
        c.showPage()
    per=8
    for pg in range(0,count,per):
        center("Answer Key",H-0.8*inch,s=22)
        for j,k in enumerate(range(pg,min(pg+per,count))):
            n,m,op,path,b=mazes[k];col,row=j%2,j//2
            cw=3.6*inch;ch=2.2*inch;cs=min((cw-10)/n,(ch-24)/m)
            x0=0.6*inch+col*(cw+0.3*inch)+(cw-n*cs)/2;y0=H-1.4*inch-(row+1)*(ch+0.15*inch)+ (ch-m*cs)/2
            c.setFont("B",9);c.drawString(0.6*inch+col*(cw+0.3*inch),y0+m*cs+3,f"Maze {k+1}")
            draw(c,op,n,m,x0,y0,cs,path,lw=1.0)
        c.showPage()
    center("Great Job, Explorer!",H/2+1*inch,s=32);center("You finished all 80 mazes.",H/2,"R",18);c.showPage()
    pages=c.getPageNumber()-1
    while pages%2: c.showPage();pages+=1
    c.save();json.dump({"pages":pages,"mazes":count,"unique":len(hashes)},open(os.path.join(OUT,"verify.json"),"w"))
    print(pages,len(hashes))
main()
