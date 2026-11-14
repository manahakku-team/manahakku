# Mana Hakku daily quality check, 2026-11-14

Build: 6290722 Home: remove the three duplicate tabs (report, problems near me, rights); one line

## 1. App logic tests
```
  popup got water/null  want sanitation/drain  | drain water entering houses after rain
  popup got null/null  want child/-  | chinna pillalu hotel lo pani chestunnaru
Auto-correction 22/22
guide: 7 tabs checked, change log 2026-10-30
```

## 2. Every screen (2 states x 2 languages x light/dark x 2 phone sizes + offline)
```
offline money text:         ప్రజా ధనం: మీ రాష్ట్ర డబ్బు, సులభంగావినండి     రాష్ట్రానికి డబ్బు ఎక్కడి

TOTAL 0
```

## 3. Live website, register and data
```
Website
  OK  / 200 1425225
  OK  /about.html 200 10376
  OK  /privacy.html 200 19981
  OK  /d/ 200 13148
  OK  /d/ap-guntur.html 200 11369
  OK  /d/ts-hyderabad.html 200 7745
  OK  /sitemap.xml 200 7594
  OK  /data/finance.json 200 12526
  OK  /data/cag-2024-25.json 200 604
  OK  /fonts/hind-guntur-telugu-400-normal.woff2 200 71540
  OK  /pdfjs/web/viewer.html 200 67729
  OK  /docs/constitution-te.pdf 200 2734789
  OK  government notice
  OK  built-in fonts
  OK  no Google Fonts request
Register (read only)
  OK  ap: 11 reports, 0 hidden, newest 2026-11-14
  OK  ts: 1 reports, 0 hidden, newest 2026-10-26
Data freshness
  OK  finance data updated 2026-10-26 (19 days ago)
LIVE_BAD 0
```

## 4. Live news check (real Google News through the register)
```
OK   ap te "మాజీ సీఎం గ్రామాల్లో పర్యటించారు" @ East Godavari: 2 naming the district
      - Gopalapuram: ఆగస్టు 5న వైఎస్సార్‌సీపీ అధినేత వైఎస్ జగన్ మోహన్ రెడ్డి పర్యటన
      - Deputy CM Pawan Kalyan: నేడు నిడదవోలుకు పవన్‌ కల్యాణ్‌.. ‘అమరజీవి జలధారా’కు శంకుస్థాపన..
OK   ap en "Drinking water shortage in villages" @ Guntur: 1 naming the district
      - Rs 550 cr drinking water project for Guntur awaits cabinet nod
OK   ap en "Road accident on highway" @ Krishna: 7 naming the district
      - 17 Injured in Road Accident Near Pendur in NTR Krishna District
      - Four Killed in Road Accident in Krishna District
      - Four dead in separate road accidents in NTR, Krishna districts in Andhra Pradesh
      - Tipper truck plunges into Krishna River after crashing into car on Karnataka bridge; driver missing
OK   ts en "Doctors absent at government hospital" @ Hyderabad: 4 naming the district
      - Hyderabad: Osmania General Hospital’s new Goshamahal complex faces delays, doctors seek faster progress
      - Doctor shortage, poor emergency care crippling Hyderabad government hospitals, says HRF
      - Telangana: Hyderabad medical colleges have 71% more doctors than required, Asifabad faces 73% vacancies
      - SWASA Hospital | Freedom to Breath | Hyderabad | Dr. Vishnu Veerapaneni | RTV
OK   ts te "రైతుల ఆందోళన" @ Khammam: 1 naming the district
      - Khammam: ప్రభుత్వ నిర్లక్ష్యంతోనే రైతుల కష్టాలు – పువ్వాడ అజయ్ కుమార్
OK   ts en "Floods damage crops" @ Warangal: 2 naming the district
      - Warangal, Hanamkonda Steps Up Relief Works After Floods
      - Cyclone Montha hits Warangal, Hanamkonda hard, colonies inundated
NEWS_NONE 0
```
