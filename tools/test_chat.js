// Tests the "Ask Mana Hakku" helper's local parts in a real browser: personal details and politics are refused
// on the phone, and the no-AI fallback (Home search) finds the right area for everyday questions.
// Usage: node tools/test_chat.js   (needs Playwright with Chromium)
const {chromium}=require("playwright");const http=require("http"),fs=require("fs"),path=require("path");
const ROOT=path.join(__dirname,"..","app","src","main","assets");
const PII=["my number is 9876543210 no water","aadhaar 1234 5678 9012 correction","Ramesh garu is not giving pension","email me at someone@gmail.com"];
const POL=["which party is better","who will win the election","ముఖ్యమంత్రి గురించి చెప్పు","vote for which MLA"];
const FALL=[ // text, expected area from the quick search (the AI is off in this test)
 ["maa ooriki neellu raavatledu","water"],["no drinking water in our village","water"],["మా ఊరికి నీళ్లు రావట్లేదు","water"],
 ["pension raledu","elderly"],["old age pension not coming","elderly"],["school lo teacher ledu","education"],["no teacher in school","education"],
 ["aadhaar correction","iddocs"],["current poyindi","power"],["power cut every night","power"],["road full of potholes","roads"],
 ["drainage overflowing","sanitation"],["garbage not collected","sanitation"],["no doctor in PHC","health"],["ration card not given","nutrition"],
 ["crop insurance not paid","agri"],["house site patta","housing"],["flood water in houses","disaster"],["caste certificate delay","certs"],["child marriage in village","child"]];
const srv=http.createServer((q,r)=>{const f=path.join(ROOT,decodeURIComponent(q.url.split("?")[0]).replace(/^\/+/,"")||"index.html");
 fs.readFile(f,(e,b)=>{if(e){r.writeHead(404);r.end();return}r.writeHead(200,{"Content-Type":f.endsWith(".html")?"text/html; charset=utf-8":f.endsWith(".json")?"application/json":"application/octet-stream"});r.end(b)})});
srv.listen(0,async()=>{const port=srv.address().port;const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on("pageerror",e=>errs.push(e.message));
 await p.route(u=>!u.href.startsWith("http://localhost:"+port),r=>r.abort());
 await p.goto(`http://localhost:${port}/index.html`);await p.waitForTimeout(800);
 const res=await p.evaluate(([PII,POL,FALL])=>{const {chatLocal,chatQuick}=window.MH_CHAT;const out={pii:[],pol:[],fall:[]};
  PII.forEach(x=>out.pii.push([x,chatLocal(x).kind]));POL.forEach(x=>out.pol.push([x,chatLocal(x).kind]));
  FALL.forEach(([x,want])=>{const loc=chatLocal(x).kind;const q=chatQuick(x);const got=q.det||(q.items[0]&&(q.items[0].sector||(q.items[0].sectors||[])[0]))||null;out.fall.push([x,want,got,loc])});return out},[PII,POL,FALL]);
 let bad=0;
 res.pii.forEach(([x,k])=>{if(k!=="pii"){bad++;console.log("  PII not refused:",x,k)}});
 res.pol.forEach(([x,k])=>{if(k!=="politics"){bad++;console.log("  politics not refused:",x,k)}});
 let fok=0;res.fall.forEach(([x,want,got,loc])=>{if(loc!=="ok"){bad++;console.log("  wrongly refused:",x,loc)}else if(got===want)fok++;else console.log("  fallback got",got,"want",want,"|",x)});
 console.log(`Chat: personal details refused ${res.pii.length-res.pii.filter(([,k])=>k!=="pii").length}/${res.pii.length} · politics refused ${res.pol.filter(([,k])=>k==="politics").length}/${res.pol.length} · quick search right ${fok}/${res.fall.length}`);
 if(errs.length){console.log("  page errors:",errs.slice(0,3));bad++}
 await b.close();srv.close();
 if(bad||fok<Math.ceil(res.fall.length*0.8)){console.error("Chat test failed");process.exit(1)}})
