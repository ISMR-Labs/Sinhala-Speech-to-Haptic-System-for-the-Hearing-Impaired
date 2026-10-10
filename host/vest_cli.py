#!/usr/bin/env python3
"""Host-side tool for the Sinhala speech-to-haptic vest.

  python vest_cli.py words                          list the vocabulary and its codes
  python vest_cli.py play ඔව් --vest sim             play one word (sim | vest.local | /dev/cu.usbmodem*)
  python vest_cli.py text "අම්මා එන්න" --vest vest.local   play a typed sentence
  python vest_cli.py listen --vest vest.local       microphone -> Sinhala ASR -> vest
  python vest_cli.py chase --vest vest.local        fire every motor once (wiring check)
  python vest_cli.py study ...                      run a word-identification session (see study/)
"""

import argparse
import sys
import time

from patterns import Vocabulary
from sender import open_vest


def play_plan(vocab, vest, plan, verbose=True):
    """plan: list of (token, entry|None). Plays words in order with the word gap."""
    for tok, entry in plan:
        if entry is None:
            if verbose:
                print(f"  {tok}: not in vocabulary -> _unknown")
            vest.send(vocab.reserved_wire("_unknown"))
            time.sleep(0.5)
            continue
        if verbose:
            seq = " -> ".join("+".join(f["motors"]) for f in entry["frames"])
            print(f"  {entry['sinhala']} ({entry['english']}): {seq}")
        vest.send(vocab.word_wire(entry))
        time.sleep((vocab.word_duration_ms(entry) + vocab.enc["word_gap_ms"]) / 1000)


def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--vocab", default=None, help="path to vocabulary.json")
    common.add_argument("--vest", default="sim", help="sim | host or URL of the vest | serial port (default sim)")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
                                 parents=[common])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("words", parents=[common])
    p = sub.add_parser("play", parents=[common]); p.add_argument("word")
    p = sub.add_parser("text", parents=[common]); p.add_argument("sentence")
    p = sub.add_parser("listen", parents=[common])
    p.add_argument("--model", default="small", help="faster-whisper model name or CTranslate2 dir")
    p.add_argument("--threshold", type=float, default=0.012, help="RMS gate for utterance start")
    p.add_argument("--device", type=int, default=None, help="sounddevice input index")
    sub.add_parser("chase", parents=[common])
    sub.add_parser("status", parents=[common])
    args = ap.parse_args()

    vocab = Vocabulary(args.vocab) if args.vocab else Vocabulary()

    if args.cmd == "words":
        print(f"{len(vocab.words)} words, frame {vocab.enc['frame_ms']} ms, gap {vocab.enc['gap_ms']} ms, "
              f"min pairwise distance {vocab.enc['min_pairwise_distance']}")
        for w in vocab.words:
            seq = " -> ".join("+".join(f["motors"]) for f in w["frames"])
            print(f"  {w['sinhala']:<12} {w['romanised']:<13} {w['english']:<14} {seq}")
        return

    vest = open_vest(args.vest)
    if args.cmd == "status":
        print(vest.status())
    elif args.cmd == "chase":
        print(vest.send("T") if args.vest != "sim" else "chase needs hardware")
    elif args.cmd == "play":
        entry = vocab.lookup(args.word)
        if entry is None:
            sys.exit(f"'{args.word}' is not in the vocabulary (try: python vest_cli.py words)")
        play_plan(vocab, vest, [(args.word, entry)])
    elif args.cmd == "text":
        play_plan(vocab, vest, vocab.sentence_plan(args.sentence))
    elif args.cmd == "listen":
        from asr import listen
        vest.send(vocab.reserved_wire("_listening")) if args.vest != "sim" else None

        def on_text(text):
            print(f"heard: {text}")
            play_plan(vocab, vest, vocab.sentence_plan(text))
            vest.send(vocab.reserved_wire("_sentence_end"))

        try:
            listen(on_text, model=args.model, device_index=args.device, threshold=args.threshold)
        except KeyboardInterrupt:
            vest.stop()


if __name__ == "__main__":
    main()
