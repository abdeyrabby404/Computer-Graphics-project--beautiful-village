"""
config.py  ── Shared configuration: canvas sizes, colour palettes,
               runtime toggles, and static scene data.

Team owner: any member can edit colours / positions here without
touching drawing logic.
"""

import random

# ── Canvas ─────────────────────────────────────────────────────────────
W,  H  = 620, 340    # inner half-extents (scene coordinates)
BW     = 20          # border thickness (মোটা কালো border)

# ── Runtime toggles  (toggled by key-handlers in main.py) ──────────────
NIGHT   = False
RAINING = False
WINDY   = False

# ── Sky palettes ───────────────────────────────────────────────────────
DAY_SKY   = ["#1E88E5","#2196F3","#42A5F5","#64B5F6",
             "#90CAF9","#BBDEFB","#E3F2FD","#F5FBFF"]
NIGHT_SKY = ["#010510","#020818","#03091F","#040C28",
             "#060E32","#08113C","#0A1445","#0D1850"]

# ── Water palettes ─────────────────────────────────────────────────────
DAY_WATER   = ["#1565C0","#1976D2","#1E88E5","#2196F3","#42A5F5","#64B5F6"]
NIGHT_WATER = ["#020C1A","#030F20","#041228","#05152F","#061838","#081C42"]

# ── Grass palettes ─────────────────────────────────────────────────────
GC_DAY = {
    "far":   "#2E7D32", "mid":   "#388E3C",
    "near":  "#43A047", "front": "#66BB6A", "edge": "#81C784",
    "forest":"#1B5E20",                      # dense tree-line colour
}
GC_NIGHT = {
    "far":   "#0D2B0E", "mid":   "#122E12",
    "near":  "#163318", "front": "#1A3A1C", "edge": "#1E4020",
    "forest":"#071408",
}

def gc(key):
    """Return grass colour for the current day/night state."""
    return GC_NIGHT[key] if NIGHT else GC_DAY[key]

# ── River geometry ─────────────────────────────────────────────────────
RIVER_TOP = 72
RIVER_BOT = -38

# ── Forest strip (fills the blue gap between river and ground) ─────────
FOREST_BOT = RIVER_BOT   # bottom of forest = top of near-ground grass
FOREST_TOP = RIVER_TOP   # top of forest = bottom of river

# ── Static random data ─────────────────────────────────────────────────
random.seed(42)

STARS = [(random.randint(-W+10, W-10), random.randint(60, H-10),
          random.choice([1,1,1,2,2,3])) for _ in range(180)]

# Background tree positions used by environment.py
BG_TREES = [
    (-510,-158,0.52),(-450,-162,0.45),(-385,-156,0.50),
    (-320,-160,0.42),(-255,-155,0.46),
    ( 310,-158,0.50),( 370,-162,0.45),( 440,-156,0.52),
    ( 500,-160,0.44),( 555,-155,0.48),
]

# Flower positions/colours used by scene.py
FLOWERS = [
    (-550,-202,"#FF1744"),(-528,-206,"#E040FB"),(-506,-200,"#FF9800"),
    (-480,-204,"#FFEB3B"),(-458,-200,"#64DD17"),
    (-305,-212,"#FF1744"),(-283,-207,"#E040FB"),(-260,-212,"#FF9800"),
    (-238,-206,"#FFEB3B"),
    ( 140,-208,"#FF1744"),( 162,-204,"#E040FB"),( 184,-210,"#FF9800"),
    ( 206,-205,"#FFEB3B"),( 228,-210,"#64DD17"),
    ( 340,-210,"#FF1744"),( 362,-205,"#E040FB"),( 388,-210,"#FFEB3B"),
    ( 414,-207,"#FF9800"),( 438,-212,"#FF1744"),
    ( 470,-208,"#E040FB"),( 498,-204,"#FFEB3B"),( 525,-210,"#FF9800"),
    ( 552,-206,"#FF1744"),( 580,-210,"#E040FB"),
    (-580,-204,"#FF9800"),(-560,-210,"#FF1744"),(-535,-205,"#FFEB3B"),
    ( 590,-204,"#64DD17"),
]

TUFTS = [
    (-555,-172),(-500,-176),(-445,-170),(-390,-174),(-335,-170),
    (-165,-174),( 225,-170),( 280,-175),( 395,-170),( 455,-175),
    ( 515,-170),( 568,-174),( 608,-170),(-620,-172),
]
