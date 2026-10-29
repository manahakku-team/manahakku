import re,sys,json
txt=open(sys.argv[1],encoding='utf-8',errors='ignore').read().split('\n')
TOK=re.compile(r'\(-\)\s*[\d,]+\.\d+|[\d,]+\.\d+|\.\.\.')
def nums(line):
    out=[];line=line.replace('. . .','...')
    for t in TOK.findall(line):
        if t=='...':out.append(0.0)
        else:
            neg=t.startswith('(-)');v=float(t.replace('(-)','').replace(',','').strip());out.append(-v if neg else v)
    return out
H={}
for i,l in enumerate(txt):
    m=re.search(r'Total\s*-\s*(\d{4})\b',l)
    if not m:continue
    c=m.group(1)
    if c[0] in '23':
        n=nums(l[m.end():])
        if len(n)>=4:
            H.setdefault(c,[]).append(('rev',n[-3]/100,n[-2]/100,i));continue
        for k in range(i+1,i+6):
            n=nums(txt[k])
            if len(n)>=4: H.setdefault(c,[]).append(('rev',n[-3]/100,n[-2]/100,i));break
        else: print('MISSING rev',c,i)
    elif c[0] in '45':
        n=nums(l)
        if len(n)<6:
            for k in range(i-1,i-5,-1):
                n=nums(txt[k])
                if len(n)>=6:break
        if len(n)>=6: H.setdefault(c,[]).append(('cap',n[4]/100,n[0]/100,i))
        else: print('MISSING cap',c,i)
    elif c[0] in '67':
        n=nums(l[m.end():])
        if len(n)>=6:
            H.setdefault(c,[]).append(('loan',n[2]/100,None,i));continue
        for k in range(i-1,i-4,-1):
            n=nums(txt[k])
            if len(n)>=6: H.setdefault(c,[]).append(('loan',n[2]/100,None,i));break
json.dump(H,open(sys.argv[2],'w'),indent=0)
dups={c:v for c,v in H.items() if len(v)>1}
print(len(H),'heads; dups:',{c:[(x[0],round(x[1],1),x[3]) for x in v] for c,v in list(dups.items())[:15]})
