"""Stack college (Sports-Reference CBB) and NBA (Basketball-Reference) free throw seasons for the 141 gaze-database
players, carry each player's gaze classification on every row, and attach the estimated league FT% ceiling."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from parse_cbb import parse
from statsmodels.nonparametric.smoothers_lowess import lowess
nba_path, cbb_dir, db_path, nba_lead_path, ncaa_lead_path, out = sys.argv[1:7]

db = pd.read_csv(db_path, keep_default_na=False)
nba = pd.read_csv(nba_path)
m = pd.read_csv(f"{cbb_dir}/_matches.csv", keep_default_na=False)

# College seasons; a page counts as the player's only if it links to his Basketball-Reference id (checked in fetch)
col, unmatched = [], []
for r in m.itertuples():
    s = parse(f"{cbb_dir}/{r.cbb_slug}.html") if r.cbb_slug else None
    if s is None or s.empty:
        unmatched.append(dict(player=r.player, reason="no Sports-Reference college page linked to this NBA player")); continue
    s["player"], s["cbb_slug"] = r.player, r.cbb_slug
    col.append(s)
col = pd.concat(col, ignore_index=True)
col = col.assign(level="NCAA", team=col.school, age=np.nan, mp=np.nan,
                 source="Sports-Reference CBB player page (" + col.table + ")")

nba = nba.assign(level="NBA", team=nba.teams, cls="", source="Basketball-Reference season totals",
                 season_label=(nba.season - 1).astype(str) + "-" + (nba.season % 100).astype(str).str.zfill(2))
keep = ["player", "level", "season", "season_label", "team", "cls", "age", "g", "mp", "ftm", "fta", "source"]
x = pd.concat([col[keep], nba[keep]], ignore_index=True)
x[["ftm", "fta"]] = x[["ftm", "fta"]].astype(int)
x["ft_pct"] = (x.ftm / x.fta).where(x.fta > 0).round(4)

# Ceiling: each season's FT% leader (observed), smoothed with LOWESS per level (estimated)
def ceiling(lead, level):
    lead = lead.sort_values("season")
    fit = lowess(lead.ft_pct, lead.season, frac=0.3, return_sorted=False)
    return pd.DataFrame(dict(level=level, season=lead.season, leader=lead.leader, leader_ft_pct=lead.ft_pct,
                             ceiling_est=fit.round(4)))
cn = ceiling(pd.read_csv(nba_lead_path), "NBA")
cc = ceiling(pd.read_csv(ncaa_lead_path), "NCAA")
ceil = pd.concat([cn, cc])
ceil.to_csv(f"{out}/ft_ceiling_by_season.csv", index=False)
x = x.merge(ceil.rename(columns={"leader": "season_ft_leader", "leader_ft_pct": "season_leader_ft_pct"}),
            on=["level", "season"], how="left")
x["gap_to_ceiling"] = (x.ft_pct - x.ceiling_est).round(4)
x["ceiling_note"] = np.where(x.ceiling_est.isna(), "no season leader on Sports-Reference (NCAA before 1992-93)", "")

ids = nba.drop_duplicates("player").set_index("player").bref_id
slugs = col.drop_duplicates("player").set_index("player").cbb_slug
x["bref_id"], x["cbb_slug"] = x.player.map(ids), x.player.map(slugs).fillna("")
x["has_college"] = x.player.isin(slugs.index).astype(int)
x = x.merge(db[["player", "eyes", "gaze_type", "ball_watcher", "position", "height_in"]], on="player")
x["gaze"] = np.where(x.ball_watcher == 1, "ball", "rim")
x["level_order"] = (x.level == "NBA").astype(int)
x = x.sort_values(["player", "season", "level_order"])
x["year_in_level"] = x.season - x.groupby(["player", "level"]).season.transform("min")
x["experience"] = x.season - x.groupby("player").season.transform("min")
x["career_row"] = x.groupby("player").cumcount() + 1
cols = ["player", "bref_id", "cbb_slug", "has_college",
        "eyes", "gaze", "gaze_type", "ball_watcher", "position", "height_in",
        "level", "season", "season_label", "career_row", "year_in_level", "experience", "team", "cls", "age", "g", "mp",
        "ftm", "fta", "ft_pct", "season_ft_leader", "season_leader_ft_pct", "ceiling_est", "gap_to_ceiling", "ceiling_note", "source"]
x = x[cols].rename(columns={"cls": "college_class"})
x.to_csv(f"{out}/ft_college_nba_merged.csv", index=False)
pd.DataFrame(unmatched).to_csv(f"{out}/college_unmatched.csv", index=False)
dup = x.groupby(["player", "season"]).size(); print("player-seasons at both levels:", (dup > 1).sum())
print(x.player.nunique(), "players;", x.has_college.groupby(x.player).first().sum(), "with college;",
      (x.level == "NCAA").sum(), "NCAA rows;", (x.level == "NBA").sum(), "NBA rows")
