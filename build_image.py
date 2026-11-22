#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261122.

Front page for Sunday 22 November 2026: two illustrated lead
features, four regional features, a dotted world map with numbered
pins, a BY THE NUMBERS strip and sixteen one-line briefs - 35
distinct stories, all first reported on 22 November 2026, across
seven regions (Gulf/Middle East, Europe, East Asia-Pacific, South
Asia, Africa, North America, South America) plus climate and markets.

Stories verified against wire reporting dated 22 November 2026
(Reuters, AP, AFP, BBC, Times of India, Arab News, Korea JoongAng
Daily). Deliberately EXCLUDED as earlier events: the Peru 6.9
quake (20 Nov local / 21 Nov GMT), the Shenzhen Trump-Xi-Putin
trilateral and its peace declaration (19-20 Nov), the Iran strike
on Ali Al Salem air base in Kuwait (18 Nov), the Qeshm Island
strike (17 Nov), the ADNOC tanker attack (17 Nov), Bayer's $7.25bn
Roundup settlement (21 Nov) and the Wildberries CEO exit (21 Nov).
Where an older event is mentioned it is labelled as context only
("a day after...", "since September...").

All art is drawn with PIL (flat editorial illustration, no photos),
so the file is fully reproducible from this script alone.

Usage: python3 build_image.py [out.png]   (default: entry.png)
Output: 1024x1024 JPEG bytes in a file named entry.png, under 1 MiB.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

PAPER = (247, 241, 227)
PAPER2 = (238, 231, 214)
INK = (17, 17, 17)
RED = (176, 30, 36)
NAVY = (22, 35, 63)
GREY = (68, 68, 68)
LGREY = (120, 112, 96)
SKY = (178, 209, 224)
SEA = (140, 185, 210)
SAND = (232, 214, 176)
GREEN = (46, 125, 70)
GOLD = (198, 148, 40)

W, H = 1024, 1024
M = 24
CW = W - 2 * M


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_w):
    size = start
    while size > 9:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 9)


def wrap(draw, text, f, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, f, fill, max_w, lh=None):
    lh = lh or int(f.size * 1.22)
    for ln in wrap(draw, text, f, max_w):
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def headline(draw, x, y, text, size, max_w, path=SERIF_BOLD, fill=INK):
    # Fixed size, natural wrap (never shrink a whole headline to one line).
    f = font(path, size)
    lines = wrap(draw, text, f, max_w)
    while any(draw.textlength(ln, font=f) > max_w for ln in lines) and size > 10:
        size -= 1
        f = font(path, size)
        lines = wrap(draw, text, f, max_w)
    lh = int(f.size * 1.08)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_BOLD, 12)
    draw.text((x, y), text, font=f, fill=color)
    return y + 16


def rule(draw, x, y, w, color=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=color, width=width)
    return y + width + 4


# ---------------------------------------------------------------------------
# Flat editorial illustrations. Each draws inside (x, y, w, h).
# ---------------------------------------------------------------------------

