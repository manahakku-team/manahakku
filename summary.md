| Target | At once | Requests | Succeeded | Typical wait | Slowest 5% | Per second | Errors |
|---|---|---|---|---|---|---|---|
| Website (GitHub Pages) | 50 | 300 | 100% | 0.23s | 0.80s | 161 | — |
| Website (GitHub Pages) | 200 | 1000 | 100% | 0.55s | 2.01s | 178 | — |
| Website (GitHub Pages) | 500 | 2000 | 100% | 0.55s | 7.78s | 182 | — |
| Reports copy (snapshot) | 50 | 300 | 100% | 0.01s | 0.17s | 1310 | — |
| Reports copy (snapshot) | 200 | 800 | 100% | 0.06s | 0.19s | 2406 | — |
| Live backend: read reports | 10 | 60 | 97% | 1.87s | 2.76s | 1 | {'TimeoutError': 2} |
| Live backend: read reports | 25 | 150 | 97% | 1.77s | 2.73s | 2 | {'TimeoutError': 5} |
| Live backend: read reports | 50 | 250 | 94% | 1.78s | 2.61s | 4 | {'TimeoutError': 14} |
| Live backend: read reports | 100 | 400 | 80% | 1.95s | 3.30s | 6 | {'200': 60, 'TimeoutError': 18} |