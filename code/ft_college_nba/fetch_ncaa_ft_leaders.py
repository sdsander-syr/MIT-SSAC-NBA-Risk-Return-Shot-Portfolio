import re, sys, os, time, requests, pandas as pd
out = sys.argv[1]; H = {"User-Agent": "Mozilla/5.0 (academic research; contact sdsander@syr.edu)"}
rows = []
for yr in range(1977, 2019):
    f = f"{out}/{yr}.html"
    if not os.path.exists(f):
        r = requests.get(f"https://www.sports-reference.com/cbb/seasons/men/{yr}-leaders.html", headers=H, timeout=60)
        time.sleep(4)
        if r.status_code != 200: print(yr, r.status_code, flush=True); continue
        open(f, "w").write(r.text)
    h = open(f).read(); i = h.find('id="leaders_ft_pct"')
    m = re.search(r"first_place.*?<a href='/cbb/players/([^']+)\.html'>([^<]+)</a>\s*<small>([^<]*)</small>.*?class=\"value\">\s*([.\d]+)", h[i:i+3000], re.S)
    if not m: print(yr, "no ft_pct leader", flush=True); continue
    rows.append(dict(season=yr, leader=m.group(2), school=m.group(3), ft_pct=float(m.group(4))))
    print(yr, rows[-1], flush=True)
pd.DataFrame(rows).to_csv(f"{out}/ncaa_ft_leaders.csv", index=False)
