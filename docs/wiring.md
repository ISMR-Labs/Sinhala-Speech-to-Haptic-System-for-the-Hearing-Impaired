# Wiring

## Controller to modules

Each vibration module has three pins. All modules share 5 V and GND from the controller box; each
IN pin has its own GPIO line. The ESP32-S3 drives IN at 3.3 V, which is enough for the module's
NPN/MOSFET input stage.

| Motor index | Position | GPIO | Motor index | Position | GPIO |
|---|---|---|---|---|---|
| 0 | F1 (front, top-left) | 14 | 9 | B1 (back, top-left) | 18 |
| 1 | F2 | 13 | 10 | B2 | 20 |
| 2 | F3 | 12 | 11 | B3 | 47 |
| 3 | F4 | 11 | 12 | B4 | 48 |
| 4 | F5 (front, centre) | 10 | 13 | B5 (back, centre) | 45 |
| 5 | F6 | 9 | 14 | B6 | 40 |
| 6 | F7 | 46 | 15 | B7 | 41 |
| 7 | F8 | 3 | 16 | B8 | 42 |
| 8 | F9 (front, bottom-right) | 8 | 17 | B9 (back, bottom-right) | 2 |

Spare: GPIO 1 and 19. The order is the harness order used in the September 2026 chase test, so
the firmware table matches the cables as built. "Left" and "right" are the wearer's own.

GPIO 3, 45 and 46 are strapping pins read at reset. A 3-pin module input either floats or pulls
slightly low, which is the safe level for all three, so booting is not affected. Do not connect a
bare 2-wire motor directly to those pins.

## Power

- Modules: 5 V rail from the USB power bank, through the controller box. Each coin motor draws
  60 to 80 mA; two motors per frame is the normal case, 18 at once only during the chase test.
- ESP32-S3: USB-C from the same power bank.
- Common ground between the ESP32 and the module rail is essential; the GPIO signal is referenced
  to it.
- Put a 470 uF electrolytic across the 5 V rail at the controller box; coin motors produce supply
  dips at start-up that otherwise reset the ESP32.

## Harness

Three wires per module in 4 mm nylon braided sleeving, about 1 m long, with heat-shrink at the
pod end. The sleeving exits the controller box through the rim notches of the printed lid. For the
vest, run the nine front cables down the inside of the front panel and the nine back cables down
the inside of the back panel, with the controller box in a pocket at the lower back or hip.

## Button and LED

- Push button: GPIO 0 (BOOT) to GND, used as a manual "acknowledge" during the study and to
  trigger the chase test when held for 2 s (planned, not yet in firmware).
- Status LED: GPIO 38 (on-board LED on most DevKitC boards) lights while a frame is active.
