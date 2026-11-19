"""Paint a one-page newspaper front page for 19 November 2026.

Everything is drawn with Pillow primitives. No photos, no downloads,
no network access and no clock reads, so the same run always yields
the same picture.
"""

import textwrap

import PIL.Image as PImage
import PIL.ImageDraw as PDraw
import PIL.ImageFont as PFont

from pathlib import Path

DIM = (1024, 1024)
MARGIN = 28

TINTS = {
    "navy": (13, 34, 64),
    "navy_soft": (27, 58, 96),
    "cream": (247, 242, 231),
    "sheet": (255, 255, 255),
    "charcoal": (32, 32, 34),
    "slate": (88, 94, 104),
    "amber": (201, 150, 44),
    "amber_soft": (232, 196, 110),
    "brick": (164, 62, 52),
    "teal": (32, 110, 104),
    "mist": (226, 232, 238),
    "sky": (120, 164, 196),
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fetch_font(path, size):
    """Load a truetype face, falling back to Pillow's built-in face."""
    try:
        return PFont.truetype(path, size)
    except Exception:
        return PFont.load_default()


def wrap_lines(canvas, words, face, width):
    """Greedy word wrap measured with the real face metrics."""
    out = []
    current = ""
    for word in words.split():
        trial = word if not current else current + " " + word
        if canvas.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def paint_text_block(canvas, x, y, words, face, fill, width, leading):
    """Paint wrapped lines starting at (x, y); return the next y."""
    for line in wrap_lines(canvas, words, face, width):
        canvas.text((x, y), line, font=face, fill=fill)
        y += leading
    return y


def paint_masthead(canvas):
    """Dark navy banner with the paper name and the date line."""
    canvas.rectangle([0, 0, DIM[0], 168], fill=TINTS["navy"])
    canvas.rectangle([0, 168, DIM[0], 172], fill=TINTS["amber"])
    title_face = fetch_font(SERIF, 62)
    title = "THE WORLD TODAY"
    tw = canvas.textlength(title, font=title_face)
    canvas.text(((DIM[0] - tw) / 2, 26), title, font=title_face,
                fill=TINTS["cream"])
    small = fetch_font(SANS_BOLD, 21)
    date_line = "THURSDAY 19 NOVEMBER 2026  \u2022  WORLD NEWS IN ONE PAGE"
    dw = canvas.textlength(date_line, font=small)
    canvas.text(((DIM[0] - dw) / 2, 108), date_line, font=small,
                fill=TINTS["amber_soft"])
    edge = fetch_font(SANS, 16)
    canvas.text((MARGIN, 132), "DAILY EDITION", font=edge,
                fill=TINTS["mist"])
    right = "No. 323"
    rw = canvas.textlength(right, font=edge)
    canvas.text((DIM[0] - MARGIN - rw, 132), right, font=edge,
                fill=TINTS["mist"])


def paint_hero(canvas):
    """Full-width lead card: the trilateral summit in Shenzhen."""
    x0, y0, x1, y1 = MARGIN, 192, DIM[0] - MARGIN, 448
    canvas.rounded_rectangle([x0, y0, x1, y1], radius=10,
                             fill=TINTS["sheet"], outline=TINTS["navy"],
                             width=2)
    kicker = fetch_font(SANS_BOLD, 19)
    canvas.text((x0 + 24, y0 + 18), "DIPLOMACY  \u2022  SHENZHEN",
                font=kicker, fill=TINTS["brick"])
    head = fetch_font(SERIF, 36)
    y = paint_text_block(canvas, x0 + 24, y0 + 48,
                         "Three nuclear powers meet for the first time",
                         head, TINTS["navy"], 600, 44)
    body = fetch_font(SANS, 19)
    paint_text_block(
        canvas, x0 + 24, y + 8,
        "Trump, Xi and Putin meet on the APEC sidelines in Shenzhen, "
        "with nuclear arsenals and the Iran war on the agenda. "
        "Officials warn against expecting a deal.",
        body, TINTS["charcoal"], 600, 26)
    # Skyline panel on the right: towers plus three meeting circles.
    px0, py0, px1, py1 = 700, y0 + 24, x1 - 24, y1 - 24
    canvas.rounded_rectangle([px0, py0, px1, py1], radius=8,
                             fill=TINTS["navy_soft"])
    towers = [(716, 318, 748, 380), (756, 292, 788, 380),
              (796, 306, 828, 380), (836, 282, 868, 380),
              (876, 314, 908, 380), (916, 298, 948, 380)]
    for bx0, by0, bx1, by1 in towers:
        canvas.rectangle([bx0, by0, bx1, by1], fill=TINTS["sky"])
    canvas.rectangle([px0, 384, px1, 388], fill=TINTS["amber"])
    for i, tint in enumerate((TINTS["brick"], TINTS["amber"],
                              TINTS["sky"])):
        cx = 758 + i * 72
        canvas.ellipse([cx - 26, 238, cx + 26, 290], fill=tint,
                       outline=TINTS["cream"], width=3)
    cap = fetch_font(SANS_BOLD, 15)
    label = "SHENZHEN  \u2022  APEC SIDELINES"
    lw = canvas.textlength(label, font=cap)
    canvas.text(((px0 + px1 - lw) / 2, py1 - 24), label, font=cap,
                fill=TINTS["cream"])


def paint_quad(canvas, box, kicker, tint, headline, body, motif):
    """One of the four smaller cards in the 2x2 grid."""
    x0, y0, x1, y1 = box
    canvas.rounded_rectangle([x0, y0, x1, y1], radius=10,
                             fill=TINTS["sheet"], outline=TINTS["mist"],
                             width=2)
    kick = fetch_font(SANS_BOLD, 17)
    canvas.text((x0 + 20, y0 + 12), kicker, font=kick, fill=tint)
    head = fetch_font(SERIF, 23)
    y = paint_text_block(canvas, x0 + 20, y0 + 38, headline, head,
                         TINTS["charcoal"], x1 - x0 - 110, 28)
    plain = fetch_font(SANS, 16)
    paint_text_block(canvas, x0 + 20, y + 4, body, plain,
                     TINTS["slate"], x1 - x0 - 40, 21)
    motif(canvas, x1, y0)


def motif_stars(canvas, x1, y0):
    """Gold badge with the review score, top-right of the games card."""
    cx, cy = x1 - 48, y0 + 46
    canvas.ellipse([cx - 30, cy - 30, cx + 30, cy + 30],
                   fill=TINTS["amber"])
    num = fetch_font(SANS_BOLD, 24)
    txt = "99"
    tw = canvas.textlength(txt, font=num)
    canvas.text((cx - tw / 2, cy - 14), txt, font=num,
                fill=TINTS["navy"])


def motif_dome(canvas, x1, y0):
    """A small capitol dome, top-right of the politics card."""
    bx, by = x1 - 96, y0 + 22
    canvas.rectangle([bx, by + 34, bx + 80, by + 44],
                     fill=TINTS["navy_soft"])
    canvas.pieslice([bx + 18, by - 6, bx + 62, by + 38], 180, 360,
                    fill=TINTS["navy_soft"])
    canvas.rectangle([bx + 36, by - 18, bx + 44, by - 4],
                     fill=TINTS["navy_soft"])


def motif_radar(canvas, x1, y0):
    """Concentric rings, top-right of the Gulf card."""
    cx, cy = x1 - 48, y0 + 46
    for r in (30, 20, 10):
        canvas.ellipse([cx - r, cy - r, cx + r, cy + r],
                       outline=TINTS["brick"], width=2)
    canvas.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=TINTS["brick"])


