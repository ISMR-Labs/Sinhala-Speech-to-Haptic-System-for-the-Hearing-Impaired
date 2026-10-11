# Experiment and build log

| Date | What | Outcome |
|---|---|---|
| 2026-09-20 | Module pod enclosure designed on Forge, v1 to v11 | v11 chosen: 32.5 x 40.5 x 10.1 mm, screw-fit lid, base plate. Earlier versions were too large for the module |
| 2026-09-22 | Controller box designed on Forge | 101.8 x 70.8 x 34.7 mm; box + lid + base plate; printed |
| 2026-09-24 | 17 modules wired on 1 m sleeved leads to an ESP32-S3; chase sketch (`firmware/pin_chase`) | every module vibrates in turn; strapping pins 3/45/46 boot normally with the 3-pin modules attached. Photos and videos in `media/` |
| 2026-10-11 | Parametric mannequin model (`hardware/mannequin`) with the 18 pods, leads and controller box; turntable render for the README | placement at 80 mm pitch visualised front and back |
| 2026-10-10 | Repository created; literature review; encoding v0 designed; vocabulary of 20 words coded; vest controller firmware and host tools written; firmware compiles for ESP32-S3 | no perception data yet; the 18th module and the garment are still to be fitted |

## Open items

- Fit the 18th module (the harness has 17; GPIO 2 is wired for it in the firmware).
- Sew the Velcro grid into the vest and measure the actual pitch on two wearers.
- Add the 470 uF supply capacitor and confirm no brown-out with two motors per frame.
- Flash `vest_controller`, run `chase` from the host, then `text` with a sentence.
- Record the 20 words from 10 speakers and measure ASR accuracy of the candidate Sinhala
  Whisper checkpoints on the closed vocabulary.
- Pilot study with 8 hearing lab members (`study/protocol.md`).
