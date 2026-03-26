#!/usr/bin/env python3
"""
Generate PWA icons (icon-192.png and icon-512.png) for Open Reporting mobile app.
Requires Pillow: pip install Pillow
Run from repo root: python3 products/mobile/static/generate_icons.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).parent
SIZES = [192, 512]
BG_COLOR = "#4A7FB5"
TEXT_COLOR = "white"
TEXT = "OR"


def make_icon(size: int) -> None:
    img = Image.new("RGBA", (size, size), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Try to load a bold font; fall back to default if unavailable
    font_size = int(size * 0.38)
    font = None
    for font_path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    ]:
        if Path(font_path).exists():
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except Exception:
                pass

    if font is None:
        font = ImageFont.load_default()

    # Centre the text
    bbox = draw.textbbox((0, 0), TEXT, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (size - text_w) / 2 - bbox[0]
    y = (size - text_h) / 2 - bbox[1]
    draw.text((x, y), TEXT, font=font, fill=TEXT_COLOR)

    out_path = OUT_DIR / f"icon-{size}.png"
    img.save(out_path, "PNG")
    print(f"Saved {out_path}")


if __name__ == "__main__":
    for s in SIZES:
        make_icon(s)
    print("Done.")
