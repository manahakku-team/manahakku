import json,sys
R=lambda a,b:[str(x) for x in range(a,b+1)]
# RBI State Finances functional classification -> major heads (revenue 2xxx/3xxx, capital outlay 4xxx/5xxx, loans 6xxx)
MAP={
 'education':(R(2202,2205),['4202'],['6202']),
 'health':(['2210','2211'],['4210','4211'],['6210','6211']),
 'water':(['2215'],['4215'],['6215']),
 'housing':(['2216'],['4216'],['6216']),
 'urban':(['2217'],['4217'],[]),
 'welfare':(['2225'],['4225'],[]),
 'labour':(['2230'],[],[]),
 'socialsec':(['2235'],['4235'],[]),
 'nutrition':(['2236'],[],[]),
 'calamity':(['2245'],[],[]),
 'agri':(R(2401,2435),R(4401,4435),R(6401,6435)),
 'rural':(['2501','2505','2506','2515'],['4515'],R(6501,6515)),
 'irrigation':(R(2700,2711),R(4700,4711),R(6700,6711)),
 'energy':(R(2801,2810),R(4801,4810),R(6801,6810)),
 'industry':(R(2851,2885),R(4851,4885),R(6851,6885)),
 'transport':(R(3051,3075),R(5051,5075),[]),
}
def calc(H,cur=True):
    out={}
    for k,(rv,cp,ln) in MAP.items():
        v=0;
        for c in rv+cp:
            for x in H.get(c,[]): v+= x[1] if cur else (x[2] or 0)
        lo=sum(x[1] for c in ln for x in H.get(c,[]))
        out[k]=(round(v),round(lo))
    return out
if __name__=='__main__':
    H=json.load(open(sys.argv[1]));st=sys.argv[2]
    F=json.load(open('/home/claude/manahakku/web/data/finance.json'));cats=F['meta']['cats'];Y=F['years']
    i23=Y.index('2023-24');i24=Y.index('2024-25')
    c23=calc(H,False);c24=calc(H,True)
    print('%-10s %8s %8s %6s | %8s %6s %8s'%('area','RBI23','CAG23*','diff%','CAG24','loan24','plan24'))
    for k in MAP:
        j=cats.index(k);rbi=F[st]['cat'][i23][j][1];plan=F[st]['cat'][i24][j][0]
        r,_=c23[k];a,l=c24[k]
        print('%-10s %8s %8s %6s | %8s %6s %8s'%(k,rbi,r,round((r-rbi)/rbi*100,1) if rbi else '-',a+l,l,plan))