def motif_euro(canvas, x1, y0):
    """Ring of dots with the loan figure beneath, top-right of the EU card."""
    import math
    cx, cy = x1 - 48, y0 + 42
    for k in range(8):
        ang = k * math.pi / 4
        dx = cx + 24 * math.cos(ang)
        dy = cy + 24 * math.sin(ang)
        canvas.ellipse([dx - 4, dy - 4, dx + 4, dy + 4],
                       fill=TINTS["amber"])
    num = fetch_font(SANS_BOLD, 18)
    txt = "\u20ac45bn"
    tw = canvas.textlength(txt, font=num)
    canvas.text((cx - tw / 2, cy + 34), txt, font=num, fill=TINTS["navy"])


def paint_grid(canvas):
    """Four cards: GTA VI, Jeffries, the Gulf, and the EU loan."""
    left, right = MARGIN, DIM[0] - MARGIN
    mid = (left + right) // 2
    top, gap, row_h = 468, 16, 150
    boxes = [
        (left, top, mid - 10, top + row_h),
        (mid + 10, top, right, top + row_h),
        (left, top + row_h + gap, mid - 10, top + 2 * row_h + gap),
        (mid + 10, top + row_h + gap, right, top + 2 * row_h + gap),
    ]
    paint_quad(canvas, boxes[0], "CULTURE  \u2022  GAMING",
               TINTS["teal"],
               "GTA VI arrives after 13 years \u2014 and critics love it",
               "A worldwide launch, a 99 on Metacritic, and analysts "
               "projecting $3.2bn in sales by year-end.",
               motif_stars)
    paint_quad(canvas, boxes[1], "POLITICS  \u2022  UNITED STATES",
               TINTS["navy_soft"],
               "Jeffries wins the nomination to lead the House",
               "Democrats back him 251\u201311 in a secret ballot, on course "
               "to be the first Black Speaker.",
               motif_dome)
    paint_quad(canvas, boxes[2], "WAR  \u2022  THE GULF",
               TINTS["brick"],
               "Gulf bases come under fire as strikes escalate",
               "Iranian drones hit Ali Al-Salem in Kuwait after US jets "
               "struck an IRGC missile site on Qeshm Island.",
               motif_radar)
    paint_quad(canvas, boxes[3], "EUROPE  \u2022  UKRAINE",
               TINTS["amber"],
               "EU lines up a \u20ac45bn loan to keep Ukraine funded",
               "\u20ac25bn for the military and \u20ac20bn for the budget, "
               "covering two-thirds of Kyiv\u2019s \u20ac70bn gap.",
               motif_euro)


