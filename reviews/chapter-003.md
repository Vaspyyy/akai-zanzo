# Chapter 3 review

Build: `./tools-build.sh 003` -> `build/akai-zanzo-ch003.{cbz,pdf}` (28 pages).
Spec: `production/chapter-003.yaml` (empty balloons, lettered by `production/az letter`).

Drawn in two sessions: 10 pages on 2026-11-14 (then the Codex image quota ran out), the other
18 plus fixes on 2026-11-15 (31 image generations: 20 pages in one batch, then 3 edit passes).
Every page was reviewed on its own, then in consecutive pairs for camera continuity
(contact sheets in `production/runs/contact-chapter-003/ch3-overview-{1,2,3}-of-3.jpg`).

## Problems found and fixed
- **Empty balloons on a silent page** (p07): edited out; the road is dry now.
- **Car pointing the wrong way** (p21 last panel): edited so the front points LEFT like the other side views.
- **Pop-up headlights lit while folding down** (p21 middle panel): a second edit made every lamp dark.
- **Empty driver's seat while driving** (p16 and p19, windshield shots): the model drew the wheel
  with nobody holding it. Edited to add Akane's gloved hands, sleeves and shoulder; the spec now
  says so in those panels.
- **Lettering too small for a phone** (p23 P1 at 17 px, p28 P3 at 15 px, p28 P2 at 21 px): fixed
  without new images. `letter.py` gained `draw: true` / `tail:` for manual boxes: it paints a
  bigger balloon over the drawn one. p23's long line is split over two of Dai's balloons
  (centre first, then left; every word kept), now 25-26 px; p28 is 24-26 px.
- **More than 5 references** (p14, p25, p26 would have had 6 once their previous page existed):
  p14 and p25 dropped an extra location plate from one panel (the previous page covers it),
  p26 dropped `continue_from` and states the camera side in its notes instead.

- **The same car picture four times** (reader complaint, 2026-11-15): p15's bottom panel, the
  p18 splash and p26's bottom panel all showed one flat side view (front left, pop-ups up, spray
  behind), copied from the car sheet's side view and passed on through `continue_from`. Redrawn:
  - p15 bottom: high rear three-quarter from above, the car curving up the on-ramp to the upper
    right with taillight trails (edit of that panel only; the top panels are the approved pixels).
  - p18 splash: low angle from the outside of the curve, front three-quarter on the driver's
    flank, a real drift (body angled to its path, front wheels countersteering, spray and tire
    tracks), the overpass looming above. Second of two takes; the first had too little drift.
  - p26 bottom: close beside the driver's door, Akane's half smile readable, the car pulling away
    with its front to the RIGHT (corrected rule). The unscripted "VROOM" is gone.
  New refs: angle-specific crops of the car sheet (`red-roadster-front34.png`, `-rear.png`,
  `-interior.png`); none of the jobs got a page with an exterior car shot. Checked against the
  neighbours: p18 is wet like p17/p19, and no two exterior car shots in the chapter share a pose
  (closest pair: p15 and p21 P1 both drive away toward the upper right, but from high above on a
  curved ramp vs. shoulder height on the pier lot).

## Lettering
All lines placed in the right balloons, in right-to-left order, tails on the speaker. Type is
24-29 px everywhere except p28's end caption (18 px, `style: small` on purpose).

## Kept nits
- **Wet pavement on a dry night** (p06, p08-p11, p13-p15, p18, p21, p25, p26 P1): all three night
  location plates (station, harbor road, pier lot) are drawn wet, so the pages copy it. p07 is dry.
  Redraw the plates dry before the next dry-night scene.
- p02: the walk home looks like midday, the script says dawn.
- p04, p05, p28: night outside the window in morning scenes.
- p05: Michiko kneels on the tatami with sneakers on; p28: Dai wears sneakers on his futon.
- p06: unscripted "SCRUB SCRUB SCRUB" SFX. p28: unscripted "SHIFT" / "HEEL TOE" labels.
- p08, p10, p11: close-ups through the driver's window show the car's front pointing RIGHT,
  while p07/p09 side views point LEFT (see the note below).
- p12: Dai wears a small earring in the middle-left panel.
- p17: the heel-and-toe reads mostly through the BWAP SFX.
- p18: the car has just come out from under the overpass rather than being right under it.
- p22: Dai has no cap in P3.
- p23: P1 is a front view drawn so that Akane still reads on the RIGHT; the sea shows through
  the back window although the car faces it.
- p25: taillights glow with the engine off; Dai is not visible beside Akane in P2.

## Note for the art rules
The rule "front points LEFT, so we see its right (driver) side" is geometrically reversed: a car
whose nose points to the image's LEFT shows its LEFT side (like a face turned left shows the left
cheek). Pages that follow the rule show a mirror-image car (driver and fuel door on the near
side). The chapter follows the rule consistently, as instructed; whether to change it for later
chapters is the owner's call.
