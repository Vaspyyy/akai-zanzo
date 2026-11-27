# How this project runs (handoff for a new thread)

Everything that defines the story lives in this repo. A new thread changes nothing about the story, as long as it reads these files first. Updated 2026-11-21.

## State
- **Novel (light novel):** Volume 1, chapters 1-9 written, reviewed and built (`novel/volume-01/`). Next to write: **Ch10** (plan in `novel/OUTLINE.md` §7).
- **Manga:** chapters 1-14 drawn (`scripts/`, `production/chapter-NNN.yaml`, `reviews/`). Ch13 is the first in the new layout (46 pages, 5.6 panels a page). Next to draw: **Ch15**, which adapts novel Ch11 (mapping in `novel/OUTLINE.md` §2: novel V1 chN = manga ch(N+4) from Ch4 on).
- **Builds:** `./tools-build.sh NNN` (manga) and `novel/build-epub.sh` (novel) both copy the results to `~/Dokumente/Akai Zanzō/`.

## Read first
- `STORY_BIBLE.md`: canon, including §8 pacing and page density.
- **The novel:**
  - `novel/README.md`;
  - `novel/OUTLINE.md` (the whole 7-volume plan; **never reveal it to the creator**);
  - `novel/STYLE.md`, especially "Lessons from reviews" in §11;
  - `novel/LEDGER.md` (the facts at the end of the latest chapter);
  - `novel/summaries/`.
- **The manga:**
  - `production/README.md` and `prompts/art-direction.md`;
  - the latest `scripts/chapter-NNN.md`, `production/chapter-NNN.yaml` and `reviews/chapter-NNN.md`.
- `continuity/` (characters, cars, locations, period research).

## The creator's rules
- **One chapter at a time:** start a chapter only after the creator's OK, and don't chain chapters. If the image limit cuts off an approved manga chapter, finishing it by a scheduled run after the reset is fine.
- **No spoilers:**
  - the creator reads mainly the manga, and the novel runs ahead;
  - report a finished novel chapter by its title, length and review outcome only;
  - never reveal outline content.
- **How to reply:** plain, simple English (ELI10), no em dashes, times in German local time.
- **Models:** Claude Opus 5.5 helpers by default. GPT-6.1 Terra (Codex) does reviews and draws the art. It runs a manga chapter only when the creator says Claude usage is low.

## Novel chapter loop
1. **Writer:** an Opus helper (`delegate_task`, claudeAgent, claude-opus-5-5, effort high).
   - Reads everything listed in `novel/README.md` plus the previous two chapters in full.
   - Writes `chapter-NN.md` at 5,000-7,000 words, and does not commit.
2. **Three reviewers in parallel:** Opus, Sonnet (claude-sonnet-5-5) and GPT (codex, gpt-6.1-terra, reasoningEffort high, serviceTier default; tell it "don't end your turn for progress updates").
   - Each reads as a reader first, then lists its problems strictly.
   - Each checks the facts against LEDGER: money, dates, perception, period, mechanics, medicine.
3. **Fixer:** an Opus helper.
   - Starts as soon as the first review arrives; forward the later reviews as messages.
   - **Verify reviewer claims before passing them on.** For example, reviewers often demand 2-3 similes, while STYLE's aim is about 12.
   - Then it updates LEDGER, writes `summaries/vNN-chNN.md`, and adds at most one STYLE lesson.
   - Then it rebuilds, commits only its own paths, and pushes.

## Manga chapter loop
One Opus helper per chapter adapts the novel chapter closely. It writes the script, makes the references, writes the spec, runs `production/az lint` and `az run`, reviews every page singly and in pairs, redraws hard failures, builds, writes the review and pushes.
- **Density:** about 40 pages at 5-6 panels a page, max 7 (lint warns).
- **The car rules:**
  - right-hand drive, with the FRONT pointing RIGHT in a side view that shows the driver;
  - an explicit camera angle and an angle crop for every car shot;
  - never a page with a similar car pose as a ref;
  - Dai drives from the right seat.
- **Max 5 refs per job.**
- **Polling:** helpers must poll their jobs and not end their turn while they wait.
- **Image limits:** about 100 images per 24 h, plus the plan limit, which resets daily at about 17:36-17:40. On `usage_limit_reached`, read the reset time from `production/runs/<batch>/<page>/stderr.txt` or `events.jsonl`. Wait if it's under ~6 h; otherwise commit and report.
- **Gemini stand-in:** a page can be drawn through T3's Antigravity provider (gemini-4-argon) when the creator wants to read now. Mirror its left-to-right panels, resize the page to 1024x1536, then run `az letter`.
- **Before reporting:** check the contact sheets (`production/runs/contact-chapter-NNN*/`) yourself.

## Recurring cast added by the creator
The Sasakis, the ward family from novel Ch6 / manga ch10, return as family friends: see `continuity/characters.md` and `novel/OUTLINE.md` §6.
