| Target | At once | Requests | Succeeded | Typical wait | Slowest 5% | Per second | Errors |
|---|---|---|---|---|---|---|---|
| Website (GitHub Pages) | 50 | 300 | 100% | 0.19s | 0.37s | 194 | — |
| Website (GitHub Pages) | 200 | 1000 | 100% | 0.47s | 1.73s | 209 | — |
| Website (GitHub Pages) | 500 | 2000 | 100% | 0.47s | 8.46s | 213 | — |
| Reports copy (snapshot) | 50 | 300 | 100% | 0.01s | 0.11s | 1684 | — |
| Reports copy (snapshot) | 200 | 800 | 100% | 0.05s | 0.15s | 2560 | — |
| Live backend: read reports | 10 | 60 | 100% | 1.58s | 2.47s | 6 | — |
| Live backend: read reports | 25 | 150 | 100% | 1.59s | 2.26s | 14 | — |
| Live backend: read reports | 50 | 250 | 100% | 1.60s | 2.46s | 27 | — |
| Live backend: read reports | 100 | 400 | 60% | 1.90s | 2.61s | 52 | {'200': 159} |