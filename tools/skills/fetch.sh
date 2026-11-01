#!/usr/bin/env bash
# Skills-gap study, step 1: downloads government reports that cannot be opened from the build machine,
# keeps only text lines about Andhra Pradesh and Telangana, and lists links found on index pages.
# Output folder (default /tmp/skills): report.txt, links.txt, <name>.txt extracts. PDFs themselves are not kept.
set +e
OUT=${1:-/tmp/skills}; mkdir -p "$OUT"; R=$OUT/report.txt; : > "$R"
UA="Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36"
get(){ out=$1; shift; for u in "$@"; do code=$(curl -sSL --retry 2 -m 240 -A "$UA" -o "$out" -w "%{http_code}" "$u" 2>>"$R"); echo "$(basename "$out") <- $u : HTTP $code, $(stat -c%s "$out" 2>/dev/null) bytes, $(file -b "$out" | cut -c1-30)" >> "$R"; [ "$code" = 200 ] && return 0; done; return 1; }
extract(){ # name pdf : text lines that mention either state, with 2 lines of context
  pdftotext -layout "$2" "$OUT/$1.full" 2>>"$R" || return
  grep -n -i -B2 -A2 -E "andhra|telangana|single.teacher|specialist|veterinar|extension" "$OUT/$1.full" | head -3000 > "$OUT/$1.txt"
  echo "$1: $(wc -l < "$OUT/$1.full") lines, $(wc -l < "$OUT/$1.txt") kept" >> "$R"; rm -f "$OUT/$1.full"; }
links(){ # name page-url regex : PDF links on an index page
  get "$OUT/$1.html" "$2" && grep -o -i -E 'href="[^"]+"' "$OUT/$1.html" | sed 's/href="//;s/"$//' | grep -i -E "$3" | sort -u | sed "s|^|$1 |" >> "$OUT/links.txt"; rm -f "$OUT/$1.html"; }
T=$(mktemp -d)
# Index pages: where the current reports are linked
links hmis "https://hmis.mohfw.gov.in/" "dynamic|rhs|hdi|pdf"
links hmis_pub "https://hmis.mohfw.gov.in/#!/publications" "dynamic|pdf"
links mohfw_pub "https://mohfw.gov.in/?q=publications-11" "dynamic|statistic|pdf"
links mohfw_arch "https://www.mohfw.gov.in/documents/publication/archives" "dynamic|pdf"
links udise "https://udiseplus.gov.in/" "report|pdf|card"
links cag_ap "https://cag.gov.in/ag/andhra-pradesh/en/audit-report" "health|phims|pdf"
links cag_ts "https://cag.gov.in/ag/telangana/en/audit-report" "health|pdf"
# Known reports
get $T/udise.pdf "https://dashboard.udiseplus.gov.in/report2026/static/media/UDISE+2024_25_Booklet_existing.118ba29d4773e6372f72.pdf" && extract udise_booklet $T/udise.pdf
get $T/cag1.pdf "https://cag.gov.in/uploads/download_audit_report/2024/Chapter-2-Human-Resources-0676d3322b08c80.89268941.pdf" && extract cag_hr_chapter $T/cag1.pdf
get $T/cag2.pdf "https://cag.gov.in/uploads/download_audit_report/2024/AG-Report-PHIMS-Eng-067f8b204b96f61.37967228.pdf" && extract cag_phims $T/cag2.pdf
get $T/cag3.pdf "https://cag.gov.in/uploads/download_audit_report/2024/6-Executive-Summary-067567e0a5152f9.68802700.pdf" && extract cag_exec_summary $T/cag3.pdf
# Any Health Dynamics PDF found on the index pages
grep -i -E "dynamic" "$OUT/links.txt" | awk '{print $2}' | head -5 | while read -r u; do case "$u" in http*) ;; /*) u="https://hmis.mohfw.gov.in$u";; *) continue;; esac; n=hdi_$(echo "$u" | md5sum | cut -c1-6); get $T/$n.pdf "$u" && extract $n $T/$n.pdf; done
ls -la "$OUT" >> "$R"
