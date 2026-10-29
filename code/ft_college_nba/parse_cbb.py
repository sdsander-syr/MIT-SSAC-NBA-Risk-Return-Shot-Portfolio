import io, sys, pandas as pd
def parse(path):
    html = open(path).read().replace("<!--", "").replace("-->", "")
    for tid, per_game in (("players_totals", False), ("players_per_game", True)):
        try: t = pd.read_html(io.StringIO(html), attrs={"id": tid})[0]
        except ValueError: continue
        if isinstance(t.columns, pd.MultiIndex): t.columns = t.columns.get_level_values(-1)
        t = t[t.Season.astype(str).str.match(r"^\d{4}-\d{2}$")].copy()
        if t.empty or "FTA" not in t: continue
        for c in ("G", "FT", "FTA"): t[c] = pd.to_numeric(t[c], errors="coerce")
        if per_game: t["FT"], t["FTA"] = (t.FT * t.G).round(), (t.FTA * t.G).round()
        t = t[t.FTA.notna()]   # seasons on the roster without stats (e.g. transfer sit-out years)
        t["season"] = t.Season.str[:4].astype(int) + 1
        t["school"] = t["Team"] if "Team" in t else t.get("School", "")
        g = t.groupby("season").agg(season_label=("Season", "first"), school=("school", lambda s: "/".join(s)),
                                    cls=("Class", "first") if "Class" in t else ("Season", lambda s: ""),
                                    g=("G", "sum"), ftm=("FT", "sum"), fta=("FTA", "sum")).reset_index()
        g["table"] = "totals" if not per_game else "per_game x G (rounded)"
        return g
    return None
if __name__ == "__main__": print(parse(sys.argv[1]))
