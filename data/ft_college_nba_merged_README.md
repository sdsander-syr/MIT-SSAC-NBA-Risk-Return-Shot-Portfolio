# ft_college_nba_merged.csv

One row per player-season of free throw shooting, college (NCAA) and NBA regular season, for the 141 players in the
Weiss (2019) shooting-eyes database. 1,909 rows: 301 NCAA (113 players with a college career) and 1,608 NBA (1979-80 to 2025-26).

| Column | Meaning |
|---|---|
| player | name as in `gaze_database.csv` (join key) |
| bref_id, cbb_slug | Basketball-Reference and Sports-Reference CBB ids |
| has_college | 1 if a Sports-Reference college record linked to the player's NBA id was found |
| eyes, gaze, gaze_type, ball_watcher | the player's gaze (process) classification, repeated on every row |
| position, height_in | from the database |
| level | `NCAA` or `NBA` |
| season, season_label | season end year (2016) and label (2015-16) |
| career_row, year_in_level, experience | row number in the career; seasons since first season at this level; seasons since first college or NBA season |
| team, college_class, age, g, mp | school or NBA team(s) (traded players: `SAC/TOR`); NCAA class; NBA age and minutes |
| ftm, fta, ft_pct | free throws made, attempted, percentage (blank when fta = 0) |
| season_ft_leader, season_leader_ft_pct | that season's FT% leader at that level (observed ceiling) |
| ceiling_est | estimated ceiling: LOWESS (frac 0.3) of the leader FT% series, fitted separately per level |
| gap_to_ceiling | ft_pct - ceiling_est |
| ceiling_note | why ceiling_est is blank (NCAA seasons before 1992-93: no leader on Sports-Reference) |
| source | Basketball-Reference season totals or Sports-Reference CBB player page |

Sources: NBA from Basketball-Reference player totals (via github.com/sumitrodatta/bball-reference-datasets);
college from Sports-Reference CBB player pages, each accepted only if it links to the player's Basketball-Reference id;
NBA leaders from `ft_leaders.csv`; NCAA leaders from Sports-Reference season leader pages (1992-93 to 2017-18).

Related files: `ft_ceiling_by_season.csv` (leader and estimated ceiling by level and season),
`ncaa_ft_leaders.csv`, `college_unmatched.csv` (28 players with no college record: international players and high school
entrants), `upload_vs_bref.csv` (an uploaded NBA FT file checked against Basketball-Reference; 176 of 234 rows disagree,
so it was not used).

Rebuild: `code/ft_college_nba/` — build_ft_player_seasons.py, fetch_cbb_pages.py, fetch_ncaa_ft_leaders.py, merge_college_nba.py.
