# Risk and Return in NBA Team-Game Shot-Selection Portfolios

Replication material for the MIT Sloan Sports Analytics Conference (SSAC27) abstract
**"Jimmies and Joes or X's and O's? More Risk for Less Return in Modern NBA Shot-Selection:
An ML and Markowitz Portfolio Analysis of 2nd-Order Shot Statistics in a 1st-Order Analytic League."**

Shane Sanders · Department of Sport Analytics, Falk College of Sport, Syracuse University · sdsander@syr.edu

## What this studies

Each NBA shot is a Bernoulli trial scaled by its point value, so a team's shot distribution
is a portfolio with both a return and a risk. Because attempts are independent trials rather
than correlated holdings, covariance vanishes, portfolio variance is linear in the
attempt-share weights, and the efficient frontier solves a linear rather than quadratic
program. Across 390 team-seasons and roughly 2.77 million field goal attempts (2013-14
through 2025-26), the league sits strictly inside that frontier, and the gap widens every
season.

## Reproducing

Everything is in one R Markdown document.

```r
source("install.R")                  # once, installs the packages below
rmarkdown::render("reproduce.Rmd")   # -> reproduce.pdf
```

`reproduce.Rmd` recomputes the six-zone tables, the three arbitrage measures, Farrell
technical efficiency, both counterfactual paths and the zone-share regressions from
`team_season_zones.csv` alone. It prints a PASS/FAIL table against the values published in
the abstract and **stops the knit if any check fails**. It then redraws both figures and the
volume trend, writing tables to `derived/` and graphics to `figures/`.

Packages: `lpSolve` (the linear program), `ggplot2`, `dplyr`, `tidyr`, `scales`, `knitr`,
`rmarkdown`. Optional: `patchwork` for the two-panel layout, `plot3D` for the perspective
version of Figure 1.

## Data

| File | Rows × Cols | Key | Contents |
|---|---|---|---|
| `team_season_zones.csv` | 390 × 44 | `season`, `ab` | **Everything is computed from this.** Zone shares and conversion rates, with the linear-program solutions on raw inputs (`mk__*`) and GAM-fitted inputs (`mkgam__*`). |
| `season_series.csv` | 13 × 96 | `season` | Season-level series as previously computed. Columns carry their source as a prefix: `arbitrage__*`, `farrell__*`, `cf_paths__*`, `trend_series__*`. Useful for cross-checking what `reproduce.Rmd` regenerates. |
| `team_season_boxscore.csv` | 390 × 62 | `season`, team | Basketball Reference Advanced and Per Game panel. |
| `gam_zone_team_season.csv` | 2,340 × 11 | `season`, `ab`, `zone` | GAM estimation sample with fitted values (`p_gam`). |
| `gam_partial_effects.csv` | 360 × 7 | `zone`, smooth | GAM partial effects. |
| `cf_surface_grid.csv` | 338 × 4 | `season`, `risk` | Counterfactual frontier surfaces. `reproduce.Rmd` regenerates this into `derived/`. |
| `zones_raw_transcription.csv` | 390 × 14 | `season`, `ab` | Pre-validation transcription from the Basketball Reference shooting tables. Provenance only — use `team_season_zones.csv`. |

## Key numbers, and where they come from

All recomputed by `reproduce.Rmd` and checked against the abstract:

| Quantity | 2025-26 |
|---|---|
| Points available at unchanged risk | 6.68 |
| Risk sheddable at unchanged scoring | 1.22 |
| Balanced solution | +5.68 points and −1.04 risk |
| Technical efficiency, output-oriented | 0.945 |
| Technical efficiency, input-oriented | 0.892 |
| Shooter-development gain, cumulative | +9.32 |
| Risk added by shot selection, cumulative | +0.70 |

## Layout

```
README.md                     this file
install.R                     installs the required packages
reproduce.Rmd                 the whole analysis: compute, verify, draw
.gitignore                    ignores derived/ and figures/
team_season_zones.csv         the file everything is computed from
season_series.csv             previously computed series, for cross-checking
team_season_boxscore.csv      Basketball Reference panel
gam_zone_team_season.csv      GAM estimation sample
gam_partial_effects.csv       GAM partial effects
cf_surface_grid.csv           counterfactual frontier surfaces
zones_raw_transcription.csv   pre-validation transcription, provenance
abstract/                     the submitted abstract and its two graphics
legacy/                       superseded earlier draft, with a note
```

## Caveats

- **The R has not been executed.** It was written in an environment with no R available, so
  while every input file and column it references has been verified to exist and the chunks
  parse, the knit itself is untested. The verification table in section 7 is there precisely
  so the first render tells you whether it reproduces. Expect to adjust figure dimensions.
- The figures redrawn here are `ggplot2` and `plot3D` versions of the submitted graphics,
  which were produced in Python. They convey the same quantities but are not pixel-identical.
  The submitted PDFs are in `abstract/` and are what the `.tex` compiles against.
- Zone-level free-throw values are not identified from box-score aggregates. The free-throw
  value `theta` is flat within shot type, not zone-specific. Separating it by zone needs
  play-by-play data with fouls attached to the attempts that drew them.
- The zone-share regressions use six observations and three parameters. They are descriptive,
  not inferential, and are presented as such.
- Scoring variance here is the shot-selection component only; it excludes pace and turnovers.
- `legacy/` holds an earlier draft that predates the equilibrium reframing. See
  `legacy/NOTE.txt`.

## License

Data derived from publicly available Basketball Reference tables. Code released for
replication use.
