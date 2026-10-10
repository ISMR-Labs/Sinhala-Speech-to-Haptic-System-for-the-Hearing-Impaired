# Bill of materials

Prices are approximate Colombo retail (tronic.lk and similar), October 2026.

| Qty | Item | Role | Notes |
|---|---|---|---|
| 1 | ESP32-S3 DevKitC (ESP32-S3-WROOM-1, USB-C) | vest controller | 20 free GPIOs used for 18 motors + 2 spare; Wi-Fi to the host |
| 18 | Vibration motor module, 3-pin (VCC, GND, IN) with on-board transistor and 10 mm coin ERM motor | tactors | IN is driven straight from a GPIO; the module's transistor switches the motor. 17 built so far |
| 18 | Printed module pod + lid (`hardware/enclosures/vibration-motor-enclosure`) | holds a module against the skin | PLA+, M2.5 self-tapping screws; inner space 21 x 29 x 8.6 mm |
| 1 | Printed controller box + lid + base plate (`hardware/enclosures/controller-box`) | houses the ESP32-S3, power and the push button | inner 52 x 83 x 32 mm |
| 1 | Momentary push button (panel mount) | manual test / acknowledge | on the controller box |
| 20 m | 3-core wire (VCC, GND, IN per module) in 4 mm nylon braided sleeving | harness | about 1 m per module |
| 18 | 3-pin JST-XH or Dupont connectors | detachable modules | optional but saves re-soldering |
| 1 | 5 V 3 A USB power bank with USB-C output | power | 18 coin motors draw up to about 1.5 A if all run together; worst case is 2 motors per frame |
| 1 | Logic-level MOSFET or 5 V regulator stage | only if modules are powered from a separate battery | not needed with a USB power bank |
| 1 | Sleeveless sports vest or fitted compression shirt, two layers | garment | pods sit between the layers, held by Velcro patches |
| 18 | Velcro patches 40 x 40 mm | module placement | allows the 3 x 3 pitch to be adjusted per wearer |
| 1 | Laptop with microphone (host) | speech recognition | any machine that runs faster-whisper on CPU |

Approximate total without the laptop: LKR 25 000 to 35 000 (USD 80 to 115).

## Notes on the vibration modules

- The common 3-pin modules take 3.3 V logic on IN and switch a coin motor rated 3 V, 60 to 80 mA,
  about 9000 to 12000 rpm (150 to 200 Hz at full voltage). Spin-up is 50 to 100 ms, which sets the
  shortest useful frame length.
- Vibration frequency and amplitude are coupled in an ERM motor, so "level" in the firmware changes
  both. Three distinguishable levels (off, half, full) are a safe assumption; more will need a
  perception test.
- Coin LRAs (linear resonant actuators) at 175 to 235 Hz with a dedicated driver (DRV2605L) would
  give faster onset and independent amplitude, and are the planned upgrade if the ERM modules prove
  too slow or too fuzzy in the study.
