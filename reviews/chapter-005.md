# Chapter 5 review

Build: `./tools-build.sh 005` -> `build/akai-zanzo-ch005.{cbz,pdf}` (30 pages), copied to the documents folder.
Script: `scripts/chapter-005.md` (adapts light novel Vol. 1 Ch. 2, "Second Term"). Spec: `production/chapter-005.yaml`.

Drawn on 2026-11-16 in one session: 65 image generations in all.
- 5 references: Hotta-sensei's sheet (`character-sheets/hotta.png`, made from approved ch4 p13/p5 panels, now in
  `cast.yaml`), and plates for the gym, the school corridor, the shoe lockers and the canal past the driving school.
- 30 pages (about 170 panels), then the redraws and edits below.
- New cast entries without sheets: the principal, Okuda, the girl with the bank sheet, the learner and the instructor,
  the driving-school sedan; new outfits for Sota (pajamas, school) and Aya (tank top).

Every page was reviewed on its own, then in consecutive pairs and as overview sheets
(`production/runs/contact-chapter-005/ch5-overview-{01-10,11-20,21-30}.jpg`, read right to left).

## Redrawn or edited
- **p28** (whole page, 2nd take): the 1st take drew Akane standing outside the car and swapped two speakers. The spec
  now says three rows, Dai right and Akane left in each row, and that she never leaves the driver's seat.
- **p25** (top-right panel only): the 1st take put the fuel door on the LEFT flank and a stray caption in the panel.
  Redrawn from behind-right with the fuel door on the right rear fender; the other panels are the 1st take's pixels.
- **p29** (top panel and third-row right panel): the driver's seat was empty in the top panel, and Akane stood
  outside the car in the "HOW OLD ARE YOU" panel. Both redrawn with her seated; the rest is the 1st take.
- **p01** (bottom-right panel only): the principal filled the panel, leaving two narrow balloons for his long
  lines. Redrawn smaller, with two wide balloons above him.
- **p20** (2nd take): the 1st job was refused by the image safety filter (no image), probably the close-ups of a
  child's bare foot with an adult hand on it. Now Sota wears socks and Dai only points and demonstrates.
- **p10, p12**: the 1st jobs failed before drawing (six references; image_gen takes five). The spec now drops
  `continue_from` on p10 and Sota from one p12 panel.
- **p02** (by hand): a kanji stamp (内定) on the bank sheet, painted out to a plain seal.

## Lettering
- Stray empty caption boxes (p04, p09, p13, p17, p29, p30) were filled with lines from the novel instead of
  redrawn: "DOWN ON THE SPORTS GROUND...", "IT ROARED...", "IN THE SQUARE FOR THE NINETEENTH...", "THE THIRD
  TIME, HE CAME OUT OF THE BACK ROOM...", "FOR A LONG TIME SHE DIDN'T SAY ANYTHING...", "SHE DIDN'T LOOK OVER."
- Hand-painted balloons or boxes: p01 (principal x2, last caption), p04 (Hotta x2), p05 (Hotta x2, one was not
  detected), p13 (Aya), p22 (Mom), p23 (Kubo's line split over two balloons, two captions un-overlapped),
  p27 (Dai's long line, "I'VE DONE IT" dropped to fit), p28 (CONGRATU-LATIONS hyphenated in the drawn balloon).
- Type is 19-29 px on nearly every line; a few dense hand-placed balloons sit at 17-19 px (p01, p04, p05, p09 "SANKO."
  is small on purpose; p21 "BRAKE. CLUTCH..." is a murmur, small on purpose).
- All speakers checked against the art: right-to-left order, one speaker per panel, tails on the speaker.

## Checks
- **Akane and the Roadster** appear only on p23-p30. Right-hand drive throughout: Akane at the RIGHT-hand window,
  gear lever to her left (p27), fuel door on the right rear (p25). The camera stays on the driver's side: Dai on the
  image left, Akane at the window on the image right, except the straight-on windshield shot (p25) and the
  overhead (p29, driver's door on the image right).
- **No car pose repeats:** p23 far head-on lamps; p24 high front three-quarter of the right flank, then a hood
  close-up with lamps folding; p25 rear three-quarter from behind-right, a mirror close-up, straight-on front;
  p29 top-down; p30 small from behind, pulling away left. The rest are window, door and interior close-ups.
  The driving-school sedans (p8) are far, low-rear, windshield and footwell shots.
- Hotta matches his new sheet on every page; Nobu matches his; Okuda and the bank girl look like nobody else.
- Dry nights everywhere except p17's sideways rain (as in the novel).

## Kept nits
- p15 top and p18 bottom: the windows are dark for Saturday afternoon and 6:50 a.m.
- p19-p21: the pedal row is drawn in a slightly different order from panel to panel (the phone book is sometimes
  open, the dictionary sometimes looks like a second book).
- p22: the receipt close-up shows unrelated sums (as in ch4).
- p20 top: the open book on the left is a second dictionary.
- p27 top and p30 top-left: two similar profile shots of Akane in her window (same spot, a few minutes apart).
- Unscripted SFX: p11 CLACK, p27 CLACK.
