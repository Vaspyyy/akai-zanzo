"""Run image jobs through `codex exec`, place results, log provenance."""
from __future__ import annotations

import glob
import hashlib
import json
import os
import re
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from PIL import Image

from .build import Job, load_template
from .spec import PROD, REPO, art_path, prev_path, rel

MODEL = "gpt-6.1-terra"
EFFORT = "medium"
TIER = "default"  # never priority
CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
RUNS = PROD / "runs"
LOG = PROD / "logs" / "provenance.jsonl"
PROVENANCE_MD = REPO / "artwork" / "PROVENANCE.md"
MAX_PARALLEL = 6
_lock = threading.Lock()


def codex_cmd(workdir: Path, last_msg: Path) -> list[str]:
    return [
        "codex", "exec",
        "-m", MODEL,
        "-c", f'model_reasoning_effort="{EFFORT}"',
        "-c", f'service_tier="{TIER}"',
        "--skip-git-repo-check",
        "-C", str(REPO),
        "--json",
        "-o", str(last_msg),
        "-",  # prompt on stdin
    ]


@dataclass
class Result:
    job: Job
    status: str = "pending"  # ok | failed
    out: Path | None = None
    art: Path | None = None
    workdir: Path | None = None
    thread_id: str | None = None
    generations: int = 0
    refs_passed: list[list[str]] = field(default_factory=list)
    revised_prompts: list[str] = field(default_factory=list)
    size: tuple[int, int] | None = None
    seconds: float = 0
    warnings: list[str] = field(default_factory=list)
    reply: str = ""
    letter_report: str = ""


def log(msg: str):
    with _lock:
        print(msg, flush=True)


def find_rollout(thread_id: str) -> Path | None:
    hits = glob.glob(str(CODEX_HOME / "sessions" / "**" / f"rollout-*{thread_id}.jsonl"), recursive=True)
    return Path(hits[0]) if hits else None


def parse_rollout(path: Path, res: Result):
    """Read which references image_gen really got, and how many images it made."""
    for line in open(path, encoding="utf-8"):
        if "image_gen" not in line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        p = rec.get("payload", {})
        if p.get("type") in ("custom_tool_call", "function_call"):
            code = p.get("input") or p.get("arguments") or ""
            if "imagegen" in code:
                m = re.search(r"referenced_image_paths\"?\s*:\s*(\[[^\]]*\])", code)
                if m:
                    try:
                        res.refs_passed.append(json.loads(m.group(1)))
                    except json.JSONDecodeError:
                        res.refs_passed.append([m.group(1)])
                else:
                    res.refs_passed.append([])
        if p.get("type") == "item_completed":
            it = p.get("item", {})
            if it.get("kind") == "image_gen.generation" and it.get("status") == "completed":
                res.generations += 1
                if it.get("revisedPrompt"):
                    res.revised_prompts.append(it["revisedPrompt"])


def run_one(job: Job, batch_dir: Path, attempts: int, tpl: dict, letter: bool) -> Result:
    res = Result(job)
    pg = job.page
    wd = batch_dir / pg.key
    wd.mkdir(parents=True, exist_ok=True)
    res.workdir = wd
    staging = wd / "result.png"
    prompt = job.codex_prompt(staging, attempts, tpl)
    (wd / "prompt.txt").write_text(prompt, encoding="utf-8")
    (wd / "image_prompt.txt").write_text(job.image_prompt, encoding="utf-8")
    last = wd / "last.txt"
    t0 = time.time()
    log(f"[{pg.label}] started ({len(job.refs)} refs)")
    try:
        with open(wd / "events.jsonl", "w") as ev, open(wd / "stderr.txt", "w") as er:
            proc = subprocess.run(codex_cmd(wd, last), input=prompt, text=True, stdout=ev, stderr=er,
                                  timeout=25 * 60, cwd=REPO, stdin=None)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        rc = -1
        res.warnings.append("codex exec timed out after 25 min")
    res.seconds = round(time.time() - t0, 1)
    for line in open(wd / "events.jsonl", encoding="utf-8", errors="replace"):
        if '"thread.started"' in line:
            try:
                res.thread_id = json.loads(line).get("thread_id")
            except json.JSONDecodeError:
                pass
            break
    if last.exists():
        res.reply = last.read_text(encoding="utf-8", errors="replace").strip()
    if res.thread_id:
        ro = find_rollout(res.thread_id)
        if ro:
            parse_rollout(ro, res)
    if not staging.exists() and res.thread_id:
        cands = sorted(glob.glob(str(CODEX_HOME / "generated_images" / res.thread_id / "*.png")), key=os.path.getmtime)
        if cands:
            res.warnings.append("agent did not copy the image; took its newest generated image")
            staging.write_bytes(Path(cands[-1]).read_bytes())
    if not staging.exists():
        res.status = "failed"
        res.warnings.append(f"no image produced (codex exit {rc}); see {wd}")
        log(f"[{pg.label}] FAILED after {res.seconds}s: {res.warnings[-1]}")
        write_log(res)
        return res

    with Image.open(staging) as im:
        res.size = im.size
    w, h = res.size
    want_portrait = pg.orientation == "portrait"
    if want_portrait != (h > w):
        res.warnings.append(f"orientation mismatch: wanted {pg.orientation}, got {w}x{h}")
    requested = [r.abspath for r in job.refs]
    if res.refs_passed and any(sorted(rp) != sorted(requested) for rp in res.refs_passed):
        res.warnings.append("image_gen got a different reference list than requested (see provenance log)")
    if not res.refs_passed and requested:
        res.warnings.append("could not confirm the references passed to image_gen")

    # place the result
    if pg.lettering == "empty":
        target = art_path(pg)
    else:
        target = pg.output
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        os.replace(target, prev_path(target))
    Path(target).write_bytes(staging.read_bytes())
    res.art = target
    res.out = target
    res.status = "ok"
    if pg.lettering == "empty" and letter:
        from .letter import letter_page
        try:
            rep = letter_page(pg, debug_dir=wd)
            res.out = pg.output
            res.letter_report = rep.summary()
            if not rep.ok:
                res.warnings.append("lettering incomplete: " + rep.summary().splitlines()[0])
        except Exception as e:  # keep the art even if lettering breaks
            res.warnings.append(f"lettering failed: {e}")
    log(f"[{pg.label}] ok in {res.seconds}s, {res.generations} image(s) -> {rel(res.out)}"
        + ("".join(f"\n    ! {w}" for w in res.warnings)))
    write_log(res)
    return res


