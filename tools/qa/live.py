# Daily live checks: website pages, report register (read-only), data freshness. Usage: python3 tools/qa/live.py
import json, re, time, urllib.request
B = "https://manahakku-team.github.io/manahakku"
html = open("app/src/main/assets/index.html", encoding="utf-8").read()
REG = re.search(r"https://script\.google\.com/macros/s/[A-Za-z0-9_-]+/exec", html).group(0)
bad = 0
def get(u, t=60):
    r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ManaHakku-QA"}), timeout=t)
    return r.status, r.read()
print("Website")
for p in ["/", "/about.html", "/privacy.html", "/d/", "/d/ap-guntur.html", "/d/ts-hyderabad.html", "/sitemap.xml", "/data/finance.json",
          "/data/cag-2024-25.json", "/fonts/hind-guntur-telugu-400-normal.woff2", "/pdfjs/web/viewer.html", "/docs/constitution-te.pdf"]:
    try: s, body = get(B + p); ok = s == 200 and len(body) > 50
    except Exception as e: ok, s, body = False, str(e)[:40], b""
    bad += not ok; print(f"  {'OK ' if ok else 'BAD'} {p} {s} {len(body)}")
try:
    s, body = get(B + "/"); t = body.decode("utf-8", "ignore")
    for need, label in [("Not a government app", "government notice"), ("fonts/anek-telugu", "built-in fonts")]:
        ok = need in t; bad += not ok; print(f"  {'OK ' if ok else 'BAD'} {label}")
    ok = "fonts.googleapis" not in t; bad += not ok; print(f"  {'OK ' if ok else 'BAD'} no Google Fonts request")
except Exception as e: bad += 1; print("  BAD home page", e)
print("Register (read only)")
for st in ["ap", "ts"]:
    try:
        s, body = get(REG + "?state=" + st, 90); j = json.loads(body); reps = j.get("reports", [])
        last = max((r.get("created", "") for r in reps), default="")
        print(f"  OK  {st}: {len(reps)} reports, {len(j.get('hidden', []))} hidden, newest {last[:10] or '-'}")
    except Exception as e: bad += 1; print(f"  BAD {st}: {e}")
print("Data freshness")
try:
    s, body = get(B + "/data/finance.json"); f = json.loads(body); up = f["meta"]["updated"]
    age = (time.time() - time.mktime(time.strptime(up, "%Y-%m-%d"))) / 86400
    print(f"  {'OK ' if age < 120 else 'OLD'} finance data updated {up} ({int(age)} days ago)")
except Exception as e: bad += 1; print("  BAD finance data", e)
print("LIVE_BAD", bad)
