# Checks a register address without writing anything: list loads, unknown step is refused, unknown flag id is not found.
import json,urllib.request,sys
u=sys.argv[1]
def post(d):
    r=urllib.request.Request(u,data=json.dumps(d).encode(),headers={'Content-Type':'text/plain;charset=utf-8'})
    return urllib.request.urlopen(r,timeout=90).read().decode()[:200]
for st in ['ap','ts']:
    g=json.loads(urllib.request.urlopen(u+'?state='+st,timeout=90).read())
    print(st,'ok',g.get('ok'),'reports',len(g.get('reports',[])),'hidden',len(g.get('hidden',[])))
print('step check:',post({"type":"step","s":"zz_check","state":"ap"}))
print('flag check:',post({"type":"flag","id":"rzzzzprobe2","reason":"other","note":"","state":"ap","dev":"probecheck0000000000000002"}))
print('owner check (wrong code):',post({"type":"owner_check","code":"x"}))
