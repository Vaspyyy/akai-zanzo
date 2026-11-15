"""Lettering pass: find empty balloons/caption boxes in page art and fill in the spec's text.

Pipeline
1. White regions (>= WHITE) are labelled. The white area touching the page edge is the
   margin + gutters; what it encloses are the panels.
2. Every other enclosed white region is a candidate. It must be flat white inside, have a
   dark outline, and look like an oval (balloon) or a rectangle (caption box).
   Balloons that break the panel border merge with the gutter; a morphological opening of
   the gutter recovers those.
3. Panels are ordered right-to-left / top-to-bottom (XY cut); balloons inside a panel are
   ordered right-to-left, higher first when stacked.
4. Spec dialogue lines go to balloons, captions to boxes, in that order, per panel (or over
   the whole page if the panel count does not match the spec).
5. Text is uppercased, wrapped to the real shape of each region and auto-sized.
A spec line with `box: [x, y, w, h]` skips detection for that line.
"""
from __future__ import annotations

import functools
from dataclasses import dataclass, field
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .spec import PROD, REPO, Line, Page, art_path, prev_path

FONT_DIR = PROD / "fonts" / "anime-ace-2"
FONTS = {
    "regular": FONT_DIR / "animeace2_reg.ttf",
    "bold": FONT_DIR / "animeace2_bld.ttf",
    "italic": FONT_DIR / "animeace2_ital.ttf",
}
WHITE = 215


# ------------------------------------------------------------------ model
@dataclass
class Region:
    x: int
    y: int
    w: int
    h: int
    mask: np.ndarray  # bool, h x w, filled shape
    kind: str  # balloon | caption | other
    score: float
    panel: int = -1
    manual: bool = False
    center: tuple[float, float] | None = None

    @property
    def cx(self):
        return self.center[0] if self.center else self.x + self.w / 2

    @property
    def cy(self):
        return self.center[1] if self.center else self.y + self.h / 2

    def box(self):
        return [int(self.x), int(self.y), int(self.w), int(self.h)]


@dataclass
class Placed:
    line: Line
    panel: int
    region: Region | None
    size: int = 0
    nlines: int = 0
    overflow: bool = False
    note: str = ""


@dataclass
class Report:
    page: str
    panels_found: int
    panels_spec: int
    mode: str
    placed: list[Placed] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    spare: list[Region] = field(default_factory=list)

    @property
    def ok(self):
        return not self.errors and all(p.region and not p.overflow for p in self.placed)

    def summary(self) -> str:
        head = (f"{'OK' if self.ok else 'CHECK'}: {sum(1 for p in self.placed if p.region)}/{len(self.placed)} "
                f"lines placed; panels found {self.panels_found}, spec {self.panels_spec} ({self.mode} mapping)")
        out = [head]
        for p in self.placed:
            who = p.line.speaker.upper() if p.line.speaker else "CAPTION"
            if p.region:
                r = p.region
                src = "manual" if r.manual else f"{r.kind} {r.score:.2f}"
                out.append(f"  P{p.panel} {who}: \"{p.line.text[:40]}\" -> box {r.box()} ({src}), {p.size}px, "
                           f"{p.nlines} line(s){' OVERFLOW' if p.overflow else ''}")
            else:
                out.append(f"  P{p.panel} {who}: \"{p.line.text[:40]}\" -> NOT PLACED {p.note}")
        out += [f"  ! {e}" for e in self.errors]
        if self.spare:
            out.append("  unused candidates (for manual `box:`): " + ", ".join(f"{r.kind} {r.box()}" for r in self.spare))
        return "\n".join(out)


# -------------------------------------------------------------- detection
def _fill(mask: np.ndarray) -> np.ndarray:
    cs, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = np.zeros(mask.shape, np.uint8)
    cv2.drawContours(out, cs, -1, 1, thickness=-1)
    return out.astype(bool)


