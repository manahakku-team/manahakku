#!/usr/bin/env python3
"""Find exactly where each script line is spoken in the take (forced alignment, no guessing).

  fa_align.py LANG take.wav   -> work/align-LANG.json  [(start, end) per line, seconds]

Uses the MMS forced-alignment model (works for Telugu and English through romanised text).
Each line's start is its first word, its end is its last word. Prints a per-line report.
"""
import json, os, re, sys
import torch, torchaudio
import uroman as ur

D = os.path.dirname(os.path.abspath(__file__))
lang, take = sys.argv[1], sys.argv[2]
rows = [r.rstrip("\n").split("\t") for r in open(f"{D}/spoken.tsv", encoding="utf-8")]
texts = [r[4].strip() for r in rows if len(r) >= 5 and r[0] == lang and r[4].strip()]

DIG = {"en": "zero one two three four five six seven eight nine".split(),
       "te": ["సున్నా", "ఒకటి", "రెండు", "మూడు", "నాలుగు", "ఐదు", "ఆరు", "ఏడు", "ఎనిమిది", "తొమ్మిది"]}
U = ur.Uroman()

def words(line):
    line = re.sub(r"\d", lambda m: " " + DIG[lang][int(m.group())] + " ", line)   # numbers are read digit by digit
    if lang == "te":
        line = U.romanize_string(line)
    line = re.sub(r"[^a-z' ]", " ", line.lower())
    return [w for w in line.split() if w.strip("'")]

bundle = torchaudio.pipelines.MMS_FA
model = bundle.get_model(with_star=False)
tok, aligner = bundle.get_tokenizer(), bundle.get_aligner()
wav, sr = torchaudio.load(take)
wav = torchaudio.functional.resample(wav.mean(0, keepdim=True), sr, bundle.sample_rate)
with torch.inference_mode():
    em, _ = model(wav)
per_line = [words(t) for t in texts]
flat = [w for ws in per_line for w in ws]
spans = aligner(em[0], tok(flat))
ratio = wav.size(1) / em.size(1) / bundle.sample_rate
out, k = [], 0
for t, ws in zip(texts, per_line):
    s = spans[k:k + len(ws)]; k += len(ws)
    a, b = s[0][0].start * ratio, s[-1][-1].end * ratio
    out.append((round(a, 3), round(b, 3)))
    print(f"{a:6.2f}-{b:6.2f}  {t}", file=sys.stderr)
os.makedirs(f"{D}/work", exist_ok=True)
json.dump(out, open(f"{D}/work/align-{lang}.json", "w"))