def art_gulf(d, x, y, w, h):
    """Strait of Hormuz at dusk: sea, two tankers, smoke, drone paths."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 42, 68))
    d.ellipse([x + w - 52, y + 8, x + w - 8, y + 52], fill=(240, 200, 110))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=SEA)
    for i in range(5):
        yy = y + h * 0.58 + i * 9
        d.line([(x + 6, yy), (x + w - 6, yy)], fill=(110, 160, 190), width=2)
    # tanker 1
    d.rectangle([x + 14, y + h * 0.42, x + 150, y + h * 0.58], fill=(40, 40, 44))
    d.rectangle([x + 110, y + h * 0.30, x + 138, y + h * 0.42], fill=(200, 200, 200))
    d.rectangle([x + 20, y + h * 0.46, x + 60, y + h * 0.52], fill=RED)
    # smoke from tanker 1 (kept inside the art box)
    for r, a in ((14, 120), (10, 90), (7, 70)):
        d.ellipse([x + 118 - r, y + 6, x + 118 + r, y + 6 + 2 * r],
                  fill=(a, a, a))
    # tanker 2, smaller, listing
    d.polygon([(x + w - 150, y + h * 0.52), (x + w - 30, y + h * 0.47),
               (x + w - 26, y + h * 0.60), (x + w - 146, y + h * 0.60)],
              fill=(70, 60, 50))
    d.rectangle([x + w - 90, y + h * 0.38, x + w - 66, y + h * 0.48],
                fill=(220, 220, 220))
    # dashed drone paths
    for k in range(7):
        px = x + 20 + k * 26
        py = y + 16 + (k % 3) * 8
        d.ellipse([px, py, px + 5, py + 5], fill=(255, 220, 120))
    d.line([(x + 30, y + 20), (x + 120, y + h * 0.30)], fill=(255, 220, 120),
           width=2)


def art_sky(d, x, y, w, h):
    """Night barrage over Ukraine: dark sky, missile arcs, city lights."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 16, 34))
    for (sx, sy, sr) in ((18, 20, 2), (70, 12, 1), (130, 26, 2), (190, 14, 1),
                         (240, 30, 2), (40, 44, 1), (160, 48, 1), (210, 40, 2)):
        d.ellipse([x + sx, y + sy, x + sx + sr * 2, y + sy + sr * 2],
                  fill=(255, 255, 220))
    # missile arcs with glowing heads
    for (x0, x1, ym, col) in ((10, 150, 30, (255, 120, 60)),
                              (60, 230, 46, (255, 180, 80)),
                              (120, 260, 22, (255, 120, 60))):
        pts = []
        for t in range(21):
            px = x + x0 + (x1 - x0) * t / 20.0
            py = y + ym + 42 * (1 - (2 * t / 20.0 - 1) ** 2) * -1 + 70
            pts.append((px, py))
        d.line(pts, fill=col, width=3)
        d.ellipse([x + x1 - 4, y + ym + 28 - 4, x + x1 + 4, y + ym + 28 + 4],
                  fill=(255, 240, 180))
    # city skyline + lights
    base = y + h - 26
    for (bx, bw, bh) in ((0, 34, 26), (36, 26, 40), (64, 40, 22), (106, 24, 34),
                         (132, 36, 18), (170, 28, 30), (200, 30, 22),
                         (232, 34, 26)):
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(30, 34, 52))
    for (lx, ly) in ((8, base - 14), (44, base - 28), (78, base - 10),
                     (116, base - 22), (146, base - 8), (182, base - 18),
                     (212, base - 12), (244, base - 16)):
        d.rectangle([x + lx, y + ly, x + lx + 3, y + ly + 3],
                    fill=(255, 210, 110))


def art_summit(d, x, y, w, h):
    """Shenzhen skyline with three flag bars: US, China, Russia."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    d.ellipse([x + w - 46, y + 10, x + w - 10, y + 46], fill=(240, 200, 110))
    # skyline (heights capped so no building pokes above the art box)
    base = y + h - 18
    for (bx, bw, bh) in ((0, 30, 34), (32, 22, 48), (56, 28, 30), (86, 20, 52),
                         (108, 30, 40), (140, 24, 50), (166, 28, 34),
                         (196, 22, 44), (220, 26, 30)):
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=NAVY)
        for wy in range(base - bh + 8, base - 6, 12):
            d.rectangle([x + bx + 5, wy, x + bx + 9, wy + 5],
                        fill=(255, 220, 120))
    # three flag bars
    fy = y + 12
    d.rectangle([x + 10, fy, x + 74, fy + 10], fill=(178, 34, 52))
    d.rectangle([x + 10, fy + 12, x + 74, fy + 22], fill=(255, 255, 255))
    d.rectangle([x + 10, fy + 24, x + 74, fy + 34], fill=(30, 60, 140))
    d.rectangle([x + 10, fy + 40, x + 74, fy + 50], fill=(222, 41, 16))
    d.rectangle([x + 10, fy + 52, x + 74, fy + 62], fill=(255, 255, 255))
    d.rectangle([x + 10, fy + 64, x + 74, fy + 74], fill=(0, 57, 166))


def art_climate(d, x, y, w, h):
    """Antalya coast: sun, sea, turbine, leaf."""
    d.rectangle([x, y, x + w, y + h], fill=(190, 220, 210))
    d.ellipse([x + 14, y + 10, x + 58, y + 54], fill=(240, 180, 60))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(90, 160, 190))
    for i in range(3):
        yy = y + h * 0.66 + i * 10
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(140, 195, 215), width=2)
    # wind turbine
    tx, ty = x + w - 52, y + h * 0.62
    d.line([(tx, ty), (tx, ty - 52)], fill=(255, 255, 255), width=4)
    for ang in (90, 210, 330):
        import math as _m
        ex = tx + 26 * _m.cos(_m.radians(ang))
        ey = ty - 52 + 26 * _m.sin(_m.radians(ang))
        d.line([(tx, ty - 52), (ex, ey)], fill=(255, 255, 255), width=4)
    # leaf
    d.ellipse([x + 16, y + h * 0.60, x + 66, y + h * 0.92], fill=GREEN)
    d.line([(x + 20, y + h * 0.88), (x + 62, y + h * 0.64)], fill=(20, 80, 40),
           width=2)


def art_americas(d, x, y, w, h):
    """Andes ridge, city below, red cross of a hospital sign."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 176))
    d.polygon([(x, y + h), (x + w * 0.30, y + 18), (x + w * 0.55, y + h)],
              fill=(120, 90, 70))
    d.polygon([(x + w * 0.40, y + h), (x + w * 0.68, y + 8),
               (x + w * 0.95, y + h)], fill=(90, 70, 58))
    d.polygon([(x + w * 0.24, y + 26), (x + w * 0.30, y + 18),
               (x + w * 0.36, y + 26)], fill=(255, 255, 255))
    d.polygon([(x + w * 0.63, y + 16), (x + w * 0.68, y + 8),
               (x + w * 0.73, y + 16)], fill=(255, 255, 255))
    base = y + h - 16
    for (bx, bw, bh) in ((6, 26, 22), (34, 20, 34), (56, 30, 18), (88, 22, 28),
                         (112, 28, 20), (142, 20, 30), (164, 26, 16),
                         (192, 24, 26), (218, 22, 18)):
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(60, 60, 66))
    # hospital cross
    cx, cy = x + w - 40, y + 16
    d.rectangle([cx - 4, cy - 12, cx + 4, cy + 12], fill=RED)
    d.rectangle([cx - 12, cy - 4, cx + 12, cy + 4], fill=RED)


