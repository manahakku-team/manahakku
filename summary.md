| Target | At once | Requests | Succeeded | Typical wait | Slowest 5% | Per second | Errors |
|---|---|---|---|---|---|---|---|
| Website (GitHub Pages) | 50 | 300 | 100% | 0.19s | 0.51s | 187 | — |
| Website (GitHub Pages) | 200 | 1000 | 100% | 0.48s | 1.74s | 206 | — |
| Website (GitHub Pages) | 500 | 2000 | 100% | 0.47s | 7.99s | 213 | — |
| Reports copy (snapshot) | 50 | 300 | 100% | 0.01s | 0.18s | 1342 | — |
| Reports copy (snapshot) | 200 | 800 | 100% | 0.05s | 0.14s | 3132 | — |
| Live backend: read reports | 10 | 60 | 100% | 2.01s | 3.93s | 4 | — |
| Live backend: read reports | 25 | 150 | 100% | 1.89s | 2.79s | 8 | — |
| Live backend: read reports | 50 | 250 | 100% | 1.91s | 2.87s | 23 | — |
| Live backend: read reports | 100 | 400 | 66% | 2.02s | 3.02s | 18 | {'200': 136} |