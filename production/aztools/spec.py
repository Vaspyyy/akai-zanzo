"""Load and normalize the YAML registries and page specs."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
PROD = REPO / "production"

DIALOGUE_EXTRAS = {"style", "at", "box", "offpanel", "note", "text", "speaker", "draw", "tail"}


class SpecError(Exception):
    pass


def load_yaml(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@dataclass
class Registry:
    characters: dict
    cars: dict
    locations: dict

    @classmethod
    def load(cls) -> "Registry":
        cast = load_yaml(PROD / "cast.yaml")
        locs = load_yaml(PROD / "locations.yaml")
        return cls(cast.get("characters", {}), cast.get("cars", {}), locs)

    def is_car(self, cid: str) -> bool:
        return cid in self.cars


@dataclass
class Line:
    kind: str  # dialogue | caption | sfx
    text: str
    speaker: str | None = None
    style: str | None = None  # small, bold, shout ...
    at: str | None = None  # placement hint inside the panel
    offpanel: bool = False
    note: str | None = None
    box: list | None = None  # manual lettering box [x, y, w, h]
    draw: bool = False  # paint a fresh white balloon/box over the art at `box` (covers a too-small drawn one)
    tail: list | None = None  # with draw: tail tip [x, y] for the painted balloon


@dataclass
class CastRef:
    id: str
    outfit: str | None = None
    state: str | None = None
    facing: str | None = None
    note: str | None = None
    hidden: bool = False
    view: str | None = None  # cars: key in the car's `views` (angle-specific sheet crop)
    camera: str | None = None  # cars: the explicit camera angle for this car shot


def is_exterior_car(c: "CastRef", reg: "Registry") -> bool:
    """A car seen from outside (not an 'interior only' cast entry)."""
    return c.id in reg.cars and "interior" not in (c.note or "").lower()


@dataclass
class Panel:
    index: int
    pos: str
    shot: str | None
    action: str
    cast: list[CastRef]
    dialogue: list[Line]
    captions: list[Line]
    sfx: list[Line]
    notes: list[str] = field(default_factory=list)
    location: str | None = None  # overrides the page location for this panel
    keep: bool = False  # edit pages: this panel stays as it is (no cast refs, short prompt line)


@dataclass
class Page:
    key: str  # file stem: page-01, page-08-09, harbor-station-night
    label: str  # human label: "p01" or plate id
    number: int | None
    kind: str  # page | plate
    title: str | None
    orientation: str
    location: str | None
    time: str | None
    weather: str | None
    lettering: str  # ai | empty | none
    panels: list[Panel]
    refs: list[dict]
    continue_from: int | None
    driver_hidden: bool
    notes: list[str]
    guards: list[str]
    edit: dict | None
    description: str | None
    output: Path
    raw: dict


@dataclass
class Spec:
    path: Path
    name: str
    chapter: int | None
    title: str | None
    output_dir: Path
    pages: list[Page]

    def select(self, sel: str | None) -> list[Page]:
        if not sel or sel == "all":
            return list(self.pages)
        wanted: list[Page] = []
        for part in [p.strip() for p in sel.split(",") if p.strip()]:
            m = re.fullmatch(r"(\d+)-(\d+)", part)
            if m and not any(pg.key == f"page-{part}" for pg in self.pages):
                lo, hi = int(m.group(1)), int(m.group(2))
                hits = [pg for pg in self.pages if pg.number is not None and lo <= pg.number <= hi]
            elif part.isdigit():
                hits = [pg for pg in self.pages if pg.number == int(part)]
            else:
                hits = [pg for pg in self.pages if pg.key in (part, f"page-{part}") or pg.label == part]
            if not hits:
                raise SpecError(f"{self.path.name}: no page matches '{part}'")
            for h in hits:
                if h not in wanted:
                    wanted.append(h)
        return wanted

    def page_by_number(self, n: int) -> Page | None:
        return next((p for p in self.pages if p.number == n), None)


def spec_path(chapter: str | None, spec: str | None) -> Path:
    if spec:
        p = Path(spec)
        return p if p.is_absolute() else (Path.cwd() / p)
    if chapter is None:
        raise SpecError("give --chapter N or --spec FILE")
    if str(chapter).isdigit():
        return PROD / f"chapter-{int(chapter):03d}.yaml"
    return PROD / f"{chapter}.yaml"


def _as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def _cast_ref(item) -> CastRef:
    if isinstance(item, str):
        cid, _, outfit = item.partition(":")
        return CastRef(id=cid.strip(), outfit=outfit.strip() or None)
    if isinstance(item, dict):
        return CastRef(
            id=item["id"],
            outfit=item.get("outfit"),
            state=item.get("state"),
            facing=item.get("facing"),
            note=item.get("note"),
            hidden=bool(item.get("hidden", False)),
            view=item.get("view"),
            camera=item.get("camera"),
        )
    raise SpecError(f"bad cast entry: {item!r}")


def _dialogue(item, where: str) -> Line:
    if isinstance(item, str):
        raise SpecError(f"{where}: dialogue needs a speaker, e.g. '- dai: \"TEXT\"' (got {item!r})")
    if "text" in item and "speaker" in item:
        speaker, text = item["speaker"], item["text"]
    else:
        keys = [k for k in item if k not in DIALOGUE_EXTRAS]
        if len(keys) != 1:
            raise SpecError(f"{where}: dialogue entry must have exactly one speaker key: {item!r}")
        speaker, text = keys[0], item[keys[0]]
        if isinstance(text, dict):  # - kubo: {text: "...", at: "..."}
            item = {**item, **text}
            text = text.get("text", "")
    return Line(
        "dialogue",
        str(text),
        speaker=str(speaker),
        style=item.get("style"),
        at=item.get("at"),
        offpanel=bool(item.get("offpanel", False)),
        note=item.get("note"),
        box=item.get("box"),
        draw=bool(item.get("draw", False)),
        tail=item.get("tail"),
    )


def _plain(item, kind: str) -> Line:
    if isinstance(item, str):
        return Line(kind, item)
    return Line(kind, str(item["text"]), style=item.get("style"), at=item.get("at"),
                note=item.get("note"), box=item.get("box"), draw=bool(item.get("draw", False)))


def page_key(raw: dict) -> tuple[str, str, int | None]:
    if "id" in raw:
        return str(raw["id"]), str(raw["id"]), None
    p = raw.get("page")
    if p is None:
        raise SpecError(f"page entry without 'page' or 'id': {raw!r}")
    if isinstance(p, int):
        return f"page-{p:02d}", f"p{p:02d}", p
    s = str(p)
    m = re.fullmatch(r"(\d+)-(\d+)", s)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return f"page-{a:02d}-{b:02d}", f"p{a:02d}-{b:02d}", a
    raise SpecError(f"bad page number {p!r}")


def load_spec(path: Path, reg: Registry | None = None) -> Spec:
    if not path.exists():
        raise SpecError(f"spec not found: {path}")
    data = load_yaml(path)
    chapter = data.get("chapter")
    if data.get("output_dir"):
        out_dir = REPO / data["output_dir"]
    elif isinstance(chapter, int):
        out_dir = REPO / "artwork" / "pages" / f"chapter-{chapter:03d}"
    else:
        raise SpecError(f"{path.name}: set 'output_dir' (no numeric chapter)")
    default_lettering = data.get("lettering", "ai")
    defaults = data.get("defaults", {}) or {}
    pages = []
    for raw in data.get("pages", []):
        raw = {**defaults, **raw}
        key, label, number = page_key(raw)
        kind = raw.get("kind", "page")
        where = f"{path.name} {label}"
        panels = []
        for i, rp in enumerate(raw.get("panels", []) or [], start=1):
            pw = f"{where} P{i}"
            panels.append(Panel(
                index=i,
                pos=str(rp.get("pos", "")),
                shot=rp.get("shot"),
                action=str(rp.get("action", "")).strip(),
                cast=[_cast_ref(c) for c in _as_list(rp.get("cast"))],
                dialogue=[_dialogue(d, pw) for d in _as_list(rp.get("dialogue"))],
                captions=[_plain(c, "caption") for c in _as_list(rp.get("captions"))],
                sfx=[_plain(s, "sfx") for s in _as_list(rp.get("sfx"))],
                notes=[str(n) for n in _as_list(rp.get("notes"))],
                location=rp.get("location"),
                keep=bool(rp.get("keep", False)),
            ))
        refs = []
        for r in _as_list(raw.get("refs")):
            refs.append({"path": r, "use": None} if isinstance(r, str) else dict(r))
        cf = raw.get("continue_from")
        if cf == "previous":
            cf = (number - 1) if number else None
        output = REPO / raw["output"] if raw.get("output") else out_dir / f"{key}.png"
        pages.append(Page(
            key=key,
            label=label,
            number=number,
            kind=kind,
            title=raw.get("title"),
            orientation=raw.get("orientation", "landscape" if kind in ("plate", "sheet", "car_sheet") else "portrait"),
            location=raw.get("location"),
            time=raw.get("time"),
            weather=raw.get("weather"),
            lettering="none" if kind in ("plate", "sheet", "car_sheet") else raw.get("lettering", default_lettering),
            panels=panels,
            refs=refs,
            continue_from=cf,
            driver_hidden=bool(raw.get("driver_hidden", False)),
            notes=[str(n) for n in _as_list(raw.get("notes"))],
            guards=[str(g) for g in _as_list(raw.get("guards"))],
            edit=raw.get("edit"),
            description=raw.get("description"),
            output=output,
            raw=raw,
        ))
    spec = Spec(path, path.stem, chapter if isinstance(chapter, int) else None, data.get("title"), out_dir, pages)
    if reg is not None:
        problems = [p for p in lint(spec, reg) if p.startswith("ERROR")]
        if problems:
            raise SpecError("\n".join(problems))
    return spec


def art_path(page: Page) -> Path:
    """Where the unlettered art goes in 'empty' lettering mode."""
    return page.output.with_name(page.output.stem + ".art.png")


def prev_path(p: Path) -> Path:
    return p.with_name(p.stem + ".prev.png")


# Owner, 2026-11-21: ch11-12 at ~8 panels a page felt too dense; ch4 (4.7) and ch8 (6.8) felt right.
# Keep the chapter's panel count, spread it over more pages (about 40), and leave room for big panels.
MAX_PANELS_PER_PAGE = 7
AVG_PANELS_PER_PAGE = 6.0


def lint(spec: Spec, reg: Registry) -> list[str]:
    """Return ERROR/WARN strings for a spec."""
    out = []
    story = [p for p in spec.pages if p.kind == "page" and p.panels and not p.edit]
    if len(story) >= 10:
        avg = sum(len(p.panels) for p in story) / len(story)
        if avg > AVG_PANELS_PER_PAGE:
            out.append(f"WARN {spec.path.name}: {avg:.1f} panels per page on average (owner wants about 5-6); "
                       f"add pages instead of packing them")
    seen = set()
    for pg in spec.pages:
        w = f"{spec.path.name} {pg.label}"
        if pg.key in seen:
            out.append(f"ERROR {w}: duplicate page")
        seen.add(pg.key)
        if pg.lettering not in ("ai", "empty", "none"):
            out.append(f"ERROR {w}: lettering must be ai or empty")
        if pg.location and pg.location not in reg.locations:
            out.append(f"ERROR {w}: unknown location '{pg.location}'")
        if pg.kind == "page" and not pg.panels:
            out.append(f"ERROR {w}: no panels")
        if pg.kind == "page" and len(pg.panels) > MAX_PANELS_PER_PAGE and not pg.edit:
            out.append(f"WARN {w}: {len(pg.panels)} panels on one page (owner wants at most {MAX_PANELS_PER_PAGE}, about 5-6 on average); "
                       f"split it over more pages")
        if pg.kind == "plate" and not pg.location:
            out.append(f"ERROR {w}: plate needs a location")
        for r in pg.refs:
            if not (REPO / r["path"]).exists():
                out.append(f"WARN {w}: extra ref missing: {r['path']}")
        if pg.continue_from and not spec.page_by_number(pg.continue_from):
            out.append(f"WARN {w}: continue_from page {pg.continue_from} not in this spec")
        for pn in pg.panels:
            pw = f"{w} P{pn.index}"
            ids = [c.id for c in pn.cast]
            if pn.location and pn.location not in reg.locations:
                out.append(f"ERROR {pw}: unknown location '{pn.location}'")
            for c in pn.cast:
                if c.id in reg.characters:
                    ch = reg.characters[c.id]
                    if c.outfit and c.outfit not in ch.get("outfits", {}):
                        out.append(f"WARN {pw}: outfit '{c.outfit}' not in cast.yaml for {c.id} (used as free text)")
                elif c.id not in reg.cars:
                    out.append(f"ERROR {pw}: unknown cast id '{c.id}'")
                else:
                    views = reg.cars[c.id].get("views", {})
                    if c.view and c.view not in views:
                        out.append(f"ERROR {pw}: car view '{c.view}' not in cast.yaml for {c.id} (have: {', '.join(views) or 'none'})")
                    if is_exterior_car(c, reg) and not c.camera and not pg.edit:
                        out.append(f"WARN {pw}: exterior shot of {c.id} without `camera:` (the model copies the car sheet's pose; give every car shot its own angle)")
            speakers = []
            for d in pn.dialogue:
                if d.speaker not in reg.characters and d.speaker != "unknown":
                    out.append(f"ERROR {pw}: unknown speaker '{d.speaker}'")
                if d.speaker not in ids and not d.offpanel:
                    out.append(f"WARN {pw}: speaker '{d.speaker}' not in panel cast (treated as off-panel)")
                if d.speaker not in speakers:
                    speakers.append(d.speaker)
            people = [i for i in ids if i in reg.characters]
            if len(speakers) > 1 and len(set(people) & set(speakers)) > 1:
                out.append(f"WARN {pw}: two on-panel speakers ({', '.join(speakers)}): speaker-swap risk, consider splitting")
        for ref_page in car_shot_ref_pages(pg, spec, reg):
            out.append(f"WARN {w}: has an exterior car shot and passes {ref_page.label} as a reference, which also has one "
                       f"(the model copies the car pose); use a location plate or an interior page instead")
    return out


def car_shot_ref_pages(pg: Page, spec: Spec, reg: Registry) -> list[Page]:
    """Pages of this spec passed as references (continue_from / refs) that also show a car from outside,
    when this page shows one too. Edit sources (the page itself) don't count."""
    def exterior(p: Page) -> bool:
        return any(is_exterior_car(c, reg) for pn in p.panels for c in pn.cast)

    if pg.kind != "page" or not exterior(pg):
        return []
    hits = []
    if pg.continue_from:
        prev = spec.page_by_number(pg.continue_from)
        if prev and prev is not pg:
            hits.append(prev)
    for r in pg.refs:
        rp = (REPO / r["path"]).resolve()
        for other in spec.pages:
            if other is not pg and rp in (other.output.resolve(), art_path(other).resolve()):
                hits.append(other)
    return [h for h in hits if exterior(h)]


def rel(p: Path) -> str:
    """Repo-relative path for display; absolute when outside the repo."""
    try:
        return str(Path(p).resolve().relative_to(REPO))
    except ValueError:
        return str(p)
