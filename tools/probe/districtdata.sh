#!/bin/bash
# Reads official sites and lists any district-wise reports (links + titles). Read-only.
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
sudo apt-get install -y -qq poppler-utils >/dev/null 2>&1
get(){ curl -sL -A "$UA" --max-time 60 "$1" -o "/tmp/$2" ; echo "== $2  $(stat -c%s /tmp/$2 2>/dev/null) bytes  <- $1"; }
links(){ grep -oiE '<a[^>]+href="[^"]+"[^>]*>[^<]{3,140}' "/tmp/$1" | sed -E 's/<a[^>]+href="([^"]+)"[^>]*>/\1 | /' | grep -iE "$2" | sort -u | head -${3:-40}; }
get "https://nreganarep.nic.in/netnrega/MISreport4.aspx" nrega.html; links nrega.html "financ|expend|fund|wage|district" 50
get "https://ejalshakti.gov.in/IMISReports/" jjm.html; links jjm.html "district|financ" 30
get "https://egramswaraj.gov.in/" egs.html; links egs.html "report|financ|receipt|expend" 30
get "https://rhreporting.nic.in/netiay/newreport.aspx" pmayg.html; links pmayg.html "financ|fund|district|sanction|complet" 40
get "https://sbm.gov.in/sbmgdashboard/statesdashboard.aspx" sbm.html; links sbm.html "district|report" 20
get "https://finance.telangana.gov.in/" tsfin.html; links tsfin.html "budget|outcome|district" 30
get "https://nhm.gov.in/index1.php?lang=1&level=0&linkid=49&lid=61" nhm.html; links nhm.html "district|fund|state" 15
echo "== AP Outcome Budget 2025-26 (Vol VII/1)"
for u in "https://apfinance.gov.in/...Bud@et25-26/documents/Volume-VII-1.pdf" "https://apfinance.gov.in/uploads/budget-volumes/2025-26/Volume-VII-1.pdf"; do curl -sL -A "$UA" --max-time 90 "$u" -o /tmp/ob.pdf; file /tmp/ob.pdf | head -1; if pdftotext -layout /tmp/ob.pdf /tmp/ob.txt 2>/dev/null; then echo "pages text: $(wc -l </tmp/ob.txt) lines; 'district' mentions: $(grep -ci district /tmp/ob.txt)"; grep -i -m 25 district /tmp/ob.txt | cut -c1-160; break; fi; done
echo "== AP budget 2025-26 index (links to volumes)"; get "https://apfinance.gov.in/...Bud@et25-26/" apb.html; grep -oiE 'href="[^"]+\.pdf"' /tmp/apb.html | head -40
