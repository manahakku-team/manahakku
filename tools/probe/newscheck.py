import json,sys,urllib.request,urllib.parse
REG="https://script.google.com/macros/s/AKfycbz08xXmFDTHqrcos-bO8lQW72yBKCRlL2gC8i3zktchZxnMngXD89ki6AyogSja9RyMNw/exec"
for lang,q in [("en",'"East Godavari" (ex OR former) (cm OR "chief minister")'),("te",'"తూర్పు గోదావరి" (మాజీ OR ex OR former) (సీఎం OR ముఖ్యమంత్రి OR cm)'),("en","East Godavari ex cm visited villages")]:
    u=REG+"?action=news&lang="+lang+"&q="+urllib.parse.quote(q)
    try: j=json.load(urllib.request.urlopen(u,timeout=60))
    except Exception as e: print("ERR",e); continue
    print("\n==",lang,q,"| engine",j.get("engine"),"| items",len(j.get("items",[])))
    for it in j.get("items",[])[:12]: print(" -",("[T] " if it.get("trusted") else "    ")+it.get("title","")[:110],"|",it.get("source",""),"|",it.get("date","")[:16])
