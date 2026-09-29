SSAC ABSTRACT -- DATA AND R MARKDOWN
====================================
28 source CSVs consolidated to 7, merged on their natural keys.

CSV (7)
-------
season_series.csv            13 rows, 96 cols.  season = key.
                             Every season-level series merged: the A/B/C arbitrage
                             measures, Farrell efficiency, the counterfactual paths,
                             frontier and slack series, equilibrium quantities, the
                             zone-league aggregates and the volume trend.
                             Columns are prefixed by their source file, e.g.
                             arbitrage__a_dm, farrell__eo, cf_paths__mD.

team_season_zones.csv        390 rows, 44 cols.  season + ab = key.
                             Zone shares and conversion rates for all 390
                             team-seasons, merged with the Markowitz LP solutions
                             on raw inputs (mk__) and GAM-fitted inputs (mkgam__).

team_season_boxscore.csv     390 rows, 62 cols.  Basketball Reference Advanced and
                             Per Game panel. Kept separate: different provenance
                             and a much wider column set than the zone data.

gam_zone_team_season.csv     2,340 rows.  The GAM estimation sample, one row per
                             zone-team-season, with fitted values (p_gam).

gam_partial_effects.csv      360 rows.  Partial effects by zone and smooth.

cf_surface_grid.csv          338 rows.  season x risk grid holding the two
                             counterfactual frontier surfaces behind Figure 1
                             (z_dev_frozen, z_sel_frozen).

zones_raw_transcription.csv  390 rows.  zones_a + zones_b concatenated. The raw
                             transcription from the 13 Basketball Reference
                             shooting tables, before validation. Provenance only;
                             team_season_zones.csv is the version to use.

R MARKDOWN (3)
--------------
cf3d.Rmd                 Figure 1's surfaces. Explains why ggplot2 cannot do 3D
                         and gives three routes (plot3D, rayshader, plotly) plus a
                         ggplot2-native 2D alternative. Reads cf_surface_grid.csv
                         and the cf_paths columns of season_series.csv.
trend3par.Rmd            ggplot2 source for the 3PA volume trend figure.
nba_shot_portfolios.Rmd  SUPERSEDED. Predates the equilibrium reframing; its
                         conclusions were reversed by later work. Provenance only.

NOTE: none of the three .Rmd files has been executed. There is no R in the
environment they were written in, so they are lint-checked only. Expect to adjust
label offsets and paths on first knit.

VERIFIED AFTER CONSOLIDATION
  2025-26 A iso-risk gain 6.68, B risk shed 1.22, C balanced 5.68 and 1.04,
  Farrell 0.945 output-oriented and 0.892 input-oriented -- all match the abstract.
  390 team-seasons, 13 seasons, 2,340 GAM rows.
