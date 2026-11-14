"""Turn a page spec into the codex prompt + reference list."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .spec import PROD, REPO, Page, Panel, Registry, Spec, SpecError

TEMPLATE = PROD / "templates" / "prompt.md"


class _Keep(dict):
    def __missing__(self, k):
        return "{" + k + "}"


def load_template(path: Path = TEMPLATE) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    cur = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.fullmatch(r"## ([a-z0-9-]+)\s*", line)
        if m:
            cur = m.group(1)
            sections[cur] = []
        elif cur:
            sections[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def fill(t: str, **kw) -> str:
    return t.format_map(_Keep(**kw))


@dataclass
class Ref:
    path: str  # repo-relative
    legend: str

    @property
    def abspath(self) -> str:
        return str(REPO / self.path)


@dataclass
class Job:
    page: Page
    spec: Spec
    image_prompt: str
    self_check: list[str]
    refs: list[Ref]
    warnings: list[str] = field(default_factory=list)

    def codex_prompt(self, staging_path: Path, max_attempts: int, tpl: dict) -> str:
        ref_list = "\n".join(f"{i}. {r.abspath}" for i, r in enumerate(self.refs, 1)) or "(none)"
        return fill(
            tpl["job"],
            staging_path=str(staging_path),
            ref_list=ref_list,
            max_attempts=max_attempts,
            image_prompt=self.image_prompt,
            self_check="\n".join(self.self_check),
        )


POS_WORDS = [
    (r"\bwide\b", "full width"),
    (r"\bright\b", "RIGHT side"),
    (r"\bleft\b", "LEFT side"),
]


def humanize_pos(pos: str) -> str:
    s = pos.replace("-", " ").replace("_", " ")
    for a, b in POS_WORDS:
        s = re.sub(a, b, s)
    s = re.sub(r"^(top|middle|bottom)\b,?\s*", r"\1 row, ", s)
    return s.strip().rstrip(",")


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", text)) or 1


class Builder:
    def __init__(self, reg: Registry, tpl: dict | None = None):
        self.reg = reg
        self.tpl = tpl or load_template()

    # ---------------------------------------------------------------- refs
    def _outfit(self, cid: str, outfit: str | None) -> tuple[str, str, str | None, str]:
        ch = self.reg.characters[cid]
        key = outfit or ch.get("default_outfit")
        outfits = ch.get("outfits", {})
        if key in outfits:
            o = outfits[key]
            return key, o["desc"], o.get("ref_note"), o["ref"]
        default = outfits[ch["default_outfit"]]
        return key or "", str(outfit), None, default["ref"]

    def collect(self, page: Page, spec: Spec, warnings: list[str]):
        """Ordered refs plus per-id reference index."""
        refs: list[Ref] = []
        index: dict[str, int] = {}

        def add(path: str, legend: str, key: str | None = None) -> int:
            for i, r in enumerate(refs):
                if r.path == path:
                    if key:
                        index[key] = i + 1
                    return i + 1
            if not (REPO / path).exists():
                warnings.append(f"reference missing on disk: {path}")
            refs.append(Ref(path, legend))
            if key:
                index[key] = len(refs)
            return len(refs)

        if page.edit:
            src = page.edit.get("source") or str(page.output.relative_to(REPO))
            add(src, "the CURRENT version of this page (edit target): keep its layout, style and faces except for the requested change", "edit")

        seen = []
        for pn in page.panels:
            for c in pn.cast:
                k = (c.id, c.outfit)
                if k in seen:
                    continue
                seen.append(k)
                if c.id in self.reg.characters:
                    ch = self.reg.characters[c.id]
                    okey, _, note, ref = self._outfit(c.id, c.outfit)
                    legend = f"character sheet for {ch['name']} ({okey} outfit): match face, hair and clothes exactly"
                    if note:
                        legend += f"; look at {note}"
                    add(ref, legend, f"{c.id}:{okey}")
                    index.setdefault(c.id, index[f"{c.id}:{okey}"])
                elif c.id in self.reg.cars:
                    car = self.reg.cars[c.id]
                    add(car["ref"], f"car sheet for {car['name']}: match its body, wheels and details exactly", c.id)

        loc = self.reg.locations.get(page.location) if page.location else None
        if page.kind != "plate":
            loc_ids = [page.location] if page.location else []
            loc_ids += [pn.location for pn in page.panels if pn.location and pn.location not in loc_ids]
            for lid in loc_ids:
                lo = self.reg.locations[lid]
                plate = lo.get("plate")
                if plate and (REPO / plate).exists():
                    add(plate, f"empty location plate for {lo['name']}: copy its architecture, props and mood", f"loc:{lid}")
                else:
                    srcs = lo.get("sources", [])[:1]
                    if plate:
                        warnings.append(f"location plate not made yet ({plate}); using {srcs} instead (contains people/cars)")
                    for s in srcs:
                        add(s, f"an earlier page showing {lo['name']}: copy ONLY the architecture and setting, NOT its people, vehicles, panel layout or text", f"loc:{lid}")
        elif loc and page.kind == "plate":
            for s in loc.get("sources", []):
                add(s, f"an approved manga page showing {loc['name']}: copy its art style, architecture, props and lighting, but NONE of its people, vehicles, panels or text", "location")

        if page.continue_from:
            prev = spec.page_by_number(page.continue_from)
            if prev and prev.output.exists():
                add(str(prev.output.relative_to(REPO)),
                    "the previous page of this scene: keep the camera on the SAME side as its last panel, same lighting, same setting, same faces",
                    "continue")
            else:
                warnings.append(f"continue_from page {page.continue_from} has no image yet")

        for r in page.refs:
            add(r["path"], r.get("use") or "extra reference")
        if len(refs) > 6:
            warnings.append(f"{len(refs)} reference images: more than 6 can dilute each one")
        return refs, index

    # -------------------------------------------------------------- panels
    def _who(self, cid: str) -> str:
        if cid in self.reg.characters:
            ch = self.reg.characters[cid]
            return f"{ch['name']} ({ch['tell']})"
        return self.reg.cars[cid]["name"]

    def panel_text(self, page: Page, pn: Panel, empty: bool) -> str:
        head = f"PANEL {pn.index} ({humanize_pos(pn.pos)}"
        head += f"; {pn.shot})" if pn.shot else ")"
        lines = [f"{head}: {pn.action}".rstrip()]
        if pn.location and pn.location != page.location:
            lo = self.reg.locations[pn.location]
            lines.append(f"  Location of this panel: {lo['name']}. {' '.join(lo['description'].split())}")
        people = [c for c in pn.cast if c.id in self.reg.characters]
        cars = [c for c in pn.cast if c.id in self.reg.cars]
        if people:
            names = []
            for c in people:
                s = self._who(c.id)
                if c.hidden:
                    s += " [face hidden: silhouette or from behind]"
                if c.note:
                    s += f" [{c.note}]"
                names.append(s)
            only = "ONLY " if len(people) == 1 else ""
            lines.append(f"  In this panel: {only}{'; '.join(names)}.")
        elif not cars:
            lines.append("  No people in this panel.")
        for c in cars:
            car = self.reg.cars[c.id]
            bits = [car["name"]]
            if c.state:
                bits.append(car.get("states", {}).get(c.state, c.state.replace("_", " ")))
            if c.facing:
                bits.append(f"its FRONT points to the {c.facing.upper()} edge of the panel")
            if c.note:
                bits.append(c.note)
            one = car["name"].removeprefix("the ")
            lines.append(f"  Car: {', '.join(bits)}. Only one {one} in this panel.")
        for n in pn.notes:
            lines.append(f"  Note: {n}")

        speakers = []
        for d in pn.dialogue:
            if d.speaker not in speakers:
                speakers.append(d.speaker)
        on_panel = {c.id for c in people}
        if len(speakers) == 1 and len(people) > 1 and speakers[0] in on_panel:
            sp = self.reg.characters[speakers[0]]["name"]
            quiet = [self.reg.characters[c.id]["name"] for c in people if c.id != speakers[0]]
            lines.append(f"  Only {sp} speaks in this panel; {', '.join(quiet)} says nothing.")
        multi = len(pn.dialogue) > 1
        if empty and (multi or len(pn.captions) > 0) and (len(pn.dialogue) + len(pn.captions)) > 1:
            lines.append("  Balloon order: balloon 1 is the right-most (or top-most) one, the next ones follow to its left or below it, in reading order.")
        for i, d in enumerate(pn.dialogue, 1):
            name = self.reg.characters.get(d.speaker, {}).get("name", d.speaker.upper())
            off = d.offpanel or d.speaker not in on_panel
            tail = "tail points off-panel toward where " + name + " is" if off else "tail points at " + name
            where = f", placed {d.at}" if d.at else ""
            style = f", {d.style}" if d.style else ""
            label = f"Balloon {i}" if multi else "Balloon"
            if empty:
                n = words(d.text)
                lines.append(f"  {label} (EMPTY, roomy enough for about {n} word{'s' if n != 1 else ''}{style}): spoken by {name}, {tail}{where}.")
            else:
                lines.append(f"  {label}: {name} says \"{d.text}\" ({tail}{where}{style}).")
        for c in pn.captions:
            where = f", placed {c.at}" if c.at else ""
            if empty:
                n = words(c.text)
                lines.append(f"  Caption box (EMPTY rectangle, roomy enough for about {n} words{where}).")
            else:
                lines.append(f"  Caption box{where}: \"{c.text}\"")
        for s in pn.sfx:
            note = f" ({s.note})" if s.note else (f" ({s.style})" if s.style else "")
            lines.append(f"  Sound effect, hand-drawn{note}: \"{s.text}\"")
        if not (pn.dialogue or pn.captions or pn.sfx):
            lines.append("  No text in this panel.")
        return "\n".join(lines)

    # --------------------------------------------------------------- build
    def build(self, page: Page, spec: Spec) -> Job:
        t = self.tpl
        warnings: list[str] = []
        refs, idx = self.collect(page, spec, warnings)
        loc = self.reg.locations.get(page.location) if page.location else None
        time = page.time or (loc or {}).get("default_time") or "unspecified"
        weather = f" Weather: {page.weather}." if page.weather else ""
        parts: list[str] = []
        check: list[str] = []

        if page.kind == "plate":
            parts.append(t["format-plate"])
            parts.append("STYLE: " + t["style"])
            parts.append(t["lettering-plate"])
            if refs:
                parts.append(fill(t["references"], ref_legend="\n".join(f"{i}. {r.legend}" for i, r in enumerate(refs, 1))))
            parts.append(fill(t["setting"], location_name=loc["name"], location_description=loc["description"], time=time, weather=weather))
            if page.description:
                parts.append("IMAGE: " + page.description.strip())
            rules = [
                "The place is completely EMPTY: absolutely NO people, NO human figures, NO silhouettes, NO reflections of people.",
                "NO vehicles of any kind: no cars, no trucks, no motorbikes, no bicycles, no forklifts. Empty parking spaces and empty road only.",
                "Copy the architecture, props, lighting and screentone style of the reference pages, but none of their people, cars, panel borders or lettering.",
            ] + list(loc.get("guards", [])) + page.guards + page.notes
            parts.append(t["rules-intro"] + "\n" + "\n".join(f"- {r}" for r in rules))
            check += t["self-check-plate"].splitlines()
            return Job(page, spec, "\n\n".join(parts), check, refs, warnings)

        empty = page.lettering == "empty"
        parts.append(t["format-landscape" if page.orientation == "landscape" else "format-portrait"])
        parts.append("STYLE: " + t["style"])
        parts.append(t["lettering-empty" if empty else "lettering-ai"])
        if page.edit:
            keep = page.edit.get("keep")
            parts.append(fill(t["edit"], change=page.edit.get("change", "").strip(),
                              keep=(f" Keep especially: {keep}." if keep else "")))
        if refs:
            parts.append(fill(t["references"], ref_legend="\n".join(f"{i}. {r.legend}" for i, r in enumerate(refs, 1))))
        if loc:
            parts.append(fill(t["setting"], location_name=loc["name"], location_description=loc["description"], time=time, weather=weather))
        else:
            parts.append(f"SETTING: Japan, 1995. Time: {time}.{weather}")

        # cast block: only who is on the page
        cast_lines = []
        done = set()
        car_ids = []
        for pn in page.panels:
            for c in pn.cast:
                if c.id in self.reg.characters:
                    okey, desc, _, _ = self._outfit(c.id, c.outfit)
                    k = (c.id, okey)
                    if k in done:
                        continue
                    done.add(k)
                    ch = self.reg.characters[c.id]
                    cast_lines.append(fill(t["cast-character"], name=ch["name"], traits=" ".join(ch["traits"].split()),
                                           outfit=desc, ref_index=idx.get(f"{c.id}:{okey}", "-")))
                elif c.id in self.reg.cars and c.id not in car_ids:
                    car_ids.append(c.id)
        for cid in car_ids:
            car = self.reg.cars[cid]
            rules = "".join(f"\n  {r}" for r in car.get("rules", []))
            cast_lines.append(fill(t["cast-car"], name=car["name"].upper(), traits=" ".join(car["traits"].split()),
                                   ref_index=idx.get(cid, "-"), rules=rules))
        if cast_lines:
            parts.append(t["cast-intro"] + "\n" + "\n".join(cast_lines))
        else:
            parts.append("CHARACTERS: nobody (no people on this page).")

        parts.append(fill(t["panels-intro"], panel_count=len(page.panels)) + "\n" +
                     "\n".join(self.panel_text(page, pn, empty) for pn in page.panels))

        rules = []
        if "roadster" not in car_ids:
            rules.append("There is NO small roadster or sports car anywhere on this page. If a reference page shows one, do not copy it.")
        else:
            rules.append("The red Roadster is RIGHT-HAND DRIVE. In every side view that shows the driver's side, its FRONT points to the LEFT edge of the panel. Never two Roadsters in one panel.")
        if page.driver_hidden:
            rules.append("The Roadster's driver is NEVER recognizable: the cabin is in deep shadow or behind windshield glare; at most gloved hands and a dark silhouette. Do NOT put Dai or any recognizable face in the driver's seat.")
        rules.append("Draw people and vehicles only where a panel lists them; do not copy people or vehicles from the location references.")
        if page.continue_from and "continue" in idx:
            rules.append(f"This page continues the scene of reference {idx['continue']}: the camera stays on the SAME side as its last panel, with the same lighting and setting.")
        if loc:
            rules += list(loc.get("guards", []))
        rules += page.guards + page.notes
        parts.append(t["rules-intro"] + "\n" + "\n".join(f"- {r}" for r in rules))

        n = len(page.panels)
        check += [fill(x, panel_count=n) for x in t["self-check-page"].splitlines()]
        check += t["self-check-empty" if empty else "self-check-ai"].splitlines()
        check += t["self-check-roadster" if "roadster" in car_ids else "self-check-no-car"].splitlines()
        return Job(page, spec, "\n\n".join(parts), check, refs, warnings)
