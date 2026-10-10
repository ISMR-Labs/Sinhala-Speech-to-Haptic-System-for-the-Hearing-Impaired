"""Vocabulary loading, word lookup and encoding to the vest wire format."""

import difflib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_VOCAB = os.path.join(HERE, "..", "patterns", "vocabulary.json")

# Sinhala Unicode block plus ZWJ, which Sinhala conjuncts use
_SINHALA_WORD = re.compile(r"[඀-෿‍]+")


class Vocabulary:
    def __init__(self, path=DEFAULT_VOCAB):
        with open(path, encoding="utf-8") as f:
            self.doc = json.load(f)
        self.enc = self.doc["encoding"]
        self.words = self.doc["words"]
        self.reserved = self.doc["reserved"]
        self.by_sinhala = {w["sinhala"]: w for w in self.words}
        self.by_roman = {w["romanised"].lower(): w for w in self.words}
        self.by_english = {w["english"].split(" /")[0].lower(): w for w in self.words}

    # ---- lookup ---------------------------------------------------------------
    def lookup(self, token, fuzzy=0.75):
        """Return the vocabulary entry for a token (Sinhala, romanised or English), or None."""
        t = token.strip().lower()
        for table in (self.by_sinhala, self.by_roman, self.by_english):
            if t in table:
                return table[t]
        # fuzzy match on Sinhala script: ASR output often differs by a vowel sign or a final letter
        if _SINHALA_WORD.fullmatch(token.strip()):
            best = difflib.get_close_matches(token.strip(), list(self.by_sinhala), n=1, cutoff=fuzzy)
            if best:
                return self.by_sinhala[best[0]]
        return None

    def tokenize(self, text):
        """Split a transcript into Sinhala word tokens (keeps non-Sinhala tokens for diagnostics)."""
        return re.findall(r"[඀-෿‍]+|[A-Za-z]+", text)

    # ---- encoding -------------------------------------------------------------
    def frames_to_wire(self, frames, gap_ms=None):
        gap = self.enc["gap_ms"] if gap_ms is None else gap_ms
        parts = [f"G {gap}"]
        for fr in frames:
            idx = ",".join(str(i) for i in fr["on"])
            parts.append(f"F {idx} {fr['ms']} {fr.get('level', self.enc['level'])}")
        return ";".join(parts)

    def word_wire(self, entry):
        return self.frames_to_wire(entry["frames"])

    def reserved_wire(self, name):
        return self.frames_to_wire(self.reserved[name]["frames"])

    def sentence_plan(self, text):
        """Map a transcript to a list of (token, entry_or_None)."""
        return [(tok, self.lookup(tok)) for tok in self.tokenize(text)]

    def word_duration_ms(self, entry):
        n = len(entry["frames"])
        return sum(f["ms"] for f in entry["frames"]) + n * self.enc["gap_ms"]
