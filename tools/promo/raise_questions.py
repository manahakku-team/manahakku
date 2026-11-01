#!/usr/bin/env python3
"""Lift the end of question lines so they sound like asking.
Args: input.wav output.wav "start,end,semitones;start,end,semitones;..."
Each segment's last 45% glides up to +semitones (PSOLA, voice stays natural)."""
import sys, parselmouth
from parselmouth.praat import call
src, dst, spec = sys.argv[1], sys.argv[2], sys.argv[3]
snd = parselmouth.Sound(src)
man = call(snd, "To Manipulation", 0.01, 75, 400)
tier = call(man, "Extract pitch tier")
pitch = snd.to_pitch(0.01, 75, 400)
for part in spec.split(";"):
    a, b, st = map(float, part.split(","))
    start = a + (b - a) * 0.55
    pts = [(call(tier, "Get time from index", i), call(tier, "Get value at index", i))
           for i in range(1, call(tier, "Get number of points") + 1)]
    for t, v in pts:
        if start <= t <= b:
            k = (t - start) / (b - start)
            call(tier, "Remove point near", t)
            call(tier, "Add point", t, v * 2 ** (st * k / 12))
call([tier, man], "Replace pitch tier")
out = call(man, "Get resynthesis (overlap-add)")
out.save(dst, "WAV")
print("saved", dst)
