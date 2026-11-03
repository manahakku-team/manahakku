# Mana Hakku daily quality check, 2026-11-03

Build: f2732bd Sunday load test at 5:37 AM so the report arrives before 7 AM

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
  OK  / 200 1414528
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
  OK  ap: 8 reports, 0 hidden, newest 2026-10-30
  OK  ts: 1 reports, 0 hidden, newest 2026-10-26
Data freshness
  OK  finance data updated 2026-10-26 (8 days ago)
LIVE_BAD 0
```

## 4. Live news check (real Google News through the register)
```
OK   ap te "మాజీ సీఎం గ్రామాల్లో పర్యటించారు" @ East Godavari: 1 naming the district
      - Deputy CM Pawan Kalyan: నేడు నిడదవోలుకు పవన్‌ కల్యాణ్‌.. ‘అమరజీవి జలధారా’కు శంకుస్థాపన..
OK   ap en "Drinking water shortage in villages" @ Guntur: 1 naming the district
      - Rs 550 cr drinking water project for Guntur awaits cabinet nod
OK   ap en "Road accident on highway" @ Krishna: 7 naming the district
      - 17 Injured in Road Accident Near Pendur in NTR Krishna District
      - Four killed in road accident in Vuyyuru
      - Four Killed in Road Accident in Krishna District
      - Four dead in separate road accidents in NTR, Krishna districts in Andhra Pradesh
OK   ts en "Doctors absent at government hospital" @ Hyderabad: 2 naming the district
      - Doctor shortage, poor emergency care crippling Hyderabad government hospitals, says HRF
      - Telangana: Hyderabad medical colleges have 71% more doctors than required, Asifabad faces 73% vacancies
OK   ts te "రైతుల ఆందోళన" @ Khammam: 2 naming the district
      - Farmers | మక్కలు అమ్మిన రైతుల పేర్లు ఆన్‌లైన్‌లో గల్లంతు.. ఖమ్మం మార్క్‌ఫెడ్‌ అధికారుల నిర్లక్ష్యం!
      - ఖమ్మం జిల్లాపై ‘అర్నబ్‌’ తుపాను ప్రభావం.. జిల్లా వ్యాప్తంగా మోస్తరు వర్షం
OK   ts en "Floods damage crops" @ Warangal: 2 naming the district
      - Revanth to Conduct Aerial Survey in Warangal, Husnabad
      - Cyclone Montha hits Warangal, Hanamkonda hard, colonies inundated
NEWS_NONE 0
```
