#!/usr/bin/env python3
"""Read-only load test for Mana Hakku. Sends GET requests only: it never writes a report, suggestion or flag.
Usage: loadtest.py  -> prints a Markdown summary (also saved to /tmp/load/summary.md)."""
import asyncio, time, statistics, os, json, aiohttp

SITE = "https://manahakku-team.github.io/manahakku/"
SNAP = "https://raw.githubusercontent.com/manahakku-team/manahakku/snapshot/reports-ap.json"
REG = os.environ.get("REGISTER_URL", "")

async def one(s, url, out):
    t = time.monotonic()
    try:
        async with s.get(url, timeout=aiohttp.ClientTimeout(total=60)) as r:
            body = await r.read()
            ok = r.status == 200 and len(body) > 50
            if ok and "script.google" in url:
                try: ok = json.loads(body).get("ok") is True
                except Exception: ok = False
            out.append((ok, time.monotonic() - t, r.status))
    except Exception as e:
        out.append((False, time.monotonic() - t, type(e).__name__))

async def wave(url, conc, total):
    out = []; sem = asyncio.Semaphore(conc)
    async with aiohttp.ClientSession(headers={"User-Agent": "ManaHakku-loadtest"}) as s:
        async def go(i):
            async with sem: await one(s, url + ("&" if "?" in url else "?") + f"lt={i}-{time.time_ns()}", out)
        t0 = time.monotonic(); await asyncio.gather(*[go(i) for i in range(total)]); el = time.monotonic() - t0
    lat = sorted(x[1] for x in out if x[0]); okn = sum(1 for x in out if x[0])
    errs = {}
    for x in out:
        if not x[0]: errs[str(x[2])] = errs.get(str(x[2]), 0) + 1
    p = lambda q: f"{lat[min(len(lat)-1,int(len(lat)*q))]:.2f}s" if lat else "—"
    return dict(conc=conc, total=total, ok=okn, rate=f"{okn/total*100:.0f}%", p50=p(.5), p95=p(.95), rps=f"{total/el:.0f}", errs=errs)

async def main():
    rows = []
    plan = [("Website (GitHub Pages)", SITE, [(50, 300), (200, 1000), (500, 2000)]),
            ("Reports copy (snapshot)", SNAP, [(50, 300), (200, 800)])]
    if REG: plan.append(("Live backend: read reports", REG + "?state=ap", [(10, 60), (25, 150), (50, 250), (100, 400)]))
    for name, url, waves in plan:
        for conc, total in waves:
            r = await wave(url, conc, total); r["name"] = name; rows.append(r); print(r, flush=True)
            if "backend" in name and int(r["rate"][:-1]) < 50: print("stopping backend waves: too many failures", flush=True); break
            await asyncio.sleep(20 if "backend" in name else 3)
    md = "| Target | At once | Requests | Succeeded | Typical wait | Slowest 5% | Per second | Errors |\n|---|---|---|---|---|---|---|---|\n"
    md += "\n".join(f"| {r['name']} | {r['conc']} | {r['total']} | {r['rate']} | {r['p50']} | {r['p95']} | {r['rps']} | {r['errs'] or '—'} |" for r in rows)
    os.makedirs("/tmp/load", exist_ok=True); open("/tmp/load/summary.md", "w").write(md); print(md)

asyncio.run(main())
