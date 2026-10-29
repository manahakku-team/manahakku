"""
Mana Hakku news collector: every few hours, gathers Andhra Pradesh and Telangana headlines (Telugu and English) from
Google News and government sources, and tags each with state, district, problem type and whether the outlet is trusted.
Keeps a rolling 30-day feed of headline + outlet + date + link only (never article text).

Usage: python3 tools/news/collect.py <feed dir>     (needs web/data/keywords.json, built by tools/export_keywords.js)
"""
import hashlib, json, os, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUT = sys.argv[1] if len(sys.argv) > 1 else "newsfeed"
KEEP_DAYS = 30
html = open(os.path.join(ROOT, "app/src/main/assets/index.html"), encoding="utf-8").read()
mandals = json.load(open(os.path.join(ROOT, "web/data/mandals.json"), encoding="utf-8"))
kw = json.load(open(os.path.join(ROOT, "web/data/keywords.json"), encoding="utf-8"))["sectors"]

def js_array(name):
    m = re.search(r"const " + name + r"=(\[\[.*?\]\]);", html, re.S)
    return json.loads(m.group(1))
DISTRICTS = {"ap": js_array("AP_DISTRICTS"), "ts": js_array("TS_DISTRICTS")}
STATE = {"ap": ("Andhra Pradesh", "ఆంధ్రప్రదేశ్"), "ts": ("Telangana", "తెలంగాణ")}
TRUSTED = [("The Hindu", "thehindu.com"), ("The New Indian Express", "newindianexpress.com"), ("Deccan Chronicle", "deccanchronicle.com"),
           ("The Hans India", "thehansindia.com"), ("Times of India", "timesofindia.indiatimes.com"), ("Eenadu", "eenadu.net"),
           ("Sakshi", "sakshi.com"), ("PIB", "pib.gov.in"), ("Telangana Today", "telanganatoday.com"), ("Andhra Jyothy", "andhrajyothy.com"),
           ("The News Minute", "thenewsminute.com"), ("The Indian Express", "indianexpress.com"), ("NDTV", "ndtv.com"),
           ("ETV Bharat", "etvbharat.com"), ("Hindustan Times", "hindustantimes.com"), ("Deccan Herald", "deccanherald.com")]
ALIAS = {"Rajahmundry": "East Godavari", "Rajamundry": "East Godavari", "Vizag": "Visakhapatnam", "Anantapur": "Ananthapuramu",
         "Kadapa": "YSR Kadapa", "Cuddapah": "YSR Kadapa", "Hanamkonda": "Hanumakonda", "Secunderabad": "Hyderabad",
         "Vijayawada": "NTR", "Tirupati": "Tirupati", "Nellore": "Sri Potti Sriramulu Nellore"}
# Problem topics to search (English, Telugu). The app's own keywords decide the final problem type.
TOPICS = [("drinking water", "తాగునీరు"), ("hospital doctors", "ఆసుపత్రి"), ("road damaged", "రోడ్డు"), ("power cut electricity", "విద్యుత్"),
          ("school students teachers", "పాఠశాల"), ("farmers crop", "రైతులు"), ("floods rain damage", "వరదలు"), ("housing scheme", "ఇళ్ల పట్టాలు"),
          ("drainage garbage sanitation", "పారిశుధ్యం"), ("pension welfare scheme", "పింఛన్"), ("ration rice", "రేషన్"), ("villagers protest", "గ్రామస్తుల ఆందోళన"),
          ("anganwadi nutrition", "అంగన్వాడీ"), ("collector grievance", "కలెక్టర్ ఫిర్యాదు")]

def host(u):
    m = re.match(r"https?://([^/:?#]+)", u or "", re.I)
    return m.group(1).lower().removeprefix("www.") if m else ""
def trusted_for(h):
    return next((t for t in TRUSTED if h == t[1] or h.endswith("." + t[1])), None)
def tag(item, name):
    m = re.search(r"<" + name + r"[^>]*>([\s\S]*?)</" + name + r">", item, re.I)
    if not m: return ""
    x = re.sub(r"<!\[CDATA\[([\s\S]*?)\]\]>", r"\1", m.group(1))
    x = re.sub(r"<[^>]+>", " ", x)
    for a, b in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&#39;", "'"), ("&apos;", "'")]: x = x.replace(a, b)
    return re.sub(r"\s+", " ", x).strip()

