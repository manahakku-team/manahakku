#!/bin/bash
B=https://manahakku-team.github.io/manahakku
for u in / /about.html /privacy.html /d/ /d/ap-guntur.html /d/ts-hyderabad.html /sitemap.xml /robots.txt /og.png /sw.js /data/finance.json /data/cag-2024-25.json /fonts/hind-guntur-telugu-400-normal.woff2 /fonts/anek-telugu-telugu-700-normal.woff2 /pdfjs/web/viewer.html /docs/constitution-te.pdf /nope-404; do
  printf '%-48s %s %s\n' "$u" $(curl -s -o /dev/null -w '%{http_code} %{size_download}' "$B$u"); done
curl -s "$B/" | grep -c 'fonts.googleapis' | sed 's/^/google-font-refs: /'
curl -s "$B/" | grep -o 'Not a government app[^"]\{0,30\}' | head -1
curl -s "$B/sitemap.xml" | grep -c '<loc>' | sed 's/^/sitemap urls: /'
