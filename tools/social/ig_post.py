#!/usr/bin/env python3
"""Post to the Mana Hakku Instagram account through the official Instagram API.

  ig_post.py check                         -> confirms the key works and names the account (posts nothing)
  ig_post.py image  URL CAPTION_FILE       -> one picture (JPEG at a public URL)
  ig_post.py carousel URL1,URL2,... CAPTION_FILE
  ig_post.py reel   URL CAPTION_FILE       -> a video (MP4 at a public URL)
  ig_post.py refresh                       -> renews the 60-day key; prints days left

The key and account ID come only from the environment (GitHub secrets IG_ACCESS_TOKEN, IG_USER_ID).
Nothing secret is printed.
"""
import json, os, sys, time, urllib.parse, urllib.request, urllib.error

TOKEN = os.environ.get("IG_ACCESS_TOKEN", "").strip()
USER = os.environ.get("IG_USER_ID", "").strip()
# Unified (Facebook) login gives a system-user key for graph.facebook.com; an Instagram-login key uses graph.instagram.com.
API = os.environ.get("IG_API", "https://graph.facebook.com/v21.0").rstrip("/")


def call(method, path, **params):
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}" if not path.startswith("http") else path
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode())
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace").replace(TOKEN, "***")[:400]
        sys.exit(f"Instagram said no ({e.code}): {body}")


def wait_ready(cid):
    for _ in range(60):
        st = call("GET", cid, fields="status_code").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            sys.exit(f"Instagram could not process the media ({st}).")
        time.sleep(10)
    sys.exit("Instagram took too long to process the media.")


def publish(cid):
    wait_ready(cid)
    r = call("POST", f"{USER}/media_publish", creation_id=cid)
    link = call("GET", r["id"], fields="permalink").get("permalink", "")
    print("Posted:", link or r["id"])


def main():
    if not TOKEN or not USER:
        sys.exit("The Instagram key is not set yet (GitHub secrets IG_ACCESS_TOKEN and IG_USER_ID).")
    mode = sys.argv[1]
    if mode == "check":
        me = call("GET", USER, fields="username,media_count")
        print(f"Key works for @{me.get('username')}, {me.get('media_count')} posts so far.")
        return
    if mode == "refresh" and "graph.facebook.com" in API:
        print("System-user key: it does not expire, nothing to renew.")
        return
    if mode == "refresh":
        r = call("GET", "https://graph.instagram.com/refresh_access_token", grant_type="ig_refresh_token")
        days = int(r.get("expires_in", 0)) // 86400
        out = os.environ.get("GITHUB_OUTPUT")
        if out:
            with open(out, "a") as f:
                f.write(f"token={r.get('access_token', '')}\n")
        print(f"Key renewed; valid for about {days} more days.")
        return
    caption = open(sys.argv[3], encoding="utf-8").read().strip()[:2200]
    if mode == "image":
        publish(call("POST", f"{USER}/media", image_url=sys.argv[2], caption=caption)["id"])
    elif mode == "carousel":
        kids = [call("POST", f"{USER}/media", image_url=u, is_carousel_item="true")["id"] for u in sys.argv[2].split(",")]
        for k in kids:
            wait_ready(k)
        publish(call("POST", f"{USER}/media", media_type="CAROUSEL", children=",".join(kids), caption=caption)["id"])
    elif mode == "reel":
        publish(call("POST", f"{USER}/media", media_type="REELS", video_url=sys.argv[2], caption=caption, share_to_feed="true")["id"])
    else:
        sys.exit("unknown mode")


if __name__ == "__main__":
    main()
