// Lists reports the app keeps out of the public list because a Sheet cell holds a wrong value.
// Usage: node tools/check_reports.js reports-ap.json reports-ts.json   (files from the "snapshot" branch)
const fs=require("fs"),path=require("path");
const html=fs.readFileSync(path.join(__dirname,"..","app","src","main","assets","index.html"),"utf8");
const M=require(path.join(__dirname,"..","web","data","mandals.json"));
const a=html.indexOf("const S={"),b=html.indexOf("const SKEYS=Object.keys(S);");const m={exports:{}};
new Function("module",html.slice(a,b)+"\nmodule.exports=S;")(m);const S=m.exports;
const nk=v=>String(v==null?"":v).trim().toLowerCase().replace(/\s+/g," ");let bad=0;
for(const f of process.argv.slice(2)){const st=/-ts\b/.test(f)?"ts":"ap";const D=Object.keys(M[st]).map(nk);const j=JSON.parse(fs.readFileSync(f,"utf8"));
 for(const r of j.reports||[]){const why=[];if(!D.includes(nk(r.district)))why.push(`district "${r.district}" is not a ${st.toUpperCase()} district`);if(!(nk(r.sector) in S))why.push(`sector "${r.sector}" is not a category (use one of: ${Object.keys(S).join(", ")})`);
  if(why.length){bad++;console.log(`HELD BACK ${r.id}: ${why.join("; ")}`)}}}
console.log(bad?`${bad} report(s) hidden from the public list until the Sheet is corrected.`:"All reports pass; every one is visible.");process.exitCode=bad?1:0;
