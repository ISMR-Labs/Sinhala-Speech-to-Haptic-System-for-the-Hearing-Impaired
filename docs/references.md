# References, annotated

## Tactile speech and sensory substitution

1. **Geldard, F. A. (1957).** Adventures in tactile literacy. *American Psychologist* 12(3): 115–124.
   https://doi.org/10.1037/h0040416
   Vibratese: five chest vibrators, three durations and three intensities gave 45 symbols; trained
   readers exceeded 35 words per minute. The origin of word-level tactile coding on the torso and the
   direct ancestor of this project's approach.
2. **Summers, I. R. (ed.) (1992).** *Tactile Aids for the Hearing Impaired.* Whurr, London.
   Collected chapters on tactile coding, training, and evaluation of tactile aids against cochlear
   implants. Background for why earlier aids (Tactaid and others) did not reach wide use: sparse
   innervation at the chosen sites and the training required.
3. **Reed, C. M., Tan, H. Z., Perez, Z. D., Wilson, E. C., Severgnini, F. M., Jung, J., Martinez, J. S.,
   Jiao, Y., Israr, A., Lau, F., Klumb, K., Turcott, R., Abnousi, F. (2019).** A phonemic-based tactile
   display for speech communication. *IEEE Transactions on Haptics* 12(1): 2–17.
   https://doi.org/10.1109/TOH.2018.2861010
   TAPS: 24 tactors on the forearm, 39 English phoneme codes (24 position-based consonants, 15
   movement-based vowels); 86 % recognition after 1 to 4 h of training in 10 adults. The strongest
   evidence that spatial plus movement codes are learnable; also the reason we chose words over phonemes
   for a first Sinhala device.
4. **Tan, H. Z., Reed, C. M., Jiao, Y., Perez, Z. D., Wilson, E. C., Jung, J., Martinez, J. S.,
   Severgnini, F. M. (2020).** Acquisition of 500 English words through a TActile Phonemic Sleeve (TAPS).
   *IEEE Transactions on Haptics* 13(4): 745–760. https://doi.org/10.1109/TOH.2020.2973135
   Up to 500 words learned at about one word per minute; IEEE ToH best paper 2020. Sets the ceiling we
   can expect from phoneme coding with extended training.
5. **Novich, S. D., Eagleman, D. M. (2015).** Using space and time to encode vibrotactile information:
   toward an estimate of the skin's achievable throughput. *Experimental Brain Research* 233(10): 2777–2788.
   https://doi.org/10.1007/s00221-015-4346-1
   Spatiotemporal codes on the back; estimates the skin's throughput as well below the 64 to 110 bit/s
   that speech needs. Justifies a closed vocabulary.
6. **Perrotta, M. V., Asgeirsdottir, T., Eagleman, D. M. (2021).** Deciphering sounds through patterns
   of vibration on the skin. *Neuroscience* 458: 77–86. https://doi.org/10.1016/j.neuroscience.2021.01.008
   Wrist-worn multi-motor sound-to-touch device (the basis of the Neosensory Buzz); deaf participants
   learn to identify sounds from vibration patterns. Shows the frequency-band approach for environmental
   sound; our word approach is complementary.

## Vibrotactile perception on the torso

7. **van Erp, J. B. F. (2005).** Vibrotactile spatial acuity on the torso: effects of location and timing
   parameters. *Proceedings of the First Joint Eurohaptics Conference and Symposium on Haptic Interfaces
   (WHC 2005)*, pp. 80–85. https://doi.org/10.1109/WHC.2005.144
   Acuity of 3 to 4 cm over most of the torso; stimulus onset asynchrony matters more than burst
   length. Sets our 80 mm pitch and the 80 ms gap.
8. **van Erp, J. B. F. (2005).** Presenting directions with a vibrotactile torso display. *Ergonomics*
   48(3): 302–313. https://doi.org/10.1080/0014013042000327670
   Mapping of torso locations to directions with a 15-tactor belt; absolute localisation within about 5 cm.
9. **Jones, L. A., Lockyer, B., Piateski, E. (2006).** Tactile display and vibrotactile pattern recognition
   on the torso. *Advanced Robotics* 20(12): 1359–1374. https://doi.org/10.1163/156855306778960563
   Pattern identification on the torso is better than on the forearm (99 to 100 % for seven of eight
   patterns) and unaffected by walking. Supports the torso as the site and the 3 x 3 array.
