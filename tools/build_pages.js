// Builds one plain page per district (Andhra Pradesh and Telangana) so search engines can find the district facts,
// the landmark project and its delivery record, plus sitemap.xml and robots.txt. Every fact is copied from the app's
// own data (which cites government sources); nothing is added here. Each page links into the live app scorecard.
// Usage: node tools/build_pages.js <site dir>
const fs = require("fs"), path = require("path");
const BASE = "https://manahakku-team.github.io/manahakku/";
const html = fs.readFileSync(path.join(__dirname, "..", "app", "src", "main", "assets", "index.html"), "utf8");

// Pull one object/array literal out of the app by name, skipping over strings so brackets inside text don't count.
function grab(name) {
  const at = html.search(new RegExp("(?:const|let)\\s+" + name + "\\s*="));
  if (at < 0) throw new Error("not found: " + name);
  let i = html.indexOf("=", at) + 1;
  while (/\s/.test(html[i])) i++;
  const open = html[i], close = open === "{" ? "}" : "]";
  let depth = 0, q = null;
  for (let j = i; j < html.length; j++) {
    const c = html[j];
    if (q) { if (c === "\\") j++; else if (c === q) q = null; continue; }
    if (c === '"' || c === "'" || c === "`") { q = c; continue; }
    if (c === open) depth++;
    else if (c === close && --depth === 0) return new Function("return " + html.slice(i, j + 1))();
  }
  throw new Error("unclosed: " + name);
}
const D = {
  ap: { name: ["Andhra Pradesh", "ఆంధ్రప్రదేశ్"], list: grab("AP_DISTRICTS"), info: grab("AP_DIST_INFO") },
  ts: { name: ["Telangana", "తెలంగాణ"], list: grab("TS_DISTRICTS"), info: grab("TS_DIST_INFO") },
};
const PROJ = grab("DIST_PROJ"), PTL = grab("PTL"), DELIV = grab("DELIV");

const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const bi = (en, te, tag = "p") => `<${tag} data-l="en">${esc(en)}</${tag}><${tag} data-l="te">${esc(te)}</${tag}>`;
const pair = (en, te) => `<span data-l="en">${esc(en)}</span><span data-l="te">${esc(te)}</span>`;
const STATUS = { done: ["Completed", "పూర్తయింది"], build: ["Under construction", "నిర్మాణంలో ఉంది"], part: ["Partly working", "పాక్షికంగా పనిచేస్తోంది"],
  stalled: ["Stalled", "నిలిచిపోయింది"], plan: ["Still at planning stage", "ఇంకా ప్రణాళిక దశలో"], repair: ["Needs repair", "మరమ్మతు అవసరం"] };
const money = (v, unit) => unit === "lakh" ? ["₹" + v.toLocaleString("en-IN") + " lakh", "₹" + v.toLocaleString("en-IN") + " లక్షలు"]
  : ["₹" + v.toLocaleString("en-IN") + " crore", "₹" + v.toLocaleString("en-IN") + " కోట్లు"];

const CSS = fs.readFileSync(path.join(__dirname, "..", "web", "about.html"), "utf8").match(/<style>([\s\S]*?)<\/style>/)[1]
  + "dl{margin:6px 0 0}dt{font-weight:700;margin-top:8px}dd{margin:2px 0 0}.chip{display:inline-block;border-radius:999px;padding:2px 10px;background:var(--line);font-size:.85rem;font-weight:600}"
  + ".go{display:inline-block;margin:6px 10px 0 0;padding:8px 14px;border-radius:10px;background:var(--indigo);color:#fff;text-decoration:none;font-weight:600}.grid{columns:2 220px;padding-left:1.2em}";
