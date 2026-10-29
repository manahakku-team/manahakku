#!/bin/bash
cd /tmp && npm i -s @fontsource/anek-telugu @fontsource/hind-guntur @fontsource/ibm-plex-mono >/dev/null 2>&1
cd - >/dev/null; mkdir -p out/fonts
for w in 500 600 700; do for sub in telugu latin; do cp /tmp/node_modules/@fontsource/anek-telugu/files/anek-telugu-$sub-$w-normal.woff2 out/fonts/; done; done
for w in 400 500 600; do for sub in telugu latin; do cp /tmp/node_modules/@fontsource/hind-guntur/files/hind-guntur-$sub-$w-normal.woff2 out/fonts/; done; done
cp /tmp/node_modules/@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2 out/fonts/
grep -h -A8 'telugu' /tmp/node_modules/@fontsource/hind-guntur/400.css | head -20 > out/unicode.txt
grep -h -A8 'latin' /tmp/node_modules/@fontsource/hind-guntur/400.css | grep unicode-range | head -3 >> out/unicode.txt
cat /tmp/node_modules/@fontsource/*/package.json | grep -E '"(name|version|license)"' > out/licenses.txt
ls -la out/fonts
