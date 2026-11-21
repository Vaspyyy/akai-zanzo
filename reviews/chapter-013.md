# Chapter 13 review

Build: `./tools-build.sh 013` -> `build/akai-zanzo-ch013.{cbz,pdf}` (46 pages), copied to `~/Dokumente/Akai Zanzō/Manga/Ch 13 - Twenty Yen.pdf`.
Script: `scripts/chapter-013.md` ("Twenty Yen", adapts all of novel Vol. 1 Ch. 9 "Type R"; generated from the spec). Spec: `production/chapter-013.yaml`; references: `production/chapter-013-refs.yaml`.

**The first chapter in the new layout** (the creator's request of 21 Nov): 46 pages, 256 panels, 5.6 panels a page, never more than 7 (Ch12 was 8.0). Every scene opens wide; there are 3- and 4-panel pages (p6, p15, p20, p43, p46) and half-page panels for the laugh at Fujita's (p15), the white car turning in (p43) and "You're a bad liar, Hayama-kun." (p46).

Drawn 2026-11-21 from 18:12, 53 image calls in all, no usage limit hit:
- 7 references (7 calls): one-character sheets for Kazue Sasaki (`character-sheets/kazue.png`, built on her ch10 panels), Ken Sasaki (`ken.png`), Mai Sasaki (`mai.png`) and the Type R driver (`typer-driver.png`); the white Integra Type R (`car-sheets/integra-dc2.png` with hand crops `-front34`, `-side`, `-rear`); the Mini 4WD props (`car-sheets/mini4wd.png`: Sota's blue car, Ken's red one, the tackle box); the Fujita's hobby shop plate (`locations/fujita-hobby.png`).
- 46 pages, one take each (46 calls), no redraws.
- New cast: `ken`, `mai`, `fujita`, `ishiguro`, `nobu_father`, `typer_driver`; `ward_mother` (Kazue) now has a sheet and a `cardigan` outfit; cars `integra`, `sota_car`, `ken_car`, `burnt_roadster`. New locations `fujita-hobby`, `covered-street`, `ishiguro-body-shop`, `river-road`, `kawamata-ramen`.

Every page was reviewed on its own, then in pairs on overview sheets (`production/runs/contact-chapter-013/overview-{01-10,11-20,21-30,31-40,41-46}.jpg`, two rows of five, read right to left).

## Redrawn
None. No page had a story-breaking error.

## Lettering
- Hand-placed or painted balloons and boxes on p02, p06, p12-p14, p16, p17, p19, p22, p24-p26, p29, p35, p36, p39, p43-p45, where the drawn ones were small, overlapping or missing. Every line is 20 px or larger (letterer reports for all 46 pages).
- p19: the model left out the top-right caption box; "KEN DIDN'T HEAR HER..." is painted in.
- p36 was drawn with 5 panels: the spec now matches it. Dai's "TANABE-SAN'S. TILL I'VE PAID FOR IT." is a voice from off panel in the door panel, then Nobu "DOES IT GO?" and Dai "NO. NOT YET." in the bottom row (the model had given Dai's line to Nobu's face).
- p02: Sota's lines are rebalanced over his two balloons ("MAI-CHAN. SHE'S FIVE." moved to the second), and "IN THE COVERED STREET" is dropped (p06 shows the covered street).
- Speakers were checked against the art on every page: right to left, one speaker per panel, tails on the speaker. Kazue's memory lines over Mom asleep (p17), Akane's "HARDER." in the pedal close-ups (p22) and "THREE. NO MORE." (p23) are voices from off panel.

## Checks
- **Seats:** Akane drives from the right at the pump (p4, p41, p42). In the lesson Dai is behind the wheel in the RIGHT seat and Akane on the LEFT in every cabin shot (p22-p27). The Type R driver sits on the right (p44-p46).
- **Car shots, no repeated pose:** red Roadster p3 far lights, p4 front three-quarter at the pump and the windshield view, p5 high rear three-quarter leaving, p21 far front three-quarter down the lane, p22 rear three-quarter at the stack, p24 bird's-eye along the fence, p26 front three-quarter by the tire, p27 far in the gate, p41 high at the pump, p42 far on the road. Type R p43 far lights and the low front three-quarter turning in, p44 driver's window and rear three-quarter at the filler, p46 rear three-quarter pulling away. Burned white Roadster p32. Blue wreck p28 (rear through the stack gap, torn top, cat), p36 (front three-quarter, white fender, steel wheels).
- **Toys:** Sota's blue car with its flat white rollers and Ken's red car with holes stay on model; the coins sit under the nose from p12 on, and the car lies upside down at dinner (p20).
- **Dai:** short hair throughout; the station cap ON up to p42, then on the counter, BAREHEADED with the HAYAMA name tag on p43-p46. Taped sneakers in the lesson (p21, p27). School gakuran on Monday.
- **The Sasakis:** Kazue matches her ch10 look (curly perm, cardigan, red knuckles); Mai's puffy cheeks, mask and lollipop; Ken's scalp-short hair and tackle box. They look nothing like the Hayamas.
- **The Type R driver** is planted, not announced: no name, no caption about who he is; polite and precise (hands at nine and three, counting the change again).
- **Brands:** no logos on the white car, no "TYPE R" lettering (the caption says it), the floor paper is plain. The only readable words: FUJITA (apron), SANKO BRAKE INDUSTRIES and SANKO, TANABE AUTO DISMANTLING, HAYAMA, the 280/350/600 price stickers. Banknotes on p29 and p44 are 1995 Fukuzawa notes.
- **Light:** Thursday night kitchen, midnight and 2 a.m. canopy, Saturday shop light, 6 p.m. dark kitchen, Sunday morning lot, 10 p.m. station, Monday daylight to orange 4:45 sun and dusk, 7 p.m. ramen shop, Thursday night phone box, 2 and 4 a.m. canopy.

## Kept nits
- p40-p41: it is raining at the phone box and the forecourt is wet (dry in the novel).
- p04 bottom and p41 top: Dai stands on the passenger side of the red car instead of at her window.
- p32: the Sanko gate already shows on the river road before the two boys reach it on p33.
- p37: the cat sits on a white Corolla's hood, not on the wreck's primer hood.
- p29: the eight 1,000-yen notes look like 10,000-yen Fukuzawa notes.
- p10: Mai wears her mask under her chin, the caption says "in a white mask".
- p14: a boy who looks like Sota stands among the waiting boys.
- p20: the clock reads 7:00 in the rice panel (about 6:30 in the novel).
- p21: the dawn reads as full daylight.
- p42: the far car shows headlights, not taillights.
- p44 and p46: both rear shots of the Type R are three-quarters from behind-left (one close at the pump, one far on the road).
- p43: the two stacked captions touch.
- p12: the palm close-up doesn't show the pink line.
- Unscripted SFX: VROOM (p03), WHIRRRR (p11, p15, p16, p18), SQUEAK and THUNK (p22), BRRRM! (p25), CLICK (p30), CLACK (p38).