const TOGGLE = `<script>(function(){var k="mh-lang",l="en";try{l=localStorage.getItem(k)||"en"}catch(e){}function set(x){document.documentElement.lang=x;document.querySelectorAll("[data-set]").forEach(function(b){b.setAttribute("aria-pressed",String(b.dataset.set===x))});try{localStorage.setItem(k,x)}catch(e){}}document.querySelectorAll("[data-set]").forEach(function(b){b.onclick=function(){set(b.dataset.set)}});set(l==="te"?"te":"en")})();</script>`;
const page = (title, desc, canon, head, body) => `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<link rel="canonical" href="${canon}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${canon}">
<meta property="og:image" content="${BASE}og.png">
<style>${CSS}</style>
</head>
<body>
<header><div class="wrap">${head}
  <div class="langs"><button type="button" data-set="te" aria-pressed="false">తెలుగు</button><button type="button" data-set="en" aria-pressed="true">English</button></div>
</div></header>
<main class="wrap">
${body}
<p class="note">${pair("Not a government website: Mana Hakku is independent. Facts are copied from the Mana Hakku app, which takes them from official public sources. ", "ఇది ప్రభుత్వ వెబ్‌సైట్ కాదు: మన హక్కు స్వతంత్రమైనది. వాస్తవాలు మన హక్కు యాప్ నుండి; యాప్ వాటిని అధికారిక బహిరంగ ఆధారాల నుండి తీసుకుంటుంది. ")}<a href="${BASE}about.html">${pair("About", "గురించి")}</a> · <a href="${BASE}privacy.html">${pair("Privacy", "గోప్యత")}</a></p>
</main>
${TOGGLE}
</body>
</html>
`;

function deliv(d) {
  if (!d) return "";
  const st = STATUS[d.s] || STATUS.build, rows = [];
  rows.push(`<p><span class="chip">${pair(st[0], st[1])}${d.s === "done" && d.dn ? " · " + esc(d.dn) : ""}</span></p>`);
  const kv = (en, te, v) => v ? `<dt>${pair(en, te)}</dt><dd>${esc(v)}</dd>` : "";
  let dl = kv("Work started", "పని ప్రారంభం", d.st) + kv("Promised completion", "హామీ ఇచ్చిన పూర్తి తేదీ", d.pr) + kv("Completed", "పూర్తయింది", d.s === "done" ? (d.dnL || d.dn) : "") + kv("Status as of", "ఈ తేదీ నాటికి స్థితి", d.asof);
  if (d.c && d.c.length) dl += `<dt>${pair("Cost estimates", "ఖర్చు అంచనాలు")}</dt><dd><ul>${d.c.map(x => { const m = money(x[0], d.cu); return `<li>${pair(m[0] + " (" + x[1][0] + ")", m[1] + " (" + x[1][1] + ")")}</li>`; }).join("")}</ul></dd>`;
  rows.push(`<dl>${dl}</dl>`);
  if (d.x) rows.push(bi(d.x[0], d.x[1]));
  if (d.src && d.src.length) rows.push(`<p class="note">${pair("Sources: ", "ఆధారాలు: ")}${d.src.map(s => `<a href="${esc(s[0])}" rel="noopener noreferrer">${esc(s[1])}</a>`).join(" · ")}</p>`);
  return `<section><h2>${pair("Delivery record", "అమలు రికార్డు")}</h2>${rows.join("")}</section>`;
}

