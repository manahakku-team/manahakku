#!/bin/bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
sudo apt-get install -y -qq poppler-utils >/dev/null 2>&1
curl -sL -A "$UA" "https://d1jmc0u14z2tmp.cloudfront.net/uploads/state_accounts_report/account-report-Finance-Accounts-Volume-II-2024-25-069ce5095e7fc03-82827903.pdf" -o /tmp/ts.pdf
ls -la /tmp/ts.pdf; pdftotext -layout /tmp/ts.pdf out/ts_fa2_2425.txt 2>/dev/null; wc -c out/ts_fa2_2425.txt
