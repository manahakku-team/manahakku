#!/bin/bash
# Live check of the News check chart on the public website (real network, real news list).
R=https://raw.githubusercontent.com/manahakku-team/manahakku/newsfeed
for st in ap ts; do echo "== $st list: $(curl -s -o /dev/null -w '%{http_code} %{size_download} bytes' $R/news-$st.json) | CORS: $(curl -sI $R/news-$st.json | grep -i '^access-control-allow-origin' | tr -d '\r')"; done
mkdir -p /tmp/pw && cd /tmp/pw && npm init -y >/dev/null && npm i playwright@1.48.2 >/dev/null 2>&1 && npx playwright install --with-deps chromium >/dev/null 2>&1; cd - >/dev/null
cat > /tmp/pw/pie.js <<'JS'
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const errs=[];
for(const [lang,st,d] of [['te','ts','Hyderabad'],['en','ap','Guntur'],['en','ap','Krishna']]){const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});p.on('pageerror',e=>errs.push(e.message));
 await p.goto('https://manahakku-team.github.io/manahakku/');await p.evaluate(l=>{localStorage.clear();localStorage.setItem('mh-lang',l)},lang);
 await p.goto(`https://manahakku-team.github.io/manahakku/?v=${Date.now()}#${st}/news`);await p.reload();await p.waitForTimeout(3000);
 await p.selectOption('#n-district',d);await p.waitForFunction(()=>{const x=document.getElementById('n-pie');return x&&(x.querySelector('.nprow')||/could not|దొరకలేదు|తెరవలేక|No news/.test(x.innerText))},null,{timeout:30000}).catch(()=>{});
 const txt=(await p.$eval('#n-pie',e=>e.innerText)).replace(/\n+/g,' | ');console.log(`\n${lang} ${st} ${d}: ${txt.slice(0,420)}`);
 await (await p.$('#n-pie')).screenshot({path:`out/pie_${st}_${d}.png`});
 const row=await p.$('#n-pie .nprow');if(row){await row.click();await p.waitForTimeout(800);
  const pop=await p.evaluate(()=>({h:document.getElementById('src-pop-h').innerText,open:document.querySelectorAll('#src-pop-body a.nlink').length,blocked:document.querySelectorAll('#src-pop-body .nwarn').length,hosts:[...new Set([...document.querySelectorAll('#src-pop-body a.nlink')].map(a=>new URL(a.href).host))]}));
  console.log('   popup:',JSON.stringify(pop));await p.screenshot({path:`out/pop_${st}_${d}.png`})}
 await p.close()}
console.log('\npage errors:',errs.length?errs:'none');await b.close()})();
JS
NODE_PATH=/tmp/pw/node_modules node /tmp/pw/pie.js
