# make-logo.py — draw the $PROOF logo (original artwork, no third-party assets)
#
# Renders assets/logo.png, a 512x512 PNG: a gold medal on a deep violet field,
# the medal carrying a simple robot/agent face and a checkmark ribbon.
# Design goals (from the bounty judge's packaging criterion): one bold subject,
# strong outline, high contrast, plain background, readable at thumbnail size.
#
# Run:  python3 scripts/make-logo.py
# Uses only the Python standard library plus Pillow (PIL).

import math
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 512
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")

# Palette
VIOLET_BG = (26, 11, 46, 255)        # deep violet field
VIOLET_RING = (124, 58, 237, 255)    # bright violet halo ring
GOLD = (255, 196, 0, 255)            # medal gold
GOLD_DARK = (214, 158, 0, 255)       # medal shading
GOLD_LIGHT = (255, 224, 102, 255)    # medal highlight
INK = (26, 11, 46, 255)             # face ink (same as background)
WHITE = (255, 255, 255, 255)
RIBBON_RED = (239, 68, 68, 255)
RIBBON_DARK = (185, 28, 28, 255)


def _font(size):
    """Best available bold sans font; falls back to PIL's default bitmap font."""
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_logo():
    img = Image.new("RGBA", (SIZE, SIZE), VIOLET_BG)
    d = ImageDraw.Draw(img)

    cx, cy = SIZE // 2, SIZE // 2 - 18

    # Halo ring behind the medal.
    d.ellipse([cx - 196, cy - 196, cx + 196, cy + 196], outline=VIOLET_RING, width=14)

    # Ribbon tails behind the medal (two angled bands, V shape).
    d.polygon([(cx - 118, cy + 118), (cx - 58, cy + 128), (cx - 96, cy + 226), (cx - 158, cy + 196)], fill=RIBBON_RED)
    d.polygon([(cx + 118, cy + 118), (cx + 58, cy + 128), (cx + 96, cy + 226), (cx + 158, cy + 196)], fill=RIBBON_DARK)
    # Ribbon notch cuts.
    d.polygon([(cx - 96, cy + 226), (cx - 126, cy + 196), (cx - 158, cy + 196)], fill=VIOLET_BG)
    d.polygon([(cx + 96, cy + 226), (cx + 126, cy + 196), (cx + 158, cy + 196)], fill=VIOLET_BG)

    # Medal: outer gold disc, inner ring, shaded lower half.
    d.ellipse([cx - 158, cy - 158, cx + 158, cy + 158], fill=GOLD)
    d.ellipse([cx - 158, cy - 158, cx + 158, cy + 158], outline=GOLD_DARK, width=6)
    d.ellipse([cx - 132, cy - 132, cx + 132, cy + 132], outline=GOLD_DARK, width=5)
    # Highlight arc on the upper left.
    d.arc([cx - 140, cy - 140, cx + 140, cy + 140], start=150, end=300, fill=GOLD_LIGHT, width=16)

    # Robot / agent face inside the medal: rounded head, antenna, eyes, smile.
    # Antenna.
    d.line([(cx, cy - 96), (cx, cy - 122)], fill=INK, width=10)
    d.ellipse([cx - 13, cy - 137, cx + 13, cy - 111], fill=INK)
    # Head.
    d.rounded_rectangle([cx - 88, cy - 84, cx + 88, cy + 66], radius=34, fill=INK)
    # Face screen (gold, inset).
    d.rounded_rectangle([cx - 70, cy - 66, cx + 70, cy + 48], radius=24, fill=GOLD)
    # Eyes: two bold dots.
    d.ellipse([cx - 46, cy - 38, cx - 14, cy - 6], fill=INK)
    d.ellipse([cx + 14, cy - 38, cx + 46, cy - 6], fill=INK)
    # Smile: thick arc.
    d.arc([cx - 34, cy - 6, cx + 34, cy + 44], start=15, end=165, fill=INK, width=9)
    # Cheek dots (small, keep the face friendly at thumbnail size).
    d.ellipse([cx - 58, cy + 8, cx - 46, cy + 20], fill=GOLD_DARK)
    d.ellipse([cx + 46, cy + 8, cx + 58, cy + 20], fill=GOLD_DARK)

    # Checkmark badge overlapping the medal's lower right edge.
    bx, by, br = cx + 108, cy + 108, 52
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=WHITE)
    d.ellipse([bx - br, by - br, bx + br, by + br], outline=GOLD_DARK, width=5)
    d.line([(bx - 26, by + 1), (bx - 6, by + 21), (bx + 30, by - 21)], fill=(22, 163, 74, 255), width=13, joint="curve")

    # Wordmark: $PROOF along the bottom, bold, white with gold dollar sign.
    font = _font(58)
    text = "$PROOF"
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    d.text((cx - tw // 2 - bbox[0], SIZE - 92), text, font=font, fill=WHITE)

    img.save(OUT, format="PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = draw_logo()
    size = os.path.getsize(path)
    with Image.open(path) as im:
        print(f"wrote {path} ({im.size[0]}x{im.size[1]} {im.format}, {size} bytes)")