const out = process.argv[2] || path.join(__dirname, "..", "site");
const urls = [BASE, BASE + "about.html", BASE + "privacy.html", BASE + "d/"];
fs.mkdirSync(path.join(out, "d"), { recursive: true });
const index = [];
for (const [sk, S] of Object.entries(D)) {
  const items = [];
  for (const [en, te] of S.list) {
    const info = S.info[en]; if (!info) continue;
    const file = sk + "-" + slug(en) + ".html", canon = BASE + "d/" + file;
    const app = `${BASE}#${sk}/score/${encodeURIComponent(en)}`, hist = `${BASE}#${sk}/history/${encodeURIComponent(en)}`;
    const pj = sk === "ap" ? PROJ[en] : null;
    let body = `<section><h2>${pair("About the district", "జిల్లా గురించి")}</h2><dl>
<dt>${pair("Headquarters", "ప్రధాన కేంద్రం")}</dt><dd>${pair(info[0], info[1])}</dd>
<dt>${pair("How it got its name", "పేరు ఎలా వచ్చింది")}</dt><dd>${pair(info[2][0], info[2][1])}</dd>
<dt>${pair("Known for", "ప్రత్యేకత")}</dt><dd>${pair(info[3][0], info[3][1])}</dd>
<dt>${pair("Contribution", "సహకారం")}</dt><dd>${pair(info[4][0], info[4][1])}</dd></dl></section>`;
    if (pj) {
      const tl = (PTL[en] || []).map(e => `<li><b>${esc(e[0])}</b>: ${pair(e[1], e[2])}</li>`).join("");
      body += `<section><h2>${pair("Landmark project: " + pj[0][0], "ప్రముఖ ప్రాజెక్టు: " + pj[0][1])}</h2><dl>
<dt>${pair("What it is", "ఏమిటి")}</dt><dd>${pair(pj[2][0], pj[2][1])}</dd>
${pj[3] ? `<dt>${pair("Challenges faced", "ఎదుర్కొన్న సవాళ్లు")}</dt><dd>${pair(pj[3][0], pj[3][1])}</dd>` : ""}
${tl ? `<dt>${pair("Timeline", "కాలక్రమం")}</dt><dd><ol>${tl}</ol></dd>` : ""}
<dt>${pair("Today", "ప్రస్తుతం")}</dt><dd>${pair(pj[4][0], pj[4][1])}</dd></dl>
<p class="note">${pair("Government source: ", "ప్రభుత్వ ఆధారం: ")}<a href="${esc(pj[5])}" rel="noopener noreferrer">${esc(pj[6])}</a></p></section>` + deliv(DELIV[en]);
    }
    body += `<section><h2>${pair("Problems reported here", "ఇక్కడ నమోదైన సమస్యలు")}</h2>${bi("The live scorecard shows how many problems people reported in " + en + ", how many were solved and how many have waited over 30 days, next to state spending on each area.", te + "లో ప్రజలు ఎన్ని సమస్యలు నమోదు చేశారు, ఎన్ని పరిష్కారమయ్యాయి, ఎన్ని 30 రోజులకు పైగా వేచి ఉన్నాయి, ప్రతి విభాగంపై రాష్ట్ర ఖర్చుతో పాటు ప్రత్యక్ష స్కోర్‌కార్డ్ చూపిస్తుంది.")}
<a class="go" href="${app}">${pair("Open the live scorecard", "ప్రత్యక్ష స్కోర్‌కార్డ్ తెరవండి")}</a><a class="go" href="${hist}">${pair("District history in the app", "యాప్‌లో జిల్లా చరిత్ర")}</a></section>`;
    body += `<p><a href="${BASE}d/">${pair("← All districts", "← అన్ని జిల్లాలు")}</a></p>`;
    const head = `<h1>${esc(en)} · ${esc(te)}</h1>${bi(S.name[0] + " · district facts and scorecard", S.name[1] + " · జిల్లా వాస్తవాలు, స్కోర్‌కార్డ్")}`;
    const desc = `${en} district, ${S.name[0]}: headquarters ${info[0]}, known for ${info[3][0].replace(/\.$/, "")}.${pj ? " Landmark project: " + pj[0][0] + "." : ""} Problems reported and solved, from Mana Hakku.`;
    fs.writeFileSync(path.join(out, "d", file), page(`${en} district (${S.name[0]}) · Mana Hakku`, desc.slice(0, 300), canon, head, body));
    urls.push(canon); items.push(`<li><a href="${file}">${pair(en, te)}</a></li>`);
  }
  index.push(`<section><h2>${pair(S.name[0], S.name[1])}</h2><ul class="grid">${items.join("")}</ul></section>`);
}
fs.writeFileSync(path.join(out, "d", "index.html"), page("Districts of Andhra Pradesh and Telangana · Mana Hakku",
  "Facts, landmark projects, delivery records and problem scorecards for every district of Andhra Pradesh and Telangana.", BASE + "d/",
  `<h1>Mana Hakku · మన హక్కు</h1>${bi("Every district: facts, projects and scorecards", "ప్రతి జిల్లా: వాస్తవాలు, ప్రాజెక్టులు, స్కోర్‌కార్డ్‌లు")}`,
  index.join("") + `<p><a class="go" href="${BASE}">${pair("Open the app", "యాప్ తెరవండి")}</a></p>`));
const day = new Date().toISOString().slice(0, 10);
fs.writeFileSync(path.join(out, "sitemap.xml"), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map(u => `<url><loc>${u}</loc><lastmod>${day}</lastmod></url>`).join("\n")}\n</urlset>\n`);
fs.writeFileSync(path.join(out, "robots.txt"), `User-agent: *\nAllow: /\nSitemap: ${BASE}sitemap.xml\n`);
console.log("district pages:", urls.length - 4, "-> " + path.join(out, "d"));
