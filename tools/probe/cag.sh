#!/bin/bash
# Lists CAG state-accounts PDFs for AP (64) and Telangana (93) and converts the Finance Accounts to text in out/.
set -x
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
sudo apt-get install -y -qq poppler-utils >/dev/null 2>&1
for id in 64 93; do
  for pg in 0 1 2; do
    curl -sL -A "$UA" "https://cag.gov.in/en/state-accounts-report?defuat_state_id=$id&page=$pg" -o out/list_${id}_$pg.html
  done
  cat out/list_${id}_*.html | grep -oE 'https?://[^"]+\.pdf|/uploads/state_accounts_report/[^"]+\.pdf' | sort -u > out/links_$id.txt
  wc -l out/links_$id.txt
done
rm -f out/list_*.html
grep -ihE 'finance-accounts|glance' out/links_*.txt
get(){ u="$1"; n="$2"; case "$u" in /*) u="https://cag.gov.in$u";; esac
  curl -sL -A "$UA" "$u" -o /tmp/$n.pdf; ls -la /tmp/$n.pdf; pdftotext -layout /tmp/$n.pdf out/$n.txt; wc -c out/$n.txt; }
get "https://d1jmc0u14z2tmp.cloudfront.net/uploads/state_accounts_report/account-report-Finance-Accounts-Volume-II-2024-25-069aadbc2ef08b4-64872690.pdf" ap_fa2_2425
get "https://cag.gov.in/uploads/state_accounts_report/account-report-Accounts-at-a-Glance-2024-25-069ce4f81576fe5-74328385.pdf" ts_aag_2425
get "https://cag.gov.in/uploads/state_accounts_report/account-report-Accounts-at-a-Glance-2024-25-069aadac6722241-00178073.pdf" ap_aag_2425
i=0; for u in $(grep -ihE 'finance-accounts' out/links_*.txt); do i=$((i+1)); get "$u" "fa_$i"; head -c 600 out/fa_$i.txt | tr -s ' \n' ' '; echo; echo "fa_$i = $u"; done
ls -la out
