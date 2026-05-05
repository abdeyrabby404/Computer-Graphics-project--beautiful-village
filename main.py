"""
main.py  ── Entry point shared by the whole team.
             Sets up the screen, creates turtle layers, runs the
             animation loop, and handles keyboard input.

             Do NOT put drawing logic here — use the four modules below.

Project layout (5 files total):
    village_scene/
    ├── config.py       — colours, sizes, toggles, static data      [Member 1]
    ├── renderer.py     — draw primitives + border + HUD overlay     [Member 2]
    ├── environment.py  — sky, water, landscape, forest, trees       [Member 3]
    ├── scene.py        — houses, fence, bushes, lamps, details      [Member 4]
    ├── animation.py    — birds, fireflies, rain, wind               [Member 4]
    └── main.py         — screen wiring, loop, keys  ← EVERYONE
"""

import turtle
import config      as C
import renderer    as R
import environment as ENV
import scene       as SCN
import animation   as ANI

# ── Screen ─────────────────────────────────────────────
screen = turtle.Screen()
screen.title("Beautiful Village Riverside scene  |  M=Night  R=Rain  W=Wind")
screen.setup(width=1280, height=720)
screen.bgcolor("#111111")
turtle.tracer(0, 0)

# ── Turtle layers  (draw order = creation order) ───────
border_t  = R.mk()
sky_t     = R.mk()
star_t    = R.mk()
sun_t     = R.mk()
cloud_t   = R.mk()
water_t   = R.mk()
boat_t    = R.mk()
forest_t  = R.mk()   # NEW: green forest strip behind houses
far_t     = R.mk()
grass_t   = R.mk()
tree_t    = R.mk()
house_t   = R.mk()
detail_t  = R.mk()
bird_t    = R.mk()
fx_t      = R.mk()
over_t    = R.mk()


# ── Static scene (redrawn when day/night toggles) ──────
def draw_static():
    ENV.draw_sky(sky_t)
    ENV.draw_stars(star_t)
    ENV.draw_sun_moon(sun_t)
    ENV.draw_river(water_t)           # river drawn before forest/grass
    ENV.draw_forest_strip(forest_t)   # green forest fills the blue gap
    ENV.draw_far_foliage(far_t)       # far-bank silhouette above river
    ENV.draw_grass(grass_t)           # ground layers + path

    tree_t.clear()
    ENV.draw_bg_trees(tree_t)
    ENV.draw_branch(tree_t)
    ENV.draw_palm(tree_t, -158, -198)
    ENV.draw_round_tree(tree_t, 118, -128)

    house_t.clear()
    SCN.draw_houses(house_t)
    SCN.draw_fence(house_t)
    SCN.draw_bushes(house_t)

    SCN.draw_details(detail_t)


def full_redraw():
    draw_static()
    ENV.draw_clouds(cloud_t)
    ENV.draw_boats(boat_t)
    ANI.draw_birds(bird_t)
    fx_t.clear()
    ANI.draw_fireflies(fx_t)
    ANI.draw_rain(fx_t)
    ANI.draw_wind_leaves(fx_t)
    R.draw_overlay(over_t)


# ── Animation loop ─────────────────────────────────────
def animate():
    ENV.tick()                          # advance water, sun-ray, star frame

    ENV.draw_river(water_t)
    if not C.NIGHT:
        ENV.draw_sun_moon(sun_t)
    ENV.draw_stars(star_t)

    ENV.update_clouds();  ENV.draw_clouds(cloud_t)
    ENV.update_boats();   ENV.draw_boats(boat_t)
    ANI.update_birds();   ANI.draw_birds(bird_t)

    fx_t.clear()
    ANI.update_fireflies(); ANI.draw_fireflies(fx_t)
    ANI.update_rain();      ANI.draw_rain(fx_t)
    ANI.update_wind();      ANI.draw_wind_leaves(fx_t)

    R.draw_overlay(over_t)
    turtle.update()
    screen.ontimer(animate, 20)


# ── Key bindings ───────────────────────────────────────
def toggle_night():
    C.NIGHT = not C.NIGHT
    draw_static()
    R.draw_overlay(over_t)
    turtle.update()

def toggle_rain():
    C.RAINING = not C.RAINING
    R.draw_overlay(over_t)

def toggle_wind():
    C.WINDY = not C.WINDY
    R.draw_overlay(over_t)


# ── Entry point ────────────────────────────────────────
if __name__ == "__main__":
    R.draw_border(border_t)
    full_redraw()
    turtle.update()

    screen.listen()
    screen.onkey(toggle_night, "m"); screen.onkey(toggle_night, "M")
    screen.onkey(toggle_rain,  "r"); screen.onkey(toggle_rain,  "R")
    screen.onkey(toggle_wind,  "w"); screen.onkey(toggle_wind,  "W")

    animate()
    turtle.done()
