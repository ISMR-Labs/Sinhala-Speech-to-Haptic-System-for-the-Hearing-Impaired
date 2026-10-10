# User study protocol (v0)

**Question.** Can people learn to identify 20 Sinhala words delivered as two-frame vibration
patterns on an 18-motor vest, how fast, and which words are confused?

## Participants

- Pilot: 8 hearing adults from the lab wearing ear defenders and with the motors masked by pink
  noise through headphones, so that they cannot hear the motors. This checks the codebook and
  the procedure before involving the target group.
- Main: 10 to 12 deaf or hard-of-hearing adults who are native Sinhala readers, recruited through
  the Sri Lanka Central Federation of the Deaf. Instructions and consent in Sinhala and Sri Lankan
  Sign Language with an interpreter.
- Ethics approval from the host institution's committee before the main study; the pilot uses
  lab members only.

## Setup

- Vest worn over a thin T-shirt; pods adjusted so that each is in firm contact. Chase test to
  confirm every motor is felt.
- Host laptop runs `host/vest_cli.py study` (see below) which presents patterns and records
  answers; the participant answers on a 20-button screen showing the Sinhala words with a small
  picture each.
- Room temperature 24 to 28 °C (vibrotactile sensitivity drops in the cold).

## Sessions

Each participant does three sessions on separate days.

| Phase | Duration | Content |
|---|---|---|
| 1. Familiarisation | 10 min | each word played twice with its label shown; participant may replay |
| 2. Training with feedback | 20 min, 2 blocks of 60 trials | random word, participant answers, correct answer shown and replayed if wrong |
| 3. Identification test | 10 min, 60 trials | random word, answer, no feedback |
| 4. Sentence test (session 3 only) | 10 min | 10 two- and three-word sentences, free recall of the words |
| Questionnaire | 5 min | comfort, clarity of front vs back, words that feel alike |

Retention: the session 2 and 3 identification tests start without familiarisation, which gives
a 24 h and 48 h retention measure.

## Measures

- Identification accuracy per session (primary), learning curve over the training blocks.
- Confusion matrix of the 20 words; pairs with more than 15 % confusion are candidates for
  re-coding.
- Reaction time from end of pattern to answer.
- Sentence word recall and order errors.
- Reported comfort and any skin irritation.

## Analysis

`study/analyse.py` reads the CSV log (`timestamp, participant, session, phase, trial, word,
answer, rt_ms`) and prints accuracy per session, the confusion matrix and the pairs to re-code.
A codebook change is accepted only if the minimum pairwise distance does not drop.

## Success criteria for v0

- Mean identification accuracy above 80 % at session 3 for the main group.
- No word pair confused in more than 25 % of its presentations.
- Participants rate the vest as wearable for at least 30 min.

## What this study does not test

Recognition accuracy of the speech recogniser, which is measured separately on recordings of
the 20 words from 10 speakers (`study/asr-eval.md`, planned).
