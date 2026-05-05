"""
animation.py  ── All moving / particle effects:
                  birds (flapping), fireflies (night), rain drops,
                  and wind-blown leaves.

Team owner: responsible for all animated overlay effects and their
per-frame update logic.
"""

import math
import random
import config as C
from renderer import circ, poly

# ══════════════════════════════════════════════════════
#  BIRDS
# ══════════════════════════════════════════════════════
BIRDS = [
    {"x":-560,"y":242,"spd":1.9,"sz":1.00,"ph":0.0},
    {"x":-525,"y":258,"spd":1.9,"sz":0.85,"ph":0.5},
    {"x":-545,"y":228,"spd":1.9,"sz":0.78,"ph":1.0},
    {"x": 190,"y":280,"spd":1.5,"sz":1.10,"ph":0.2},
    {"x": 225,"y":265,"spd":1.5,"sz":0.90,"ph":0.8},
    {"x": -90,"y":310,"spd":1.1,"sz":0.65,"ph":0.4},
    {"x": 380,"y":252,"spd":1.7,"sz":0.80,"ph":0.9},
    {"x": 412,"y":268,"spd":1.7,"sz":0.68,"ph":1.4},
]
_bird_frame = 0


def draw_birds(bird_t):
    bird_t.clear()
    col = "#DDDDDD" if C.NIGHT else "#1A237E"
    for b in BIRDS:
        flap = math.sin(_bird_frame * 0.18 + b["ph"])
        wu   = flap * 11 * b["sz"]
        bx, by, s = b["x"], b["y"], b["sz"]
        bird_t.pencolor(col)
        bird_t.pensize(max(1, int(2.2 * s)))
        bird_t.penup(); bird_t.goto(bx, by); bird_t.pendown()
        bird_t.goto(bx - 13*s, by + wu); bird_t.penup()
        bird_t.goto(bx, by); bird_t.pendown()
        bird_t.goto(bx + 13*s, by + wu); bird_t.penup()
        circ(bird_t, bx, by, int(2.2*s), col)


def update_birds():
    global _bird_frame
    _bird_frame += 1
    for b in BIRDS:
        b["x"] += b["spd"]
        if b["x"] > C.W + 70:
            b["x"] = -C.W - 70


# ══════════════════════════════════════════════════════
#  FIREFLIES  (night only)
# ══════════════════════════════════════════════════════
random.seed(99)
FIREFLIES = [
    {"x":  random.randint(-380, 380),
     "y":  random.randint(-175, 55),
     "ph": random.uniform(0, 6.28),
     "sx": random.uniform(-0.5, 0.5),
     "sy": random.uniform(-0.3, 0.3)}
    for _ in range(28)
]
_ff_frame = 0


def draw_fireflies(fx_t):
    if not C.NIGHT:
        return
    for ff in FIREFLIES:
        br = (math.sin(_ff_frame * 0.13 + ff["ph"]) + 1) / 2
        if br > 0.45:
            r = int(5 * br)
            circ(fx_t, ff["x"], ff["y"], r+4, "#FFFFE0")
            circ(fx_t, ff["x"], ff["y"], r,   "#FFFF00")


def update_fireflies():
    global _ff_frame
    _ff_frame += 1
    for ff in FIREFLIES:
        ff["x"] += ff["sx"] + 0.12*math.sin(_ff_frame*0.05 + ff["ph"])
        ff["y"] += ff["sy"] + 0.09*math.cos(_ff_frame*0.07 + ff["ph"])
        if ff["x"] >  400: ff["x"] = -400
        if ff["x"] < -400: ff["x"] =  400
        if ff["y"] >   60: ff["y"] = -175
        if ff["y"] < -175: ff["y"] =   60


# ══════════════════════════════════════════════════════
#  RAIN
# ══════════════════════════════════════════════════════
random.seed(55)
RAIN = [
    {"x":   random.randint(-C.W, C.W),
     "y":   random.randint(-C.H, C.H),
     "spd": random.uniform(9, 16),
     "ln":  random.randint(10, 22)}
    for _ in range(130)
]


def draw_rain(fx_t):
    if not C.RAINING:
        return
    fx_t.pencolor("#90CAF9" if not C.NIGHT else "#1565C0")
    fx_t.pensize(1)
    for rd in RAIN:
        fx_t.penup(); fx_t.goto(rd["x"], rd["y"]); fx_t.pendown()
        fx_t.goto(rd["x"]-3, rd["y"]-rd["ln"]); fx_t.penup()


def update_rain():
    if not C.RAINING:
        return
    for rd in RAIN:
        rd["y"] -= rd["spd"]; rd["x"] -= 3
        if rd["y"] < -C.H:
            rd["y"] = C.H; rd["x"] = random.randint(-C.W, C.W)


# ══════════════════════════════════════════════════════
#  WIND LEAVES
# ══════════════════════════════════════════════════════
random.seed(33)
WIND_LEAVES = [
    {"x":   random.randint(-C.W, C.W),
     "y":   random.randint(-200, C.H),
     "spd": random.uniform(2, 5),
     "rot": random.uniform(0, 6.28),
     "rs":  random.uniform(-0.2, 0.2),
     "col": random.choice(["#388E3C","#2E7D32","#F57F17","#E65100","#43A047"])}
    for _ in range(40)
]


def draw_wind_leaves(fx_t):
    if not C.WINDY:
        return
    for wl in WIND_LEAVES:
        rx, ry = 9, 5; rad = wl["rot"]; pts = []
        for d in range(0,361,6):
            a  = math.radians(d)
            lx = wl["x"] + rx*math.cos(a)*math.cos(rad) - ry*math.sin(a)*math.sin(rad)
            ly = wl["y"] + rx*math.cos(a)*math.sin(rad) + ry*math.sin(a)*math.cos(rad)
            pts.append((lx,ly))
        poly(fx_t, pts, wl["col"])


def update_wind():
    if not C.WINDY:
        return
    for wl in WIND_LEAVES:
        wl["x"] += wl["spd"]
        wl["y"] += math.sin(wl["rot"]) * 1.5
        wl["rot"] += wl["rs"]
        if wl["x"] > C.W+20:
            wl["x"] = -C.W-20
            wl["y"] = random.randint(-200, C.H)
