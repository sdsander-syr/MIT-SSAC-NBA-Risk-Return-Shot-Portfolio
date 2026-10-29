"""Fetch Sports-Reference CBB pages for each database player; a page is kept only if it links to the player's BRef id."""
import re, sys, os, time, unicodedata, requests, pandas as pd
panel, out = sys.argv[1], sys.argv[2]
H = {"User-Agent": "Mozilla/5.0 (academic research; contact sdsander@syr.edu)"}
FIX = {"Steph Curry": "Stephen Curry", "Nic Batum": "Nicolas Batum", "Wes Matthews": "Wesley Matthews",
       "Pat McCaw": "Patrick McCaw", "Thad Young": "Thaddeus Young", "Jordan Lloyd": "Jordan Loyd",
       "Rob Williams": "Robert Williams"}
def slug(n):
    s = unicodedata.normalize("NFKD", FIX.get(n, n)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", "-", re.sub(r"[.'’]", "", s).strip())
p = pd.read_csv(panel).drop_duplicates("player")[["player", "bref_id"]]
log = []
for player, bid in zip(p.player, p.bref_id):
    base = slug(player); found = ""
    for n in range(1, 7):
        sl = f"{base}-{n}"; f = f"{out}/{sl}.html"
        if os.path.exists(f): html, code = open(f).read(), 200
        else:
            r = requests.get(f"https://www.sports-reference.com/cbb/players/{sl}.html", headers=H, timeout=60)
            time.sleep(3.5); code, html = r.status_code, r.text
            if code == 429: print("rate limited; stopping", flush=True); sys.exit(1)
            if code == 200: open(f, "w").write(html)
        if code != 200: break
        if f"/players/{bid[0]}/{bid}.html" in html: found = sl; break
    log.append(dict(player=player, bref_id=bid, cbb_slug=found, tried=n)); print(player, found or "-", flush=True)
pd.DataFrame(log).to_csv(f"{out}/_matches.csv", index=False)
