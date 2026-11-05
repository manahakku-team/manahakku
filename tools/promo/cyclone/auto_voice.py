#!/usr/bin/env python3
"""Turn one long voice take into the appeal's voice track, unattended.

  auto_voice.py align  LANG take.wav            -> work/align.json, prints the lift spec for questions that don't rise
  auto_voice.py build  LANG take.wav            -> LANG.mp3 + LANG.vtt (gaps tightened so the video stays under 55 s)

Lines come from spoken.tsv (lang, rate, pitch, pause-after, text).
"""
import json, os, subprocess, sys, unicodedata, wave
import numpy as np

D = os.path.dirname(os.path.abspath(__file__))
mode, lang, take = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(f"{D}/work", exist_ok=True)

rows = [r.rstrip("\n").split("\t") for r in open(f"{D}/spoken.tsv", encoding="utf-8")]
rows = [r for r in rows if len(r) >= 5 and r[0] == lang and r[4].strip()]
texts = [r[4].strip() for r in rows]

w = wave.open(take); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
xf = x.astype(float) / 32768
hop = int(0.02 * sr)
rms = np.array([np.sqrt(np.mean(xf[i:i + hop] ** 2)) for i in range(0, len(xf) - hop, hop)])

def segments():
    thr = max(np.percentile(rms, 95) * 0.12, 0.01)
    on = rms > thr
    segs, i, n = [], 0, len(on)
    while i < n:
        if on[i]:
            j = i
            while j < n and (on[j] or on[j:j + 15].any()):  # bridge gaps under 0.3 s
                j += 1
            segs.append((i * 0.02, j * 0.02)); i = j
        else:
            i += 1
    return [(a, b) for a, b in segs if b - a > 0.15]

def align():
    segs = segments()
    ch = [len([c for c in t if unicodedata.category(c)[0] in "LMN"]) for t in texts]
    k = sum(b - a for a, b in segs) / sum(ch)
    n, m, INF = len(texts), len(segs), 1e18
    C = [[INF] * (m + 1) for _ in range(n + 1)]; P = [[0] * (m + 1) for _ in range(n + 1)]; C[0][0] = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            for s in range(max(0, j - 4), j):
                if C[i - 1][s] >= INF: continue
                dur = segs[j - 1][1] - segs[s][0]
                c = C[i - 1][s] + (dur - k * ch[i - 1]) ** 2 / (k * ch[i - 1] + 0.5)
                if c < C[i][j]: C[i][j] = c; P[i][j] = s
    # allow stray noise segments at the very start or end to be dropped
    best, bj = INF, m
    for j in range(max(1, m - 2), m + 1):
        if C[n][j] < best: best, bj = C[n][j], j
    al, j = [], bj
    for i in range(n, 0, -1):
        s = P[i][j]; al.append((segs[s][0], segs[j - 1][1])); j = s
    return al[::-1]

def f0_rise(a, b):
    s = xf[int(a * sr):int(b * sr)]; W = int(0.04 * sr); out = []
    loud = max(0.02, np.percentile(rms, 95) * 0.25)
    for i in range(0, len(s) - W, W // 4):
        fr = s[i:i + W]
        if np.sqrt(np.mean(fr ** 2)) < loud: continue
        fr = fr - fr.mean(); ac = np.correlate(fr, fr, "full")[W - 1:]
        lo, hi = int(sr / 400), int(sr / 75); l = lo + int(np.argmax(ac[lo:hi]))
        if ac[l] > 0.4 * ac[0]: out.append(sr / l)
    if len(out) < 8: return 0.0
    out = np.array(out)
    return float(12 * np.log2(np.median(out[-6:]) / np.median(out)))

if mode == "align":
    al = align()
    json.dump(al, open(f"{D}/work/align-{lang}.json", "w"))
    spec = []
    for (a, b), t in zip(al, texts):
        if not t.endswith("?"): continue
        r = f0_rise(a, b)
        print(f"{t}  rise {r:+.1f} st", file=sys.stderr)
        if r < 2.5: spec.append(f"{a:.2f},{b:.2f},{min(10, max(4, 2 * (4 - r))):.0f}")
    for (a, b), t in zip(al, texts): print(f"{a:6.2f}-{b:6.2f} {t}", file=sys.stderr)
    print(";".join(spec))

elif mode == "build":
    # Calm pace that uses the full length: speech slowed a little (same pitch), then the pauses
    # between lines grow until the video reaches TARGET seconds (lead 0.3 s + end card 2.2 s included).
    TARGET = float(os.environ.get("TARGET", "56.5"))
    TEMPO = float(os.environ.get("TEMPO", "0.92"))
    al = json.load(open(f"{D}/work/align-{lang}.json"))
    al = [(max(0, a - 0.04), b + 0.08) for a, b in al]
    segs = []
    for i, (a, b) in enumerate(al):
        seg = x[int(a * sr):int(b * sr)].astype(float)
        fl = int(0.02 * sr); seg[:fl] *= np.linspace(0, 1, fl); seg[-fl:] *= np.linspace(1, 0, fl)
        src, dst = f"{D}/work/s{i}.wav", f"{D}/work/s{i}t.wav"
        ww = wave.open(src, "wb"); ww.setnchannels(1); ww.setsampwidth(2); ww.setframerate(sr); ww.writeframes(seg.astype(np.int16).tobytes()); ww.close()
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", f"atempo={TEMPO}", "-ar", str(sr), "-ac", "1", dst], check=True)
        w2 = wave.open(dst); segs.append(np.frombuffer(w2.readframes(w2.getnframes()), np.int16).astype(float)); w2.close()
    speech = sum(len(g) for g in segs) / sr
    base = [float(r[3]) + 0.45 for r in rows[:-1]]          # the script's own pause after each line
    room = TARGET - 0.3 - 2.2 - speech
    if room > sum(base):                                      # spread the spare time, more after the longer pauses
        extra = room - sum(base); w = [g for g in base]; tot = sum(w)
        gaps = [min(2.2, g + extra * g / tot) for g in base]
    else:
        f = max(room, 0.15 * len(base)) / sum(base); gaps = [max(0.15, g * f) for g in base]
    out, cues, t = [], [], 0.0
    for i, seg in enumerate(segs):
        cues.append((t, t + len(seg) / sr, texts[i])); out.append(seg); t += len(seg) / sr
        if i < len(gaps): out.append(np.zeros(int(gaps[i] * sr))); t += gaps[i]
    y = np.concatenate(out).astype(np.int16)
    tmp = f"{D}/work/{lang}.wav"
    ww = wave.open(tmp, "wb"); ww.setnchannels(1); ww.setsampwidth(2); ww.setframerate(sr); ww.writeframes(y.tobytes()); ww.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-b:a", "192k", f"{D}/{lang}.mp3"], check=True)
    ts = lambda s: f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{s % 60:06.3f}".replace(".", ",")
    open(f"{D}/{lang}.vtt", "w", encoding="utf-8").write(
        "".join(f"{i + 1}\n{ts(a)} --> {ts(b)}\n{tx}\n\n" for i, (a, b, tx) in enumerate(cues)))
    print(f"voice {t:.2f} s, speech {speech:.2f} s, gaps {sum(gaps):.2f} s", file=sys.stderr)
