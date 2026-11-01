import subprocess,csv,json,os
D=os.path.dirname(os.path.abspath(__file__));L=f"{D}/lines"
rows=[r for r in csv.reader(open(f"{L}/spec.tsv",encoding='utf-8'),delimiter='\t') if len(r)>=5]
def dur(f):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
for lang in ['en','te']:
    items=[(i,r) for i,r in enumerate(rows) if r[0]==lang]
    t=0.0;cues=[];inputs=[];filt=[];n=0
    for i,r in items:
        f=f"{L}/{i:03d}-{lang}.mp3";subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',f,'-af','silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse',f+'.t.wav'],check=True);d=dur(f+'.t.wav')
        # edge-tts adds ~0.1s silence at start/end; trim a little so pauses are the ones we chose
        cues.append((t,t+d,r[4]));inputs+=['-i',f];filt.append(f"[{n}:a]aresample=24000,silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur={float(r[3])+0.08}[a{n}]");n+=1
        t+=d+float(r[3])+0.08
    filt.append("".join(f"[a{k}]" for k in range(n))+f"concat=n={n}:v=0:a=1[out]")
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y',*inputs,'-filter_complex',";".join(filt),'-map','[out]','-c:a','libmp3lame','-q:a','2',f"{D}/{lang}.mp3"],check=True)
    def ts(x):h=int(x//3600);m=int(x%3600//60);s=x%60;return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.',',')
    with open(f"{D}/{lang}.vtt",'w',encoding='utf-8') as fo:
        for k,(a,b,txt) in enumerate(cues):fo.write(f"{k+1}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")
    print(lang,round(t,2),'s voice')
