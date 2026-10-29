// Daily live news check: runs the real "Is this news true?" search (real register, real Google News) for sample
// stories in both states and reports how many results name the chosen district. Usage: node tools/qa/news_live.js <base url>
const {chromium}=require('playwright');(async()=>{const BASE=process.argv[2]||'http://localhost:8765';const b=await chromium.launch();
const CASES=[['ap','te','మాజీ సీఎం గ్రామాల్లో పర్యటించారు','East Godavari'],['ap','en','Drinking water shortage in villages','Guntur'],['ap','en','Road accident on highway','Krishna'],
 ['ts','en','Doctors absent at government hospital','Hyderabad'],['ts','te','రైతుల ఆందోళన','Khammam'],['ts','en','Floods damage crops','Warangal']];
let bad=0;for(const [st,lang,txt,d] of CASES){const p=await b.newPage({viewport:{width:390,height:844}});
 await p.goto(BASE+'/index.html');await p.evaluate(l=>{localStorage.clear();localStorage.setItem('mh-lang',l)},lang);await p.goto(`${BASE}/index.html#${st}/news`);await p.reload();await p.waitForTimeout(2500);
 await p.fill('#n-text',txt);await p.selectOption('#n-district',d).catch(()=>{});await p.waitForTimeout(300);await p.click('#n-auto');
 await p.waitForFunction(()=>{const x=document.getElementById('src-pop');return x&&x.open},null,{timeout:90000}).catch(()=>{});await p.waitForTimeout(500);
 const r=await p.evaluate(()=>{const body=document.getElementById('src-pop-body');if(!body)return null;const blocks=[...body.querySelectorAll('.block')];
  const main=blocks.find(x=>!x.classList.contains('wide')),wide=blocks.find(x=>x.classList.contains('wide'));const titles=e=>e?[...new Set([...e.querySelectorAll('.nitem')].map(n=>n.innerText.split('\n')[0].trim()).filter(Boolean))]:[];
  return {main:titles(main),wide:titles(wide),none:!main&&body.innerText.slice(0,120)}});
 const ok=r&&r.main.length>0;if(!ok)bad++;
 console.log(`${ok?'OK  ':'NONE'} ${st} ${lang} "${txt}" @ ${d}: ${r?r.main.length:0} naming the district${r&&r.wide.length?`, ${r.wide.length} wider`:''}`);
 (r?r.main:[]).slice(0,4).forEach(t=>console.log('      - '+t.slice(0,110)));await p.close()}
console.log('NEWS_NONE',bad);await b.close()})();