def _disk(r: int):
    r = max(1, int(r))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def _evaluate(gray: np.ndarray, comp: np.ndarray, x: int, y: int) -> Region | None:
    """comp: bool mask of the component inside bbox (x, y)."""
    h, w = comp.shape
    if min(w, h) < max(28, 0.028 * gray.shape[1]):
        return None
    pad = 6
    H, W = gray.shape
    x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad)
    big = np.zeros((y1 - y0, x1 - x0), bool)
    big[y - y0:y - y0 + h, x - x0:x - x0 + w] = comp
    g = gray[y0:y1, x0:x1]
    filled = _fill(big)
    area = filled.sum()
    if area == 0:
        return None
    # flat white inside (empty balloon), ignoring a thin rim
    inner = cv2.erode(filled.astype(np.uint8), _disk(3)).astype(bool)
    if inner.sum() < 50:
        return None
    white_inside = (g[inner] >= WHITE + 10).mean()
    # dark outline just outside
    ring = cv2.dilate(filled.astype(np.uint8), _disk(3)).astype(bool) & ~filled
    dark_ring = (g[ring] < 128).mean() if ring.any() else 0
    if white_inside < 0.96 or dark_ring < 0.45:
        return None
    cs, _ = cv2.findContours(filled.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)
    (_, _), (rw, rh), ang = cv2.minAreaRect(c)
    rect_fill = area / max(1.0, rw * rh)
    axis_aligned = min(abs(ang) % 90, 90 - abs(ang) % 90) < 4
    hull = cv2.convexHull(c)
    solidity = area / max(1.0, cv2.contourArea(hull))
    # ellipse fit on the core (erosion strips the tail), grown back
    r = max(2, int(0.12 * min(w, h)))
    core = cv2.erode(filled.astype(np.uint8), _disk(r))
    iou, center = 0.0, None
    ccs, _ = cv2.findContours(core, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if ccs:
        cc = max(ccs, key=cv2.contourArea)
        if len(cc) >= 5:
            (ex, ey), (ea, eb), eang = cv2.fitEllipse(cc)
            em = np.zeros(filled.shape, np.uint8)
            cv2.ellipse(em, ((ex, ey), (ea + 2 * r, eb + 2 * r), eang), 1, -1)
            em = em.astype(bool)
            iou = (em & filled).sum() / max(1, (em | filled).sum())
            center = (ex + x0, ey + y0)
    if rect_fill >= 0.93 and axis_aligned:
        kind, score = "caption", rect_fill
    elif iou >= 0.80:
        kind, score = "balloon", iou
    elif solidity >= 0.82 and rect_fill < 0.93:
        kind, score = "other", 0.7 * solidity
    else:
        return None
    score = score * (0.6 + 0.4 * min(1.0, dark_ring / 0.8))
    ys, xs = np.nonzero(filled)
    bx, by = xs.min(), ys.min()
    m = filled[by:ys.max() + 1, bx:xs.max() + 1]
    return Region(int(bx + x0), int(by + y0), m.shape[1], m.shape[0], m, kind, float(score),
                  center=center if kind != "caption" else None)


def detect(gray: np.ndarray):
    H, W = gray.shape
    page = H * W
    white = (gray >= WHITE).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(white, connectivity=4)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    gutter = np.isin(lab, list(edge))
    regions: list[Region] = []
    lo, hi = 0.0012 * page, 0.12 * page
    for i in range(1, n):
        if i in edge:
            continue
        x, y, w, h, a = stats[i]
        if a < lo or a > hi:
            continue
        r = _evaluate(gray, lab[y:y + h, x:x + w] == i, x, y)
        if r:
            regions.append(r)
    # balloons that break the panel border and merge into the gutter
    k = max(9, int(0.022 * W))
    opened = cv2.morphologyEx(gutter.astype(np.uint8), cv2.MORPH_OPEN, _disk(k // 2))
    n2, lab2, st2, _ = cv2.connectedComponentsWithStats(opened, connectivity=4)
    edge2 = set(np.unique(np.concatenate([lab2[0], lab2[-1], lab2[:, 0], lab2[:, -1]]))) - {0}
    for i in range(1, n2):
        if i in edge2:
            continue
        x, y, w, h, a = st2[i]
        if a < lo or a > hi:
            continue
        # grow the opened blob back to the real balloon outline
        grow = k // 2 + 2
        x0, y0 = max(0, x - grow), max(0, y - grow)
        x1, y1 = min(W, x + w + grow), min(H, y + h + grow)
        blob = (lab2[y0:y1, x0:x1] == i).astype(np.uint8)
        blob = cv2.dilate(blob, _disk(grow)).astype(bool) & gutter[y0:y1, x0:x1]
        r = _evaluate(gray, blob, x0, y0)
        if r:
            r.score *= 0.9
            regions.append(r)
    # panels = what the gutter encloses, minus the balloons (a balloon that bridges a
    # gutter would otherwise glue two panels together); the opening then cuts thin links
    solid = (~gutter).astype(np.uint8)
    for r in regions:
        sub = solid[r.y:r.y + r.h, r.x:r.x + r.w]
        sub[r.mask] = 0
    pad = max(3, W // 200)
    for r in regions:  # also remove the balloon outline (dilate on a padded canvas)
        canvas = np.zeros((r.h + 2 * (pad + 3), r.w + 2 * (pad + 3)), np.uint8)
        canvas[pad + 3:pad + 3 + r.h, pad + 3:pad + 3 + r.w] = r.mask
        canvas = cv2.dilate(canvas, _disk(pad + 2))
        cy0, cx0 = r.y - pad - 3, r.x - pad - 3
        ys, xs = np.nonzero(canvas)
        ys, xs = ys + cy0, xs + cx0
        ok = (ys >= 0) & (ys < H) & (xs >= 0) & (xs < W)
        solid[ys[ok], xs[ok]] = 0
    solid = cv2.morphologyEx(solid, cv2.MORPH_OPEN, _disk(pad))
    m, _, pstats, _ = cv2.connectedComponentsWithStats(solid, connectivity=4)
    panels = [tuple(int(v) for v in pstats[i, :4]) for i in range(1, m) if pstats[i, 4] > 0.012 * page]
    return panels, regions


# --------------------------------------------------------------- ordering
def order_boxes(boxes: list[tuple], tol: int = 6) -> list[int]:
    """Manga reading order (XY cut): rows top->bottom, columns right->left, recursive."""
    idx = list(range(len(boxes)))

    def cut(ids):
        if len(ids) <= 1:
            return ids
        # horizontal cut: a y that no box straddles
        spans = sorted((boxes[i][1], boxes[i][1] + boxes[i][3]) for i in ids)
        groups, cur_end = [], None
        for i in sorted(ids, key=lambda i: boxes[i][1]):
            top, bot = boxes[i][1], boxes[i][1] + boxes[i][3]
            if cur_end is None or top >= cur_end - tol:
                groups.append([i])
                cur_end = bot
            else:
                groups[-1].append(i)
                cur_end = max(cur_end, bot)
        if len(groups) > 1:
            return [j for g in groups for j in cut(g)]
        groups, cur_start = [], None
        for i in sorted(ids, key=lambda i: -(boxes[i][0] + boxes[i][2])):
            left, right = boxes[i][0], boxes[i][0] + boxes[i][2]
            if cur_start is None or right <= cur_start + tol:
                groups.append([i])
                cur_start = left
            else:
                groups[-1].append(i)
                cur_start = min(cur_start, left)
        if len(groups) > 1:
            return [j for g in groups for j in cut(g)]
        del spans
        return sorted(ids, key=lambda i: (boxes[i][1], -(boxes[i][0] + boxes[i][2])))

    return cut(idx)


def _balloon_cmp(a: Region, b: Region) -> int:
    ov = min(a.x + a.w, b.x + b.w) - max(a.x, b.x)
    if ov > 0.4 * min(a.w, b.w):  # stacked: higher first
        return -1 if a.y < b.y else 1
    return -1 if a.cx > b.cx else 1  # side by side: right first


def order_in_panel(rs: list[Region]) -> list[Region]:
    return sorted(rs, key=functools.cmp_to_key(_balloon_cmp))


def _panel_of(r: Region, panels: list[tuple]) -> int:
    best, bd = -1, 1e18
    for i, (x, y, w, h) in enumerate(panels):
        if x <= r.cx <= x + w and y <= r.cy <= y + h:
            return i
        dx = max(x - r.cx, 0, r.cx - x - w)
        dy = max(y - r.cy, 0, r.cy - y - h)
        d = dx * dx + dy * dy
        if d < bd:
            best, bd = i, d
    return best


# ------------------------------------------------------------------ fitting
def _font(style: str, size: int):
    path = FONTS.get(style, FONTS["regular"])
    if not path.exists():
        raise FileNotFoundError(f"lettering font missing: {path} (run production/fonts/fetch-fonts.sh)")
    return ImageFont.truetype(str(path), size)


def _join(tokens: list[str]) -> str:
    """Join tokens with spaces, except after a hyphen break ("KUBO-" + "SAN.")."""
    out = ""
    for t in tokens:
        out += t if (not out or out.endswith("-")) else " " + t
    return out


def _tokens(text: str, split_hyphens: bool) -> list[str]:
    toks = []
    for w in text.upper().split():
        if split_hyphens and "-" in w.strip("-"):
            parts = w.split("-")
            toks += [p + "-" for p in parts[:-1]] + [parts[-1]]
        else:
            toks.append(w)
    return [t for t in toks if t]


def layout(region: Region, text: str, style: str, page_w: int, small: bool, cap: int | None = None):
    """Return (size, [(line, cx, cy)], overflow)."""
    m = region.mask.astype(np.uint8)
    short = min(region.w, region.h)
    pad = max(5, int(0.06 * short)) if region.kind != "caption" else max(7, int(0.08 * short))
    inner = cv2.erode(m, _disk(pad)).astype(bool)
    rows_l = np.full(region.h, -1)
    rows_r = np.full(region.h, -1)
    for yy in range(region.h):
        xs = np.flatnonzero(inner[yy])
        if xs.size:
            rows_l[yy], rows_r[yy] = xs[0], xs[-1]
    cy = (region.cy - region.y) if region.center else (np.flatnonzero(rows_l >= 0).mean() if (rows_l >= 0).any() else region.h / 2)
    max_size = int(page_w * (0.022 if small else 0.029))
    if cap:
        max_size = min(max_size, cap)
    min_size = max(10, int(page_w * 0.011))

    def slots(n, lh):
        y0 = cy - n * lh / 2
        out = []
        for k in range(n):
            a, b = int(round(y0 + k * lh)), int(round(y0 + (k + 1) * lh))
            if a < 0 or b > region.h:
                return None
            l, r = rows_l[a:b], rows_r[a:b]
            if (l < 0).any():
                return None
            lo_, hi_ = int(l.max()), int(r.min())
            slack = int(0.03 * (hi_ - lo_)) + 1  # italic overhang, ink bleed
            out.append((lo_ + slack, hi_ - slack, (a + b) / 2))
        return out

    def fit(tokens):
        for size in range(max_size, min_size - 1, -1):
            f = _font(style, size)
            lh = size * 1.2
            for n in range(1, len(tokens) + 1):
                sl = slots(n, lh)
                if sl is None:
                    break
                lines, cur, k, okay = [], [], 0, True
                for tk in tokens:
                    if f.getlength(_join(cur + [tk])) <= sl[k][1] - sl[k][0]:
                        cur.append(tk)
                        continue
                    if not cur:
                        okay = False
                        break
                    lines.append(_join(cur))
                    k += 1
                    cur = [tk]
                    if k >= n or f.getlength(tk) > sl[k][1] - sl[k][0]:
                        okay = False
                        break
                if okay and cur:
                    lines.append(_join(cur))
                if okay and len(lines) <= n:
                    sl = slots(len(lines), lh) or sl  # re-center on the real line count
                    return size, [(ln, region.x + (s[0] + s[1]) / 2, region.y + s[2]) for ln, s in zip(lines, sl)]
        return None

    best = fit(_tokens(text, False))
    if (best is None or best[0] < 0.8 * max_size) and "-" in text:
        alt = fit(_tokens(text, True))
        if alt and (best is None or alt[0] > best[0] + 1):
            best = alt
    if best:
        return best[0], best[1], False
    # overflow: smallest size, one word per line around the centre
    words = _tokens(text, True)
    size, lh = min_size, min_size * 1.2
    y0 = region.y + cy - len(words) * lh / 2
    return size, [(wd, region.x + region.w / 2, y0 + (k + 0.5) * lh) for k, wd in enumerate(words)], True


# --------------------------------------------------------------- main entry
def _manual_region(line: Line) -> Region:
    x, y, w, h = [int(v) for v in line.box]
    m = np.zeros((h, w), np.uint8)
    if line.kind == "caption":
        m[:] = 1
        kind = "caption"
    else:
        cv2.ellipse(m, ((w / 2, h / 2), (w, h), 0), 1, -1)
        kind = "balloon"
    return Region(x, y, w, h, m.astype(bool), kind, 1.0, manual=True)


def _paint_manual(img: Image.Image, items: list[tuple[Line, Region]], ss: int = 4):
    """Paint fresh balloons/caption boxes (`draw: true`) over the art: white fill, black outline, optional tail.
    Drawn supersampled so the outline is smooth. The new shape should cover any drawn balloon under it."""
    W, H = img.size
    for ln, r in items:
        pad = 12
        x0, y0 = max(0, r.x - pad), max(0, r.y - pad)
        x1, y1 = min(W, r.x + r.w + pad), min(H, r.y + r.h + pad)
        if ln.tail:
            tx, ty = [int(v) for v in ln.tail]
            x0, y0, x1, y1 = min(x0, tx - pad), min(y0, ty - pad), max(x1, tx + pad), max(y1, ty + pad)
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
        bw, bh = x1 - x0, y1 - y0
        ink = Image.new("L", (bw * ss, bh * ss), 0)     # outline+fill shape (alpha of black)
        fill = Image.new("L", (bw * ss, bh * ss), 0)    # inner white
        di, df = ImageDraw.Draw(ink), ImageDraw.Draw(fill)
        lw = 3 * ss
        bx = [(r.x - x0) * ss, (r.y - y0) * ss, (r.x + r.w - x0) * ss, (r.y + r.h - y0) * ss]
        shape = di.rectangle if ln.kind == "caption" else di.ellipse
        fshape = df.rectangle if ln.kind == "caption" else df.ellipse
        shape(bx, fill=255)
        fshape([bx[0] + lw, bx[1] + lw, bx[2] - lw, bx[3] - lw], fill=255)
        if ln.tail and ln.kind != "caption":
            cx, cy = (bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2
            tx, ty = (int(ln.tail[0]) - x0) * ss, (int(ln.tail[1]) - y0) * ss
            vx, vy = tx - cx, ty - cy
            n = (vx * vx + vy * vy) ** 0.5 or 1
            px, py = -vy / n, vx / n
            base = 0.18 * min(bx[2] - bx[0], bx[3] - bx[1])
            # base sits inside the ellipse (75% of the way to its edge) so the tail joins it seamlessly
            ux, uy = vx / n, vy / n
            a, b = (bx[2] - bx[0]) / 2, (bx[3] - bx[1]) / 2
            t = 0.75 / ((ux / a) ** 2 + (uy / b) ** 2) ** 0.5
            mx, my = cx + ux * t, cy + uy * t
            b1 = (mx + px * base, my + py * base)
            b2 = (mx - px * base, my - py * base)
            di.polygon([b1, b2, (tx, ty)], fill=255)
            # inner white tail, shrunk toward the tip by the line width
            sh = lw * 1.8
            df.polygon([(b1[0] - px * lw, b1[1] - py * lw), (b2[0] + px * lw, b2[1] + py * lw),
                        (tx - vx / n * sh, ty - vy / n * sh)], fill=255)
        ink = ink.resize((bw, bh), Image.LANCZOS)
        fill = fill.resize((bw, bh), Image.LANCZOS)
        patch = img.crop((x0, y0, x1, y1))
        patch.paste((0, 0, 0), (0, 0), ink)
        patch.paste((255, 255, 255), (0, 0), fill)
        img.paste(patch, (x0, y0))


def _assign(cands: list[Region], dlg: list[Line], caps: list[Line]):
    """Pick regions for dialogue (balloons) and captions (boxes). Returns (d_regions, c_regions, spare, notes)."""
    notes = []
    balloons = sorted([r for r in cands if r.kind in ("balloon", "other")], key=lambda r: -r.score)
    boxes = sorted([r for r in cands if r.kind == "caption"], key=lambda r: -r.score)
    c_pick = boxes[:len(caps)]
    rest_boxes = boxes[len(caps):]
    d_pick = balloons[:len(dlg)]
    rest_balloons = balloons[len(dlg):]
    if len(c_pick) < len(caps) and rest_balloons:
        k = len(caps) - len(c_pick)
        notes.append(f"used {min(k, len(rest_balloons))} oval(s) as caption box")
        c_pick += rest_balloons[:k]
        rest_balloons = rest_balloons[k:]
    if len(d_pick) < len(dlg) and rest_boxes:
        k = len(dlg) - len(d_pick)
        notes.append(f"used {min(k, len(rest_boxes))} rectangle(s) as balloon")
        d_pick += rest_boxes[:k]
        rest_boxes = rest_boxes[k:]
    return d_pick, c_pick, rest_balloons + rest_boxes, notes


def letter_page(page: Page, debug_dir: Path | None = None, src: Path | None = None) -> Report:
    src = src or art_path(page)
    if not src.exists():
        raise FileNotFoundError(f"no art to letter: {src}")
    img = Image.open(src).convert("RGB")
    gray = np.array(img.convert("L"))
    H, W = gray.shape
    panels, regions = detect(gray)
    order = order_boxes(panels)
    panels = [panels[i] for i in order]
    spec_panels = page.panels
    rep = Report(page.key, len(panels), len(spec_panels), "per-panel" if len(panels) == len(spec_panels) else "page-wide")

    manual = []
    for pn in spec_panels:
        for ln in pn.dialogue + pn.captions:
            if ln.box:
                manual.append(_manual_region(ln))
    if manual:  # drop detections that overlap a manual box
        def overlaps(a, b):
            ix = max(0, min(a.x + a.w, b.x + b.w) - max(a.x, b.x))
            iy = max(0, min(a.y + a.h, b.y + b.h) - max(a.y, b.y))
            return ix * iy > 0.3 * min(a.w * a.h, b.w * b.h)
        regions = [r for r in regions if not any(overlaps(r, m) for m in manual)]
    for r in regions:
        r.panel = _panel_of(r, panels) if panels else 0

    jobs: list[tuple[Line, int, Region | None]] = []
    if rep.mode == "per-panel":
        groups = [(pi, [r for r in regions if r.panel == pi], [spec_panels[pi]]) for pi in range(len(spec_panels))]
    else:
        rep.errors.append(f"panel count differs (found {len(panels)}, spec {len(spec_panels)}): lines mapped in page order, check speakers")
        groups = [(-1, regions, spec_panels)]
    for pi, cands, sps in groups:
        dlg = [(pn.index, ln) for pn in sps for ln in pn.dialogue if not ln.box]
        caps = [(pn.index, ln) for pn in sps for ln in pn.captions if not ln.box]
        d_pick, c_pick, spare, notes = _assign(cands, [l for _, l in dlg], [l for _, l in caps])
        rep.spare += spare
        for n_ in notes:
            rep.errors.append(f"P{pi + 1 if pi >= 0 else '?'}: {n_}")

        def page_order(rs):
            if pi >= 0:
                return order_in_panel(rs)
            ranked = []
            for p_i in range(len(panels) or 1):
                ranked += order_in_panel([r for r in rs if r.panel == p_i])
            return ranked + [r for r in rs if r not in ranked]

        d_sorted, c_sorted = page_order(d_pick), page_order(c_pick)
        for k, (pidx, ln) in enumerate(dlg):
            jobs.append((ln, pidx, d_sorted[k] if k < len(d_sorted) else None))
        for k, (pidx, ln) in enumerate(caps):
            jobs.append((ln, pidx, c_sorted[k] if k < len(c_sorted) else None))
        if len(d_sorted) < len(dlg):
            rep.errors.append(f"P{pi + 1 if pi >= 0 else '?'}: {len(dlg)} balloon(s) in spec, {len(d_sorted)} found")
        if len(c_sorted) < len(caps):
            rep.errors.append(f"P{pi + 1 if pi >= 0 else '?'}: {len(caps)} caption box(es) in spec, {len(c_sorted)} found")
    mi = iter(manual)
    for pn in spec_panels:
        for ln in pn.dialogue + pn.captions:
            if ln.box:
                jobs.append((ln, pn.index, next(mi)))

    out = img.copy()
    d = ImageDraw.Draw(out)
    _paint_manual(out, [(ln, reg) for ln, _, reg in jobs if reg is not None and reg.manual and ln.draw])

    def style_of(ln):
        return "italic" if ln.kind == "caption" else ("bold" if (ln.style or "") in ("bold", "shout", "loud") else "regular")

    # one type size per page: cap normal dialogue at the median of what fits
    fits = sorted(layout(reg, ln.text, style_of(ln), W, False)[0]
                  for ln, _, reg in jobs if reg is not None and ln.kind == "dialogue" and not ln.style)
    cap = fits[len(fits) // 2] if fits else None
    for ln, pidx, reg in jobs:
        pl = Placed(ln, pidx, reg)
        if reg is None:
            pl.note = "(no free balloon/box)"
            rep.placed.append(pl)
            continue
        style = style_of(ln)
        small = (ln.style or "").startswith("small")
        size, lines, overflow = layout(reg, ln.text, style, W, small, cap=cap)
        f = _font(style, size)
        for text, x, y in lines:
            d.text((x, y), text, font=f, fill=(0, 0, 0), anchor="mm")
        pl.size, pl.nlines, pl.overflow = size, len(lines), overflow
        rep.placed.append(pl)
    # keep spec order in the report
    order_key = {id(l): i for i, l in enumerate([l for pn in spec_panels for l in pn.dialogue + pn.captions])}
    rep.placed.sort(key=lambda p: order_key.get(id(p.line), 0))

    dst = page.output
    if dst.exists() and dst.resolve() != src.resolve():
        dst.replace(prev_path(dst))
    out.save(dst)
    if debug_dir is not None:
        debug_dir.mkdir(parents=True, exist_ok=True)
        dbg = out.copy()
        dd = ImageDraw.Draw(dbg)
        for i, (x, y, w, h) in enumerate(panels):
            dd.rectangle([x, y, x + w, y + h], outline=(0, 90, 255), width=4)
            dd.text((x + 8, y + 6), f"P{i + 1}", fill=(0, 90, 255), font=_font("bold", 28))
        for p in rep.placed:
            if p.region:
                r = p.region
                col = (0, 170, 0) if r.kind == "balloon" else (255, 140, 0)
                dd.rectangle([r.x, r.y, r.x + r.w, r.y + r.h], outline=col, width=3)
                tag = (p.line.speaker or "cap").upper()
                dd.text((r.x + 4, r.y + 2), tag, fill=(220, 0, 0), font=_font("bold", 16))
        for r in rep.spare:
            dd.rectangle([r.x, r.y, r.x + r.w, r.y + r.h], outline=(255, 0, 0), width=2)
        dbg.save(debug_dir / f"{page.key}.letter-debug.jpg", quality=85)
    return rep
