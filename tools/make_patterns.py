#!/usr/bin/env python3
"""Generate patterns/vocabulary.json: a word-level vibrotactile codebook for the 18-motor vest.

Encoding (v0)
-------------
* Motors: 9 on the front (F1..F9, 3x3 as seen by the wearer: row 1 = top, column 1 = left)
  and 9 on the back (B1..B9), indices 0..8 front, 9..17 back.
* A word is a sequence of two frames. Each frame switches on one motor, or two adjacent
  motors (horizontal or vertical pair) on the same side, for FRAME_MS, followed by GAP_MS of
  silence. Words are separated by WORD_GAP_MS.
* Level is fixed at full for v0; intensity is reserved as a third coding dimension.

Codes are assigned by a greedy search that keeps the minimum pairwise distance between all
words as large as possible, so that confusions found in the user study can be traded for
spare codes later. Distance between two words = sum over the two frame positions of the
Jaccard distance between their motor sets, plus 1 if the side sequence (front/back per frame)
differs. Run `python3 tools/make_patterns.py` to regenerate; the search is deterministic.
"""

import itertools
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "patterns", "vocabulary.json")

FRAME_MS = 200
GAP_MS = 80
WORD_GAP_MS = 400
LEVEL = 255

# (sinhala, romanised, english, category)
WORDS = [
    ("ඔව්", "ow", "yes", "response"),
    ("නැහැ", "naehae", "no", "response"),
    ("එන්න", "enna", "come", "command"),
    ("යන්න", "yanna", "go", "command"),
    ("නවත්වන්න", "nawathwanna", "stop", "command"),
    ("ඉන්න", "inna", "wait / stay", "command"),
    ("උදව්", "udaw", "help", "alert"),
    ("අනතුර", "anathura", "danger", "alert"),
    ("ආයුබෝවන්", "ayubowan", "hello", "social"),
    ("ස්තූතියි", "sthuthiyi", "thank you", "social"),
    ("හොඳයි", "hondayi", "good / OK", "social"),
    ("කන්න", "kanna", "eat", "need"),
    ("බොන්න", "bonna", "drink", "need"),
    ("වතුර", "wathura", "water", "need"),
    ("අම්මා", "amma", "mother", "person"),
    ("තාත්තා", "thaththa", "father", "person"),
    ("කොහෙද", "koheda", "where", "question"),
    ("මොකක්ද", "mokakda", "what", "question"),
    ("දැන්", "daen", "now", "time"),
    ("පස්සේ", "passe", "later", "time"),
]

# Reserved, hand-designed signals (not words)
RESERVED = {
    "_listening": {"english": "system is listening", "frames": [{"on": [0, 2, 6, 8], "ms": 120}]},
    "_unknown": {"english": "word not in vocabulary", "frames": [{"on": list(range(9)), "ms": 150},
                                                                 {"on": list(range(9, 18)), "ms": 150}]},
    "_sentence_end": {"english": "end of sentence", "frames": [{"on": [4], "ms": 100}, {"on": [13], "ms": 100}]},
}


def motor_name(i):
    return ("F" if i < 9 else "B") + str(i % 9 + 1)


def candidate_frames():
    """Singles and adjacent pairs on the same side."""
    frames = []
    for side in (0, 9):
        for i in range(9):
            frames.append(frozenset([side + i]))
        for r in range(3):
            for c in range(3):
                i = r * 3 + c
                if c < 2:
                    frames.append(frozenset([side + i, side + i + 1]))      # horizontal pair
                if r < 2:
                    frames.append(frozenset([side + i, side + i + 3]))      # vertical pair
    return frames


def side_of(frame):
    return "F" if min(frame) < 9 else "B"


def jaccard(a, b):
    return 1.0 - len(a & b) / len(a | b)


def word_distance(w1, w2):
    d = sum(jaccard(f1, f2) for f1, f2 in zip(w1, w2))
    if [side_of(f) for f in w1] != [side_of(f) for f in w2]:
        d += 1.0  # a different front/back sequence is the easiest cue to feel
    return d


def assign_codes(n_words, seed=7):
    frames = candidate_frames()
    codes = list(itertools.product(frames, frames))
    # bias the search towards codes that use both sides or move across the body
    rng = random.Random(seed)
    rng.shuffle(codes)
    chosen = []
    # greedy max-min: start from a fixed code, then repeatedly add the code farthest from the set
    chosen.append(codes[0])
    while len(chosen) < n_words:
        best, best_d = None, -1.0
        for c in codes:
            if c in chosen:
                continue
            d = min(word_distance(c, k) for k in chosen)
            if d > best_d:
                best, best_d = c, d
        chosen.append(best)
    return chosen


def main():
    codes = assign_codes(len(WORDS))
    words = []
    for (si, rom, en, cat), code in zip(WORDS, codes):
        words.append({
            "sinhala": si, "romanised": rom, "english": en, "category": cat,
            "frames": [{"on": sorted(f), "motors": [motor_name(i) for i in sorted(f)], "ms": FRAME_MS, "level": LEVEL}
                       for f in code],
        })
    dmin = min(word_distance(a, b) for a, b in itertools.combinations(codes, 2))
    doc = {
        "version": "0.1.0",
        "encoding": {
            "motors": 18, "front": [motor_name(i) for i in range(9)], "back": [motor_name(i) for i in range(9, 18)],
            "frame_ms": FRAME_MS, "gap_ms": GAP_MS, "word_gap_ms": WORD_GAP_MS, "level": LEVEL,
            "frames_per_word": 2, "max_motors_per_frame": 2,
            "min_pairwise_distance": round(dmin, 3),
            "notes": "See docs/pattern-design.md. Indices 0-8 front (row-major, top-left first as worn), 9-17 back.",
        },
        "words": words,
        "reserved": {k: {"english": v["english"],
                         "frames": [{"on": f["on"], "motors": [motor_name(i) for i in f["on"]], "ms": f["ms"], "level": LEVEL}
                                    for f in v["frames"]]} for k, v in RESERVED.items()},
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"wrote {os.path.relpath(OUT)}: {len(words)} words, min pairwise distance {dmin:.2f}")
    for w in words:
        print(f"  {w['sinhala']:<12} {w['english']:<14} " + " -> ".join("+".join(f["motors"]) for f in w["frames"]))


if __name__ == "__main__":
    main()
