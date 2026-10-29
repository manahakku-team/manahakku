#!/bin/bash
# Checks the old address: pages must be the forwarding page, data files must still be served.
O=${OLD_SITE:?set OLD_SITE to the old address}
for p in / privacy.html about.html "#ts/history" data/finance.json data/keywords.json data/mandals.json sw.js; do
  b=$(curl -s "$O/$p"); echo "$(curl -s -o /dev/null -w '%{http_code}' "$O/$p") fwd=$(echo "$b" | grep -c 'manahakku-team.github.io/manahakku') size=${#b} $p"
done