def fetch(q, lang):
    hl = "&hl=te&gl=IN&ceid=IN:te" if lang == "te" else "&hl=en-IN&gl=IN&ceid=IN:en"
    u = "https://news.google.com/rss/search?q=" + urllib.parse.quote(q + " when:3d") + hl
    try:
        xml = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 ManaHakku-news"}), timeout=40).read().decode("utf-8", "ignore")
    except Exception as e:
        print("  fetch failed:", q[:50], e); return []
    out = []
    for it in re.findall(r"<item>[\s\S]*?</item>", xml, re.I):
        title, link, source = tag(it, "title"), tag(it, "link"), tag(it, "source")
        src_url = (re.search(r'<source[^>]*url="([^"]+)"', it) or [None, ""])[1]
        if source and title.endswith(" - " + source): title = title[: -(len(source) + 3)]
        dom = host(src_url); t = trusted_for(dom)
        try: d = parsedate_to_datetime(tag(it, "pubDate")).astimezone(timezone.utc).isoformat()[:16]
        except Exception: d = ""
        if title and link.startswith("https://"):
            out.append({"t": title[:220], "link": link, "src": t[0] if t else (source or dom)[:60], "dom": dom, "trusted": bool(t),
                        "gov": dom.endswith("gov.in") or dom.endswith("nic.in"), "date": d, "lang": lang})
    return out

def norm(s): return " " + re.sub(r"[^a-z0-9ఀ-౿]+", " ", s.lower()) + " "
PLACES = {}   # state -> list of (word, district, strength) ; strength 2 = district name or alias, 1 = mandal unique to one district
for st, dl in DISTRICTS.items():
    lst, owners = [], {}
    for en, te in dl:
        for m_en, m_te in mandals.get(st, {}).get(en, []):
            e = re.sub(r"\b(rural|urban)\b", "", m_en.lower()).strip()
            if len(e) >= 5: owners.setdefault(norm(e).strip(), set()).add(en)
            if m_te and len(m_te) >= 4: owners.setdefault(m_te, set()).add(en)
    for en, te in dl:
        lst += [(norm(en).strip(), en, 2), (te, en, 2)]
    lst += [(norm(a).strip(), d, 2) for a, d in ALIAS.items() if d in [x[0] for x in dl]]
    lst += [(w, next(iter(ds)), 1) for w, ds in owners.items() if len(ds) == 1]
    PLACES[st] = lst
def has_place(title, h, w):
    if re.match(r"^[a-z0-9 ]+$", w): return (" " + w + " ") in h
    # Telugu: the name must start a word (endings like -లో, -కు may follow), never sit inside another word
    return re.search(r"(^|[^\u0C00-\u0C7F])" + re.escape(w), title) is not None
def district_of(title, st):
    h = norm(title); best = None
    for w, d, s in PLACES[st]:
        if has_place(title, h, w):
            if not best or s > best[1]: best = (d, s)
            if s == 2: break
    return best[0] if best else ""
def sector_of(title):
    s0 = " " + title.lower() + " "; best, sc = "", 0
    for k, v in kw.items():
        x = sum((2 if len(w) > 4 else 1) for w in v["kw"] if w.lower() in s0)
        if x > sc: best, sc = k, x
    return best


# Official and trusted YouTube channels (titles and links only). Handles are tried in order; the first that resolves is kept.
YT = [("PIB India", ["@PIBIndia"], True), ("DD News", ["@DDNewslive", "@ddnews"], True), ("DD Saptagiri", ["@DDSaptagiri", "@ddsaptagiri"], True),
      ("DD Yadagiri", ["@DDYadagiri", "@DDYadagiriOfficial"], True), ("The Hindu", ["@TheHindu-Official", "@thehindu"], False), ("NDTV", ["@NDTV"], False),
      ("ETV Andhra Pradesh", ["@ETVAndhraPradesh"], False), ("ETV Telangana", ["@ETVTelanganaOfficial", "@etvtelangana"], False), ("Sakshi TV", ["@SakshiTV"], False),
      ("ABN Telugu", ["@abntelugutv", "@ABNTeluguTV"], False), ("TV9 Telugu", ["@TV9TeluguLive"], False), ("V6 News", ["@V6NewsTelugu"], False),
      ("NTV Telugu", ["@NtvTeluguLive"], False)]