def paint_strip(canvas):
    """Full-width numbers strip: the Pew projection to 2035."""
    x0, y0, x1, y1 = MARGIN, 800, DIM[0] - MARGIN, 996
    canvas.rounded_rectangle([x0, y0, x1, y1], radius=10,
                             fill=TINTS["navy"])
    year = fetch_font(SERIF, 74)
    canvas.text((x0 + 28, y0 + 22), "2035", font=year,
                fill=TINTS["amber"])
    cap = fetch_font(SANS_BOLD, 18)
    paint_text_block(canvas, x0 + 28, y0 + 112,
                     "THE YEAR ISLAM BECOMES THE WORLD\u2019S LARGEST FAITH",
                     cap, TINTS["cream"], 260, 24)
    bx = x0 + 330
    bw_max = 600
    rows = [
        ("Muslims", "2.57bn", 2.57, TINTS["amber"]),
        ("Christians", "2.52bn", 2.52, TINTS["sky"]),
    ]
    lab = fetch_font(SANS_BOLD, 18)
    val = fetch_font(SANS_BOLD, 18)
    y = y0 + 30
    for name, figure, share, tint in rows:
        canvas.text((bx, y), name, font=lab, fill=TINTS["cream"])
        fw = canvas.textlength(figure, font=val)
        canvas.text((x1 - 28 - fw, y), figure, font=val,
                    fill=TINTS["cream"])
        bar_w = int(bw_max * share / 2.57)
        canvas.rectangle([bx, y + 30, bx + bw_max, y + 52],
                         fill=TINTS["navy_soft"])
        canvas.rectangle([bx, y + 30, bx + bar_w, y + 52], fill=tint)
        y += 78
    src = fetch_font(SANS, 15)
    canvas.text((bx, y1 - 30), "Source: Pew Research Center \u2022 "
                "driven by higher birth rates", font=src,
                fill=TINTS["mist"])


def compose_poster():
    """Assemble every section onto one 1024x1024 page."""
    sheet = PImage.new("RGB", DIM, TINTS["cream"])
    canvas = PDraw.Draw(sheet)
    paint_masthead(canvas)
    paint_hero(canvas)
    paint_grid(canvas)
    paint_strip(canvas)
    return sheet


def render_to(path):
    """Render the poster and save it to the given path."""
    compose_poster().save(path, format="PNG")


render_to(Path(__file__).resolve().parent / "entry.png")
