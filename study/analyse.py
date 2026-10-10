#!/usr/bin/env python3
"""Summarise a study log: accuracy per session, confusion matrix, pairs to re-code.

CSV columns: timestamp, participant, session, phase, trial, word, answer, rt_ms
Only phase == "test" rows count towards accuracy.
"""

import csv
import sys
from collections import Counter, defaultdict


def main(path):
    rows = [r for r in csv.DictReader(open(path, encoding="utf-8")) if r["phase"] == "test"]
    if not rows:
        sys.exit("no test rows")
    by_session = defaultdict(lambda: [0, 0])
    conf = Counter()
    presented = Counter()
    rts = []
    for r in rows:
        s = by_session[(r["participant"], r["session"])]
        s[1] += 1
        if r["word"] == r["answer"]:
            s[0] += 1
        conf[(r["word"], r["answer"])] += 1
        presented[r["word"]] += 1
        if r.get("rt_ms"):
            rts.append(float(r["rt_ms"]))

    print("accuracy per participant/session")
    for (p, s), (ok, n) in sorted(by_session.items()):
        print(f"  {p:<10} session {s}: {ok}/{n} = {100 * ok / n:.0f}%")
    tot_ok = sum(v[0] for v in by_session.values())
    tot_n = sum(v[1] for v in by_session.values())
    print(f"overall {tot_ok}/{tot_n} = {100 * tot_ok / tot_n:.1f}%")
    if rts:
        rts.sort()
        print(f"median reaction time {rts[len(rts) // 2]:.0f} ms")

    print("\nconfusions above 15% of presentations")
    for (w, a), n in sorted(conf.items(), key=lambda kv: -kv[1]):
        if w != a and n / presented[w] > 0.15:
            print(f"  {w} -> {a}: {n}/{presented[w]} ({100 * n / presented[w]:.0f}%)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "study/log.csv")