def art_europe(d, x, y, w, h):
    """Border fence and watchtower under a grey northern sky."""
    d.rectangle([x, y, x + w, y + h], fill=(200, 208, 214))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(150, 165, 140))
    # fence posts + wire
    for px in range(8, w, 26):
        d.line([(x + px, y + h * 0.30), (x + px, y + h * 0.62)],
               fill=(70, 70, 70), width=3)
    for wy in (0.34, 0.44, 0.54):
        d.line([(x, y + h * wy), (x + w, y + h * wy)], fill=(70, 70, 70),
               width=2)
    # watchtower
    d.rectangle([x + w - 62, y + 12, x + w - 30, y + 34], fill=NAVY)
    d.line([(x + w - 58, y + 34), (x + w - 58, y + h * 0.62)], fill=NAVY,
           width=4)
    d.line([(x + w - 34, y + 34), (x + w - 34, y + h * 0.62)], fill=NAVY,
           width=4)
    # stars
    for (sx, sy) in ((20, 18), (52, 30), (84, 16), (116, 28), (148, 18)):
        d.ellipse([x + sx, y + sy, x + sx + 5, y + sy + 5], fill=GOLD)


# Dotted world map (stylised, 60 x 17). '#' is land.
MAP_ROWS = [
    "        ######    ####                  ##########################      ",
    "     ############    ###     ########  #############################    ",
    "    ##############    #########################   ##################  ",
    "     ############      #######################     ###############   ",
    "      ##########        ###################         #############    ",
    "       ########          #################            ##########     ",
    "        ######            ###############              ########      ",
    "         ####              #############                 ######       ",
    "          ##                ###########                   ####        ",
    "           #                 #########                     ##         ",
    "                             ########                       #         ",
    "            ##               ######                          ##        ",
    "           ####               ####                         ######     ",
    "          ######              ###                         ########    ",
    "           ####                #                          ######      ",
    "            ##                                            ####       ",
    "             #                                             ##        ",
]

# (fraction x, fraction y, label) - pins on the map.
PINS = [
    (0.62, 0.38, "1 OMAN: tankers hit"),
    (0.52, 0.20, "2 POLAND: missile crash"),
    (0.53, 0.14, "3 ESTONIA: border to shut"),
    (0.55, 0.30, "4 ANTALYA: COP31 deal near"),
    (0.22, 0.62, "5 SAO PAULO: Bolsonaro in ICU"),
    (0.15, 0.32, "6 SINALOA: cartel boss seized"),
    (0.51, 0.55, "7 NIGERIA: boat sinks, 24 dead"),
    (0.68, 0.32, "8 RANCHI: Cyclone Akvan"),
]

NUMBERS = [
    ("400", "drones and 110 missiles fired at Ukraine in one night"),
    ("24", "dead as a boat carrying mourners capsizes in Nigeria"),
    ("15", "militants killed by Pakistani forces in Balochistan"),
    ("14", "flights cancelled at Ranchi as Cyclone Akvan nears"),
    ("10,000", "temporary forest staff to be insured, Prince William announces"),
]

