#!/bin/bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
for st in telangana andhra-pradesh; do for ty in 359 360 361 362 363 364 365 366 367 368; do
  curl -sL -A "$UA" "https://cag.gov.in/ae/$st/en/state-accounts-report?defuat_account_report_type=$ty" -o /tmp/p.html
  echo "== $st $ty $(grep -o '<title>[^<]*' /tmp/p.html | head -1) $(wc -c </tmp/p.html)"
  grep -oE '(https?://[^"'"'"' ]+|/uploads/[^"'"'"' ]+)\.pdf' /tmp/p.html | sort -u | head -40
done; done
