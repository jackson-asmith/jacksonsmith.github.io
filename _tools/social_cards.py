"""Render 1200x630 social preview cards for jacksonasmith.com.

Usage:
    python3 -m pip install pillow
    INTER_DIR=/path/to/Inter-4.1/extras/ttf python3 _tools/social_cards.py .

Inter (SIL Open Font License) comes from https://github.com/rsms/inter/releases.
Cards are written to assets/img/social/. To add one for a new case study,
add a card(...) line at the bottom and set `image:` in the page's front matter.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

SITE = sys.argv[1]
OUT = os.path.join(SITE, "assets", "img", "social")
FONTS = os.environ["INTER_DIR"]

W, H = 1200, 630
PAD = 80
BG = "#ffffff"
INK = "#24292e"      # Primer text
MUTED = "#586069"    # Primer secondary text
ACCENT = "#0366d6"   # Primer link blue


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def fit(draw, text, max_lines, width, sizes):
    """Largest size from `sizes` at which `text` wraps into max_lines."""
    for size in sizes:
        fnt = font("InterDisplay-Bold.ttf", size)
        lines = wrap(draw, text, fnt, width)
        if len(lines) <= max_lines:
            return fnt, lines
    raise ValueError(f"title too long: {text}")


def avatar(size):
    img = Image.open(os.path.join(SITE, "assets", "img", "avatar-240.webp")).convert("RGB")
    img = img.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * 4, size * 4), fill=255)
    return img, mask.resize((size, size), Image.LANCZOS)


def card(path, eyebrow, title, subtitle=None):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 16, H), fill=ACCENT)

    text_w = W - 2 * PAD
    y = PAD
    d.text((PAD, y), eyebrow.upper(), font=font("Inter-SemiBold.ttf", 26), fill=ACCENT)
    y += 62

    tfont, lines = fit(d, title, 3, text_w, range(76, 40, -2))
    line_h = int(tfont.size * 1.18)
    for line in lines:
        d.text((PAD, y), line, font=tfont, fill=INK)
        y += line_h

    if subtitle:
        y += 18
        sfont = font("Inter-Regular.ttf", 32)
        for line in wrap(d, subtitle, sfont, text_w)[:2]:
            d.text((PAD, y), line, font=sfont, fill=MUTED)
            y += 44

    # Footer: avatar, name, domain
    size = 72
    face, mask = avatar(size)
    fy = H - PAD - size
    img.paste(face, (PAD, fy), mask)
    d.text((PAD + size + 22, fy + 6), "Jackson Smith", font=font("Inter-SemiBold.ttf", 30), fill=INK)
    d.text((PAD + size + 22, fy + 42), "jacksonasmith.com", font=font("Inter-Regular.ttf", 24), fill=MUTED)

    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, path), optimize=True)
    print(path, os.path.getsize(os.path.join(OUT, path)) // 1024, "KB")


card("default.png", "Software engineer",
     "Reliable automation, testable code, and systems that don’t page someone at 3am",
     None)
card("principles.png", "Engineering principles",
     "How I approach engineering",
     "Six principles from a decade of running production systems, and where each one shows up in real work.")
card("gh-baseline.png", "Case study",
     "gh-baseline: the required checks that accepted any source")
card("keel.png", "Case study",
     "Keel: the retry that could send one alert four times")
card("email-alignment-checker.png", "Case study",
     "Email alignment checker: quiet, honest, and self-sustaining DNS monitoring")
card("site-performance.png", "Case study",
     "Making this site faster on mobile")
