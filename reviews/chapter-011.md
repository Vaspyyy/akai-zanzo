# Chapter 11 review

Build: `./tools-build.sh 011` -> `build/akai-zanzo-ch011.{cbz,pdf}` (30 pages), copied to `~/Dokumente/Akai Zanzō/Manga/Ch 11 - Eleven.pdf`.
Script: `scripts/chapter-011.md` ("Eleven", adapts all of novel Vol. 1 Ch. 7 "Clutch"; generated from the spec). Spec: `production/chapter-011.yaml`; plate: `production/chapter-011-plates.yaml`; single-panel redraws: `production/chapter-011-fixes.yaml`.

Drawn on two days, 34 image calls that made images (plus 5 that failed on the usage limit):
- 19 Nov: the back-lot plate and p01-p16. The Codex limit stopped the run at p17 (19:22; reset Fri 20 Nov 17:36). An early retry at 15:35 on 20 Nov still hit the limit and drew nothing.
- 20 Nov, from 17:38: p17-p30, then 3 single-panel redraws (p15, p18, p27).
- 1 reference: the cleared back lot at sunrise (`artwork/locations/tanabe-backlot.png`): crushed-car stacks on three sides, the corrugated fence on the right, forklift stripes in the dew. New locations `tanabe-backlot` and `hardware-shop` (no plate; the shop is described in words).
- 30 pages, one take each (about 230 panels).
- No new character sheets: Akane's daylight outfit, Sota's pajamas with two cardigans, Dai's Sunday jacket and Mom's half-up hair are free-text outfits on the existing sheets.
- Builder fix (`production/aztools/build.py`): a page now attaches one Roadster crop per angle, so a cabin page with one exterior shot gets both the interior crop and the right exterior crop.

Every page was reviewed on its own, then in pairs and on overview sheets (`production/runs/contact-chapter-011/overview-{01-10,11-20,21-30}.jpg`, two rows of five, read right to left).

## Redrawn or edited
- **p15 P2** (single-panel redraw): Akane was drawn behind a steering wheel. She now sits in the left seat with no wheel in front of her, seen from the driver's side.
- **p18 P3** (single-panel redraw): the shivering car seen through its windshield had Akane behind the wheel on the image left. Redrawn with Dai at the wheel on the image left, Akane on the right.
- **p27 P5** (single-panel redraw): in the big first-roll panel the seats were mirrored, and the forklift stood at the wrong end. Redrawn from on top of the far wall, with Dai at the wheel on the image left and the forklift at the near corner by the fence.
- **p14 P3** (hand edit, no image call): the side view showed Akane in the near seat with the front pointing right, which put her in the driver's seat. The panel was mirrored, so it now shows the passenger side.
- **p03 bottom row:** the drawn panel order put Dai's silent beat before Mom's line. His panel now has "SHE KEPT HER VOICE DOWN.", and her bus line is split over two balloons in the drawn order (every word kept).
- **Stray empty caption boxes** were filled from the novel: p08 "COMING SLOWLY OVER THE SHELLS AND THE POTHOLES, IN FIRST GEAR."; p12 "THE SEAT RAN BACK ON ITS RAILS AND HIT THE END."; p13 "THE BACKREST CAME UP TWO CLICKS."; p20 "SOMETHING CRACKLED UNDER THE FRONT TIRES. ONCE, AND THEN AGAIN."; p24 "HER HAND WENT OUT FLAT AGAINST THE DASH."

## Lettering
- Hand-placed or painted balloons and boxes where the drawn ones were too small or got mapped wrongly: p01-p08, p11-p30 (all except p09 and p10). On p07 every caption is pinned (the letterer found one panel instead of seven).
- p21: the stall caption sits over Fumie on the forklift step, "MIND MY COROLLAS!" over the pitching cabin and "SIX." with Dai turned round, which keeps the novel's order in the drawn layout.
- Every line is 20 px or larger (letterer reports for all 30 pages).
- Trimmed to fit at 20 px:
  - p05: Sota's line lost "WHICH ONE. YOU CAN'T JUST PICK FOR IT."
  - p14: Dai's bypass answer lost "QUICK" and "LEVER INTO THE LOWER GEAR", plus the futon caption.
  - p15: lost "LOOSE IN THE MIDDLE, THE WAY THE BOOK SAID."
  - p16: both captions shortened.
  - p19: dropped "COMING UP THROUGH THE FLOOR".
  - p22: dropped "AND I HADN'T SEEN HER DO IT" and "THE WAY I'D DONE IT ON MY FUTON A THOUSAND TIMES".
  - p26: the bite caption lost "LIKE SOMEONE IN THE NEXT ROOM HAD LEANED ON A TABLE".
  - p28: dropped "FOR A SECOND".