10. **Jóhannesson, Ó. I., Hoffmann, R., Valgeirsdóttir, V. V., Unnþórsson, R., Moldoveanu, A.,
    Kristjánsson, Á. (2017).** Relative vibrotactile spatial acuity of the torso. *Experimental Brain
    Research* 235: 3505–3515. https://doi.org/10.1007/s00221-017-5073-6
    Acuity down to 13 mm tactor spacing in a relative task; confirms that an 80 mm pitch is conservative.
11. **Cholewiak, R. W., Brill, J. C., Schwab, A. (2004).** Vibrotactile localization on the abdomen:
    effects of place and space. *Perception & Psychophysics* 66(6): 970–987.
    https://doi.org/10.3758/BF03194989
    Localisation is best near anatomical landmarks (navel, spine); informs placing the centre column on
    the midline.
12. **Makous, J. C., Friedman, R. M., Vierck, C. J. (1995).** A critical band filter in touch. *Journal of
    Neuroscience* 15(4): 2808–2818. https://doi.org/10.1523/JNEUROSCI.15-04-02808.1995
    Pacinian channel peaks near 250 Hz; coin ERM motors at 150 to 200 Hz sit on the sensitive part of the
    curve. LRAs at 175 to 235 Hz would be closer to the peak.

## Sinhala speech recognition

13. **Kjartansson, O., Sarin, S., Pipatsrisawat, K., Jansche, M., Ha, L. (2018).** Crowd-sourced speech
    corpora for Javanese, Sundanese, Sinhala, Nepali, and Bangladeshi Bengali. *Proc. 6th Workshop on
    Spoken Language Technologies for Under-Resourced Languages (SLTU 2018)*, pp. 52–55.
    https://doi.org/10.21437/SLTU.2018-11
    OpenSLR SLR52: about 185 000 Sinhala utterances from 478 speakers, CC BY-SA 4.0. The main public
    training set for Sinhala ASR and the data behind the fine-tuned Whisper checkpoints we evaluate.
14. **Warusawithana, D., Kulaweera, N., Weerasinghe, L., Karunarathne, B. (2022).** A systematic approach
    to derive a refined speech corpus for Sinhala. *Proc. 13th Language Resources and Evaluation
    Conference (LREC 2022)*, pp. 5107–5113. https://aclanthology.org/2022.lrec-1.546
    Transcript standardisation and Sinhala-specific corrections on the public corpus gave a 15.9 %
    relative WER reduction. Useful for cleaning our own vocabulary recordings.
15. **Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., Sutskever, I. (2023).** Robust speech
    recognition via large-scale weak supervision. *Proc. 40th International Conference on Machine Learning
    (ICML 2023)*, PMLR 202: 28492–28518. https://proceedings.mlr.press/v202/radford23a.html
    Whisper. Sinhala is among its 97 languages but with little training data; the multilingual base
    model is weak on Sinhala, so the host uses a Sinhala fine-tune (see `host/asr.py`).
16. **Babu, A., Wang, C., Tjandra, A., Lakhotia, K., Xu, Q., Goyal, N., Singh, K., von Platen, P.,
    Saraf, Y., Pino, J., Baevski, A., Conneau, A., Auli, M. (2022).** XLS-R: self-supervised cross-lingual
    speech representation learning at scale. *Proc. Interspeech 2022*, pp. 2278–2282.
    https://doi.org/10.21437/Interspeech.2022-143
    The alternative acoustic model family; University of Colombo theses report 24 to 37 % WER on Sinhala
    with XLS-R fine-tuning. A candidate if Whisper fine-tunes are not accurate enough on the vocabulary.

## Context

17. **Department of Census and Statistics, Sri Lanka (2012).** *Census of Population and Housing 2012:
    disability tables.* Reports 389 077 persons with hearing difficulty, 21 per 1000 population.
18. **Sri Lanka Central Federation of the Deaf.** Estimates about 400 000 Sri Lankans with hearing
    impairment and a severe shortage of sign-language interpreters; the Sinhala-speaking deaf community
    has no fully standardised sign language. Motivation for a device that works from spoken Sinhala.