def write_log(res: Result):
    job, pg = res.job, res.job.page
    rec = {
        "time": datetime.now().astimezone().isoformat(timespec="seconds"),
        "spec": job.spec.path.name,
        "page": pg.key,
        "kind": pg.kind,
        "status": res.status,
        "output": rel(str(res.out)) if res.out else None,
        "art": rel(str(res.art)) if res.art else None,
        "lettering": pg.lettering,
        "model": MODEL, "effort": EFFORT, "service_tier": TIER,
        "refs": [r.path for r in job.refs],
        "refs_passed": res.refs_passed,
        "image_gen_calls": res.generations,
        "seconds": res.seconds,
        "thread_id": res.thread_id,
        "size": res.size,
        "warnings": res.warnings + job.warnings,
        "prompt_sha1": hashlib.sha1(job.image_prompt.encode()).hexdigest()[:12],
        "prompt": job.image_prompt,
        "revised_prompts": res.revised_prompts,
        "agent_reply": res.reply,
        "workdir": rel(str(res.workdir)) if res.workdir else None,
    }
    with _lock:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def append_provenance_md(results: list[Result]):
    rows = []
    today = datetime.now().strftime("%Y-%m-%d")
    for r in results:
        if r.status != "ok":
            continue
        out = r.out.relative_to(REPO / "artwork")
        refs = ", ".join(x.path.removeprefix("artwork/") for x in r.job.refs) or "none"
        notes = f"runner: {r.generations} image_gen call(s)"
        if r.job.page.lettering != "none":
            notes += f", {r.job.page.lettering} lettering"
        if r.warnings:
            notes += "; " + "; ".join(r.warnings)
        rows.append(f"| {out} | {today} | {refs} | generated, not reviewed | {notes} |")
    if not rows:
        return
    text = PROVENANCE_MD.read_text(encoding="utf-8")
    header = "## Runner log"
    if header not in text:
        text = text.rstrip() + (
            f"\n\n{header}\n\nRows appended by `production/az run` (full prompts and refs: "
            "`production/logs/provenance.jsonl`). Change the status by hand after review.\n\n"
            "| File | Date | References given | Status | Notes |\n| --- | --- | --- | --- | --- |\n")
    else:
        text = text.rstrip() + "\n"
    PROVENANCE_MD.write_text(text + "\n".join(rows) + "\n", encoding="utf-8")


def waves(pages: list) -> list[list]:
    """Pages whose `continue_from` page is in the same batch wait for it (its image is a reference)."""
    remaining, out = list(pages), []
    while remaining:
        nums = {p.number for p in remaining}
        wave = [p for p in remaining if not (p.continue_from and p.continue_from in nums and p.continue_from != p.number)]
        if not wave:
            wave = remaining
        out.append(wave)
        remaining = [p for p in remaining if p not in wave]
    return out


def run_batch(pages: list, spec, builder, parallel: int, attempts: int, letter: bool = True) -> tuple[list[Result], Path]:
    """Build and run jobs wave by wave (prompts are built right before each wave)."""
    parallel = max(1, min(parallel, MAX_PARALLEL))
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    batch_dir = RUNS / f"{stamp}-{spec.name}"
    batch_dir.mkdir(parents=True, exist_ok=True)
    tpl = load_template()
    plan = waves(pages)
    log(f"batch {rel(batch_dir)}: {len(pages)} job(s) in {len(plan)} wave(s), {parallel} in parallel, "
        f"{MODEL} / {EFFORT} / tier {TIER}")
    results: list[Result] = []
    for wave in plan:
        jobs = [builder.build(pg, spec) for pg in wave]
        for j in jobs:
            for w in j.warnings:
                log(f"WARN {j.page.label}: {w}")
        with ThreadPoolExecutor(max_workers=parallel) as ex:
            results += list(ex.map(lambda j: run_one(j, batch_dir, attempts, tpl, letter), jobs))
    append_provenance_md(results)
    return results, batch_dir
