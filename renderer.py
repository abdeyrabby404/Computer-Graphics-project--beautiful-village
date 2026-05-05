"""
renderer.py  ── Low-level drawing primitives, turtle factory, canvas
                border, and HUD overlay.

Team owner: responsible for the drawing toolkit and the on-screen UI
(title text, mode indicator, border frame).
"""

import math
import turtle
import config as C


# ══════════════════════════════════════════════════════
#  TURTLE FACTORY
# ══════════════════════════════════════════════════════
def mk():
    """Return a hidden, instant-speed turtle."""
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.hideturtle()
    return t


# ══════════════════════════════════════════════════════
#  PRIMITIVES
# ══════════════════════════════════════════════════════
def poly(t, pts, fill, edge=None, pw=1):
    """Draw a filled polygon through *pts*."""
    if len(pts) < 2:
        return
    t.penup(); t.goto(pts[0])
    t.fillcolor(fill)
    t.pencolor(edge if edge else fill)
    t.pensize(pw)
    t.pendown(); t.begin_fill()
    for p in pts[1:]:
        t.goto(p)
    t.goto(pts[0]); t.end_fill(); t.penup()


def rect(t, x, y, w, h, fill, edge=None, pw=1):
    """Draw a filled axis-aligned rectangle."""
    poly(t, [(x,y),(x+w,y),(x+w,y+h),(x,y+h)], fill, edge, pw)


def circ(t, cx, cy, r, fill, edge=None, pw=1):
    """Draw a filled circle centred at (cx, cy)."""
    t.penup(); t.goto(cx, cy - r); t.setheading(0)
    t.fillcolor(fill)
    t.pencolor(edge if edge else fill)
    t.pensize(pw)
    t.pendown(); t.begin_fill(); t.circle(r); t.end_fill(); t.penup()


def ellipse(t, cx, cy, rx, ry, fill, edge=None, pw=1):
    """Draw a filled ellipse."""
    pts = [(cx + rx*math.cos(math.radians(d)),
            cy + ry*math.sin(math.radians(d))) for d in range(0,361,3)]
    poly(t, pts, fill, edge, pw)


def bezier_line(t, p0, p1, p2, p3, steps=30, col="#000", pw=2):
    """Draw a cubic Bézier curve."""
    t.pencolor(col); t.pensize(pw)
    t.penup(); t.goto(p0); t.pendown()
    for i in range(steps + 1):
        u = i / steps
        x = ((1-u)**3*p0[0] + 3*(1-u)**2*u*p1[0]
             + 3*(1-u)*u**2*p2[0] + u**3*p3[0])
        y = ((1-u)**3*p0[1] + 3*(1-u)**2*u*p1[1]
             + 3*(1-u)*u**2*p2[1] + u**3*p3[1])
        t.goto(x, y)
    t.penup()


# ══════════════════════════════════════════════════════
#  BORDER  (drawn once at startup on border_t)
# ══════════════════════════════════════════════════════
def draw_border(border_t):
    """Draw a thick black border around the scene."""
    W, H, BW = C.W, C.H, C.BW

    # Black filled border rectangle (মোটা কালো border)
    border_t.penup(); border_t.goto(-W - BW, -H - BW)
    border_t.pencolor("black"); border_t.fillcolor("black"); border_t.pensize(1)
    border_t.pendown(); border_t.begin_fill()
    for _ in range(2):
        border_t.forward((W + BW) * 2); border_t.left(90)
        border_t.forward((H + BW) * 2); border_t.left(90)
    border_t.end_fill(); border_t.penup()


# ══════════════════════════════════════════════════════
#  OVERLAY  (redrawn every frame on over_t)
# ══════════════════════════════════════════════════════
def draw_overlay(over_t):
    """Re-stamp the thick black border on top of all layers (no text)."""
    W, H, BW = C.W, C.H, C.BW
    over_t.clear()

    # Re-stamp thick black border so animated layers never bleed outside
    over_t.penup(); over_t.goto(-W - BW, -H - BW)
    over_t.pencolor("black"); over_t.pensize(BW * 2 + 18)
    over_t.pendown()
    for _ in range(2):
        over_t.forward((W + BW) * 2); over_t.left(90)
        over_t.forward((H + BW) * 2); over_t.left(90)
    over_t.penup()
