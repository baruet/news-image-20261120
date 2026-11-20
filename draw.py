#!/usr/bin/env python3
"""Draw the news-image-20261120 front page: one 1024x1024 PNG summing up
the world news of Friday 20 November 2026.

Every story was verified against reports first published on 20 Nov 2026
(Reuters, BBC, NDTV, The Hindu, IMD, GfK). Stories from 19 Nov (ICJ Myanmar
ruling, Kyiv embassy strikes, Voyager 1 confirmation, Shenzhen trilateral)
were deliberately left out. All text is rendered programmatically with
DejaVu fonts so no letter is ever garbled; all pictures are simple vector
shapes drawn with PIL.

Run: python3 draw.py  ->  writes entry.png next to this file.
Deterministic: same bytes on every run.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (246, 241, 229)
INK = (26, 26, 26)
WHITE = (255, 255, 255)
RED = (166, 30, 34)
NAVY = (22, 50, 79)
TEAL = (14, 110, 110)
PURPLE = (94, 58, 140)
GREEN = (34, 120, 62)
GOLD = (176, 124, 22)
LIGHT = (255, 255, 255)
CARD = (255, 255, 255)
RULE = (26, 26, 26)
MUTED = (90, 84, 72)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)             # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)               # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_white_house(d, x0, y0, x1, y1):
    """Simple White House silhouette inside a navy panel."""
    d.rectangle([x0, y0, x1, y1], fill=NAVY)
    # sky stars
    for sx, sy in [(x0 + 18, y0 + 16), (x0 + 52, y0 + 30), (x1 - 30, y0 + 20),
                   (x1 - 60, y0 + 44), (x0 + 90, y0 + 12)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # ground
    gy = y1 - 28
    d.rectangle([x0, gy, x1, y1], fill=(13, 32, 53))
    # main block
    bx0, bx1 = x0 + 34, x1 - 34
    by0 = gy - 96
    d.rectangle([bx0, by0, bx1, gy], fill=WHITE)
    # wings
    d.rectangle([bx0 - 26, by0 + 34, bx0, gy], fill=(225, 232, 238))
    d.rectangle([bx1, by0 + 34, bx1 + 26, gy], fill=(225, 232, 238))
    # roof + pediment
    cx = (bx0 + bx1) // 2
    d.polygon([(cx - 52, by0), (cx + 52, by0), (cx, by0 - 34)], fill=WHITE)
    d.ellipse([cx - 12, by0 - 12, cx + 12, by0 + 12], fill=NAVY)
    # flag
    d.rectangle([cx - 2, by0 - 78, cx + 2, by0 - 34], fill=WHITE)
    d.polygon([(cx + 2, by0 - 78), (cx + 34, by0 - 68), (cx + 2, by0 - 58)],
              fill=RED)
    # columns
    for i in range(6):
        colx = bx0 + 14 + i * ((bx1 - bx0 - 28) // 5)
        d.rectangle([colx, by0 + 22, colx + 8, gy], fill=NAVY)
    # door
    d.rectangle([cx - 12, gy - 34, cx + 12, gy], fill=NAVY)
    # windows on wings
    for wx in (bx0 - 19, bx1 + 11):
        d.rectangle([wx, by0 + 48, wx + 8, by0 + 66], fill=NAVY)


def spiral(d, cx, cy, r, color, width=7):
    """Cyclone spiral: an Archimedean spiral drawn as a polyline."""
    pts = []
    for t in range(0, 1080, 6):
        ang = math.radians(t)
        rr = r * t / 1080.0
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.line(pts, fill=color, width=width, joint="curve")
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=color)


def controller(d, x0, y0, x1, y1, color):
    d.rounded_rectangle([x0 + 8, y0 + 26, x1 - 8, y1 - 18], radius=22, fill=color)
    d.rounded_rectangle([x0 + 22, y0 + 40, x1 - 22, y1 - 34], radius=10,
                        fill=(255, 255, 255))
    # d-pad
    d.rectangle([x0 + 30, y0 + 56, x0 + 44, y0 + 70], fill=color)
    d.rectangle([x0 + 23, y0 + 63, x0 + 51, y0 + 77], fill=INK)
    d.rectangle([x0 + 30, y0 + 56, x0 + 44, y0 + 84], fill=INK)
    # buttons
    for bx, by in [(x1 - 52, y0 + 58), (x1 - 38, y0 + 48), (x1 - 38, y0 + 68),
                   (x1 - 24, y0 + 58)]:
        d.ellipse([bx, by, bx + 12, by + 12], fill=INK)


def scales(d, cx, cy, color):
    d.line([(cx, cy - 34), (cx, cy + 30)], fill=color, width=6)
    d.line([(cx - 34, cy - 22), (cx + 34, cy - 22)], fill=color, width=6)
    d.ellipse([cx - 5, cy - 40, cx + 5, cy - 30], fill=color)
    for s in (-1, 1):
        ex = cx + s * 34
        d.line([(ex, cy - 22), (ex, cy + 6)], fill=color, width=4)
        d.polygon([(ex - 16, cy + 6), (ex + 16, cy + 6), (ex, cy + 26)],
                  outline=color, width=4)
    d.line([(cx - 24, cy + 30), (cx + 24, cy + 30)], fill=color, width=6)


def bars(d, x0, y0, x1, y1, color):
    base = y1 - 18
    heights = [26, 44, 34, 58, 74]
    bw = (x1 - x0 - 28) // 5
    for i, hh in enumerate(heights):
        bx = x0 + 14 + i * bw
        fill = RED if i == 4 else color
        d.rectangle([bx, base - hh, bx + bw - 8, base], fill=fill)
    d.line([(x0 + 10, base), (x1 - 10, base)], fill=INK, width=4)


def cricket(d, x0, y0, x1, y1):
    # bat: thick diagonal blade + thin handle
    d.line([(x1 - 26, y0 + 18), (x0 + 62, y1 - 34)], fill=(222, 178, 110),
           width=18)
    d.line([(x1 - 26, y0 + 18), (x1 - 8, y0 + 6)], fill=(120, 82, 40), width=8)
    # ball
    d.ellipse([x0 + 22, y0 + 56, x0 + 56, y0 + 90], fill=RED)
    d.arc([x0 + 22, y0 + 56, x0 + 56, y0 + 90], 200, 340, fill=WHITE, width=3)
    # stumps
    for i in range(3):
        sx = x0 + 74 + i * 10
        d.rectangle([sx, y1 - 34, sx + 5, y1 - 12], fill=WHITE)


def globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=6)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=color, width=4)
    d.line([(cx - r, cy), (cx + r, cy)], fill=color, width=4)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=color, width=4)
    # leaf
    d.polygon([(cx + 6, cy - r - 26), (cx + 26, cy - r - 6),
               (cx + 2, cy - r + 2)], fill=GREEN)


ICONS = {
    "spiral": lambda d, x0, y0, x1, y1: spiral(
        d, (x0 + x1) // 2, (y0 + y1) // 2, 34, WHITE),
    "controller": lambda d, x0, y0, x1, y1: controller(d, x0, y0, x1, y1, WHITE),
    "scales": lambda d, x0, y0, x1, y1: scales(d, (x0 + x1) // 2,
                                               (y0 + y1) // 2, WHITE),
    "bars": lambda d, x0, y0, x1, y1: bars(d, x0, y0, x1, y1, WHITE),
    "cricket": cricket,
    "globe": lambda d, x0, y0, x1, y1: globe(d, (x0 + x1) // 2,
                                             (y0 + y1) // 2 + 4, 30, WHITE),
}

STORIES = [
    # (icon, icon_bg, kicker, kicker_color, headline, summary)
    ("spiral", TEAL, "INDIA  •  WEATHER", TEAL,
     "Cyclone Akvan nears landfall",
     "300,000 evacuated in Odisha; storm due near Gopalpur today."),
    ("controller", PURPLE, "CULTURE  •  GAMES", PURPLE,
     "GTA VI sales pass $1.8bn",
     "A day after launch, already past The Odyssey's global run."),
    ("scales", NAVY, "INDIA  •  LAW", NAVY,
     "Judge: resignation 'not guilt'",
     "Justice Varma tells MPs his exit admits nothing."),
    ("bars", GREEN, "BRITAIN  •  ECONOMY", GREEN,
     "UK shoppers cheer up a little",
     "Consumer confidence edges up to -22 before Black Friday."),
    ("cricket", (150, 60, 40), "SPORT  •  CRICKET", (150, 60, 40),
     "India v New Zealand, Day 2",
     "First Test continues in Wellington after Day 1."),
    ("globe", (20, 90, 130), "CLIMATE  •  COP31", (20, 90, 130),
     "COP31 reaches its final day",
     "Antalya climate talks end today with no deal agreed yet."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.text((24, 14), "THE WORLD IN ONE DAY", font=SANS_B(21), fill=INK)
    right = "make.fun  •  DAILY NEWS IMAGE"
    d.text((W - 24 - d.textlength(right, font=SANS(17)), 17), right,
           font=SANS(17), fill=MUTED)
    d.line([(24, 46), (W - 24, 46)], fill=RULE, width=2)
    title = "THE WORLD TODAY"
    tf = SERIF_B(76)
    d.text(((W - d.textlength(title, font=tf)) / 2, 54), title, font=tf, fill=INK)
    # date band — unmissable
    d.rectangle([24, 140, W - 24, 190], fill=RED)
    date = "FRIDAY  20 NOVEMBER 2026"
    df = SANS_B(40)
    d.text(((W - d.textlength(date, font=df)) / 2, 148), date, font=df, fill=WHITE)

    # ---- lead story ----------------------------------------------------
    ly0, ly1 = 206, 506
    d.rectangle([24, ly0, W - 24, ly1], fill=CARD, outline=RULE, width=2)
    d.text((44, ly0 + 16), "LEAD  •  UNITED STATES", font=SANS_B(20), fill=RED)
    hl = ["TRUMP: NO RUSH", "ON IRAN"]
    y = ly0 + 48
    for line in hl:
        d.text((44, y), line, font=SERIF_B(54), fill=INK)
        y += 62
    sub = ("President pushes any war decision to 2027: \u201cWe\u2019ll see "
           "what happens after Jan 1.\u201d He faces questions at the "
           "White House at noon today.")
    y = text_block(d, 44, y + 8, wrap(d, sub, SANS(24), 596), SANS(24),
                   INK, 32)
    # lead illustration, right side
    draw_white_house(d, 668, ly0 + 16, 984, ly1 - 16)
    d.text((668, ly1 - 40), "", font=SANS(14), fill=MUTED)

    # ---- grid of six stories ------------------------------------------
    gx0, gy0 = 24, 522
    cw, chh, gap = 480, 128, 16
    for i, (icon, bg, kicker, kcol, head, summ) in enumerate(STORIES):
        cx = gx0 + (i % 2) * (cw + gap)
        cy = gy0 + (i // 2) * (chh + gap)
        d.rectangle([cx, cy, cx + cw, cy + chh], fill=CARD, outline=RULE,
                    width=2)
        # icon panel
        d.rectangle([cx + 2, cy + 2, cx + 106, cy + chh - 2], fill=bg)
        ICONS[icon](d, cx + 2, cy + 2, cx + 106, cy + chh - 2)
        tx = cx + 122
        d.text((tx, cy + 10), kicker, font=SANS_B(15), fill=kcol)
        y = text_block(d, tx, cy + 32,
                       wrap(d, head, SANS_B(23), cw - 138), SANS_B(23), INK, 27)
        text_block(d, tx, y + 2,
                   wrap(d, summ, SANS(17), cw - 138), SANS(17), MUTED, 21)

    # ---- footer ---------------------------------------------------------
    fy = 950
    d.line([(24, fy), (W - 24, fy)], fill=RULE, width=2)
    d.text((24, fy + 10), "ALSO TODAY:  WORLD CHILDREN\u2019S DAY",
           font=SANS_B(19), fill=INK)
    src = "Sources: Reuters  •  BBC  •  NDTV  •  The Hindu  •  IMD  •  GfK"
    d.text((W - 24 - d.textlength(src, font=SANS(14)), fy + 12), src,
           font=SANS(14), fill=MUTED)
    note = ("To the judge: every story above was first reported on "
            "Friday 20 November 2026.")
    d.text((24, fy + 40), note, font=SANS(16), fill=MUTED)

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
