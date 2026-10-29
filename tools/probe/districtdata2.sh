#!/bin/bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
echo "== JJM district FHTC report"; curl -sL -A "$UA" --max-time 90 "https://ejalshakti.gov.in/JJM/JJMReports/Physical/JJMRep_DistrictWiseFHTCCoverage.aspx" -o /tmp/j.html; echo "$(stat -c%s /tmp/j.html) bytes"
python3 - <<'PY'
import re,html
t=open('/tmp/j.html',encoding='utf-8',errors='ignore').read()
txt=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S);txt=html.unescape(re.sub(r'<[^>]+>','|',txt));txt=re.sub(r'\|[\s|]*\|','|',txt)
print('headings:',[h for h in re.findall(r'[A-Za-z][A-Za-z %()/.-]{6,60}',txt) if re.search(r'(?i)district|state|connection|coverage|households|as on|%',h)][:25])
for name in ['Guntur','Krishna','Prakasam','Khammam','Warangal','Nalgonda','ANDHRA','TELANGANA']:
    i=txt.find(name);print(name,'->',txt[max(0,i-80):i+200].replace('\n',' ') if i>=0 else 'not on first page')
print('state dropdown:', 'ddState' in t or 'ddlState' in t, re.findall(r'<select[^>]+id="([^"]+)"',t)[:5])
PY
for u in "http://nreganarep.nic.in/netnrega/MISreport4.aspx" "https://nreganarep.nic.in/netnrega/MISreport4.aspx" "https://egramswaraj.gov.in/" "https://rhreporting.nic.in/" "https://finance.telangana.gov.in/" "https://www.telangana.gov.in/" ; do echo "$u -> $(curl -s -o /dev/null -A "$UA" --max-time 45 -w '%{http_code} %{size_download}b %{time_total}s' "$u")"; done
