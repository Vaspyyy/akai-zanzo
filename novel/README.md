# Akai Zanzō: the light novel

The story is written first as a light novel that runs ahead of the manga; the manga then adapts finished novel chapters [CANON]. First person (Dai), past tense. Book I is long: about 7 volumes of 10-12 chapters, 5,000-7,000 words each. It is a personal reading project for the creator, not for publication.

No single helper can hold the whole story, so the novel runs on a writers' room of small files that every writer loads.

**Status:** foundation only. `OUTLINE.md` and `STYLE.md` wait for the creator's approval. **Write no chapters until he approves them.**

## Files

```
novel/
  README.md            this workflow
  OUTLINE.md           the map: Book I volumes, setups and payoffs, cast, current volume chapter by chapter
  STYLE.md             the voice coach, AI-prose don'ts, sample passage
  LEDGER.md            current facts: date, age, money, secrets, cars, injuries, open threads
  summaries/
    manga-ch01.md ...  "previously on" recaps of manga chapters 1-3
    v01-ch01.md ...    one recap per novel chapter (200-300 words + "State at end")
  volume-01/
    chapter-01.md      the text ("# Chapter 1: Title" on line 1)
    chapter-01.plan.md the writer's scene plan (kept, short; useful for the manga later)
    images/            illustrations, added later
  build-epub.sh        builds a volume's EPUB into ../build/ (not committed)
```

Outside `novel/`: `STORY_BIBLE.md` (canon labels), `continuity/` (character, car and place facts), `scripts/` (manga scripts). Don't edit `production/`, `artwork/` or `scripts/` from novel work.

## Per chapter

1. **Load.** A fresh writer gets: `STORY_BIBLE.md`, `OUTLINE.md`, `STYLE.md`, `LEDGER.md`, every file in `summaries/`, and the previous two chapters in full.
2. **Plan.** Write `chapter-NN.plan.md`: 3-6 scenes, each with place, time, who, what changes, and the closing image. Check it against the chapter's paragraph in `OUTLINE.md` and against `LEDGER.md` (dates, money, who knows what). Departures from the outline are allowed if they are better; list them at the top of the plan.
3. **Write** 5,000-7,000 words in Dai's voice.
4. **Review.** A separate reviewer, who did not write it, reads it as a reader and reports:
   - where it got boring or where they skimmed;
   - contradictions with `LEDGER.md`, the bible, the summaries or earlier chapters;
   - AI tics and anything on the STYLE don'ts list (including any em dash);
   - voice drift: does Dai still sound like the sample; can you tell speakers apart without tags;
   - in races: was it always clear where the cars were;
   - period errors (1995-97) and car facts.
5. **Fix** what the review found.
6. **Record.**
   - Overwrite `LEDGER.md` with the new state.
   - Add `summaries/vNN-chNN.md`: 200-300 words, then "State at end", then "New PROVISIONAL facts" (any name, date, price or backstory the chapter invented) so the creator can see them.
   - Commit.
7. **Checks before committing:** `grep -rnP '\x{2014}' novel/` (the em dash) finds nothing; `wc -w` is in range.

## Per volume

- After the last chapter, one helper reads the whole volume in one go (60-80k words fits in one context) and edits for continuity, pacing, repeated beats and voice.
- Then update `OUTLINE.md`: write the next volume's chapter-by-chapter plan (the rolling plan), adjust later volumes to what the writing discovered, and show the creator the changes before the next volume starts.
- Record anything the creator approves in `STORY_BIBLE.md` (and `continuity/`), with its label changed to CANON.

## Canon rules

- CANON / PROVISIONAL / PROPOSAL labels follow `STORY_BIBLE.md`. Never quietly promote PROVISIONAL or PROPOSAL to canon.
- If the novel needs something that contradicts canon, stop and ask the creator. Don't rewrite canon silently.
- The novel shows only what Dai sees, hears or is told.

## Building the EPUB

Calibre's `ebook-convert` is installed; pandoc is **not**. One script builds a volume:

```sh
novel/build-epub.sh 1        # -> build/akai-zanzo-novel-v01.epub
```

It joins `volume-NN/chapter-NN.md` in order (skipping the `.plan.md` files), converts the Markdown with Python's `markdown` module (curly quotes only, no dash or ellipsis changes; Calibre's own markdown input if the module is missing), renders `* * *` as a centred scene break, adds a serif stylesheet, a contents page by chapter and the manga's chapter 1 page 1 as the cover. It then checks the book with `ebook-meta` and a round trip to plain text that must contain no em dashes or markdown symbols. Output goes to the top-level `build/`, which is gitignored.

## Illustrations

One or two per chapter, drawn later with the same Codex image pipeline and reference sheets as the manga (`production/`, `artwork/`), in black-and-white manga style. Save them as `volume-NN/images/chNN-1.png` and reference them in the chapter with `![](images/chNN-1.png)`; `build-epub.sh` copies the `images/` folder into the build. Don't run the pipeline from novel work while a manga chapter is being drawn.
