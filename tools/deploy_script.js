// Deploys backend/Code.gs to the live Apps Script web app, without the script editor.
// Run by the "Deploy Sheet script" GitHub workflow. Needs: AUTH (the address shown after approving Google access,
// or just its code), SCRIPT_ID (Project Settings → Script ID, saved once as a repository variable) and the live
// deployment ID (read from the app's register address). Tokens live only in memory and are never printed.
const fs=require("fs");
const CID="1072944905499-vm2v2i5dvn0a0d2o4ca36i1vge8cvbn0.apps.googleusercontent.com"; // clasp's public desktop client
const CSEC="v6V3fKV_zWU7iw1DrpO1rknX"; // published in clasp's source; not a secret
const REDIRECT="http://localhost:8888";
const die=m=>{console.error("✗ "+m);console.log("::error title=Deploy failed::"+String(m).replace(/\r?\n/g," "));process.exit(1)};
(async()=>{
 const sid=String(process.env.SCRIPT_ID||"").trim();if(!/^[A-Za-z0-9_-]{20,}$/.test(sid))die("SCRIPT_ID is missing. Add it once under Settings → Secrets and variables → Actions → Variables.");
 const html=fs.readFileSync("app/src/main/assets/index.html","utf8");const m=html.match(/script\.google\.com\/macros\/s\/([A-Za-z0-9_-]+)\/exec/);if(!m)die("Live deployment ID not found in the app.");const dep=m[1];
 let accessToken="";
 if(String(process.env.CLASPRC_JSON||"").trim()){
  // Automatic route: the saved clasp login (GitHub secret CLASPRC_JSON) gives a long-lived refresh token.
  if(/^\s*https?:|localhost/.test(process.env.CLASPRC_JSON))die("CLASPRC_JSON holds a web address, not the login file. On the laptop run: notepad %USERPROFILE%\\.clasprc.json, then Ctrl+A, Ctrl+C and paste that text as the secret.");
  let rc;try{rc=JSON.parse(String(process.env.CLASPRC_JSON).replace(/^\uFEFF/,""))}catch(e){die("CLASPRC_JSON is not valid JSON. Open .clasprc.json in Notepad, Ctrl+A, Ctrl+C and paste it again as the secret.")}
  const t=rc.token||rc.tokens&&rc.tokens.default||rc;const rt=t.refresh_token;
  if(!rt)die("CLASPRC_JSON has no refresh_token. Run clasp logout, then clasp login, and save the file again.");
  const cs=rc.oauth2ClientSettings||{};
  const tr=await fetch("https://oauth2.googleapis.com/token",{method:"POST",headers:{"content-type":"application/x-www-form-urlencoded"},body:new URLSearchParams({refresh_token:rt,client_id:cs.clientId||t.client_id||CID,client_secret:cs.clientSecret||t.client_secret||CSEC,grant_type:"refresh_token"})});
  const tk=await tr.json();if(!tk.access_token)die("Google refused the saved clasp login ("+(tk.error_description||tk.error||tr.status)+"). Run clasp login again with the Mana Hakku account and update the CLASPRC_JSON secret.");
  accessToken=tk.access_token;console.log("• Signed in with the saved clasp login.");
 } else {
 const raw=String(process.env.AUTH||"").trim();let code=raw;
 // Accept the full address with or without http://, or just the code; undo %2F-style encoding.
 const cm=raw.match(/[?&#]code=([^&#\s]+)/);if(cm)code=cm[1];code=code.replace(/\+/g," ").trim();try{code=decodeURIComponent(code)}catch(e){}
 console.log("• Approval code read: "+code.length+" characters, starts "+(code.startsWith("4/")?"correctly (4/…)":"UNEXPECTEDLY — copy the whole address again")+(raw.includes("scope=")?", scope present":", no scope seen"));
 if(!code)die("No approval code. Open the approval link again and paste the full address you land on.");
 const tr=await fetch("https://oauth2.googleapis.com/token",{method:"POST",headers:{"content-type":"application/x-www-form-urlencoded"},body:new URLSearchParams({code,client_id:CID,client_secret:CSEC,redirect_uri:REDIRECT,grant_type:"authorization_code"})});
 const tk=await tr.json();if(!tk.access_token)die("Google did not accept the approval code ("+(tk.error||tr.status)+"). Codes work once and expire in a few minutes: approve again and run right away.");
  accessToken=tk.access_token;
 }
 const H={authorization:"Bearer "+accessToken,"content-type":"application/json"};
 const api=async(method,path,body)=>{const r=await fetch("https://script.googleapis.com/v1/projects/"+sid+path,{method,headers:H,body:body?JSON.stringify(body):undefined});const j=await r.json().catch(()=>({}));if(!r.ok)die(method+" "+path.split("?")[0]+" failed: "+((j.error&&j.error.message)||r.status)+(r.status===403?" (turn on the Apps Script API at script.google.com/home/usersettings)":""));return j};
 const deps=await api("GET","/deployments");const live=(deps.deployments||[]).find(d=>d.deploymentId===dep);
 if(!live)die("Nothing changed: this Script ID is not the project behind the app's web address. Open the register Sheet → Extensions → Apps Script → Project Settings and copy that Script ID.");
 const cur=await api("GET","/content");const files=cur.files||[];
 const code_gs=fs.readFileSync("backend/Code.gs","utf8");
 const target=files.find(f=>f.type==="SERVER_JS"&&/^code$/i.test(f.name))||files.find(f=>f.type==="SERVER_JS");if(!target)die("No script file found in the project.");
 console.log("• Project has "+files.length+" file(s); replacing '"+target.name+"' ("+(target.source||"").length+" → "+code_gs.length+" characters).");
 target.source=code_gs;await api("PUT","/content",{files});
 const ver=await api("POST","/versions",{description:"Mana Hakku deploy "+new Date().toISOString().slice(0,16)});
 console.log("• Saved as version "+ver.versionNumber+".");
 await api("PUT","/deployments/"+dep,{deploymentConfig:{scriptId:sid,versionNumber:ver.versionNumber,manifestFileName:"appsscript",description:"Mana Hakku v"+ver.versionNumber}});
 console.log("✓ Live web app now runs version "+ver.versionNumber+" at the same address.");
})().catch(e=>die(String(e&&e.message||e)));
