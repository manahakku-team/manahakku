#!/bin/bash
# Checks that the website and its data files open (status code and size).
B=${1:-https://manahakku-team.github.io/manahakku}
for p in / about.html privacy.html data/finance.json data/keywords.json data/mandals.json sw.js; do
  echo "$(curl -s -o /dev/null -w '%{http_code} %{size_download}' "$B/$p") $B/$p"
done
curl -s "$B/" | grep -o '<title>[^<]*' | head -1
