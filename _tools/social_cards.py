"""Render 1200x630 social preview cards for jacksonasmith.com.

Usage:
    python3 -m pip install pillow
    INTER_DIR=/path/to/Inter-4.1/extras/ttf python3 _tools/social_cards.py .

Inter (SIL Open Font License) comes from https://github.com/rsms/inter/releases.
Cards are written to assets/img/social/. To add one for a new case study,
add a card(...) line at the bottom and set `image:` in the page's front matter.
The LinkedIn profile background (linkedin-banner.png, 1584x396) comes from banner(...);
it isn't referenced by the site. Upload it on LinkedIn by hand after regenerating.
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


def banner(path, eyebrow, title, url):
    """1584x396 LinkedIn background. The profile photo covers the left side
    (bottom-left on desktop, left-center on mobile), so text sits right-aligned
    in the right ~60%."""
    bw, bh, pad = 1584, 396, 72
    img = Image.new("RGB", (bw, bh), BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, bh - 12, bw, bh), fill=ACCENT)

    right = bw - pad
    efont = font("Inter-SemiBold.ttf", 24)
    tfont = font("InterDisplay-Bold.ttf", 54)
    ufont = font("Inter-SemiBold.ttf", 30)
    # Pass an explicit "\n" to control line breaks; otherwise wrap to width.
    lines = title.split("\n") if "\n" in title else wrap(d, title, tfont, int(bw * 0.55))
    line_h = int(tfont.size * 1.18)
    block = 24 + 26 + len(lines) * line_h + 22 + 30
    y = (bh - 12 - block) // 2

    def right_text(text, fnt, fill, y):
        d.text((right - d.textlength(text, font=fnt), y), text, font=fnt, fill=fill)

    right_text(eyebrow.upper(), efont, ACCENT, y)
    y += 24 + 26
    for line in lines:
        right_text(line, tfont, INK, y)
        y += line_h
    right_text(url, ufont, MUTED, y + 22)

    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, path), optimize=True)
    print(path, os.path.getsize(os.path.join(OUT, path)) // 1024, "KB")


banner("linkedin-banner.png", "Platform & reliability engineering",
       "Building systems that\nhold up in production",
       "jacksonasmith.com")
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
card("post-testing-automation.png", "Writing",
     "Testing automation you didn’t write",
     "Adding Pester tests to an existing PowerShell script before touching a single line of logic.")
card("post-graph-sendmail.png", "Writing",
     "Your Send-MailMessage replacement might be sending email twice")
card("post-egress-firewall.png", "Writing",
     "Running GitHub’s Actions egress firewall on a small Go project")
card("post-kiota-eight-sdks.png", "Writing",
     "One retry fix, eight Kiota SDKs",
     "The fix was the same everywhere. The code around it wasn’t.")
card("post-checks-evidence.png", "Writing",
     "Checks that parsed their own evidence")
