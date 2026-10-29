# Season FTM/FTA/FT% for every NBA regular season of the 141 players in the Weiss (2019) gaze database.
# Source: Basketball-Reference player totals, via github.com/sumitrodatta/bball-reference-datasets ("Player Totals.csv").
# Usage: python build_ft_player_seasons.py "Player Totals.csv" gaze_database.csv data/
# Traded players: the combined TOT/2TM/3TM row is kept and the teams are listed in `teams`.
import re, sys, unicodedata, pandas as pd
tot_path, db_path, out_dir = sys.argv[1:4]
ALIASES = {"Steph Curry": "Stephen Curry", "Nic Batum": "Nicolas Batum", "Wes Matthews": "Wesley Matthews",
           "Pat McCaw": "Patrick McCaw", "Thad Young": "Thaddeus Young", "Jordan Lloyd": "Jordan Loyd",
           "Rob Williams": "Robert Williams"}
SUFFIX = re.compile(r"\s+(jr|sr|ii|iii|iv)$")
def norm(name):
    s = unicodedata.normalize("NFKD", name.replace("*", "")).encode("ascii", "ignore").decode()
    s = s.lower().replace(".", "").replace("'", "").replace("’", "").replace("-", " ")
    return SUFFIX.sub("", re.sub(r"\s+", " ", s).strip())
t = pd.read_csv(tot_path)
t = t[t.lg == "NBA"].copy()
t["key"] = t.player.map(norm)
db = pd.read_csv(db_path, keep_default_na=False)
db["key"] = [norm(ALIASES.get(p, p)) for p in db.player]
ids = t.groupby("key").player_id.unique()
rep = []
for p, k in zip(db.player, db.key):
    c = list(ids.get(k, []))
    rep.append(dict(player=p, n=len(c), ids=";".join(c)))
rep = pd.DataFrame(rep)
assert (rep.n == 1).all(), rep[rep.n != 1]
idmap = dict(zip(rep.player, rep.ids))
db["bref_id"] = db.player.map(idmap)
x = t[t.player_id.isin(db.bref_id)].copy()
x["multi"] = x.team.astype(str).str.match(r"^(TOT|\d+TM)$")
x = x.sort_values(["player_id", "season", "multi"], ascending=[True, True, False])
teams = (x[~x.multi].groupby(["player_id", "season"]).team.agg(lambda s: "/".join(s.astype(str)))
         .rename("teams"))
x = x.drop_duplicates(["player_id", "season"]).merge(teams, on=["player_id", "season"], how="left")
x["teams"] = x.teams.fillna(x.team)
x = x.merge(db[["player", "bref_id", "eyes", "gaze_type", "ball_watcher", "position", "height_in"]],
            left_on="player_id", right_on="bref_id", suffixes=("_bref", ""))
x["ftm"], x["fta"] = x.ft.astype(int), x.fta.astype(int)
x["ft_pct"] = (x.ftm / x.fta).where(x.fta > 0).round(4)
x["year_in_career"] = x.season - x.groupby("player_id").season.transform("min")
cols = ["player", "bref_id", "season", "year_in_career", "age", "teams", "g", "mp", "ftm", "fta", "ft_pct",
        "eyes", "gaze_type", "ball_watcher", "position", "height_in"]
x = x[cols].sort_values(["player", "season"])
import os; os.makedirs(out_dir, exist_ok=True)
x.to_csv(f"{out_dir}/ft_player_seasons.csv", index=False)
print(len(x), "player-seasons,", x.player.nunique(), "players,", x.season.min(), "-", x.season.max())
print("zero-FTA seasons:", (x.fta == 0).sum())