def yt_ids(cache_path):
    ids = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
    for name, handles, _ in YT:
        if ids.get(name): continue
        for h in handles:
            try:
                page = urllib.request.urlopen(urllib.request.Request("https://www.youtube.com/" + h, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en"}), timeout=30).read().decode("utf-8", "ignore")
                m = re.search(r'"(?:externalId|channelId)":"(UC[\w-]{22})"', page)
                if m: ids[name] = m.group(1); break
            except Exception as e:
                print("  youtube handle failed:", h, str(e)[:60])
        if not ids.get(name): print("  youtube channel not found:", name)
        elif list(ids.values()).count(ids[name]) > 1:
            print("  youtube handle points to another channel, dropped:", name); ids[name] = ""
    json.dump(ids, open(cache_path, "w"), indent=1)
    return ids
def yt_items(ids):
    out = []
    for name, _, gov in YT:
        cid = ids.get(name)
        if not cid: continue
        try:
            xml = urllib.request.urlopen("https://www.youtube.com/feeds/videos.xml?channel_id=" + cid, timeout=30).read().decode("utf-8", "ignore")
        except Exception as e:
            print("  youtube feed failed:", name, str(e)[:60]); continue
        for e in re.findall(r"<entry>[\s\S]*?</entry>", xml):
            title = tag(e, "title"); link = (re.search(r'<link rel="alternate" href="([^"]+)"', e) or [None, ""])[1]
            date = tag(e, "published")[:16]
            if title and link.startswith("https://"):
                out.append({"t": title[:220], "link": link, "src": name + " (YouTube)", "dom": "youtube.com", "trusted": gov, "gov": gov,
                            "date": date, "lang": "te" if re.search("[\u0C00-\u0C7F]", title) else "en"})
        time.sleep(0.5)
    return out

def main():
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "feed.json")
    feed = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {"items": []}
    seen = {i["id"]: i for i in feed["items"]}
    now = datetime.now(timezone.utc); new = 0
    for st, (en_name, te_name) in STATE.items():
        queries = [(f'"{en_name}" {e}', "en") for e, _ in TOPICS] + [(f"{te_name} {t}", "te") for _, t in TOPICS]
        queries += [(f'site:pib.gov.in "{en_name}"', "en"), (f'site:gov.in "{en_name}"', "en"), (f'"{en_name}" collector OR minister announces', "en")]
        for q, lang in queries:
            for it in fetch(q, lang):
                key = re.sub(r"\W+", "", it["t"].lower())[:120]
                iid = hashlib.md5(key.encode()).hexdigest()[:12]
                if iid in seen: continue
                it.update({"id": iid, "state": st, "district": district_of(it["t"], st), "sector": sector_of(it["t"]), "seen": now.isoformat()[:16]})
                seen[iid] = it; new += 1
            time.sleep(1.2)
    # YouTube: keep only videos that name a state, district or mandal
    for it in yt_items(yt_ids(os.path.join(OUT, "youtube_channels.json"))):
        key = re.sub(r"\W+", "", it["t"].lower())[:120]; iid = hashlib.md5(key.encode()).hexdigest()[:12]
        if iid in seen: continue
        for st, (en_name, te_name) in STATE.items():
            d = district_of(it["t"], st)
            if d or en_name.lower() in it["t"].lower() or te_name in it["t"] or (st == "ap" and re.search(r"\bAP\b|ఏపీ", it["t"])):
                it.update({"id": iid, "state": st, "district": d, "sector": sector_of(it["t"]), "seen": now.isoformat()[:16]}); seen[iid] = it; new += 1; break
    cut = (now - timedelta(days=KEEP_DAYS)).isoformat()[:16]
    items = sorted([i for i in seen.values() if (i.get("date") or i["seen"]) >= cut], key=lambda i: i.get("date") or i["seen"], reverse=True)
    json.dump({"updated": now.isoformat()[:16], "items": items}, open(path, "w", encoding="utf-8"), ensure_ascii=False)
    # Small summary: last 7 days, counts by state > district > problem type (trusted or government outlets only)
    wk = (now - timedelta(days=7)).isoformat()[:16]; summ = {}
    for i in items:
        if (i.get("date") or i["seen"]) < wk or not (i["trusted"] or i["gov"]): continue
        d = summ.setdefault(i["state"], {}).setdefault(i["district"] or "(state-wide / unknown)", {})
        d[i["sector"] or "other"] = d.get(i["sector"] or "other", 0) + 1
    json.dump({"updated": now.isoformat()[:16], "last7days_trusted": summ}, open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    tagged = sum(1 for i in items if i["district"])
    print(f"new {new}; kept {len(items)} (30 days); with a district {tagged}; trusted/gov {sum(1 for i in items if i['trusted'] or i['gov'])}")

if __name__ == "__main__":
    main()
