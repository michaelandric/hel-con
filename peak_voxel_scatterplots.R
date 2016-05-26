# Making scatter plots
#
# This plots the difference in weighted global connectivity (WGC) against
# intrasubject correlation, using peak voxel data from
# the significant clusters derived in the intrasubject correlation seed
# from calcarine sulcus against difference in WGC
library(dplyr)
library(ggplot2)
library(gridExtra)
library(reshape2)

ScatterPlot <- function(df, xname, yname, title_name) {
  # This takes only the cluster name (e.g., 'lh_vis_ctx_0')
  # of the data frame "df_peak_intrasubj"
  # works off 3 column data frame, with variable name in one column and
  # values in each the other two columns (those are the "x" and "y" in plot).
  ggplot(df, aes_string(x=xname, y=yname)) + geom_point(size = 3) +
    geom_smooth(method=lm, se=FALSE, size=1.15) + theme_bw() +
    ggtitle(paste(title_name))
}


setwd('/Users/andric/Documents/workspace/hel/behav_correlations_etc/')

# Read in the two datasets
peak_diff_dat <- read.csv('avg_corrZ_task_diff_peak_voxel_data.csv')
intrasubj_corr_dat <- read.csv('tcorr_prsn_gm_mskd_Z_peak_voxel_data.csv')
lh_highlev <- read.csv('lh_highlevel.txt', header=F)
lh_ttg <- read.csv('lh_ttg.txt', header=F)
lh_vis_ctx <- read.csv('lh_vis_ctx.txt', header=F)

# melt them down into two columns
mlt_peak_diff <- melt(peak_diff_dat)
mlt_intrasubj <- melt(intrasubj_corr_dat)

# put them into a data.frame
df_peak_intrasubj <- data.frame(mlt_peak_diff, mlt_intrasubj$value)
df_peak_intrasubj <- tbl_df(df_peak_intrasubj)
# names(df_peak_intrasubj) <- c('clust', 'diff_wgc', 'intra_subj_cor', 'seed_val')

# Doing alternate version with seed vec
# there are 3 vis clusters and 2 highlev clusters:
seed_vec <- c(rep(lh_vis_ctx$V1, 3), rep(lh_highlev$V, 2))
df_peak_intrasubj <- data.frame(mlt_peak_diff, mlt_intrasubj$value, seed_vec)
names(df_peak_intrasubj) <- c('clust', 'diff_wgc',
                              'intra_subj_cor', 'seed_val')
# Plot the vectors
plots <- list()
plt_cnt = 0
pdf('peak_voxel_scatterplots_v2.pdf')  # "v2" uses seed_val
for (clstr in levels(df_peak_intrasubj$clust)) {
  plt_cnt = plt_cnt + 1
  plt <- ScatterPlot(filter(df_peak_intrasubj, clust==clstr),
                     names(df_peak_intrasubj)[2], names(df_peak_intrasubj)[4],
                     clstr)
  plots[[plt_cnt]] <- plt  # add each plot into plot list
  print(plt)
}
dev.off()

# Do some correlation tests
for (clstr in levels(df_peak_intrasubj$clust)) {
  corrtest <- cor.test(filter(df_peak_intrasubj, clust==clstr)$diff_wgc,
                       filter(df_peak_intrasubj, clust==clstr)$intra_subj_cor)
  print(corrtest)
}

for (clstr in levels(df_peak_intrasubj$clust)) {
  corrtest <- cor.test(filter(df_peak_intrasubj, clust==clstr)$diff_wgc,
                       filter(df_peak_intrasubj, clust==clstr)$seed_val)
  print(corrtest)
}
