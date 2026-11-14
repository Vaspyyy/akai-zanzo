# Chapter 3 review (in progress)

Spec: `production/chapter-003.yaml` (empty balloons, lettered by `production/az letter`).

**Status 2026-11-14:** 10 of 28 pages drawn, then the Codex image quota ran out
(`usage_limit_reached`, resets 2026-11-15 14:36 German time). 13 image generations used.

| Page | State |
| --- | --- |
| p01, p02, p03, p04, p06, p12, p23, p27 | accepted |
| p07, p21 | rejected, `edit:` blocks queued in the spec |
| p05, p08-p11, p13-p20, p22, p24-p26, p28 | not drawn yet |

Resume (after the quota resets): `production/az run -c 3 -p 5,7-11,13-22,24-26,28 -j 4`.
p07 and p21 run in edit mode; remove their `edit:` blocks once they pass.

## Problems found
- **More than 5 references fails the job** (p13, p22): `image_gen` takes at most 5
  `referenced_image_paths`. The builder now warns above 5 (was 6); p13 dropped Kubo's sheet
  (he is a tiny figure), p22 dropped the extra pier plate, p08 dropped the ch2 p20 face ref.
- **p07:** the model drew two empty balloons and an empty caption box on a page with no
  text (the letterer has nothing to put in them), and a wet road on a dry night. Edit queued.
- **p21:** last panel's side view has the car's front pointing RIGHT; middle panel's
  headlights stay lit while "folding down". Edit queued.

## Lettering
All placed lines fit their balloons (report from `az letter`). p23 P1 (Dai's long line)
came out at 17 px in 7 lines: small but readable.

## Kept nits
- p02: the walk home looks like midday, the script says dawn.
- p04: night outside the tatami-room window in a morning scene.
- p06: unscripted "SCRUB SCRUB SCRUB" SFX; the forecourt looks wet.
- p12: Dai wears a small earring in the middle-left panel.
- p23: P1 is a front view drawn so that Akane still reads on the RIGHT (strictly a
  left-hand-drive layout); the sea shows through the back window although the car faces it.