BRIEFS = [
    "Narendra Modi opens the Nitish Setu bridge linking Patna and Vaishali in Bihar.",
    "Japan will train live-fire at Indian facilities for the first time.",
    "Eisenkot invites Netanyahu's Likud to join Israeli coalition talks.",
    "Four Palestinians killed and 14 wounded in Israeli ceasefire violations in Gaza.",
    "Lebanon's President Aoun demands an end to Israeli occupation and Iranian interference.",
    "A Saudi-led coalition shoots down three Houthi missiles aimed at Riyadh.",
    "France marches for a sixth weekend over living costs and public services.",
    "Belgium braces for an air shutdown as a national strike looms on Monday.",
    "Pat Cummins keeps Australia's Test captaincy with unanimous board backing.",
    "India face New Zealand in a windy Wellington Test; Advani wins snooker opener.",
    "US \u2018open to welcoming\u2019 a UN chief from the Western Hemisphere, says Waltz.",
    "South Korea repeats a $75,000 bounty for tip-offs on exam cheating.",
    "Hegseth sets fresh limits on US-Canada defence ties.",
    "Air India extends its Jeddah suspension until 24 November.",
    "India's ICMR completes 100 technology transfers at a health research summit.",
    "Zelenskyy: Putin called him a \u2018murderer\u2019 after Trump called him his friend.",
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 234, 238))
    rows = len(MAP_ROWS)
    cols = len(MAP_ROWS[0])
    cw, ch = w / cols, h / rows
    for r, row in enumerate(MAP_ROWS):
        for c, ch_ in enumerate(row):
            if ch_ == '#':
                d.ellipse([x + c * cw + 1, y + r * ch + 1,
                           x + (c + 1) * cw - 1, y + (r + 1) * ch - 1],
                          fill=NAVY)
    for i, (fx, fy, _label) in enumerate(PINS, 1):
        px, py = x + fx * w, y + fy * h
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((px - 3, py - 6), str(i), font=font(SANS_BOLD, 11),
               fill=(255, 255, 255))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 10], fill=RED)
    y = 18
    f_title = font(SERIF_BLACK, 62)
    d.text((M, y), "THE WORLD", font=f_title, fill=INK)
    f_date = font(SANS_BOLD, 17)
    d.text((W - M - d.textlength("SUNDAY 22 NOVEMBER 2026", font=f_date), y + 6),
           "SUNDAY 22 NOVEMBER 2026", font=f_date, fill=RED)
    f_sub = font(SERIF_ITALIC, 15)
    d.text((W - M - d.textlength("One day \u00b7 35 stories \u00b7 7 regions", font=f_sub),
            y + 30), "One day \u00b7 35 stories \u00b7 7 regions",
           font=f_sub, fill=GREY)
    d.text((M, y + 66), "THE DAILY FRONT PAGE  \u2014  EVERY STORY THAT MATTERED, IN ONE IMAGE",
           font=font(SANS_BOLD, 12), fill=GREY)
    y = 104
    d.line([(M, y), (W - M, y)], fill=INK, width=3)
    y += 10

    # ---- lead row: Gulf + Ukraine --------------------------------------
    lead_y = y
    lead_h = 228
    col1_w = 560
    col2_x = M + col1_w + 16
    col2_w = W - M - col2_x

    # Gulf (left)
    x = M
    y = kicker(d, x, lead_y, "THE GULF  \u00b7  LEAD")
    y = headline(d, x, y, "TANKERS HIT OFF OMAN AS GULF WAR SPREADS", 23,
                 col1_w)
    y += 4
    art_gulf(d, x, y, col1_w, 92)
    y += 98
    y = para(d, x, y,
             "Multiple tankers were hit off the Oman coast as the US-Iran "
             "naval confrontation escalated. Tehran said blasts on Qeshm "
             "Island were American munitions disposal, not a fresh attack. "
             "Bahrain opened an inquiry after a Patriot interceptor crashed, "
             "and US airlines were warned of a possible al-Qaeda-linked "
             "threat before Thanksgiving. Oil fell more than 3% despite "
             "the fighting.",
             font(SANS, 11), INK, col1_w, lh=14)
    # Ukraine (right)
    x = col2_x
    y = kicker(d, x, lead_y, "UKRAINE  \u00b7  LEAD")
    y = headline(d, x, y, "400 DRONES, 110 MISSILES IN WAR'S BIGGEST NIGHT", 23,
                 col2_w)
    y += 4
    art_sky(d, x, y, col2_w, 92)
    y += 98
    y = para(d, x, y,
             "Russia fired about 400 drones and 110 missiles at Ukraine in "
             "one of the war's largest aerial attacks, and a Russian missile "
             "and a drone crashed in Poland. Melania Trump pressed for more "
             "ceasefires before Christmas, and Zelenskyy said the Shenzhen "
             "summit had been \u2018very unsuccessful\u2019 for Russia.",
             font(SANS, 11), INK, col2_w, lh=14)

    y = lead_y + lead_h + 4
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 10

    # ---- second row: four regional features ----------------------------
    feat_y = y
    feat_h = 208
    fw = (CW - 3 * 14) // 4
    feats = [
        ("ASIA-PACIFIC", "TRUMP: IRAN DEAL \u2018COULD LAST 20 YEARS\u2019",
         art_summit,
         "Donald Trump said a deal with Iran could last 20 years and "
         "claimed the US had removed Tehran's leadership twice. He also "
         "called China's nuclear buildup \u2018rapid and concerning\u2019 after "
         "meeting Xi Jinping."),
        ("CLIMATE \u00b7 COP31", "ANTALYA NEARS A FINAL DEAL",
         art_climate,
         "Climate talks in Antalya neared a final deal, the summit "
         "president said, after days deadlocked over fossil fuels. A pledge "
         "on AI drew no backing from major US tech firms."),
        ("THE AMERICAS", "BOLSONARO IN ICU; CARTEL BOSS SEIZED",
         art_americas,
         "Brazil's jailed former president Jair Bolsonaro was admitted to "
         "intensive care with an acute bowel obstruction. In Mexico, troops "
         "arrested cartel leader \u2018El Chapo Isidro\u2019 as 11 people were "
         "killed in Sinaloa violence."),
        ("EUROPE", "ESTONIA TO SHUT ITS RUSSIA BORDER",
         art_europe,
         "Estonia said it would close its border with Russia, which Moscow "
         "denounced as a \u2018new Iron Curtain\u2019. Denmark said Russia "
         "plotted to kill a US-Ukrainian citizen, and France asked the UN "
         "to act on Myanmar's rejection of a court ruling."),
    ]
    for i, (kick, head, art, body) in enumerate(feats):
        x = M + i * (fw + 14)
        yy = kicker(d, x, feat_y, kick)
        yy = headline(d, x, yy, head, 16, fw)
        yy += 4
        art(d, x, yy, fw, 74)
        yy += 80
        para(d, x, yy, body, font(SANS, 11), INK, fw, lh=12)

    y = feat_y + feat_h + 2
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 8

    # ---- world map ------------------------------------------------------
    y = kicker(d, M, y, "WHERE IT HAPPENED  \u00b7  22 NOVEMBER 2026")
    map_y = y
    draw_map(d, M, map_y, CW, 96)
    y = map_y + 96 + 6
    # pin legend, two lines
    f_leg = font(SANS_BOLD, 11)
    line1 = "   ".join(PINS[i][2] for i in range(4))
    line2 = "   ".join(PINS[i][2] for i in range(4, 8))
    d.text((M, y), line1, font=f_leg, fill=INK)
    y += 15
    d.text((M, y), line2, font=f_leg, fill=INK)
    y += 19
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 8

    # ---- by the numbers --------------------------------------------------
    y = kicker(d, M, y, "BY THE NUMBERS")
    bw = (CW - 4 * 10) // 5
    for i, (num, label) in enumerate(NUMBERS):
        x = M + i * (bw + 10)
        d.rectangle([x, y, x + bw, y + 58], fill=PAPER2,
                    outline=LGREY, width=1)
        f_num = fit_font(d, num, SERIF_BLACK, 26, bw - 12)
        d.text((x + 6, y + 4), num, font=f_num, fill=RED)
        para(d, x + 6, y + 30, label, font(SANS, 10), INK, bw - 12, lh=12)
    y += 66
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 8

    # ---- the day in brief ------------------------------------------------
    y = kicker(d, M, y, "THE DAY IN BRIEF")
    col_w = (CW - 20) // 2
    f_br = font(SANS, 11)
    half = (len(BRIEFS) + 1) // 2
    max_y = y
    for col in range(2):
        x = M + col * (col_w + 20)
        yy = y
        for j, item in enumerate(BRIEFS[col * half:(col + 1) * half]):
            n = col * half + j + 1
            d.text((x, yy), "%d." % n, font=font(SANS_BOLD, 11), fill=RED)
            yy = para(d, x + 22, yy, item, f_br, INK, col_w - 22, lh=13)
            yy += 1
        max_y = max(max_y, yy)
    y = max_y + 4
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 6
    d.text((M, y), "All stories first reported on Sunday 22 November 2026. "
           "Sources: Reuters, AP, AFP, BBC, Times of India, Arab News.",
           font=font(SERIF_ITALIC, 11), fill=GREY)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry.png")
    img = build()
    img.save(out, "JPEG", quality=88, optimize=True)
    print(out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
