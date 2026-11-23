#!/usr/bin/env python3
"""og.png 1200x630 — Grampy's Bakery (Leesburg FL), 2x supersample. v3 per vision:
berry filling + golden lattice with contrast, crust rim, pie sitting in a berry dish,
steam curls, pie lowered + badge enlarged. Shop identity only. t_100bb27b 2026-11-23."""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 1200, 630
S = 2
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

COCOA = (46, 28, 20); COCOA2 = (67, 41, 27)
BUTTER = (201, 143, 44); BUTTER_HI = (227, 180, 92)
BERRY = (156, 47, 57); BERRY_DARK = (110, 42, 50); BERRY_DEEP = (88, 34, 42); BERRY_RIM = (186, 104, 112)
CRUST = (196, 128, 58); CRUST_HI = (216, 152, 74); CRUST_LOW = (146, 92, 44)
FILLING = (125, 45, 52); FILL_HI = (146, 58, 62)
STEAM = (172, 144, 104)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except Exception: pass
    return ImageFont.load_default()

serif  = lambda s: font(["Georgia Bold.ttf", "Times New Roman Bold.ttf"], s * S)
serifm = lambda s: font(["Georgia.ttf", "Times New Roman.ttf"], s * S)
sans   = lambda s: font(["Helvetica-Bold.ttf", "Arial Bold.ttf"], s * S)

img = Image.new("RGB", (W * S, H * S), COCOA)
d = ImageDraw.Draw(img, "RGBA")
def P(x, y): return (x * S, y * S)

for cx, cy, r, col in [(1010, 80, 480, (87, 53, 31)), (90, 600, 380, (74, 44, 25))]:
    d.ellipse([P(cx - r, cy - r), P(cx + r, cy + r)], fill=col)

# berry notice ribbon
d.rectangle([0, 0, W * S, 52 * S], fill=BERRY)
d.text(P(46, 15), "GRAND OPENING \u00b7 TUESDAY NOVEMBER 24 \u00b7 11:45 A.M.", font=sans(19), fill=(253, 243, 227))

# gold hairline frame
d.rectangle([P(18, 70), P(W - 18, H - 18)], outline=BUTTER, width=2 * S)

L = 56
d.text(P(L, 100), "FAMILY-RUN BAKERY \u00b7 LEESBURG, FLORIDA", font=sans(17), fill=(180, 152, 110))
d.text(P(L, 146), "Grampy\u2019s", font=serif(118), fill=BUTTER_HI)
d.text(P(L + 8, 288), "Bakery", font=serifm(88), fill=(253, 246, 231))
d.rectangle([P(L, 412), P(L + 320, 416)], fill=BUTTER)
d.text(P(L, 440), "Pies \u00b7 specialty cakes \u00b7 cannoli \u00b7 a full bread program", font=serif(24), fill=(233, 214, 176))
d.text(P(L, 482), "and gourmet specialty coffees \u2014 announced for the holidays.", font=serifm(21), fill=(201, 179, 137))

# address plate
d.rounded_rectangle([P(L, 522), P(L + 560, 588)], radius=10 * S, fill=COCOA2, outline=(122, 92, 58), width=2 * S)
d.text(P(L + 22, 536), "1410 GRIFFIN ROAD \u00b7 LEESBURG, FL 34748", font=sans(17), fill=BUTTER_HI)
d.text(P(L + 22, 562), "just off U.S. 441 \u00b7 ribbon-cutting with the Leesburg Area Chamber", font=serifm(15), fill=(214, 190, 148))

# ---------- pie in a berry dish ----------
DISH = [745, 330, 1155, 455]; DISH_S = [x * S for x in DISH]
PIE  = [790, 283, 1110, 407]; PIE_S  = [x * S for x in PIE]
INSE = [820, 299, 1080, 391]; INSE_S = [x * S for x in INSE]   # lattice mask (same cx/cy, inset)

# dish (behind the pie)
d.ellipse(DISH_S, fill=BERRY_DARK)
d.ellipse([P(770, 345), P(1130, 440)], fill=BERRY_DEEP)

# pie body: baked crust side
d.ellipse(PIE_S, fill=CRUST)
# bottom shading on the crust side
d.arc(PIE_S, 0, 180, fill=CRUST_LOW, width=4 * S)
# top surface: berry filling (upper half of the ellipse)
d.pieslice(PIE_S, 180, 360, fill=FILLING)
d.pieslice(PIE_S, 180, 360, fill=None, outline=FILL_HI, width=1 * S)
# golden lattice over the filling, clipped to the inset top surface
mask = Image.new("L", img.size, 0)
md = ImageDraw.Draw(mask)
md.pieslice(INSE_S, 180, 360, fill=255)
ov = Image.new("RGBA", img.size, (0, 0, 0, 0))          # transparent: gaps show the berry filling
od = ImageDraw.Draw(ov)
for i in range(-4, 5):
    od.line([(760 + i * 66) * S, 400 * S, (760 + i * 66 + 230) * S, (400 - 230) * S], fill=(222, 156, 80, 255), width=13 * S)
    od.line([(760 + i * 66) * S, 260 * S, (760 + i * 66 + 230) * S, (260 + 230) * S], fill=(232, 172, 96, 255), width=13 * S)
img.paste(ov, (0, 0), mask)
d = ImageDraw.Draw(img, "RGBA")
# thick golden crust rim around the top surface
d.arc(PIE_S, 180, 360, fill=CRUST_HI, width=11 * S)
d.arc(PIE_S, 180, 360, fill=(150, 96, 44), width=2 * S)
# dish front rim highlight
d.arc(DISH_S, 0, 180, fill=BERRY_RIM, width=3 * S)

# steam: three sine curls rising off the dome
def curl(cx, y0, y1, amp):
    pts = []
    for k in range(24):
        t = k / 23
        y = y0 - (y0 - y1) * t
        x = cx + amp * math.sin(t * math.pi * 1.6)
        pts.append(P(x, y))
    d.line(pts, fill=STEAM, width=8 * S, joint="curve")
curl(898, 278, 158, 20); curl(950, 270, 138, 22); curl(1002, 278, 158, 20)

# berry invite pill (enlarged)
d.rounded_rectangle([P(850, 500), P(1160, 578)], radius=39 * S, fill=BERRY, outline=(94, 28, 34), width=2 * S)
d.text(P(876, 514), "NOTHING TO BUY.", font=sans(19), fill=(253, 243, 227))
d.text(P(876, 544), "YOU\u2019RE ALREADY INVITED.", font=sans(19), fill=(253, 243, 227))

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
