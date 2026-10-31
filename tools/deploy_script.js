// Deploys backend/Code.gs to the live Apps Script web app, without the script editor.
// Run by the "Deploy Sheet script" GitHub workflow. Needs: AUTH (the address shown after approving Google access,
// or just its code), SCRIPT_ID (Project Settings → Script ID, saved once as a repository variable) and the live
// deployment ID (read from the app's register address). Tokens live only in memory and are never printed.
const fs=require("fs");
const CID="1072944905499-vm2v2i5dvn0a0d2o4ca36i1vge8cvbn0.apps.googleusercontent.com"; // clasp's public desktop client
const CSEC="v6V3fKV_zWU7iw1DrpO1rknX"; // published in clasp's source; not a secret
const REDIRECT="http://localhost:8888";
const die=m=>{console.error("✗ "+m);process.exit(1)};
(async()=>{
 const raw=String(process.env.AUTH||"").trim();let code=raw;try{if(/^https?:/.test(raw))code=new URL(raw).searchParams.get("code")||""}catch(e){}
 if(!code)die("No approval code. Open the approval link again and paste the full address you land on.");
 const sid=String(process.env.SCRIPT_ID||"").trim();if(!/^[A-Za-z0-9_-]{20,}$/.test(sid))die("SCRIPT_ID is missing. Add it once under Settings → Secrets and variables → Actions → Variables.");
 const html=fs.readFileSync("app/src/main/assets/index.html","utf8");const m=html.match(/script\.google\.com\/macros\/s\/([A-Za-z0-9_-]+)\/exec/);if(!m)die("Live deployment ID not found in the app.");const dep=m[1];
 const tr=await fetch("https://oauth2.googleapis.com/token",{method:"POST",headers:{"content-type":"application/x-www-form-urlencoded"},body:new URLSearchParams({code,client_id:CID,client_secret:CSEC,redirect_uri:REDIRECT,grant_type:"authorization_code"})});
 const tk=await tr.json();if(!tk.access_token)die("Google did not accept the approval code ("+(tk.error||tr.status)+"). Codes work once and expire in a few minutes: approve again and run right away.");
 const H={authorization:"Bearer "+tk.access_token,"content-type":"application/json"};
 const api=async(method,path,body)=>{const r=await fetch("https://script.googleapis.com/v1/projects/"+sid+path,{method,headers:H,body:body?JSON.stringify(body):undefined});const j=await r.json().catch(()=>({}));if(!r.ok)die(method+" "+path.split("?")[0]+" failed: "+((j.error&&j.error.message)||r.status)+(r.status===403?" (turn on the Apps Script API at script.google.com/home/usersettings)":""));return j};
 const cur=await api("GET","/content");const files=cur.files||[];
 const code_gs=fs.readFileSync("backend/Code.gs","utf8");
 const target=files.find(f=>f.type==="SERVER_JS"&&/^code$/i.test(f.name))||files.find(f=>f.type==="SERVER_JS");if(!target)die("No script file found in the project.");
 console.log("• Project has "+files.length+" file(s); replacing '"+target.name+"' ("+(target.source||"").length+" → "+code_gs.length+" characters).");
 target.source=code_gs;await api("PUT","/content",{files});
 const ver=await api("POST","/versions",{description:"Mana Hakku deploy "+new Date().toISOString().slice(0,16)});
 console.log("• Saved as version "+ver.versionNumber+".");
 const deps=await api("GET","/deployments");const live=(deps.deployments||[]).find(d=>d.deploymentId===dep);if(!live)die("The app's live deployment is not in this project. Check SCRIPT_ID.");
 await api("PUT","/deployments/"+dep,{deploymentConfig:{scriptId:sid,versionNumber:ver.versionNumber,manifestFileName:"appsscript",description:"Mana Hakku v"+ver.versionNumber}});
 console.log("✓ Live web app now runs version "+ver.versionNumber+" at the same address.");
})().catch(e=>die(String(e&&e.message||e)));
