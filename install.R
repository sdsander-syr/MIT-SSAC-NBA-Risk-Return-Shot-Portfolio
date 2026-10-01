# Run once before knitting reproduce.Rmd
pkgs <- c("lpSolve", "ggplot2", "dplyr", "tidyr", "knitr", "rmarkdown", "scales",
          "patchwork", "plot3D")
new <- pkgs[!(pkgs %in% rownames(installed.packages()))]
if (length(new)) install.packages(new, repos = "https://cloud.r-project.org")
cat("ready. now run: rmarkdown::render('reproduce.Rmd')\n")
