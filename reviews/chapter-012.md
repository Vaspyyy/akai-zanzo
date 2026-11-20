# Chapter 12 review

Build: `./tools-build.sh 012` -> `build/akai-zanzo-ch012.{cbz,pdf}` (**29 pages so far**), copied to the documents folder (`~/Dokumente/Akai Zanzō`).
Script: `scripts/chapter-012.md` ("Timing Belt", adapts all of novel Vol. 1 Ch. 8 "Timing Belt"; generated from the spec). Spec: `production/chapter-012.yaml`; references: `production/chapter-012-cars.yaml`, `production/chapter-012-plates.yaml`; single-panel redraws: `production/chapter-012-fixes.yaml`.

**Page 30 (4 a.m., the dark kitchen, the tooth) is not drawn yet.** Its job hit the Codex usage limit at 20:51 on 20 Nov (`resets_at` = Sat 21 Nov 17:40). Its spec is final: run `production/az run -c 12 -p 30`, review it, rebuild.

Drawn 2026-11-20 from 19:29, about 66 image calls:
- 5 references (9 calls): the wreck's engine bay (`car-sheets/blue-roadster-wreck-engine.png`: as found, then with the cover off and the broken belt), Kubo's green Super Cub with the roped-on red toolbox (`car-sheets/supercub.png`), Fumie's two-ton flatbed with TANABE on the doors (`car-sheets/flatbed.png`, plus a hand crop `flatbed-front34.png`), and plates for Okabe Tire and the staff room (`locations/okabe-tire.png`, `locations/staff-room.png`).
- 29 pages, one take each (about 230 panels), plus 2 single-panel redraws.
- The first batch was cut off at 19:49 after p01, p03 and p04 (its provenance rows were added by hand); the rest ran in a second batch from 20:10.
- New cast: Kubo's own Sunday clothes (`kubo:own`), Okabe in navy overalls (`okabe:overalls`), Hotta in a grey cardigan (`hotta:cardigan`); cars `supercub`, `flatbed`, `okabe_van`; the wreck's `engine` view. New locations `okabe-tire`, `staff-room`.

Every page was reviewed on its own, then in pairs on overview sheets (`production/runs/contact-chapter-012/overview-{01-10,11-20,21-30}.jpg`, two rows of five, read right to left).

## Redrawn
- **p06 P4** (single panel): the starter close-up showed the two bare cam pulleys, which gave away the p08 reveal. Redrawn with the black timing cover still bolted on.
- **p24 bottom-right** (single panel): the forklift lowering the car onto its new tires was drawn in front of Okabe's shop. Redrawn in the yard weeds by the fence, side view of the right flank with the front pointing right.

## Lettering
- Hand-placed or painted balloons and boxes where the drawn ones were small or mapped wrongly on most pages; every line on p01-p29 is 20 px or larger (letterer reports).
- Stray empty boxes filled from the novel: p05 "HE FOLDED THE CAP BACK..." and "THE BLACK ONE WENT ON BARE METAL...", p07 "HE SLID IN UNDER THE FRONT WITH A LONG BAR AND A BIG SOCKET.", p14 "HE PUT THE RAG IN THE TOOLBOX AND SHUT THE DRAWER.", p15 "THE KITCHEN WAS ALL OIL AND NOISE.", p20 "SHE PRESSED THE HORN TWICE.", p25 "WHEN I PUSHED ON THE FENDER, IT ROCKED ON ITS SPRINGS AND CAME BACK."
- Trimmed or split to fit at 20 px:
  - p09: the tensioner line split over two balloons.
  - p14: Kubo's parts list lost "THE SEALS AT THE FRONT" and "TOP AND BOTTOM".
  - p17: "DID YOU ASK IT? ITS NAME?" is one balloon.
  - p22: the slip-sign speech is split and tightened.
  - p23: "CALL IT 11,000. THE 124'S FOR COMING BACK." is set in digits.
  - p26: Hotta's lines are shortened, and Ono-sensei's line moved into the wide staff-room panel.
- Speakers were checked against the art on every page: right to left, one speaker per panel, tails on the speaker. Kubo's lines from under the car and Okabe's lines over the tire close-ups are off-panel.

## Checks
- **The diagnosis** reads as detective work, in order:
  1. the tires and the dry ground (p03);
  2. the dipstick (p04);
  3. the leads (p05);
  4. the wrong starter note (p06);
  5. "Half of it isn't pushing back", then the cam in the flashlight (p07);
  6. the cam doesn't move and the cover comes off (p08);
  7. the bare pulleys, the broken belt and the tooth (p09);
  8. non-interference (p10);
  9. the engine turned by hand (p11).
- **Who holds what:** Kubo has the dipstick, the leads, the bar and the ratchet. Dai has the flashlight (p07-p08), then the bar (p11). The tooth goes into Dai's LEFT palm with the pink line (p09), he looks at it (p10), and it is between his fingers under the car (p12).
- **The car:** two flat tires and cracked sidewalls up to p14; plain rusty steel wheels from p18; standing level on used tires on p25.
- **Car shots, no repeated pose:**
  - p03: bird's-eye.
  - p07: ground level from the left.
  - p14: close on the tires.
  - p18: wide side view of the left flank with the forklift.
  - p24: side view of the right flank with the forklift.
  - p25: low rear three-quarter, then a front three-quarter of the left flank.
  - The red car only as a bumper close-up (p18) and its door at the pump (p17).
  - The truck: high from the office stair, far across the canal, close on its door (p19-p20).
- **Seats:** Fumie drives from the right of the cab, Dai sits on the left (p19). No cabin panel shows both of them.
- **Money:** 1995 notes only: Fukuzawa 10,000 and Soseki 1,000 (p24, p27), plus 100-yen coins.
- **No tire brands:** all sidewalls are plain. The only readable words are FOR LEASE, OKABE TIRE on the van, TANABE on the truck door and the receipt, and HAYAMA on the pay envelope.
- **Mom's peak (p28-p29):**
  - she reads the letter twice, with her finger under the lines;
  - she pushes herself up and stands at the stove with her back to the room, wordless;
  - she turns the gas off, pins the letter to the fridge and presses it twice with her thumb.
  - Her face is never shown at the stove.

## Kept nits
- p11 P1: the front bumper behind Dai looks boxy, not like the Roadster's.
- p23 P1: Dai measures with a round pressure gauge instead of the small tread gauge.
- p27 bottom and p28 big panel: the windows look dark for 4:10-4:15 p.m.
- p23 bottom: Okabe's two balloons graze his eyes.
- p29: Sota lies on the tatami holding his inhaler instead of a comic.
- Unscripted SFX: none of note.
