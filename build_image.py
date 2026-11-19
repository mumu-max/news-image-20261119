"""Build the entry image for make.fun news-image-20261119.

Pipeline (build time only; the graded program main.py just copies the
result, which the competition rules explicitly allow):
  1. collage.png — one AI-illustrated 2x3 panel collage (GPT-Image-2 via
     APIMart, no text in it), generated separately and saved next to this
     script. Each of its 6 cells illustrates one story in news.json.
  2. This script slices the collage into 6 cells, lays them out as a
     newspaper front page (masthead + date, one captioned panel per story),
     and writes entry.png (1024x1024, at most 1 MiB; JPEG fallback if the
     PNG is too big — the file keeps the name entry.png either way).

Usage:  python3 build_image.py [collage.png] [news.json] [entry.png]
"""

import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MAX_BYTES = 1048576
NAVY = (20, 36, 61)
GOLD = (217, 164, 65)
PAPER = (247, 243, 234)
INK = (24, 24, 24)
GREY = (90, 90, 90)
RULE = (180, 175, 160)

FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
]


def font(name, size):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    collage_path = sys.argv[1] if len(sys.argv) > 1 else "collage.png"
    news_path = sys.argv[2] if len(sys.argv) > 2 else "news.json"
    out_path = sys.argv[3] if len(sys.argv) > 3 else "entry.png"

    with open(news_path, encoding="utf-8") as fh:
        news = json.load(fh)
    stories = news["stories"][:6]
    assert len(stories) == 6, "need exactly 6 stories"

    collage = Image.open(collage_path).convert("RGB")
    cw, ch = collage.size
    cell_w, cell_h = cw // 2, ch // 3
    cells = []
    for i in range(6):
        x, y = (i % 2) * cell_w, (i // 2) * cell_h
        cells.append(collage.crop((x, y, x + cell_w, y + cell_h)))

    page = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(page)

    # --- masthead band ---
    d.rectangle([0, 0, SIZE, 128], fill=NAVY)
    f_mast = font("LiberationSerif-Bold.ttf", 58)
    f_date = font("LiberationSans-Bold.ttf", 25)
    d.text((SIZE // 2, 34), news["masthead"], font=f_mast, fill="white",
           anchor="ma")
    d.text((SIZE // 2, 94), "T H U R S D A Y ,  1 9  N O V E M B E R  2 0 2 6",
           font=f_date, fill=GOLD, anchor="ma")

    # --- story grid: 2 cols x 3 rows ---
    margin, gutter = 16, 16
    grid_top, grid_bottom = 144, 976
    panel_w = (SIZE - 2 * margin - gutter) // 2
    panel_h = (grid_bottom - grid_top - 2 * gutter) // 3
    img_h, cap_h = 180, panel_h - 180
    f_head = font("LiberationSans-Bold.ttf", 21)
    f_sum = font("LiberationSans-Regular.ttf", 16)

    for i, story in enumerate(stories):
        px = margin + (i % 2) * (panel_w + gutter)
        py = grid_top + (i // 2) * (panel_h + gutter)
        # picture: centre-crop the collage cell to the panel image ratio
        cell = cells[i]
        target_ratio = panel_w / img_h
        w, h = cell.size
        if w / h > target_ratio:  # too wide: crop sides
            nw = int(h * target_ratio)
            cell = cell.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
        else:  # too tall: crop top/bottom
            nh = int(w / target_ratio)
            cell = cell.crop((0, (h - nh) // 2, w, (h + nh) // 2))
        cell = cell.resize((panel_w, img_h), Image.LANCZOS)
        page.paste(cell, (px, py))
        # caption bar
        cy = py + img_h
        d.rectangle([px, cy, px + panel_w, py + panel_h], fill="white")
        d.line([px, cy, px + panel_w, cy], fill=RULE, width=2)
        head_lines = wrap(d, story["headline"], f_head, panel_w - 20)[:2]
        y = cy + 8
        for line in head_lines:
            d.text((px + 10, y), line, font=f_head, fill=INK)
            y += 24
        sum_lines = wrap(d, story["summary"], f_sum, panel_w - 20)[:1]
        for line in sum_lines:
            d.text((px + 10, y + 2), line, font=f_sum, fill=GREY)

    # --- footer ---
    f_foot = font("LiberationSans-Regular.ttf", 14)
    d.text((SIZE // 2, 992), news["footer"], font=f_foot, fill=GREY,
           anchor="ma")

    # --- save, honouring the 1 MiB cap ---
    page.save(out_path, "PNG", optimize=True)
    size = os.path.getsize(out_path)
    if size > MAX_BYTES:
        page.save(out_path, "JPEG", quality=88, optimize=True)
        size = os.path.getsize(out_path)
    print(f"wrote {out_path}: {page.size[0]}x{page.size[1]}, {size} bytes "
          f"({'OK' if size <= MAX_BYTES else 'OVER LIMIT'})")
    assert size <= MAX_BYTES, "entry image over 1 MiB"
    assert page.size[0] <= SIZE and page.size[1] <= SIZE


if __name__ == "__main__":
    main()
