"""Contact sheets: 3 pages side by side, ~640 px tall, labelled."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HEIGHT = 640
LABEL = 28
GAP = 12


def _font(size: int):
    for p in ("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def contact_sheet(items: list[tuple[str, Path]], out: Path, height: int = HEIGHT) -> Path:
    tiles = []
    for label, path in items:
        im = Image.open(path).convert("RGB")
        w = round(im.width * height / im.height)
        tiles.append((label, im.resize((w, height), Image.LANCZOS)))
    width = sum(t.width for _, t in tiles) + GAP * (len(tiles) + 1)
    sheet = Image.new("RGB", (width, height + LABEL + GAP * 2), (60, 60, 60))
    d = ImageDraw.Draw(sheet)
    f = _font(18)
    x = GAP
    for label, t in tiles:
        d.text((x + 4, GAP // 2 + 2), label, fill=(255, 255, 255), font=f)
        sheet.paste(t, (x, LABEL + GAP))
        x += t.width + GAP
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=85)
    return out


def sheets(items: list[tuple[str, Path]], out_dir: Path, prefix: str = "contact", per: int = 3) -> list[Path]:
    outs = []
    for i in range(0, len(items), per):
        outs.append(contact_sheet(items[i:i + per], out_dir / f"{prefix}-{i // per + 1:02d}.jpg"))
    return outs
