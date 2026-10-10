# Sinhala Speech-to-Haptic System for the Hearing Impaired

A wearable vest that lets a deaf or hard-of-hearing person "feel" spoken
Sinhala. Speech is captured and recognised on a laptop, converted into
Sinhala words, and each word is delivered to the wearer as a distinct
vibration pattern across 18 vibration modules on the vest (9 on the front,
9 on the back).

The device is intended only for hearing-impaired users; the research question
is whether word-level vibrotactile patterns can be learned and reliably
distinguished, and how many words such a vocabulary can hold.

## Concept

```
 microphone -> speech recognition (laptop) -> Sinhala words
            -> word-to-pattern mapping -> vest controller (ESP32)
            -> 18 vibration modules (3x3 front, 3x3 back)
```

- **Speech recognition** runs on the laptop (Sinhala ASR model, to be selected).
- **Word-to-pattern mapping** assigns every vocabulary word a pattern defined
  by which modules fire, in what order, for how long and how strongly.
  Spatial, temporal and combined encodings will be compared.
- **Vest controller** receives the pattern over Bluetooth or Wi-Fi and drives
  the motors through PWM motor-driver boards.

## Planned layout

| Folder | Contents |
|---|---|
| `firmware/` | ESP32 code: receives patterns, drives the 18 modules |
| `host/` | laptop software: speech capture, recognition, mapping, sending |
| `patterns/` | vocabulary and pattern definitions (JSON) |
| `hardware/` | wiring diagram, module placement on the vest, bill of materials |
| `study/` | user-study protocol and results (learnability, recognition accuracy) |
| `paper/` | write-up |

## Status

Concept stage. Hardware and software are not built yet.

## Team

ISMR Labs.
