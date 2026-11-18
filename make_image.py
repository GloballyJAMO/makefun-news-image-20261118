#!/usr/bin/env python3
"""Draw entry.png: the world news of Wednesday 18 November 2026 in one image.

The picture is a newspaper front page. Every story on it was reported on
18 November 2026 (UTC day, any time zone):

- APEC, Shenzhen: Xi Jinping and Vladimir Putin met, and Donald Trump
  arrived in China, ahead of the first-ever US-China-Russia trilateral
  talks set for Thursday 19 November. Xi called for an open Asia-Pacific
  economy and against trade protectionism.
- Iran said its drones struck US platforms at Ali Al Salem Air Base in
  Kuwait; Bahrain reported intercepting Iranian attacks; a UAE ADNOC
  vessel was struck in the Strait of Hormuz with one crew member missing.
- Israel began a "concentrated operation" in three areas of central Gaza;
  the UK sanctioned firms behind West Bank settlement expansion and a
  group blocking aid into Gaza.
- Germany announced a new military aid package for Ukraine: more air
  defence systems, guided missiles and ammunition for F-16 jets.
- Severe Cyclonic Storm Akvan approached Odisha, India, and people in
  unsafe houses in Ganjam district were moved to shelters; in Florida,
  potentially catastrophic rain closed schools and pushed the St. Johns
  River to major flood stage.
- Democrat Mary Peltola defeated Republican Dan Sullivan in Alaska,
  giving Democrats a projected 56-44 majority in the incoming US Senate.
- Grand Theft Auto VI, 13 years after the previous game, launches at
  midnight.
- Also that day: a magnitude 6 earthquake in Papua New Guinea, Quad
  leaders meeting in Manila for the first time in over two years, an
  India-US trade deal nearly final with its signing delayed, and PM Modi
  wrapping up the ASEAN summit in Manila.

Run locally (needs Pillow) to regenerate entry.png:
    python3 make_image.py
The graded program is main.py, which only copies entry.png; this script
is kept in the repository so anyone can see how the image was made.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype"
SANS = os.path.join(FONT_DIR, "liberation", "LiberationSans-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "liberation", "LiberationSans-Bold.ttf")
SERIF_B = os.path.join(FONT_DIR, "liberation", "LiberationSerif-Bold.ttf")

PAPER = (247, 243, 234)
CARD = (255, 255, 255)
INK = (20, 29, 47)
MUTED = (84, 94, 112)
NAVY = (16, 32, 58)
RED = (178, 34, 43)
GOLD = (232, 160, 32)
TEAL = (14, 116, 110)
BLUE = (30, 84, 160)
SKY = (219, 231, 244)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.12):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def card(draw, box, accent):
    draw.rounded_rectangle(box, radius=14, fill=CARD, outline=(214, 208, 194), width=2)
    x0, y0, _, _ = box
    draw.rounded_rectangle((x0, y0, x0 + 10, box[3]), radius=5, fill=accent)


# --- small flag drawings (simplified, recognisable) -----------------------

def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flag_china(draw, x, y, w, h):
    draw.rectangle((x, y, x + w, y + h), fill=(222, 41, 16))
    star(draw, x + 20, y + 18, 11, (255, 222, 0))
    star(draw, x + 38, y + 10, 5, (255, 222, 0))
    star(draw, x + 42, y + 22, 5, (255, 222, 0))
    star(draw, x + 38, y + 34, 5, (255, 222, 0))


def flag_russia(draw, x, y, w, h):
    t = h // 3
    draw.rectangle((x, y, x + w, y + t), fill=(245, 245, 245))
    draw.rectangle((x, y + t, x + w, y + 2 * t), fill=(0, 57, 166))
    draw.rectangle((x, y + 2 * t, x + w, y + h), fill=(213, 43, 30))


def flag_usa(draw, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else (245, 245, 245)
        draw.rectangle((x, y + i * stripe, x + w, y + (i + 1) * stripe), fill=col)
    draw.rectangle((x, y, x + w * 0.45, y + stripe * 4), fill=(60, 59, 110))
    for r in range(3):
        for c in range(4):
            cx, cy = x + 8 + c * 11, y + 6 + r * 9
            draw.ellipse((cx, cy, cx + 4, cy + 4), fill=(255, 255, 255))


# --- simple white-on-colour icons -----------------------------------------

def icon_drone(draw, cx, cy, col):
    for dx, dy in ((-26, -16), (26, -16), (-26, 16), (26, 16)):
        draw.line((cx, cy, cx + dx, cy + dy), fill=col, width=5)
        draw.ellipse((cx + dx - 10, cy + dy - 5, cx + dx + 10, cy + dy + 5), outline=col, width=4)
    draw.rounded_rectangle((cx - 13, cy - 9, cx + 13, cy + 9), radius=4, fill=col)


def icon_pin(draw, cx, cy, col):
    draw.ellipse((cx - 17, cy - 24, cx + 17, cy + 10), fill=col)
    draw.polygon([(cx - 12, cy + 2), (cx + 12, cy + 2), (cx, cy + 26)], fill=col)
    draw.ellipse((cx - 7, cy - 17, cx + 7, cy - 3), fill=CARD)


def icon_shield(draw, cx, cy, col):
    draw.polygon([(cx, cy - 26), (cx + 20, cy - 18), (cx + 20, cy + 4),
                  (cx, cy + 27), (cx - 20, cy + 4), (cx - 20, cy - 18)], fill=col)
    draw.line((cx, cy - 14, cx, cy + 14), fill=CARD, width=6)
    draw.line((cx - 10, cy - 4, cx + 10, cy - 4), fill=CARD, width=6)


def icon_cyclone(draw, cx, cy, col):
    pts = []
    for i in range(160):
        t = i / 159 * 4.6 * math.pi
        r = 3 + i / 159 * 24
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    draw.line(pts, fill=col, width=5)


def icon_capitol(draw, cx, cy, col):
    draw.arc((cx - 22, cy - 26, cx + 22, cy + 8), start=180, end=360, fill=col, width=6)
    draw.line((cx, cy - 26, cx, cy - 34), fill=col, width=5)
    for dx in (-18, -6, 6, 18):
        draw.line((cx + dx, cy - 2, cx + dx, cy + 20), fill=col, width=5)
    draw.line((cx - 26, cy + 26, cx + 26, cy + 26), fill=col, width=6)


def icon_controller(draw, cx, cy, col):
    draw.rounded_rectangle((cx - 30, cy - 16, cx + 30, cy + 16), radius=14, outline=col, width=6)
    draw.line((cx - 20, cy, cx - 8, cy), fill=col, width=5)
    draw.line((cx - 14, cy - 6, cx - 14, cy + 6), fill=col, width=5)
    draw.ellipse((cx + 8, cy - 8, cx + 16, cy), fill=col)
    draw.ellipse((cx + 18, cy + 1, cx + 26, cy + 9), fill=col)


ICONS = {"drone": icon_drone, "pin": icon_pin, "shield": icon_shield,
         "cyclone": icon_cyclone, "capitol": icon_capitol, "pad": icon_controller}


def story(draw, box, accent, icon, kicker, headline, sub):
    card(draw, box, accent)
    x0, y0, x1, _ = box
    draw.rounded_rectangle((x0 + 22, y0 + 16, x0 + 78, y0 + 72), radius=12, fill=accent)
    ICONS[icon](draw, x0 + 50, y0 + 44, CARD)
    draw.text((x0 + 94, y0 + 18), kicker, font=font(SANS_B, 23), fill=accent)
    y = text_block(draw, (x0 + 94, y0 + 48), headline, font(SANS_B, 31), INK, x1 - x0 - 116, 1.08)
    text_block(draw, (x0 + 24, y + 6), sub, font(SANS, 22), MUTED, x1 - x0 - 48, 1.18)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead: the date is the biggest thing on the page.
    draw.rectangle((0, 0, W, 120), fill=NAVY)
    draw.text((W // 2, 10), "T H E   W O R L D   I N   O N E   I M A G E",
              font=font(SANS_B, 25), fill=GOLD, anchor="ma")
    draw.text((W // 2, 40), "Wednesday 18 November 2026",
              font=font(SERIF_B, 58), fill=(255, 255, 255), anchor="ma")

    # Lead story: APEC summit in Shenzhen.
    lead = (28, 136, W - 28, 354)
    card(draw, lead, RED)
    draw.text((54, 152), "LEAD STORY · APEC SUMMIT · SHENZHEN, CHINA",
              font=font(SANS_B, 25), fill=RED)
    y = text_block(draw, (54, 184), "Xi & Putin meet as Trump lands in China",
                   font(SERIF_B, 47), INK, 640, 1.08)
    text_block(draw, (54, y + 8),
               "First-ever US-China-Russia trilateral talks set for Thursday. "
               "Xi urges open Asia-Pacific trade.",
               font(SANS, 24), MUTED, 640, 1.18)
    fx, fy, fw, fh = 730, 190, 100, 62
    flag_china(draw, fx, fy, fw, fh)
    flag_russia(draw, fx + 118, fy, fw, fh)
    flag_usa(draw, fx, fy + 84, fw, fh)
    draw.text((fx + 118 + fw // 2, fy + 88), "APEC", font=font(SANS_B, 32), fill=NAVY, anchor="ma")
    draw.text((fx + 118 + fw // 2, fy + 124), "2026", font=font(SANS_B, 28), fill=MUTED, anchor="ma")

    # Four story cards in a 2x2 grid.
    gx, gy, gw, gh, gap = 28, 370, 474, 178, 16
    story(draw, (gx, gy, gx + gw, gy + gh), RED, "drone",
          "IRAN WAR ESCALATES",
          "Iran says drones hit US base in Kuwait",
          "Bahrain intercepts attacks. Tanker struck in Hormuz, crew missing.")
    story(draw, (gx + gw + gap, gy, gx + 2 * gw + gap, gy + gh), TEAL, "pin",
          "GAZA",
          "Israel begins operation in central Gaza",
          "UK sanctions settlement firms and a group blocking Gaza aid.")
    story(draw, (gx, gy + gh + gap, gx + gw, gy + 2 * gh + gap), BLUE, "shield",
          "UKRAINE",
          "Germany pledges new air defences",
          "Missiles and F-16 ammunition as Russia steps up air attacks.")
    story(draw, (gx + gw + gap, gy + gh + gap, gx + 2 * gw + gap, gy + 2 * gh + gap), GOLD, "cyclone",
          "STORMS & FLOODS",
          "Cyclone Akvan nears Odisha; Florida floods",
          "Shelters open in India. Schools shut as Florida rivers rise.")

    # Bottom row: US politics and the culture story of the day.
    by, bh = gy + 2 * gh + 2 * gap, 178
    story(draw, (gx, by, gx + gw, by + bh), NAVY, "capitol",
          "US POLITICS",
          "Democrat Peltola wins Alaska",
          "Democrats projected to hold a 56-44 Senate majority.")
    story(draw, (gx + gw + gap, by, gx + 2 * gw + gap, by + bh), (111, 66, 193), "pad",
          "CULTURE · GAMES",
          "GTA VI launches at midnight",
          "The 13-year wait for gaming's biggest release ends tonight.")

    # Ticker: the rest of the day, briefly.
    ty = by + bh + 12
    draw.rectangle((0, ty, W, H), fill=NAVY)
    draw.text((28, ty + 8), "ALSO TODAY", font=font(SANS_B, 23), fill=GOLD)
    text_block(draw, (196, ty + 8),
               "M6.0 earthquake hits Papua New Guinea · Quad leaders meet in Manila · "
               "India-US trade deal nearly final",
               font(SANS, 23), (255, 255, 255), W - 224, 1.3)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
