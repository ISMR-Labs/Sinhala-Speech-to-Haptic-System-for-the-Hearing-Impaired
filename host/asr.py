"""Microphone capture and Sinhala speech recognition with faster-whisper.

Utterances are cut with a simple energy gate (RMS above a threshold starts an utterance,
0.7 s below it ends one) and transcribed with language="si". A fine-tuned Sinhala Whisper
checkpoint can be passed as --model (any CTranslate2 model directory or Hugging Face id that
faster-whisper accepts).
"""

import queue
import time

import numpy as np

SAMPLE_RATE = 16000


class EnergyGate:
    def __init__(self, threshold=0.012, end_silence_s=0.7, max_len_s=8.0, pre_roll_s=0.3):
        self.thr, self.end_s, self.max_s = threshold, end_silence_s, max_len_s
        self.pre = int(pre_roll_s * SAMPLE_RATE)
        self.buf, self.active, self.last_voice = [], False, 0.0
        self.ring = np.zeros(0, dtype=np.float32)

    def feed(self, block, now):
        """Returns a finished utterance (np.float32) or None."""
        rms = float(np.sqrt(np.mean(block ** 2)))
        if not self.active:
            self.ring = np.concatenate([self.ring, block])[-self.pre:]
            if rms > self.thr:
                self.active, self.last_voice = True, now
                self.buf = [self.ring.copy(), block]
            return None
        self.buf.append(block)
        if rms > self.thr:
            self.last_voice = now
        total = sum(len(b) for b in self.buf) / SAMPLE_RATE
        if now - self.last_voice > self.end_s or total > self.max_s:
            utt = np.concatenate(self.buf)
            self.buf, self.active, self.ring = [], False, np.zeros(0, dtype=np.float32)
            return utt
        return None


class Recognizer:
    def __init__(self, model="small", device="cpu", compute_type="int8", language="si"):
        from faster_whisper import WhisperModel
        self.model = WhisperModel(model, device=device, compute_type=compute_type)
        self.language = language

    def transcribe(self, audio):
        segments, info = self.model.transcribe(audio, language=self.language, beam_size=5,
                                               vad_filter=False, condition_on_previous_text=False)
        text = " ".join(s.text.strip() for s in segments).strip()
        return text, info


def listen(on_text, model="small", device_index=None, threshold=0.012, verbose=True):
    """Blocking loop: capture the microphone, cut utterances, recognise, call on_text(text)."""
    import sounddevice as sd
    rec = Recognizer(model)
    gate = EnergyGate(threshold=threshold)
    q = queue.Queue()

    def cb(indata, frames, t, status):
        q.put(indata[:, 0].copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", blocksize=1600,
                        device=device_index, callback=cb):
        if verbose:
            print(f"listening (model={model}, threshold={threshold}); Ctrl-C to stop")
        while True:
            block = q.get()
            utt = gate.feed(block, time.time())
            if utt is None:
                continue
            t0 = time.time()
            text, info = rec.transcribe(utt)
            if verbose:
                print(f"[{len(utt) / SAMPLE_RATE:.1f}s audio, {time.time() - t0:.1f}s asr, "
                      f"p={info.language_probability:.2f}] {text}")
            if text:
                on_text(text)
