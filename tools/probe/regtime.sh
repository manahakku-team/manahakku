#!/bin/bash
# Times the report register (read only): 4 calls per state, a few seconds apart.
for st in ap ts; do for i in 1 2 3 4; do curl -s -L -o /dev/null -w "$st call $i: %{time_total}s (%{size_download} bytes)\n" "https://script.google.com/macros/s/AKfycbz08xXmFDTHqrcos-bO8lQW72yBKCRlL2gC8i3zktchZxnMngXD89ki6AyogSja9RyMNw/exec?state=$st&t=$RANDOM"; sleep 3; done; done
echo "raw.githubusercontent (CDN) for comparison:"; for i in 1 2; do curl -s -o /dev/null -w "news-ap.json: %{time_total}s\n" https://raw.githubusercontent.com/manahakku-team/manahakku/newsfeed/news-ap.json; done
