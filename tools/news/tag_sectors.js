// Gives each news headline the same problem type the app would give it, using the app's own sorting (detect).
// Reads a JSON array of headlines on stdin and prints a JSON array of types ("" when the app would ask the person).
const fs=require("fs"),path=require("path");
const html=fs.readFileSync(path.join(__dirname,"..","..","app","src","main","assets","index.html"),"utf8");
const a=html.indexOf("const S={"),b=html.indexOf("const SKEYS=Object.keys(S);"),c=html.indexOf("const kwScore="),d=html.indexOf("let subPick=null;");
if(a<0||b<0||c<0||d<0)throw new Error("sorting code not found in the app");
const m={exports:{}};new Function("module","let LANG='en';const L=v=>Array.isArray(v)?v[0]:v;"+html.slice(a,b+"const SKEYS=Object.keys(S);".length)+"\n"+html.slice(c,d)+"\nmodule.exports={detect};")(m);
const titles=JSON.parse(fs.readFileSync(0,"utf8"));
// A headline's tail after "|" is usually the channel and hashtags, not the story.
console.log(JSON.stringify(titles.map(t=>{const x=String(t||"").split(/\s[|│]\s/)[0]||String(t||"");const r=m.exports.detect(x);return r&&r.key&&r.confident?r.key:(r&&r.key)||""})));
