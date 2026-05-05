"""
environment.py  ── Everything that forms the natural world:
                    sky, sun/moon/stars/clouds, river & boats,
                    ground layers, background forest, and all trees.

Team owner: responsible for the outdoor/natural environment drawing
and all related animation state (clouds, water ripples, boats).
"""

import math
import random
import config as C
from renderer import rect, circ, poly, ellipse, bezier_line

# ══════════════════════════════════════════════════════
#  ANIMATION STATE
# ══════════════════════════════════════════════════════
sun_ray_angle = 0
star_frame    = 0
water_offset  = 0.0

CLOUDS = [
    {"x": -500, "y": 270, "s": 1.15, "spd": 0.4},
    {"x":  -80, "y": 300, "s": 0.80, "spd": 0.25},
    {"x":  240, "y": 280, "s": 1.00, "spd": 0.30},
    {"x":  480, "y": 295, "s": 0.65, "spd": 0.45},
    {"x": -260, "y": 315, "s": 0.55, "spd": 0.20},
]

BOATS = [
    {"x": -250, "y": 10,  "spd":  0.6, "col": "#8D6E63", "sail": "#EF9A9A", "flip": False},
    {"x":  180, "y": 42,  "spd": -0.4, "col": "#6D4C41", "sail": "#90CAF9", "flip": True},
]


# ══════════════════════════════════════════════════════
#  SKY
# ══════════════════════════════════════════════════════
def draw_sky(sky_t):
    sky_t.clear()
    cols = C.NIGHT_SKY if C.NIGHT else C.DAY_SKY
    bh = (C.H * 2) / len(cols)
    for i, col in enumerate(cols):
        rect(sky_t, -C.W, -C.H + i * bh, C.W * 2, bh + 2, col)


