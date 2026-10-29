# Mana Hakku daily quality check, 2026-10-29

Build: a1f7e5d Daily quality check (screens, live site/register/data, live news) and weekly Andro

## 1. App logic tests
```
  SURE  got sanitation/null  want sanitation/garbage  | chetta teeyatledu, dhomalu ekkuva
  popup got water/supply  want sanitation/toilet  | Community toilet is locked and has no water
Auto-correction 16/16
guide: 7 tabs checked, change log 2026-10-29
```

## 2. Every screen (2 states x 2 languages x light/dark x 2 phone sizes + offline)
```
offline money text:         ప్రజా ధనం: మీ రాష్ట్ర డబ్బు, సులభంగావినండి     రాష్ట్రానికి డబ్బు ఎక్కడి

TOTAL 0
```

## 3. Live website, register and data
```
Website
  OK  / 200 910172
  OK  /about.html 200 10376
  OK  /privacy.html 200 15038
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
  OK  ap: 7 reports, 0 hidden, newest 2026-10-27
  OK  ts: 1 reports, 0 hidden, newest 2026-10-26
Data freshness
  OK  finance data updated 2026-10-26 (3 days ago)
LIVE_BAD 0
```

## 4. Live news check (real Google News through the register)
```
OK   ap te "మాజీ సీఎం గ్రామాల్లో పర్యటించారు" @ East Godavari: 4 naming the district
      - దేవరపల్లి: జెన్‌జీ సైతం వైఎస్‌ జగన్‌ వెంటే..
      - దేవరపల్లి: జెన్‌జీ సైతం వైఎస్‌ జగన్‌ వెంటే..
      - Gopalapuram: ఆగస్టు 5న వైఎస్సార్‌సీపీ అధినేత వైఎస్ జగన్ మోహన్ రెడ్డి పర్యటన
      - Gopalapuram: ఆగస్టు 5న వైఎస్సార్‌సీపీ అధినేత వైఎస్ జగన్ మోహన్ రెడ్డి పర్యటన
OK   ap en "Drinking water shortage in villages" @ Guntur: 2 naming the district
      - Rs 550 cr drinking water project for Guntur awaits cabinet nod
      - Rs 550 cr drinking water project for Guntur awaits cabinet nod
OK   ap en "Road accident on highway" @ Krishna: 10 naming the district
      - 17 Injured in Road Accident Near Pendur in NTR Krishna District
      - 17 Injured in Road Accident Near Pendur in NTR Krishna District
      - Four Killed in Road Accident in Krishna District
      - Four Killed in Road Accident in Krishna District
OK   ts en "Doctors absent at government hospital" @ Hyderabad: 6 naming the district
      - Doctor shortage, poor emergency care crippling Hyderabad government hospitals, says HRF
      - Doctor shortage, poor emergency care crippling Hyderabad government hospitals, says HRF
      - Telangana: Hyderabad medical colleges have 71% more doctors than required, Asifabad faces 73% vacancies
      - Telangana: Hyderabad medical colleges have 71% more doctors than required, Asifabad faces 73% vacancies
OK   ts te "రైతుల ఆందోళన" @ Khammam: 6 naming the district
      - Farmers | మక్కలు అమ్మిన రైతుల పేర్లు ఆన్‌లైన్‌లో గల్లంతు.. ఖమ్మం మార్క్‌ఫెడ్‌ అధికారుల నిర్లక్ష్యం!
      - Farmers | మక్కలు అమ్మిన రైతుల పేర్లు ఆన్‌లైన్‌లో గల్లంతు.. ఖమ్మం మార్క్‌ఫెడ్‌ అధికారుల నిర్లక్ష్యం!
      - Kodada : సూర్యాపేట- ఖమ్మం జాతీయ రహదారిపై రైతుల ధ‌ర్నా
      - Kodada : సూర్యాపేట- ఖమ్మం జాతీయ రహదారిపై రైతుల ధ‌ర్నా
OK   ts en "Floods damage crops" @ Warangal: 6 naming the district
      - Rain Damages Crops, Disrupts Transport In Warangal
      - Rain Damages Crops, Disrupts Transport In Warangal
      - Cyclone Montha hits Warangal, Hanamkonda hard, colonies inundated
      - Cyclone Montha hits Warangal, Hanamkonda hard, colonies inundated
NEWS_NONE 0
```
