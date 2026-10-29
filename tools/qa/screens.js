// Daily screen check: every tab and money section, both states, both languages, light/dark, 320 and 390 px, and offline.
// Looks for page errors, console errors, layout overflow, missing translations, broken images and unlabelled buttons.
// Usage: node tools/qa/screens.js <base url>   (serve app/src/main/assets first)
const {chromium}=require('playwright');(async()=>{const BASE=process.argv[2]||'http://localhost:8765';const b=await chromium.launch();const issues=[];const seen=new Set();
const add=(k,m)=>{const key=k+'|'+m;if(!seen.has(key)){seen.add(key);issues.push(key)}};
const mk=(i,st,d,s,stt,days)=>({id:'r'+i+'aaaa'+st,state:st,created:new Date(Date.now()-days*864e5).toISOString(),district:d,mandal:'',place:'Ward '+i,sector:s,title:'Problem number '+i,desc:'The details of this problem are written here.',affected:40,urgency:['high','medium','low'][i%3],status:stt,verify:{level:i%2}});
const views=['','report','dashboard','all','money','news','rights','history'];
for(const st of (process.env.QUICK?['ap']:['ap','ts']))for(const lang of (process.env.QUICK?['te']:['en','te']))for(const scheme of (process.env.QUICK?['light']:['light','dark']))for(const w of (process.env.QUICK?[390]:[320,390])){
 if(scheme==='dark'&&w===320)continue;
 const ctx=await b.newContext({viewport:{width:w,height:740},colorScheme:scheme});const p=await ctx.newPage();
 const tag=`${st}/${lang}/${scheme}/${w}`;
 p.on('pageerror',e=>add('JSERR',tag+' '+e.message));p.on('console',m=>{if(m.type()==='error'&&!/net::|Failed to load resource|ERR_/.test(m.text()))add('CONSOLE',m.text().slice(0,140))});
 const D=st==='ap'?['Guntur','Krishna','Chittoor']:['Hyderabad','Warangal','Adilabad'];const SEC=['water','health','roads','education','power','women','housing','agri'];
 const REPS=[];for(let i=0;i<14;i++)REPS.push(mk(i,st,D[i%3],SEC[i%8],i%4==0?'resolved':'reported',i*5));
 await p.route(/script\.google\.com/,r=>r.fulfill({contentType:'application/json',body:JSON.stringify({ok:true,state:st,reports:REPS,hidden:[]})}));
 await p.goto(BASE+'/index.html');await p.evaluate(l=>{localStorage.clear();localStorage.setItem('mh-lang',l)},lang);
 for(const v of views){
  await p.goto(`${BASE}/index.html#${st}${v?'/'+v:''}`);await p.reload();await p.waitForTimeout(1300);
  if(v==='all')await p.evaluate(()=>document.querySelectorAll('.numbox').forEach(d=>d.open=true));
  if(v==='rights'||v==='history')await p.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
  if(v==='money'){const secs=await p.$$eval('#m-nav button',x=>x.map(b=>b.dataset.s));for(const s of secs){await p.click(`#m-nav button[data-s="${s}"]`);await p.waitForTimeout(250);await check(p,tag+' money:'+s)}continue}
  await p.waitForTimeout(200);await check(p,tag+' '+(v||'home'));
 }
 await ctx.close()}
async function check(p,where){const r=await p.evaluate(()=>{const W=document.documentElement.clientWidth,res={over:[],keys:[],img:[],btn:[]};
  if(document.documentElement.scrollWidth>W+1)res.over.push('page '+document.documentElement.scrollWidth);
  for(const el of document.querySelectorAll('body *')){if(!el.offsetParent&&el.tagName!=='BODY')continue;const r=el.getBoundingClientRect();if(r.width>0&&r.right>W+2&&!el.closest('.scroll,.mtabs,.subnav,.chips,#m-years,pre,.hscroll,[style*="overflow"]')){const cs=getComputedStyle(el.parentElement||el);if(cs.overflowX!=='auto'&&cs.overflowX!=='scroll'&&cs.overflowX!=='hidden')res.over.push((el.id||el.className||el.tagName).toString().slice(0,40)+' '+Math.round(r.right))}}
  const tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=tw.nextNode()){const s=n.textContent.trim();if(/^[a-z]+[A-Z][A-Za-z0-9]+$/.test(s)&&n.parentElement.offsetParent)res.keys.push(s)}
  for(const im of document.querySelectorAll('img'))if(im.offsetParent&&im.complete&&im.naturalWidth===0&&!/^https?:\/\/(upload|commons)/.test(im.src))res.img.push(im.src.slice(-50));
  for(const b of document.querySelectorAll('button,a'))if(b.offsetParent&&!b.textContent.trim()&&!b.getAttribute('aria-label')&&!b.title&&!b.querySelector('img[alt]'))res.btn.push((b.id||b.className||b.tagName).toString().slice(0,40));
  res.over=[...new Set(res.over)].slice(0,6);res.keys=[...new Set(res.keys)];res.btn=[...new Set(res.btn)].slice(0,6);return res});
 if(r.over.length)add('OVERFLOW',where+': '+r.over.join(', '));if(r.keys.length)add('KEY',where+': '+r.keys.join(', '));if(r.img.length)add('IMG',where+': '+r.img.join(', '));if(r.btn.length)add('NOLABEL',where.split(' ')[1]+': '+r.btn.join(', '))}
// offline: no network at all
{const ctx=await b.newContext({viewport:{width:390,height:740}});const p=await ctx.newPage();p.on('pageerror',e=>add('JSERR','offline '+e.message));
 await p.goto(BASE+'/index.html');await p.route(/^https?:\/\/(?!localhost)/,r=>r.abort());
 for(const v of views){await p.goto(`${BASE}/index.html#ap${v?'/'+v:''}`);await p.reload();await p.waitForTimeout(1500)}
 console.log('offline money text:',(await p.$eval('#v-money',e=>e.innerText.slice(0,80))).replace(/\n/g,' '));await ctx.close()}
console.log(issues.join('\n'));console.log('TOTAL',issues.length);process.exitCode=issues.length?1:0;await b.close()})();
