#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026.

A single deterministic render: fixed text, fixed fonts, fixed layout, so
running it twice produces byte-identical PNG output. Pillow only.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# Palette: warm newsprint, ink black, one red accent for the date/kickers.
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (96, 90, 82)
RULE = (60, 58, 52)
BOX = (238, 231, 216)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font, not char counts."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, fnt, max_w, leading):
    """Draw a wrapped headline in upper case; return y below it."""
    return para(draw, x, y, text.upper(), fnt, max_w, leading)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Double-ruled frame around the whole page.
    d.rectangle([14, 14, W - 15, H - 15], outline=RULE, width=2)
    d.rectangle([22, 22, W - 23, H - 23], outline=RULE, width=1)

    mx = 44                      # left margin of the text block
    cw = W - 2 * mx              # content width

    # ---- Masthead -------------------------------------------------------
    mast = font(SERIF_B, 66)
    name = "THE DAILY WORLD"
    d.text(((W - d.textlength(name, font=mast)) / 2, 34), name,
           font=mast, fill=INK)
    d.line([mx, 114, W - mx, 114], fill=RULE, width=2)

    date_f = font(SANS_B, 28)
    date = "MONDAY, 23 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=date_f)) / 2, 124), date,
           font=date_f, fill=RED)
    sub_f = font(SANS, 17)
    sub = "THE WORLD'S NEWS IN ONE IMAGE"
    d.text(((W - d.textlength(sub, font=sub_f)) / 2, 160), sub,
           font=sub_f, fill=GREY)
    d.line([mx, 188, W - mx, 188], fill=RULE, width=3)

    # ---- Lead story -----------------------------------------------------
    y = 202
    kick_f = font(SANS_B, 20)
    d.text((mx, y), "NATO WARNING", font=kick_f, fill=RED)
    y += 30
    y = headline(d, mx, y, "Russia 'ready to launch nuclear satellite'",
                 font(SERIF_B, 38), cw, 43)
    y += 6
    y = para(d, mx, y,
             "German media cite NATO intelligence: a nuclear-armed satellite, "
             "Sputnik-S, could go into orbit within weeks — possibly in "
             "December.",
             font(SERIF, 21), cw, 26)
    y = para(d, mx, y,
             "Western services say the satellite is built and stored near "
             "Moscow; a blast in orbit could knock out a third of low-orbit "
             "satellites, US Space Command warns. Russia calls it propaganda.",
             font(SANS, 19), cw, 24)
    y += 8
    d.line([mx, y, W - mx, y], fill=RULE, width=2)
    y += 10

    # ---- Secondary stories, two rows of two columns --------------------
    col_w = (cw - 28) // 2
    x2 = mx + col_w + 28

    def story(x, top, kicker, head, body):
        yy = top
        d.text((x, yy), kicker, font=kick_f, fill=RED)
        yy += 24
        yy = headline(d, x, yy, head, font(SERIF_B, 22), col_w, 24)
        yy += 4
        yy = para(d, x, yy, body, font(SANS, 17), col_w, 20)
        return yy

    row1 = story(mx, y, "UKRAINE · LIBYA",
                 "Zelenskyy: Ukraine sank Russian warship off Libya",
                 "Seven sea drones sank the corvette Merkury in Benghazi "
                 "port and hit the cargo ship MV Angara, Kyiv said Monday.")
    row1 = max(row1, story(x2, y, "CLIMATE",
                           "COP31 fallout: Bowen told to quit as Pacific despairs",
                           "Blame erupted Monday: Australia's opposition "
                           "demanded minister Chris Bowen resign; island "
                           "nations voiced despair."))
    d.line([mx, row1 + 8, W - mx, row1 + 8], fill=RULE, width=1)

    row2 = story(mx, row1 + 18, "GULF",
                 "Bahrain intercepts Iranian attacks; US hits tanker",
                 "Bahrain said it stopped Iranian attacks as Tehran massed "
                 "14 tankers to test the US blockade.")
    row2 = max(row2, story(x2, row1 + 18, "UKRAINE",
                           "Kyiv toll rises to 15 as rescuers dig on",
                           "The toll from Sunday's drone strike on a Dymer "
                           "apartment block rose through Monday; the region "
                           "declared a day of mourning."))
    d.line([mx, row2 + 8, W - mx, row2 + 8], fill=RULE, width=2)

    # ---- The day in brief ----------------------------------------------
    briefs = [
        "Democrats clinch 258-seat House majority — biggest since 1992",
        "Iran claims 78 US drones downed over the Gulf",
        "Houthis claim Saudi refinery hit; Saudi strike kills 4 in Hodeida",
        "Nepal PM Balen Shah welcomed in Delhi; meets Modi",
        "India holds 3rd place in Lowy Asia Power Index",
        "France protests ebb as 70,000 police deploy",
        "Indonesia factory fire: more remains found; 34 still missing",
        "WHO: fighting near Congo Ebola zone disrupts response",
    ]
    bf = font(SANS, 16)
    # Measure the briefs first so the box fits its content exactly.
    brief_lines = []
    for item in briefs:
        brief_lines.append(wrap(d, item, bf, cw - 54))
    box_h = 42 + sum(len(ls) * 19 + 1 for ls in brief_lines) + 4
    by = row2 + 14
    d.rectangle([mx, by, W - mx, by + box_h], fill=BOX, outline=RULE, width=1)
    d.text((mx + 16, by + 10), "THE DAY IN BRIEF", font=kick_f, fill=INK)
    d.line([mx + 16, by + 40, W - mx - 16, by + 40], fill=RULE, width=1)

    yy = by + 42
    for ls in brief_lines:
        d.text((mx + 16, yy), "•", font=bf, fill=RED)
        for line in ls:
            d.text((mx + 38, yy), line, font=bf, fill=INK)
            yy += 19
        yy += 1

    # ---- Footer ----------------------------------------------------------
    foot = font(SANS, 15)
    note = "Sources: Reuters, AP, Al Jazeera, CNN, NHK, The Daily Star"
    fy = by + box_h + 8
    d.text(((W - d.textlength(note, font=foot)) / 2, fy), note,
           font=foot, fill=GREY)

    img.save("entry.png", format="PNG")


if __name__ == "__main__":
    main()
