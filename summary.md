| Target | At once | Requests | Succeeded | Typical wait | Slowest 5% | Per second | Errors |
|---|---|---|---|---|---|---|---|
| Website (GitHub Pages) | 50 | 300 | 100% | 0.18s | 0.49s | 184 | — |
| Website (GitHub Pages) | 200 | 1000 | 100% | 0.47s | 3.32s | 207 | — |
| Website (GitHub Pages) | 500 | 2000 | 100% | 0.48s | 5.76s | 211 | — |
| Reports copy (snapshot) | 50 | 300 | 100% | 0.00s | 0.29s | 1000 | — |
| Reports copy (snapshot) | 200 | 800 | 100% | 0.05s | 0.15s | 2889 | — |
| Live backend: read reports | 10 | 60 | 100% | 1.63s | 2.48s | 5 | — |
| Live backend: read reports | 25 | 150 | 100% | 1.64s | 2.75s | 13 | — |
| Live backend: read reports | 50 | 250 | 97% | 1.75s | 2.49s | 25 | {'200': 8} |
| Live backend: read reports | 100 | 400 | 36% | 2.14s | 3.05s | 70 | {'200': 256} |