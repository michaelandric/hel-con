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

ScatterPlot <- function(df, xname, yname, xlabel, ylabel, title_name) {
  # This takes only the cluster name (e.g., 'lh_vis_ctx_0')
  # of the data frame "df_peak_intrasubj"
  # works off 3 column data frame, with variable name in one column and
  # values in each the other two columns (those are the "x" and "y" in plot).
  ggplot(df, aes_string(x=xname, y=yname)) + geom_point(size = 3, shape=15) +
    geom_smooth(method=lm, se=FALSE, size=1.15) + xlab(xlabel) +
    ylab(ylabel) + theme_bw() + ggtitle(paste(title_name))
}


setwd('/Users/andric/Documents/workspace/hel/behav_correlations_etc/')

# Read in the datasets
peak_diff_dat <- read.csv('avg_corrZ_task_all_peak_voxel_data.csv')
lh_highlevel <- read.csv('lh_highlevel.txt', header=F)
lh_ttg <- read.csv('lh_ttg.txt', header=F)
lh_vis_ctx <- read.csv('lh_vis_ctx.txt', header=F)

# melt it down into two columns
mlt_peak_diff <- melt(peak_diff_dat)

sess_names <- c()
clust_nums <- c()
seed_names <- c()
sess_name_vec <- c()
clust_num_vec <- c()
seed_name_vec <- c()
seed_data_vec <- c()
for (i in 1:length(levels(mlt_peak_diff$variable))) {
  sess_str_spl <- strsplit(levels(mlt_peak_diff$variable)[i], "_lh")[[1]]
  sess <- sess_str_spl[1]
  sess_names <- c(sess_names, sess)
  sess_name_vec <- c(sess_name_vec, rep(sess, length(subjects)))
  suff <- strsplit(sess_str_spl[2], '_')[[1]][-1]
  clust_nums <- c(clust_nums, as.numeric(tail(suff, n=1)))
  clust_num_vec <- c(clust_num_vec, rep(as.numeric(tail(suff, n=1)), length(subjects)))
  seed <- paste(head(suff, -1), collapse='_')
  seed_names <- c(seed_names, seed)
  seed_name_vec <- c(seed_name_vec, rep(seed, length(subjects)))
  seed_data <- as.matrix(get(paste('lh', seed, sep='_')))
  seed_data_vec <- c(seed_data_vec, seed_data)
}


# put them into a data.frame
df_peak_dat <- data.frame(mlt_peak_diff$value, sess_name_vec, seed_name_vec,
                          seed_data_vec, as.factor(clust_num_vec))
names(df_peak_dat) <- c('wgc', 'session', 'seed', 'seed_vals', 'clustnum')
df_peak_dat <- tbl_df(df_peak_dat)

# Plot the vectors
#plots <- list()
#plt_cnt = 0
#pdf('peak_voxel_scatterplots_v2.pdf')  # "v2" uses seed_val
#for (clstr in levels(df_peak_intrasubj$clust)) {
#  plt_cnt = plt_cnt + 1
#  plt <- ScatterPlot(filter(df_peak_intrasubj, clust==clstr),
#                     names(df_peak_intrasubj)[2], names(df_peak_intrasubj)[4],
#                     clstr)
#  plots[[plt_cnt]] <- plt  # add each plot into plot list
#  print(plt)
#}
#dev.off()

plots <- list()
plt_cnt = 0
# pdf('peak_voxel_scatterplots_v3.pdf')  # "v3" plots all clusters
# pdf('peak_voxel_scatterplots_v4.pdf')  # "v4" reversed x and y axes
pdf('peak_voxel_scatterplots_v3.2.pdf')  # uses different shape
for (sess_level in levels(df_peak_dat$session)) {
  sess_dat <- filter(df_peak_dat, session==sess_level)
  for (seed_level in unique(sess_dat$seed)) {
    sess_seed_dat <- filter(sess_dat, seed==seed_level)
    for (clst in unique(sess_seed_dat$clustnum)) {
      dat <- filter(sess_seed_dat, clustnum==clst)
      titlename <- paste(sess_level, 'WGC,',seed_level, 'seed, cluster', clst)
      plt <- ScatterPlot(dat, 'seed_vals', 'wgc', seed_level, sess_level, titlename)
      plt_cnt = plt_cnt + 1
      plots[[plt_cnt]] <- plt  # add each plot into plot list
      print(plt)
    }
  }
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
