# Chapter 11 review

**Status: 16 of 30 pages drawn and lettered (p01-p16); p17-p30 not drawn yet, and p15 needs one panel redrawn.** The Codex image limit was hit at 19:22 on 19 Nov 2026 (`usage_limit_reached`, `resets_at` 1795192578 = **Fri 20 Nov 2026, 17:36** German time). No PDF was built, so no half chapter lands in the documents folder.

After the reset:
1. `production/az run -c 11 -p 17-30 -j 4 --attempts 1` (the spec is ready and linted; every page is at 5 references or fewer).
2. Recreate the p15 source (page-15.art.png with the top-left panel filled grey, see `production/chapter-011-fixes.yaml`), run `production/az run -c chapter-011-fixes -p 15 --no-letter --attempts 1`, paste the new top-left panel back into `artwork/pages/chapter-011/page-15.art.png`, then `production/az letter -c 11 -p 15`.
3. Review, then `./tools-build.sh 011`.

Script: `scripts/chapter-011.md` ("Eleven", adapts all of novel Vol. 1 Ch. 7 "Clutch"; generated from the spec). Spec: `production/chapter-011.yaml`; plate: `production/chapter-011-plates.yaml`; panel fixes: `production/chapter-011-fixes.yaml`.

Drawn 2026-11-19, 17 image calls so far:
- 1 reference: the cleared back lot at sunrise (`artwork/locations/tanabe-backlot.png`): crushed-car stacks on three sides, the corrugated fence on the right, forklift stripes in the dew. New locations `tanabe-backlot` and `hardware-shop` (no plate; the shop is described in words).
- 16 pages, one take each (about 125 panels).
- No new character sheets: Akane's daylight outfit, Sota's pajamas with two cardigans, Dai's Sunday jacket and Mom's half-up hair are free-text outfits on the existing sheets.
- Builder fix (`production/aztools/build.py`): a page now attaches one Roadster crop per angle, so a cabin page with one exterior shot gets both the interior crop and the right exterior crop (before, only the first view on a page was attached).

Every drawn page was reviewed on its own, then in pairs and on overview sheets (`production/runs/contact-chapter-011/overview-{01-10,11-20,21-30}.jpg`, two rows of five, read right to left).

## Fixed by hand (no image calls)
- **p14 P3:** the wide panel came out as an exterior side view with Akane in the near seat while the car's front pointed right, which put her in the driver's seat. The panel was mirrored, so the car now shows its LEFT (passenger) side, front to the left, with Akane in the near seat.
- **p03 bottom row:** the drawn panels came out as Dai, Mom at the fusuma, Mom standing, so Dai's silent beat would have come before Mom's line. Dai's panel now has "SHE KEPT HER VOICE DOWN.", and her bus line is split over the two balloons in the drawn order (every word kept): "HE ASKED ME ON THE BUS" / "IF THE HOSPITAL WAS FREE. HE SAID YOU TOLD HIM IT WAS."
- **Stray empty caption boxes** were filled from the novel: p08 "COMING SLOWLY OVER THE SHELLS AND THE POTHOLES, IN FIRST GEAR."; p12 "THE SEAT RAN BACK ON ITS RAILS AND HIT THE END."; p13 "THE BACKREST CAME UP TWO CLICKS."
- **p07:** the letterer mapped the captions to the wrong panels (it found one panel instead of seven). Every caption is now pinned by hand.

## Still to redraw
- **p15 P2 (top-left):** Akane is drawn behind a steering wheel, which puts her in the driver's seat. A one-panel redraw is set up (her in the left seat, no wheel in front of her).

## Lettering
- Hand-placed or painted balloons and boxes where the drawn ones were too small or got mapped wrongly: p01, p02, p03, p04, p05, p06, p07, p08, p11, p12, p13, p14, p15, p16.
- Every line is 20 px or larger, going by the letterer reports for all 16 pages.
- Trimmed to fit at 20 px: p05 Sota "YOU HAVE TO ASK IT, THOUGH. IT'S ITS NAME." (lost "WHICH ONE. YOU CAN'T JUST PICK FOR IT."); p14 Dai's bypass answer (lost "LEVER INTO THE LOWER GEAR" and "QUICK", and the caption "I DIDN'T HAVE TO THINK..."); p15 lost "LOOSE IN THE MIDDLE, THE WAY THE BOOK SAID."; p16 trimmed the engine caption and the red-lights caption.
- Speakers were checked against the art on every page: right-to-left order, one speaker per panel, tails on the speaker. Fumie's "ONE." is a voice from off panel, as in the novel.

## Checks (p01-p16)
- **Seats:** Dai drives from the RIGHT seat and Akane sits on the LEFT in every cabin shot: through the windshield Dai is on the image left (p11, p16), from behind on the image right (p12, p14). The one exception is p15 P2 (to be redrawn).
- **Gloves:** Dai's are white cotton, still creased on p10 and on from p10 P7. Akane's are black and fingerless. On p11 the glove on the roof is drawn a little like a wrap.
- **Dai:** short hair throughout. Station jacket on Friday; summer shirt on Saturday; grey zip jacket over a white T-shirt on Sunday. The pink line on his left palm shows on p02 and p10.
- **Light:** night at the station; grey dawn under the canopy (p02); daylight on Saturday; 7 p.m. dark window (p04); night (p05); dawn sheds and the sun out of the sea at the silos (p06); low clear morning sun at Tanabe's from p06 on.
- **The lot:** p07 and p11 match the plate. The forklift is at the near corner by the fence, and the car stands in the middle with its nose to the far wall.
- **Car shots, no repeated pose:** front three-quarter of the left flank through the gate (p08); high from the office stair (p08); from behind, turning round the stacks (p10); bird's-eye (p11); head-on with Akane crossing (p11); flat side view of the left flank (p14, mirrored); low front-left with the nose dipping (p16). Wheel and sill close-ups on p08.
- **Clocks and money:** no clocks are shown. The shop shows only the price cards 780 and 98, plus one 100-yen coin. No banknotes.
- No brand logos and no readable signs, except a tiny emblem on the Roadster's nose on p08 and p16.

## Kept nits
- p08 top-left and p16 lunge are both front three-quarter views of the left flank. One is mid-distance at eye level by the crusher, the other low and close with the nose diving. Different enough to keep, but close.
- p13: Akane's close-ups in P1 and P3 are almost the same shot.
- p14 P3: after the mirror, the corrugated fence is behind the car on the left of the panel. The geography is flipped there; the seats are right.
- p06: the lane behind the fish sheds is wet (dry morning in the novel).
- p09: Fumie says "TWO YEARS, GIRL" sitting on her crate (the novel has her stand up).
- p05: Dai wears a black T-shirt in the card panels (the summer shirt was scripted).
- Unscripted SFX: p10 RUMBLE.
