"""
scene.py  ── All man-made village structures and ground details:
              houses, connecting wall, fence, bushes, lamp posts,
              flowers, and grass tufts.

Team owner: responsible for buildings, props, and decorative details.
"""

import math
import config as C
from renderer import rect, circ, poly, ellipse


# ══════════════════════════════════════════════════════
#  HOUSES
# ══════════════════════════════════════════════════════
def _draw_one_house(t, x, y, w, h2, rh, chimney=False, flip=False):
    wall="#F5F5F5"; wsh="#E0E0E0"; wdk="#BDBDBD"
    roof="#E64A19"; rhi="#FF7043"; rsh="#BF360C"
    door_c="#212121"; win_c="#90CAF9"; win_hi="#E3F2FD"; win_fr="#37474F"

    poly(t,[(x-4,y-7),(x+w+4,y-7),(x+w+4,y),(x-4,y)],"#9E9E9E")
    rect(t,x,y,w,h2,wall,"#9E9E9E",1)
    rect(t,x+w-18,y,18,h2,wsh); rect(t,x+w-6,y,6,h2,wdk)
    t.pencolor(wsh); t.pensize(1)
    for sy in range(y+12,y+h2,15):
        t.penup(); t.goto(x,sy); t.pendown(); t.goto(x+w,sy); t.penup()

    rp=[(x-12,y+h2),(x+w+12,y+h2),(x+w//2,y+h2+rh)]
    poly(t,rp,roof,"#7B2D00",1)
    poly(t,[(x-12,y+h2),(x+w//2,y+h2+rh),(x+w//2-8,y+h2+rh-5),(x-8,y+h2)],rhi)
    poly(t,[(x+w+12,y+h2),(x+w//2,y+h2+rh),(x+w//2+5,y+h2+rh-5),(x+w+8,y+h2)],rsh)
    t.pencolor("#7B2D00"); t.pensize(2)
    t.penup(); t.goto(x-12,y+h2); t.pendown(); t.goto(x+w+12,y+h2); t.penup()

    if chimney:
        chx=x+w-40
        rect(t,chx,y+h2+rh//4,20,rh//2+12,"#795548","#4E342E",1)
        rect(t,chx-4,y+h2+rh//4+rh//2+8,28,7,"#4E342E")
        if not C.NIGHT:
            for sox,soy,sr2 in [(2,8,5),(-1,18,7),(3,28,6)]:
                circ(t,chx+sox+10,y+h2+rh+soy,sr2,"#EEEEEE")

    dw=28; dh3=int(h2*0.52); dx2=x+w//2-dw//2
    rect(t,dx2,y,dw,dh3,door_c,"#000",1)
    circ(t,dx2+(dw-6 if flip else 6),y+dh3//3,3,"#FFD700")
    t.pencolor("#424242"); t.pensize(2)
    t.penup(); t.goto(dx2-2,y); t.pendown()
    t.goto(dx2-2,y+dh3+2); t.goto(dx2+dw+2,y+dh3+2)
    t.goto(dx2+dw+2,y); t.penup()

    ww2=36; wh3=30; wy2=y+dh3+12
    for wx2 in [x+10, x+w-10-ww2]:
        rect(t,wx2-3,wy2-3,ww2+6,wh3+6,win_fr)
        rect(t,wx2,wy2,ww2,wh3,win_c)
        rect(t,wx2+2,wy2+wh3-9,ww2-4,7,win_hi)
        t.pencolor(win_fr); t.pensize(1)
        t.penup(); t.goto(wx2+ww2//2,wy2); t.pendown()
        t.goto(wx2+ww2//2,wy2+wh3); t.penup()
        t.goto(wx2,wy2+wh3//2); t.pendown()
        t.goto(wx2+ww2,wy2+wh3//2); t.penup()
        rect(t,wx2-4,wy2-5,ww2+8,5,wdk)


def draw_houses(house_t):
    _draw_one_house(house_t,-218,-178,138,90,60,chimney=False,flip=False)
    _draw_one_house(house_t,  28,-178,188,90,65,chimney=True, flip=True)
    # Connecting low wall between the two houses
    rect(house_t,-80,-178,112,28,"#E0E0E0","#BDBDBD",1)
    rect(house_t,-80,-178,112,7,"#EEEEEE")


# ══════════════════════════════════════════════════════
#  FENCE
# ══════════════════════════════════════════════════════
def draw_fence(house_t):
    fc="#8D6E63"; fd="#5D4037"; fh="#A1887F"
    for ry in [-112,-144]:
        rect(house_t,238,ry,215,10,fc,fd,1)
        rect(house_t,240,ry+7,211,3,fh)
    for px in range(240,458,28):
        rect(house_t,px-5,-165,11,68,fd,"#4E342E",1)
        poly(house_t,[(px-5,-97),(px+6,-97),(px+1,-83)],fd)
        rect(house_t,px-3,-160,5,60,fc)


# ══════════════════════════════════════════════════════
#  BUSHES
# ══════════════════════════════════════════════════════
def draw_bushes(house_t):
    bs=[
        ( 28,-158,1.10,"#2E7D32","#388E3C"),
        (198,-160,0.90,"#1B5E20","#2E7D32"),
        (358,-157,0.85,"#2E7D32","#4CAF50"),
        (-44,-160,0.82,"#1B5E20","#2E7D32"),
        (428,-153,0.72,"#2E7D32","#43A047"),
    ]
    for cx,cy,s,c1,c2 in bs:
        for dx,dy,r in [(0,0,int(28*s)),(-int(18*s),-int(5*s),int(22*s)),
                         (int(18*s),-int(5*s),int(20*s)),(0,int(12*s),int(18*s))]:
            circ(house_t,cx+dx,cy+dy,r,c1)
        for dx,dy,r in [(0,5,int(18*s)),(-int(8*s),3,int(14*s)),(int(8*s),3,int(13*s))]:
            circ(house_t,cx+dx,cy+dy,r,c2)


# ══════════════════════════════════════════════════════
#  LAMP POSTS
# ══════════════════════════════════════════════════════
def draw_lamps(detail_t):
    for lx,ly in [(-460,-200),(420,-200)]:
        rect(detail_t,lx-4,ly,8,90,"#424242")
        rect(detail_t,lx-20,ly+88,40,6,"#424242")
        circ(detail_t,lx,ly+94,10,"#9E9E9E")
        gc2="#FFEE58" if not C.NIGHT else "#FFFF00"
        circ(detail_t,lx,ly+94,7,gc2)
        if C.NIGHT:
            for gr,ga in [(22,"#FFF9C4"),(35,"#FFFDE7"),(50,"#FFFFF8")]:
                ellipse(detail_t,lx,ly+94,gr,gr//2,ga)


# ══════════════════════════════════════════════════════
#  FLOWERS & GRASS TUFTS
# ══════════════════════════════════════════════════════
def draw_flowers(detail_t):
    sc="#2E7D32" if not C.NIGHT else "#1A3A1C"
    for flx,fly,flc in C.FLOWERS:
        detail_t.pencolor(sc); detail_t.pensize(2)
        detail_t.penup(); detail_t.goto(flx,fly)
        detail_t.pendown(); detail_t.goto(flx,fly+17); detail_t.penup()
        cx,cy=flx,fly+17
        for ang in range(0,360,60):
            rad=math.radians(ang)
            circ(detail_t,cx+8*math.cos(rad),cy+8*math.sin(rad),5,flc)
        circ(detail_t,cx,cy,4,"#FFD600")


def draw_tufts(detail_t):
    tc2="#2E7D32" if not C.NIGHT else "#1A3A1C"
    for gx,gy in C.TUFTS:
        detail_t.pencolor(tc2); detail_t.pensize(2)
        for i in range(6):
            ang=62+i*11; ln=9+(i%3)*5
            detail_t.penup(); detail_t.goto(gx+i*4-10,gy)
            detail_t.setheading(ang); detail_t.pendown()
            detail_t.forward(ln); detail_t.penup()


def draw_details(detail_t):
    """Draw all fine details: flowers, tufts, lamps."""
    detail_t.clear()
    draw_flowers(detail_t)
    draw_tufts(detail_t)
    draw_lamps(detail_t)
