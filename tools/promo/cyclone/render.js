const {chromium}=require('playwright');const fs=require('fs');const D=__dirname;const {execSync}=require('child_process');
const vtt=f=>fs.readFileSync(f,'utf8').split(/\n\n+/).map(b=>b.trim().split('\n')).filter(l=>l.length>=3&&l[1].includes('-->')).map(l=>{const [a,c]=l[1].split(' --> ').map(x=>{const [h,m,s]=x.replace(',','.').split(':');return +h*3600+ +m*60+ +s});return {s:a,e:c,t:l.slice(2).join(' ')}});
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('http://localhost:8799/scene.html?lang=te&t=Warm%20up%20%E0%B0%AE%E0%B0%A8');await p.waitForTimeout(1500);await p.goto('http://localhost:8799/scene.html?lang=en&t=Warm%20up');await p.waitForTimeout(1500);
for(const lang of (process.env.LANGS||'en,te').split(',')){const cues=vtt(`${D}/${lang}.vtt`);const LEAD=+(process.env.LEAD||0.3);const dur=+require('child_process').execSync(`ffprobe -v error -show_entries format=duration -of csv=p=0 ${D}/${lang}.mp3`).toString();const TOTAL=Math.min(+(process.env.MAX||55),+(LEAD+dur+(+(process.env.TAIL||1.3))).toFixed(2));fs.mkdirSync(`${D}/${lang}`,{recursive:true});
 const shots=[];
 // background only
 await p.goto(`http://localhost:8799/scene.html?lang=${lang}&t=`);await p.waitForTimeout(400);await p.evaluate(()=>{document.getElementById('body').innerHTML=''});await p.screenshot({path:`${D}/${lang}/bg.png`});
 const PRE=+(process.env.PRE||0.25),fr=x=>Math.round(x*30)/30;const N=cues.length-1;for(let i=0;i<N;i++){const st=i===0?0:fr(Math.max(0,cues[i].s+LEAD-PRE)),en=fr(cues[i+1].s+LEAD-PRE);await p.goto(`http://localhost:8799/scene.html?lang=${lang}&t=${encodeURIComponent(cues[i].t)}`);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);const f=`${D}/${lang}/s${String(i).padStart(2,'0')}.png`;await p.screenshot({path:f});shots.push({f,d:+(en-st).toFixed(3)})}
 const used=shots.reduce((a,x)=>a+x.d,0);await p.goto(`http://localhost:8799/scene.html?lang=${lang}&end=1&t=${encodeURIComponent(cues[N].t)}`);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(150);await p.screenshot({path:`${D}/${lang}/zend.png`});shots.push({f:`${D}/${lang}/zend.png`,d:+(fr(TOTAL)-used).toFixed(3)});
 fs.writeFileSync(`${D}/${lang}/shots.json`,JSON.stringify(shots));console.log(lang,shots.length,'end card',shots.at(-1).d)}
await b.close()})();