def draw_stars(star_t):
    star_t.clear()
    if not C.NIGHT:
        return
    for sx, sy, sr in C.STARS:
        tw = sr if (star_frame // 8 + hash((sx, sy))) % 5 != 0 else max(1, sr - 1)
        circ(star_t, sx, sy, tw, "white")


def draw_sun_moon(sun_t):
    sun_t.clear()
    if C.NIGHT:
        for gr, gc2 in [(75,"#0D1C4A"),(60,"#F0E68C"),(45,"#FFFDE7")]:
            circ(sun_t, -380, 275, gr, gc2)
        circ(sun_t, -358, 288, 42, C.NIGHT_SKY[2])
    else:
        for gr, gc2 in [(90,"#FFF9C4"),(74,"#FFF176"),(58,"#FFEE58"),(44,"#FFD600")]:
            circ(sun_t, 430, 295, gr, gc2)
        sun_t.pencolor("#FFD600"); sun_t.pensize(3)
        for ang in range(0, 360, 24):
            rad = math.radians(ang + sun_ray_angle)
            sun_t.penup()
            sun_t.goto(430 + 50*math.cos(rad), 295 + 50*math.sin(rad))
            sun_t.pendown()
            sun_t.goto(430 + 78*math.cos(rad), 295 + 78*math.sin(rad))
            sun_t.penup()
        circ(sun_t, 430, 295, 40, "#FFFF00")
        circ(sun_t, 430, 295, 30, "#FFFFFF")


def _draw_one_cloud(t, cx, cy, s):
    col    = "#D8E4EC" if C.NIGHT else "#FFFFFF"
    shadow = "#B0BEC5" if C.NIGHT else "#CFD8DC"
    parts  = [(0,0,42),(-52,-6,31),(52,-6,29),(-24,20,26),(24,20,24),(0,26,23)]
    for dx, dy, r in parts:
        circ(t, cx+dx*s+4, cy+dy*s-5, int(r*s), shadow)
    for dx, dy, r in parts:
        circ(t, cx+dx*s, cy+dy*s, int(r*s), col)


def draw_clouds(cloud_t):
    cloud_t.clear()
    for c in CLOUDS:
        _draw_one_cloud(cloud_t, c["x"], c["y"], c["s"])


def update_clouds():
    for c in CLOUDS:
        c["x"] += c["spd"]
        if c["x"] > C.W + 160:
            c["x"] = -C.W - 160


# ══════════════════════════════════════════════════════
#  RIVER & BOATS
# ══════════════════════════════════════════════════════
def draw_river(water_t):
    water_t.clear()
    cols = C.NIGHT_WATER if C.NIGHT else C.DAY_WATER
    bh = (C.RIVER_TOP - C.RIVER_BOT) / len(cols)
    for i, col in enumerate(cols):
        rect(water_t, -C.W, C.RIVER_BOT + i*bh, C.W*2, bh+2, col)

    shimmer = "#90CAF9" if not C.NIGHT else "#0D2040"
    bright  = "#E3F2FD" if not C.NIGHT else "#0F2850"
    for row in range(8):
        wy_base = C.RIVER_BOT + 6 + row * 11
        water_t.pencolor(bright if row % 3 == 0 else shimmer)
        water_t.pensize(1)
        water_t.penup(); water_t.goto(-C.W, wy_base); water_t.pendown()
        x = -C.W
        while x <= C.W:
            wy = wy_base + 3.5 * math.sin((x + water_offset) * 0.045 + row * 0.8)
            water_t.goto(x, wy)
            x += 3
        water_t.penup()

    refl = "#BBDEFB" if not C.NIGHT else "#0A1830"
    for i in range(3):
        water_t.pencolor(refl); water_t.pensize(2)
        water_t.penup(); water_t.goto(-C.W, C.RIVER_BOT+2+i*4)
        water_t.pendown(); water_t.goto(C.W, C.RIVER_BOT+2+i*4); water_t.penup()

    pad_col = "#2E7D32"; pad_hi = "#388E3C"
    pads = [(-430,25),(-220,38),(80,22),(290,32),(510,28),(-50,45)]
    for px, py in pads:
        circ(water_t, px, py, 13, pad_col)
        circ(water_t, px+2, py+2, 9, pad_hi)
        poly(water_t, [(px,py),(px+11,py+8),(px+13,py)], pad_col)
        if px < 0:
            circ(water_t, px, py+11, 5, "#FF80AB")
            circ(water_t, px, py+11, 3, "#E91E8C")


def _draw_one_boat(t, bx, by, col, sail_col, flip):
    d = -1 if flip else 1
    hull = [(bx-40*d,by),(bx+40*d,by),(bx+32*d,by-16),(bx-32*d,by-16)]
    poly(t, hull, col, "#4E342E", 1)
    poly(t, [(bx-38*d,by-2),(bx+38*d,by-2),(bx+30*d,by-8),(bx-30*d,by-8)],"#A1887F")
    rect(t, bx-16*d if d>0 else bx+2*d, by, 28, 14, "#EFEBE9","#BDBDBD",1)
    t.pencolor("#5D4037"); t.pensize(3)
    t.penup(); t.goto(bx+4*d,by); t.pendown(); t.goto(bx+4*d,by+52); t.penup()
    poly(t, [(bx+4*d,by+52),(bx+4*d,by+10),(bx+36*d,by+30)], sail_col,"#BDBDBD",1)
    poly(t, [(bx+4*d,by+52),(bx+4*d,by+30),(bx+20*d,by+40)],
         "#FFCDD2" if sail_col=="#EF9A9A" else "#BBDEFB")
    t.pencolor("#90CAF9" if not C.NIGHT else "#152840"); t.pensize(1)
    for ri in range(1,4):
        t.penup(); t.goto(bx-42*d-ri*8*d, by-8)
        t.pendown(); t.goto(bx-42*d-ri*8*d-12*d, by-12); t.penup()
    hull_r = [(bx-40*d,by-16),(bx+40*d,by-16),(bx+28*d,by-30),(bx-28*d,by-30)]
    poly(t, hull_r, "#1565C0" if not C.NIGHT else "#050F20")


def draw_boats(boat_t):
    boat_t.clear()
    for b in BOATS:
        _draw_one_boat(boat_t, b["x"], b["y"], b["col"], b["sail"], b["flip"])


def update_boats():
    for b in BOATS:
        b["x"] += b["spd"]
        if b["x"] >  C.W + 80: b["x"] = -C.W - 80
        if b["x"] < -C.W - 80: b["x"] =  C.W + 80


# ══════════════════════════════════════════════════════
#  LANDSCAPE: far foliage, forest strip, grass, path
# ══════════════════════════════════════════════════════
def draw_far_foliage(far_t):
    """Bumpy green silhouette on the far bank of the river."""
    far_t.clear()
    c1 = C.gc("far"); c2 = C.gc("mid")
    rect(far_t, -C.W, C.RIVER_TOP, C.W*2, 30, c1)
    random.seed(7)
    for x in range(-C.W, C.W+1, 14):
        h2 = int(16 + 13*math.sin(x*0.06) + 6*math.cos(x*0.17) + random.randint(-3,3))
        circ(far_t, x, C.RIVER_TOP+10+h2//4, max(5,int(h2*0.7)), c1)
    random.seed(13)
    for x in range(-C.W, C.W+1, 11):
        h2 = int(11 + 8*math.sin(x*0.10+1) + random.randint(-2,2))
        circ(far_t, x, C.RIVER_TOP+8+h2//5, max(4,int(h2*0.6)), c2)
    rect(far_t, -C.W, C.RIVER_TOP+28, C.W*2, 5, C.gc("near"))


def draw_forest_strip(forest_t):
    """
    Dense green forest that fills the band between the river (RIVER_BOT)
    and the near ground (~y=-60).  Replaces the old sky-blue gap that was
    visible behind the houses.
    """
    forest_t.clear()
    fd = C.gc("forest")   # darkest green
    fm = C.gc("far")
    fl = C.gc("mid")

    # Solid backing strip
    rect(forest_t, -C.W, C.RIVER_BOT-5, C.W*2, 75, fd)

    # Three rows of overlapping canopy blobs — back to front
    random.seed(3)
    for row, (y_base, col, step, r_range) in enumerate([
        (C.RIVER_BOT+52, fd,   18, (22, 34)),
        (C.RIVER_BOT+36, fm,   14, (18, 28)),
        (C.RIVER_BOT+18, fl,   11, (14, 22)),
    ]):
        for x in range(-C.W, C.W+1, step):
            r  = random.randint(*r_range)
            dy = int(8*math.sin(x*0.07 + row) + random.randint(-4,4))
            circ(forest_t, x, y_base+dy, r, col)

    # Bright highlight row at the very front of the forest
    random.seed(17)
    for x in range(-C.W, C.W+1, 10):
        r  = random.randint(10, 18)
        dy = int(5*math.cos(x*0.09))
        circ(forest_t, x, C.RIVER_BOT+8+dy, r, C.gc("near"))

    # Thin grass edge where forest meets the ground
    rect(forest_t, -C.W, C.RIVER_BOT-6, C.W*2, 7, C.gc("edge"))


def draw_grass(grass_t):
    grass_t.clear()

    # Layer A: transition strip (river-bot to first hill)
    poly(grass_t, [
        (-C.W, C.RIVER_BOT), (C.W, C.RIVER_BOT),
        (C.W, -60), (300,-48),(100,-38),(-100,-52),(-300,-44),(-C.W,-58)
    ], C.gc("far"))

    # Layer B: rolling mid hill
    pts = [(-C.W, -60)]
    for x in range(-C.W, C.W+1, 18):
        y = -72 + 18*math.sin(x*0.008) + 10*math.cos(x*0.022)
        pts.append((x, y))
    pts += [(C.W,-60),(C.W,-200),(-C.W,-200)]
    poly(grass_t, pts, C.gc("mid"))

    # Layer C: near ground
    pts2 = [(-C.W,-125)]
    for x in range(-C.W, C.W+1, 18):
        y = -135 + 12*math.sin(x*0.013+0.5) + 6*math.cos(x*0.027)
        pts2.append((x, y))
    pts2 += [(C.W,-125),(C.W,-C.H),(-C.W,-C.H)]
    poly(grass_t, pts2, C.gc("near"))

    # Layer D: bright front strip
    pts3 = [(-C.W,-160)]
    for x in range(-C.W, C.W+1, 18):
        y = -170 + 7*math.sin(x*0.017+1)
        pts3.append((x, y))
    pts3 += [(C.W,-160),(C.W,-C.H),(-C.W,-C.H)]
    poly(grass_t, pts3, C.gc("front"))

    # Grass highlight edge at river bank
    rect(grass_t, -C.W, C.RIVER_BOT-5, C.W*2, 6, C.gc("edge"))

    # ── Winding sandy path ──────────────────────────────
    pc  = "#D4A96A" if not C.NIGHT else "#8A6A35"
    pe  = "#BC935A" if not C.NIGHT else "#6A4A20"
    phi = "#E8C285" if not C.NIGHT else "#A88040"

    path_pts = [
        (-58,-C.H),(58,-C.H),(82,-240),(78,-210),(62,-170),
        (44,-135),(24,-105),(6,-80),(-16,-70),
        (-42,-82),(-62,-122),(-75,-162),(-80,-205),(-70,-240)
    ]
    poly(grass_t, path_pts, pc)
    poly(grass_t, [(-58,-C.H),(-70,-240),(-80,-205),(-75,-162),
                   (-62,-122),(-42,-82),(-16,-70),(-20,-70),
                   (-46,-84),(-65,-124),(-78,-164),(-83,-208),
                   (-72,-242),(-60,-C.H)], pe)
    poly(grass_t, [(-8,-C.H),(8,-C.H),(18,-228),(12,-198),(4,-160),
                   (-4,-130),(-8,-105),(-10,-105),(-6,-130),(2,-160),
                   (10,-198),(16,-228),(6,-C.H)], phi)

    # Gravel dots on path
    random.seed(77)
    for _ in range(80):
        gx = random.randint(-32,32)
        gy = random.randint(int(-C.H+5),-82)
        if abs(gx) < 30:
            circ(grass_t, gx, gy, random.randint(1,3), pe)

    # ── Grass patch between the two houses (covers road gap) ──
    # The houses sit from x=-218 to x=216, with a connecting wall at x=-80..32
    # Paint a green strip so no sky or road colour shows through there.
    gc_mid = C.gc("mid")
    gc_near = C.gc("near")
    # Base green fill behind wall gap area
    rect(grass_t, -82, -178, 116, 20, gc_mid)
    # A few tufts to make it look natural
    for gx2, gy2 in [(-60,-168),(-30,-165),(0,-170),(30,-166),(60,-168)]:
        for i in range(5):
            ang2 = 65 + i*12
            grass_t.pencolor(gc_near); grass_t.pensize(2)
            grass_t.penup(); grass_t.goto(gx2+i*3-6, gy2)
            grass_t.setheading(ang2); grass_t.pendown()
            grass_t.forward(8+i%3*3); grass_t.penup()


# ══════════════════════════════════════════════════════
#  TREES
# ══════════════════════════════════════════════════════
def draw_branch(tree_t):
    """Overhanging tree branch from the top-left corner."""
    bc="#4E342E"; bc2="#6D4C41"; lc="#1B5E20"; lm="#2E7D32"; lh="#43A047"
    for offset in range(-8,9,2):
        pw  = max(1, 9-abs(offset))
        col = bc if abs(offset)>4 else bc2
        bezier_line(tree_t,
                    (-C.W, C.H-20+offset),(-510, C.H-55+offset),
                    (-360, C.H-105+offset),(-220, C.H-150+offset),
                    steps=50, col=col, pw=pw)
    subs = [
        [(-590,C.H-48),(-560,C.H-98),(-528,C.H-132)],
        [(-548,C.H-75),(-518,C.H-118),(-492,C.H-158)],
        [(-490,C.H-108),(-462,C.H-150)],
        [(-428,C.H-122),(-398,C.H-168),(-368,C.H-200)],
        [(-352,C.H-132),(-318,C.H-178)],
        [(-298,C.H-145),(-265,C.H-185),(-240,C.H-208)],
        [(-240,C.H-152),(-210,C.H-192)],
    ]
    for branch in subs:
        tree_t.pencolor(bc); tree_t.pensize(4)
        tree_t.penup(); tree_t.goto(branch[0]); tree_t.pendown()
        for p in branch[1:]: tree_t.goto(p)
        tree_t.penup()
    random.seed(21)
    for branch in subs:
        ep = branch[-1]
        for _ in range(22):
            lx = ep[0]+random.randint(-38,38); ly = ep[1]+random.randint(-18,32)
            sc = random.uniform(0.7,1.4)
            ellipse(tree_t, lx, ly, int(15*sc), int(9*sc), lc)
            ellipse(tree_t, lx+2, ly+3, int(9*sc), int(5*sc), lm)
        for dx,dy,r in [(0,0,24),(-15,-4,19),(15,-4,17),(0,16,16)]:
            circ(tree_t, ep[0]+dx, ep[1]+dy, r, lm)
        circ(tree_t, ep[0]+4, ep[1]+10, 12, lh)


def draw_palm(tree_t, bx, by):
    tc="#8D6E63"; td="#5D4037"; fc="#2E7D32"; fm="#388E3C"; fh="#66BB6A"
    segs=32; lean=-22; trunk=[]
    for i in range(segs+1):
        f=i/segs; trunk.append((bx+lean*f**1.6, by+f*295))
    for pw,col in [(16,td),(11,tc),(6,"#A1887F")]:
        tree_t.pencolor(col); tree_t.pensize(pw)
        tree_t.penup(); tree_t.goto(trunk[0]); tree_t.pendown()
        for p in trunk: tree_t.goto(p)
        tree_t.penup()
    tree_t.pencolor(td); tree_t.pensize(1)
    for i in range(0,segs,2):
        f=i/segs; x=bx+lean*f**1.6; y=by+f*295
        tree_t.penup(); tree_t.goto(x-7,y); tree_t.pendown()
        tree_t.goto(x+7,y+5); tree_t.penup()
    tx,ty = trunk[-1]
    frond_data=[(88,125),(62,132),(38,128),(14,118),(-12,110),
                (-36,102),(-60,90),(110,108),(128,95),(152,82),(170,70)]
    for angle,flen in frond_data:
        rad=math.radians(angle); ex=tx+flen*math.cos(rad); ey=ty+flen*math.sin(rad)
        tree_t.pencolor(fc); tree_t.pensize(5)
        tree_t.penup(); tree_t.goto(tx,ty); tree_t.pendown()
        steps=18
        for s in range(steps+1):
            f=s/steps; droop=-60*f**2
            tree_t.goto(tx+(ex-tx)*f, ty+(ey-ty)*f+droop)
        tree_t.penup()
        for s in range(1,steps,1):
            f=s/steps; droop=-60*f**2
            fx=tx+(ex-tx)*f; fy=ty+(ey-ty)*f+droop
            ll=int(20*(1-f*0.35)); perp=math.radians(angle+90-8*f)
            for side in [-1,1]:
                tree_t.pencolor(fm if side==1 else fh); tree_t.pensize(2)
                tree_t.penup(); tree_t.goto(fx,fy); tree_t.pendown()
                tree_t.goto(fx+side*ll*math.cos(perp), fy+side*ll*math.sin(perp))
                tree_t.penup()
    for ang in [68,92,115]:
        r2=math.radians(ang); nx=tx+16*math.cos(r2); ny=ty+16*math.sin(r2)-8
        circ(tree_t,nx,ny,9,"#6D4C41"); circ(tree_t,nx+2,ny+3,4,"#8D6E63")


def draw_round_tree(tree_t, bx, by):
    tc="#6D4C41"; td="#4E342E"; ld="#1A5C1A"; lm="#2E7D32"; ll="#388E3C"; lh="#4CAF50"
    tree_t.pencolor(tc); tree_t.pensize(22)
    tree_t.penup(); tree_t.goto(bx,by); tree_t.pendown()
    tree_t.goto(bx,by+145); tree_t.penup()
    tree_t.pencolor(td); tree_t.pensize(2)
    for i in range(0,145,12):
        tree_t.penup(); tree_t.goto(bx-9,by+i); tree_t.pendown()
        tree_t.goto(bx+9,by+i+7); tree_t.penup()
    brs=[(bx,by+138,bx-62,by+215,14),(bx,by+138,bx+52,by+210,12),
         (bx-62,by+215,bx-98,by+268,10),(bx-62,by+215,bx-28,by+262,8),
         (bx+52,by+210,bx+90,by+262,9),(bx+52,by+210,bx+20,by+258,7)]
    for sx,sy,ex,ey,ps in brs:
        tree_t.pencolor(td); tree_t.pensize(ps)
        tree_t.penup(); tree_t.goto(sx,sy); tree_t.pendown()
        tree_t.goto(ex,ey); tree_t.penup()
    ccx,ccy=bx+5,by+262
    for col,parts in [
        (ld,[(0,0,110),(-65,-20,82),(65,-20,78),(-32,44,75),(32,44,70),(0,66,80),(-82,12,60),(82,12,54)]),
        (lm,[(0,14,97),(-50,-10,72),(50,-10,68),(-24,52,65),(24,52,61),(0,74,70),(-64,22,50),(64,22,46)]),
        (ll,[(0,28,80),(-35,8,58),(35,8,54),(-16,58,50),(16,58,47)]),
        (lh,[(-14,32,52),(14,24,48),(0,50,44),(-40,14,40),(40,14,36)]),
    ]:
        for dx,dy,r in parts:
            circ(tree_t,ccx+dx,ccy+dy,r,col)
    for dx,dy,r in [(-18,36,22),(14,28,18),(-4,56,16),(28,44,14)]:
        circ(tree_t,ccx+dx,ccy+dy,r,"#81C784")


def draw_bg_trees(tree_t):
    for bx,by,s in C.BG_TREES:
        tc2 = C.GC_NIGHT["mid"] if C.NIGHT else C.GC_DAY["mid"]
        th  = int(85*s)
        tree_t.pencolor("#5D4037"); tree_t.pensize(int(9*s))
        tree_t.penup(); tree_t.goto(bx,by); tree_t.pendown()
        tree_t.goto(bx,by+th); tree_t.penup()
        for dx,dy,r in [(0,0,int(40*s)),(-int(22*s),-int(8*s),int(30*s)),
                         (int(20*s),-int(8*s),int(28*s)),(0,int(20*s),int(32*s))]:
            circ(tree_t,bx+dx,by+th+dy,r,tc2)
        circ(tree_t,bx+int(5*s),by+th+int(15*s),int(18*s),
             C.GC_NIGHT["near"] if C.NIGHT else C.GC_DAY["near"])


# ══════════════════════════════════════════════════════
#  PER-FRAME TICK
# ══════════════════════════════════════════════════════
def tick():
    global sun_ray_angle, star_frame, water_offset
    sun_ray_angle = (sun_ray_angle + 0.4) % 360
    star_frame   += 1
    water_offset += 1.2
