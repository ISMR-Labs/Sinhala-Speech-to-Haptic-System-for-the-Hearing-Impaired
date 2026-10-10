# Host to vest protocol

The vest controller accepts the same text commands over two transports:

- **HTTP** on port 80 (`http://vest.local` via mDNS, or the IP printed on the serial console):
  `POST /play` with the command in the request body, `POST /stop`, `POST /test`, `GET /status`.
- **USB serial** at 115200 baud, one command per line. Do not assert DTR/RTS when opening the
  port or the ESP32 resets (the host code opens the port with both low).

## Commands

| Command | Meaning |
|---|---|
| `F <idx[,idx...]> <ms> <level>` | one frame: switch on the listed motors for `ms` milliseconds at `level` (0 to 255) |
| `F ...;F ...;F ...` | a sequence of frames, played back to back with the current gap between them |
| `G <ms>` | set the gap between frames (default 80 ms); may be the first token of a sequence |
| `S` | stop immediately, all motors off |
| `T` | chase test: every motor in turn for 250 ms |
| `?` | status: motor count, playing flag, sequences played, gap, IP |

Motor index 0 to 8 is the front 3 x 3 (row-major from the wearer's top-left), 9 to 17 the back.

A word from the vocabulary is therefore one line, for example `ඔව්` (yes):

```
G 80;F 14 200 255;F 12,13 200 255
```

The controller replies `OK frames=2` or `ERR <reason>`. A new sequence replaces the one playing.
The host is responsible for the word gap (400 ms) between successive words and for sentence
markers; it sends the reserved `_sentence_end` pattern after each utterance.

## Level

Level is a 100 Hz software PWM duty on the module's IN pin. With ERM motors this changes both
amplitude and frequency; 255 is full, 128 is a clearly weaker buzz, below about 90 the motor may
not start. The vocabulary v0 uses 255 only.

## Timing

Frames are timed on the controller with `millis()`, so network jitter does not affect the
rhythm inside a word. A sequence of up to 32 frames is buffered.