- Speakers were checked against the art on every page: right-to-left order, one speaker per panel, tails on the speaker. Fumie's "ONE.", "FIVE.", "SEVEN." and "EIGHT." are voices from off panel, as are Akane's instructions in the hand and foot close-ups.

## Checks
- **Seats:** after the redraws, Dai drives from the RIGHT seat and Akane sits on the LEFT in every cabin shot. Through the windshield Dai is on the image left (p11, p16, p18, p19, p24, p27, p29); from behind he is on the image right (p12, p14, p21, p22). On p30 Akane is back in the driver's seat.
- **Stall count vs Fumie:**
  - 1 lunge, "ONE." (p16)
  - 2 shaking leg and leap, "TWO." (p17)
  - 3 heel and shiver, "THREE." (p18)
  - 4 third gear, "FOUR." (p19)
  - 5 roll and panic brake, "FIVE." (p20)
  - 6 revs and wheelspin, "SIX." (p21)
  - 7 her handbrake and the squat, "SEVEN." (p22)
  - 8 second gear hammering, "EIGHT." (p22)
  - 9 not remembered, "NINE." with the cat (p23)
  - 10 three hops, "TEN." (p23)
  - 11 the bang (p24), "ELEVEN." (p25, again on p30)
- **Gloves:** Dai's are white cotton, still creased on p10, grey across the palms from p20, with a brown mark on the left palm at the end (p30). Akane's are black and fingerless throughout.
- **Car shots, no repeated pose:**
  - p08: front three-quarter of the left flank at the gate (eye level), and high from the office stair.
  - p10: low from behind, turning round the stacks.
  - p11: bird's-eye of the lot, and a low head-on with Akane crossing.
  - p14: flat side view of the left flank.
  - p16: low at the front-left corner, nose dipping.
  - p18: close head-on, slightly above the hood, through the windshield.
  - p21: ground level straight behind, wheelspin.
  - p23: high oblique of the left flank, three hops.
  - p24: front three-quarter of the right flank from the fence corner.
  - p27: high head-on from on top of the far wall, rolling.
  - p28: far side-on across the far wall, then close side-on to the right flank passing the forklift.
  - p30: far, straight behind, in the gate.
  - Wheel close-ups on p08, p20, p22 and p27.
- **Light:** night at the station; grey dawn under the canopy (p02); Saturday daylight; dark at 7 p.m. (p04); night (p05); dawn sheds and sunrise at the silos (p06); low clear morning sun at Tanabe's from p06 to the end, with the sun in the mirror on p24.
- **The lot:** the plate layout holds: far wall of crushed sedans, older stacks on the left, the fence on the right, the forklift at the near corner by the fence.
- No banknotes (one 100-yen coin on p02). No readable signs. A tiny emblem shows on the Roadster's nose and steering wheel in a few panels.

## Kept nits
- p08 top-left (gate) and p16 (lunge) are both front three-quarter views of the left flank, one at eye level mid-distance, the other low and close. Different enough to keep, but close.
- p11 P3 and p18 P3 are both head-on views of the front; one is empty at bumper height, the other close through the windshield with both of them inside.
- p13: Akane's close-ups in P1 and P3 are almost the same shot.
- p14 P3: after the mirror, the fence shows on the left behind the car (the geography flips there; the seats are right).
- p25 top: the sun is ahead through the windshield, although it sits behind the car in the mirror on p24.
- p26: Dai's gloves look like wraps in the top-right panel.
- p30: the gate opens onto water in the far shot; the end caption sits at the top left of the last panel.
- p06: the lane behind the fish sheds is wet (dry morning in the novel). p09: Fumie says "TWO YEARS, GIRL" sitting on her crate. p05: Dai wears a black T-shirt in the card panels.
- Unscripted SFX: p10 RUMBLE.
