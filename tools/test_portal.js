// Pilot test for the portal guide: every sample report must get a portal choice, colleges must never go to School Education,
// blame words must never be suggested, and the CPGRAMS English text must contain only allowed characters.
const fs=require("fs"),path=require("path");
const html=fs.readFileSync(path.join(__dirname,"..","app","src","main","assets","index.html"),"utf8");
const cut=(x,y)=>{const i=html.indexOf(x),j=html.indexOf(y,i);if(i<0||j<0)throw new Error("not found "+x);return html.slice(i,j)};
const a=html.indexOf("const S={"),b=html.indexOf("const SKEYS=Object.keys(S);"),c=html.indexOf("const kwScore="),d=html.indexOf("let subPick=null;");
const code="const L=v=>Array.isArray(v)?v[0]:v;"+html.slice(a,b+"const SKEYS=Object.keys(S);".length)+"\n"+html.slice(c,d)+"\n"+cut("const MK_D=","function portalBox(")+"\nmodule.exports={detect,detectSub,portalPick,cpClean,PG,MK_D};";
const m={exports:{}};new Function("module","exports",code)(m,m.exports);
const {detect,detectSub,portalPick,cpClean,PG,MK_D}=m.exports;
const cases=JSON.parse(fs.readFileSync(path.join(__dirname,"portal_cases.json"),"utf8"));
const BLAME=/corrupt|bribe|fake|misappropr|misbehav|harass|bogus|demanding money|staff misusing|favorit|colluded/i;
let fail=0,specific=0;const rows=[];
for(const [text,wantSec,wantSub,expect] of cases){
 const det=detect(text);
 // Test with the problem type the app itself picks (the person may keep it), falling back to the right one when the app asks.
 const sec=det.key||wantSec,sub=det.key&&det.key!==wantSec?(detectSub(sec,text)||null):(wantSub||(detectSub(sec,text)||null));
 const g=portalPick({sector:sec,sub,title:"",desc:text});
 const mk=!g?"NONE":g.m===null?"(own portal)":Array.isArray(g.m)?"search '"+g.m[0]+"' > "+g.m[1]:"dropdown: "+MK_D[g.m.d]+(g.m.hod?" > "+g.m.hod:"")+(g.m.subj?" > "+g.m.subj:"");
 const cp=!g||!g.c?"-":g.c.join(" > ");
 const isDefault=g&&!g.k&&!g.sub;
 let err="";
 if(!g)err="no rule";
 if(g&&BLAME.test(mk+" "+cp))err="blame word";
 if(expect&&!(mk+" "+cp).toLowerCase().includes(expect.toLowerCase()))err="expected '"+expect+"'";
 if(/college|degree|intermediate|కళాశాల/i.test(text)&&/School Education/.test(mk+cp))err="college sent to School Education";
 if(err)fail++;else if(!isDefault)specific++;
 rows.push({text:text.slice(0,70),det:det.key+(det.key===sec?"":" (≠"+sec+")"),mk,cp,def:isDefault?"fallback":"exact",err});
}
const bad=cpClean("రోడ్డు “bad” road – ₹500 needed 😀\nLine 2",2000);
if(/[^A-Za-z0-9 ,.\-_()\/:&@#$%*?+=!'"\n]/.test(bad)){fail++;console.log("cpClean left a bad character:",bad)}
if(process.argv.includes("-v"))rows.forEach(r=>console.log(`${r.err?"✗ "+r.err:"✓"} [${r.def}] ${r.text}\n    detect: ${r.det}\n    Meekosam: ${r.mk}\n    CPGRAMS: ${r.cp}`));
else rows.filter(r=>r.err).forEach(r=>console.log("✗",r.err,"|",r.text));
console.log(`portal guide: ${cases.length} cases · exact line ${specific} · fallback ${cases.length-specific-fail} · failed ${fail} · rules ${PG.length}`);
process.exit(fail?1:0);
