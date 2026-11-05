#!/usr/bin/env python3
"""Appeal voice-over with Gemini text-to-speech.

Reads the spoken script (lang, rate, pitch, pause, text) and, for each
language, voice and take, asks Gemini to read the whole script in one go
with a plain-words style direction. Writes WAV files to the output folder.
The key comes from the GEMINI_API_KEY environment variable only.
"""
import base64, json, os, sys, time, urllib.request, urllib.error, wave

SPEC, OUT = sys.argv[1], sys.argv[2]
MODEL = os.environ.get("MODEL", "gemini-2.5-flash-preview-tts")
VOICES = [v.strip() for v in os.environ.get("VOICES", "Sulafat,Leda").split(",") if v.strip()]
TAKES = int(os.environ.get("TAKES", "2"))
LANGS = os.environ.get("LANGS", "te,en").split(",")
KEY = os.environ["GEMINI_API_KEY"]

STYLE = {
    "en": ("Read this as a young Indian woman making a heartfelt appeal to her own people, "
           "in warm Indian English. Not a news reader, not an advert. Slow and natural, with "
           "real pauses between lines. The first four lines are quiet and heavy. "
           "The short lines ending in a question mark are genuine questions asked to the "
           "listener: let the voice clearly rise at the end of each one. "
           "The last lines are hopeful and gentle, never pushy."),
    "te": ("ఈ స్క్రిప్ట్‌ను ఒక యువతి తన సొంత ప్రజలను హృదయపూర్వకంగా వేడుకుంటున్నట్లుగా, సహజమైన తెలుగులో చదవండి. "
           "Read in natural spoken Telugu, warm and heartfelt, like a young woman appealing to her own "
           "people. Not a news reader. Slow, with real pauses between lines. The first four lines are "
           "quiet and heavy. Every short line ending in a question mark is a genuine question asked to "
           "the listener: the voice must clearly rise at the end of each, like asking. "
           "The last lines are hopeful and gentle, never pushy."),
}

# A different video can pass its own reading direction (STYLE_EN / STYLE_TE).
for _l in ("en", "te"):
    if os.environ.get("STYLE_" + _l.upper()): STYLE[_l] = os.environ["STYLE_" + _l.upper()]

def lines(lang):
    out = []
    for row in open(SPEC, encoding="utf-8"):
        p = row.rstrip("\n").split("\t")
        if len(p) >= 5 and p[0] == lang and p[4].strip():
            out.append(p[4].strip())
    return out

def call(prompt, voice):
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}},
        },
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    for attempt in range(6):
        req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                j = json.load(r)
            part = j["candidates"][0]["content"]["parts"][0]["inlineData"]
            return base64.b64decode(part["data"])
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:300]
            print(f"  HTTP {e.code}: {msg}", flush=True)
            if e.code in (429, 500, 503):
                time.sleep(25 * (attempt + 1)); continue
            raise
        except (KeyError, IndexError) as e:
            print(f"  no audio in reply ({e}), retrying", flush=True); time.sleep(10)
    return None

def save(pcm, path):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)

os.makedirs(OUT, exist_ok=True)
for lang in LANGS:
    script = "\n".join(lines(lang))
    prompt = STYLE[lang] + "\n\n" + script
    for voice in VOICES:
        for t in range(1, TAKES + 1):
            name = f"{lang}-{voice}-take{t}.wav"
            print("making", name, flush=True)
            pcm = call(prompt, voice)
            if pcm is None: print("  skipped (quota)"); continue
            save(pcm, os.path.join(OUT, name))
            time.sleep(8)
print("done")
