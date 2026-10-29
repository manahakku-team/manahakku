#!/bin/bash
# Live: how fast the Problems list appears on the public website, first visit (empty phone) and next visit.
mkdir -p /tmp/pw && cd /tmp/pw && npm init -y >/dev/null && npm i playwright@1.48.2 >/dev/null 2>&1 && npx playwright install --with-deps chromium >/dev/null 2>&1; cd - >/dev/null
echo "copy: $(curl -s -o /dev/null -w '%{http_code} %{size_download}b %{time_total}s' https://raw.githubusercontent.com/manahakku-team/manahakku/snapshot/reports-ap.json)"
cat > /tmp/pw/sp.js <<'JS'
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:390,height:844}});const p=await ctx.newPage();
const U='https://manahakku-team.github.io/manahakku/';await p.goto(U);await p.evaluate(()=>{localStorage.clear();localStorage.setItem('mh-lang','en')});
for(const v of ['first visit','next visit','next visit again']){await p.goto(U+'?v='+Date.now()+'#ap/all');const t0=Date.now();await p.reload();
 await p.waitForSelector('#a-list article',{timeout:20000}).catch(()=>{});console.log(`${v}: list after ${Date.now()-t0} ms · ${await p.$eval('#a-count',e=>e.innerText).catch(()=>'-')}`);await p.waitForTimeout(4000)}
await b.close()})();
JS
NODE_PATH=/tmp/pw/node_modules node /tmp/pw/sp.js
