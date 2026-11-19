"""Render a one-page news poster: six stories from 19 November 2026.

Everything here is drawn with Pillow primitives -- no downloaded assets,
no network access, no timestamps. The same input always produces the
same PNG bytes, because every coordinate, colour and string is fixed.

Layout: a masthead, one full-width hero story, a 2x2 grid of stories,
and a full-width numbers strip, then a sources footer.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass, field

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024

PAPER = (243, 238, 228)
INK = (15, 26, 44)
GOLD = (198, 148, 52)
CARD = (255, 255, 255)
CARD_EDGE = (204, 195, 178)
MUTED = (108, 103, 93)
BODY = (48, 48, 44)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


@dataclass
class Story:
    """One news item: its label, headline, short summary and palette."""

    tag: str
    headline: str
    summary: str
    accent: tuple
    painter: str


@dataclass
class Poster:
    """Holds the canvas plus the typefaces and paints the whole page."""

    stories: list = field(default_factory=list)
    sheet: Image.Image = None
    pen: ImageDraw.ImageDraw = None

    def __post_init__(self):
        self.sheet = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
        self.pen = ImageDraw.Draw(self.sheet)

    # -- type helpers -------------------------------------------------
    def face(self, name, size):
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

    def split_lines(self, text, font, width):
        """Greedy word wrap measured with the real font."""
        words = text.split()
        lines, current = [], ""
        for word in words:
            trial = f"{current} {word}".strip()
            if self.pen.textlength(trial, font=font) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def block(self, lines, font, x, y, fill, leading, max_lines=None):
        if max_lines is not None:
            lines = lines[:max_lines]
        for line in lines:
            self.pen.text((x, y), line, font=font, fill=fill)
            y += leading
        return y

    # -- page furniture ----------------------------------------------
    def masthead(self):
        self.pen.rectangle([0, 0, CANVAS_W, 108], fill=INK)
        date_font = self.face("DejaVuSerif-Bold.ttf", 42)
        date = "THURSDAY 19 NOVEMBER 2026"
        tw = self.pen.textlength(date, font=date_font)
        self.pen.text(((CANVAS_W - tw) / 2, 14), date, font=date_font, fill=(250, 248, 242))
        sub_font = self.face("DejaVuSans-Bold.ttf", 16)
        sub = "S I X   S T O R I E S   ·   O N E   P A G E   ·   T H E   W O R L D   T O D A Y"
        sw = self.pen.textlength(sub, font=sub_font)
        self.pen.text(((CANVAS_W - sw) / 2, 70), sub, font=sub_font, fill=GOLD)
        self.pen.rectangle([0, 108, CANVAS_W, 112], fill=(178, 52, 44))

    def footer(self):
        font = self.face("DejaVuSans.ttf", 15)
        note = "Sources: Reuters · AP · AFP · Al Jazeera · CNA · The Hindu · Pew Research Center"
        nw = self.pen.textlength(note, font=font)
        self.pen.text(((CANVAS_W - nw) / 2, 962), note, font=font, fill=MUTED)
        note2 = "Events of Thursday 19 November 2026, as reported that day"
        nw2 = self.pen.textlength(note2, font=font)
        self.pen.text(((CANVAS_W - nw2) / 2, 984), note2, font=font, fill=MUTED)

    # -- hero story ----------------------------------------------------
    def hero(self, story):
        x0, y0, x1, y1 = 20, 122, 1004, 320
        self.pen.rounded_rectangle([x0, y0, x1, y1], radius=10,
                                   fill=CARD, outline=CARD_EDGE, width=2)
        self.pen.rectangle([x0, y0 + 8, x0 + 7, y1 - 8], fill=story.accent)
        px, py, pw, ph = x0 + 14, y0 + 12, 236, y1 - y0 - 24
        getattr(self, story.painter)(px, py, pw, ph)
        tx = x0 + 264
        tw = x1 - tx - 16
        tag_font = self.face("DejaVuSans-Bold.ttf", 15)
        self.pen.text((tx, y0 + 16), story.tag, font=tag_font, fill=story.accent)
        head_font = self.face("DejaVuSans-Bold.ttf", 30)
        y = self.block(self.split_lines(story.headline, head_font, tw),
                       head_font, tx, y0 + 44, INK, 36, max_lines=2)
        body_font = self.face("DejaVuSans.ttf", 16)
        self.block(self.split_lines(story.summary, body_font, tw),
                   body_font, tx, y + 10, BODY, 21, max_lines=3)

    # -- one grid story card -------------------------------------------
    def card(self, story, cx, cy, cw, ch):
        self.pen.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10,
                                   fill=CARD, outline=CARD_EDGE, width=2)
        self.pen.rectangle([cx, cy + 8, cx + 7, cy + ch - 8], fill=story.accent)
        px, py, pw, ph = cx + 14, cy + 12, 148, ch - 24
        getattr(self, story.painter)(px, py, pw, ph)
        tx = cx + 174
        tw = cw - 174 - 12
        tag_font = self.face("DejaVuSans-Bold.ttf", 13)
        self.pen.text((tx, cy + 14), story.tag, font=tag_font, fill=story.accent)
        head_font = self.face("DejaVuSans-Bold.ttf", 23)
        y = self.block(self.split_lines(story.headline, head_font, tw),
                       head_font, tx, cy + 38, INK, 27, max_lines=3)
        body_font = self.face("DejaVuSans.ttf", 15)
        self.block(self.split_lines(story.summary, body_font, tw),
                   body_font, tx, y + 6, BODY, 19, max_lines=3)

    # -- numbers strip --------------------------------------------------
    def numbers_strip(self):
        x0, y0, x1, y1 = 20, 760, 1004, 948
        accent = (30, 58, 110)
        self.pen.rounded_rectangle([x0, y0, x1, y1], radius=10,
                                   fill=(232, 236, 244), outline=CARD_EDGE, width=2)
        self.pen.rectangle([x0, y0 + 8, x0 + 7, y1 - 8], fill=accent)
        tx = x0 + 22
        tag_font = self.face("DejaVuSans-Bold.ttf", 14)
        self.pen.text((tx, y0 + 14), "RELIGION · WORLD", font=tag_font, fill=accent)
        head_font = self.face("DejaVuSans-Bold.ttf", 26)
        self.pen.text((tx, y0 + 40),
                      "ISLAM SET TO BECOME THE WORLD'S LARGEST RELIGION BY 2035",
                      font=head_font, fill=INK)
        body_font = self.face("DejaVuSans.ttf", 15)
        body = ("Pew Research projects 2.57bn Muslims vs 2.52bn Christians by 2035, driven by "
                "higher birth rates — 3.1 children per woman vs 2.5. The US is projected to stop "
                "being majority Christian.")
        self.block(self.split_lines(body, body_font, x1 - tx - 16),
                   body_font, tx, y0 + 76, BODY, 19, max_lines=2)
        # Two bars: projected populations in 2035 (billions).
        bar_x, bar_y = tx, y0 + 122
        bar_w, bar_h = 560, 18
        label_font = self.face("DejaVuSans-Bold.ttf", 14)
        self.pen.text((bar_x, bar_y), "Muslims", font=label_font, fill=INK)
        self.pen.rounded_rectangle([bar_x + 110, bar_y, bar_x + 110 + bar_w, bar_y + bar_h],
                                   radius=4, fill=(24, 110, 78))
        self.pen.text((bar_x + 110 + bar_w + 10, bar_y), "2.57bn",
                      font=label_font, fill=(24, 110, 78))
        bar_y += 28
        self.pen.text((bar_x, bar_y), "Christians", font=label_font, fill=INK)
        self.pen.rounded_rectangle([bar_x + 110, bar_y, bar_x + 110 + 548, bar_y + bar_h],
                                   radius=4, fill=(38, 84, 160))
        self.pen.text((bar_x + 110 + 548 + 10, bar_y), "2.52bn",
                      font=label_font, fill=(38, 84, 160))
        # Big "2035" on the right of the strip.
        big_font = self.face("DejaVuSerif-Bold.ttf", 64)
        self.pen.text((x1 - 190, y0 + 96), "2035", font=big_font, fill=(198, 148, 52))

    # -- illustration panels -------------------------------------------
    def paint_summit(self, x, y, w, h):
        # Shenzhen dusk: three towers, three flags, a round table.
        self.pen.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(28, 44, 78))
        self.pen.ellipse([x + w - 52, y + 14, x + w - 16, y + 50], fill=(245, 214, 130))
        for tx, th, twd in [(x + 14, 96, 30), (x + 52, 128, 34), (x + 94, 78, 28),
                            (x + 130, 110, 30), (x + 168, 84, 28), (x + 202, 64, 22)]:
            self.pen.rectangle([tx, y + h - th, tx + twd, y + h], fill=(16, 28, 52))
            for wy in range(y + h - th + 10, y + h - 8, 14):
                self.pen.rectangle([tx + 5, wy, tx + twd - 5, wy + 5], fill=(240, 200, 90))
        self.pen.rectangle([x, y + h - 22, x + w, y + h], fill=(12, 20, 40))
        # Three flags on poles above a table.
        for fx, colours in [(x + 34, [(178, 52, 44), (255, 255, 255), (178, 52, 44)]),
                            (x + w // 2 - 20, [(178, 52, 44), (255, 255, 255)]),
                            (x + w - 74, [(255, 255, 255), (38, 84, 160), (178, 52, 44)])]:
            self.pen.rectangle([fx + 18, y + 12, fx + 21, y + 62], fill=(200, 200, 200))
            for i, c in enumerate(colours):
                self.pen.rectangle([fx + 21, y + 14 + i * 9, fx + 52, y + 23 + i * 9], fill=c)
        self.pen.ellipse([x + w // 2 - 62, y + h - 66, x + w // 2 + 62, y + h - 34],
                         fill=(120, 88, 50))
        self.pen.ellipse([x + w // 2 - 62, y + h - 66, x + w // 2 + 62, y + h - 50],
                         fill=(168, 128, 74))
        for sx in (x + w // 2 - 52, x + w // 2 - 6, x + w // 2 + 40):
            self.pen.ellipse([sx, y + h - 84, sx + 14, y + h - 70], fill=(240, 220, 180))

    def paint_game(self, x, y, w, h):
        # Neon Vice City sunset: gradient sky, sun, skyline, palms.
        for i in range(h):
            t = i / max(h - 1, 1)
            r = int(245 - 120 * t)
            g = int(120 + 40 * t)
            b = int(160 - 60 * t)
            self.pen.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
        self.pen.ellipse([x + w // 2 - 34, y + 18, x + w // 2 + 34, y + 86],
                         fill=(255, 214, 120))
        self.pen.rectangle([x, y + 118, x + w, y + h], fill=(24, 16, 44))
        for bx, bh, bw in [(x + 6, 52, 26), (x + 38, 74, 30), (x + 74, 44, 24),
                           (x + 104, 66, 28)]:
            self.pen.rectangle([bx, y + 118 - bh + 44, bx + bw, y + h - 30], fill=(12, 8, 28))
            for wy in range(y + 118 - bh + 52, y + h - 38, 12):
                self.pen.rectangle([bx + 4, wy, bx + bw - 4, wy + 4], fill=(255, 110, 190))
        self.pen.rectangle([x, y + h - 30, x + w, y + h], fill=(10, 40, 60))
        self.pen.line([(x, y + h - 30), (x + w, y + h - 30)], fill=(0, 220, 220), width=2)
        # Palm silhouettes.
        for px in (x + 12, x + w - 26):
            self.pen.line([(px + 8, y + h - 30), (px + 8, y + h - 78)], fill=(8, 30, 20), width=4)
            for ang in (-50, -20, 10, 40):
                ex = px + 8 + int(22 * math.cos(math.radians(ang - 90)))
                ey = y + h - 78 + int(22 * math.sin(math.radians(ang - 90)))
                self.pen.line([(px + 8, y + h - 78), (ex, ey)], fill=(8, 30, 20), width=3)
        # "VI" badge.
        vi_font = self.face("DejaVuSerif-Bold.ttf", 34)
        self.pen.text((x + w - 62, y + 8), "VI", font=vi_font, fill=(255, 255, 255))

    def paint_capitol(self, x, y, w, h):
        self.pen.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(214, 230, 244))
        self.pen.ellipse([x + 16, y + 14, x + 44, y + 42], fill=(245, 214, 130))
        self.pen.rectangle([x, y + 148, x + w, y + h], fill=(46, 110, 66))
        self.pen.ellipse([x + w // 2 - 26, y + 46, x + w // 2 + 26, y + 96], fill=(250, 250, 246))
        self.pen.rectangle([x + w // 2 - 34, y + 88, x + w // 2 + 34, y + 100],
                           fill=(232, 230, 224))
        self.pen.rectangle([x + w // 2 - 52, y + 100, x + w // 2 + 52, y + 148],
                           fill=(240, 238, 232))
        for i in range(5):
            colx = x + w // 2 - 44 + i * 18
            self.pen.rectangle([colx, y + 108, colx + 8, y + 140], fill=(200, 198, 190))
        self.pen.rectangle([x + w // 2 - 58, y + 140, x + w // 2 + 58, y + 148],
                           fill=(210, 208, 200))
        self.pen.rectangle([x + w // 2 - 2, y + 30, x + w // 2 + 2, y + 48], fill=(120, 120, 118))
        self.pen.polygon([(x + w // 2 + 2, y + 30), (x + w // 2 + 26, y + 36),
                          (x + w // 2 + 2, y + 42)], fill=(178, 52, 44))
        self.pen.rectangle([x + 12, y + 100, x + 34, y + 148], fill=(226, 224, 216))
        self.pen.rectangle([x + w - 34, y + 100, x + w - 12, y + 148], fill=(226, 224, 216))

    def paint_gulf(self, x, y, w, h):
        self.pen.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(10, 22, 44))
        for sx, sy in [(x + 20, y + 18), (x + 60, y + 34), (x + 110, y + 14),
                       (x + 132, y + 44), (x + 36, y + 52)]:
            self.pen.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
        self.pen.ellipse([x + w - 44, y + 12, x + w - 14, y + 42], fill=(240, 236, 220))
        # Radar sweep.
        cx, cy = x + w // 2, y + h - 52
        for r in (18, 30, 42):
            self.pen.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 200, 120), width=2)
        self.pen.line([cx, cy, cx + 34, cy - 24], fill=(0, 220, 140), width=3)
        self.pen.line([cx, cy, cx - 24, cy - 14], fill=(0, 160, 100), width=2)
        # Drones with trails.
        for dx, dy in [(x + 26, y + 66), (x + w - 40, y + 84), (x + w // 2 + 18, y + 44)]:
            self.pen.line([(dx - 26, dy + 8), (dx, dy)], fill=(255, 120, 60), width=2)
            self.pen.polygon([(dx, dy - 6), (dx + 12, dy), (dx, dy + 6), (dx - 4, dy)],
                             fill=(255, 180, 80))
        self.pen.rectangle([x, y + h - 26, x + w, y + h], fill=(8, 40, 66))
        for wx in range(x + 6, x + w - 6, 22):
            self.pen.arc([wx, y + h - 22, wx + 18, y + h - 8], 0, 180, fill=(0, 150, 180), width=2)

    def paint_euro(self, x, y, w, h):
        self.pen.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(16, 38, 92))
        cx, cy = x + w // 2, y + h // 2 - 6
        for k in range(12):
            ang = -math.pi / 2 + k * math.pi / 6
            sx = cx + int(58 * math.cos(ang))
            sy = cy + int(58 * math.sin(ang))
            self.pen.polygon([(sx, sy - 6), (sx + 2, sy - 1), (sx + 6, sy),
                              (sx + 2, sy + 2), (sx + 1, sy + 6), (sx - 1, sy + 2),
                              (sx - 6, sy), (sx - 2, sy - 1)], fill=(255, 214, 80))
        euro_font = self.face("DejaVuSerif-Bold.ttf", 58)
        self.pen.text((cx - 20, cy - 30), "€", font=euro_font, fill=(255, 255, 255))
        self.pen.rounded_rectangle([x + 10, y + h - 34, x + w - 10, y + h - 10], radius=5,
                                   fill=(255, 214, 80))
        self.pen.text((x + 22, y + h - 30), "€45bn for 2027",
                      font=self.face("DejaVuSans-Bold.ttf", 14), fill=(16, 38, 92))

    # -- assemble ------------------------------------------------------
    def compose(self):
        self.masthead()
        self.hero(self.stories[0])
        left, top = 20, 332
        cw = (CANVAS_W - 2 * left - 12) // 2
        ch = 200
        for idx, story in enumerate(self.stories[1:5]):
            row, col = divmod(idx, 2)
            self.card(story, left + col * (cw + 12), top + row * (ch + 12), cw, ch)
        self.numbers_strip()
        self.footer()
        return self.sheet


def build_poster():
    items = [
        Story("DIPLOMACY · SHENZHEN, CHINA",
              "TRUMP, XI AND PUTIN SIT DOWN TOGETHER — A FIRST",
              "The leaders of the US, China and Russia meet in Shenzhen on the "
              "sidelines of APEC — the first trilateral of the three nuclear "
              "powers. Nuclear arms and the war in Iran top the agenda; "
              "officials expect symbolism, not a deal.",
              (30, 58, 110), "paint_summit"),
        Story("CULTURE · GAMING",
              "GTA VI IS OUT — CRITICS CALL IT A MASTERPIECE",
              "Rockstar's epic is out worldwide after 13 years. Metacritic: "
              "99/100; $3.2bn sales seen by year-end.",
              (178, 52, 120), "paint_game"),
        Story("POLITICS · UNITED STATES",
              "JEFFRIES NOMINATED TO BE FIRST BLACK SPEAKER",
              "Democrats pick Hakeem Jeffries 251–11 after their midterm sweep. "
              "The full House votes on 3 January.",
              (38, 84, 160), "paint_capitol"),
        Story("WAR · THE GULF",
              "IRAN HITS US BASES IN KUWAIT AND BAHRAIN",
              "Iran's drones hit US facilities at Ali Al-Salem base after US "
              "jets hit an IRGC site on Qeshm Island.",
              (150, 44, 38), "paint_gulf"),
        Story("EUROPE · UKRAINE",
              "EU LENDS UKRAINE €45BN — RUSSIA TO REPAY",
              "€45bn for 2027 — €25bn military, €20bn budget — covers "
              "two-thirds of Kyiv's €70bn gap.",
              (24, 110, 78), "paint_euro"),
    ]
    return Poster(stories=items).compose()


def save_poster(path):
    build_poster().save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    import sys
    save_poster(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
