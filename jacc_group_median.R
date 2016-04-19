# get the group median from mesh140
library(dplyr)
subjects <- c()
s_nums = seq(1, 19)[seq(1,19) != 9]
for (s in s_nums)
{
    subjects <- c(subjects, paste('hel', s, sep=''))
}
graph_dir <- paste('/cnari/normal_language/HEL/graph_analyses/', sep='')
grp_jacc_dir <- paste(graph_dir, 'subrun_group_jaccard/', sep='')
nnodes <- 196002

#for (td in seq(.05, .2, .05))
for (td in c(.15))
{
    for (h in c('lh', 'rh'))
    {
        group_mat <- matrix(ncol=length(subjects), nrow=nnodes)
        for (i in 1:length(subjects))
        {
            ss <- subjects[i]
            jacc_dir <- paste(graph_dir, ss, '/subrun_jaccard_res/', sep='')
            fname <- paste('jacc_',ss,'_',td,'.ijk_',h,'_mesh140.1D', sep='')
            group_mat[, i] <- read.table(paste(jacc_dir, fname, sep=''))$V2
        }
        grp_med <- apply(group_mat, 1, median)
        grp_med_out <- cbind(seq(0, nnodes-1), grp_med)
        outname <- paste(grp_jacc_dir, 'subrun_group_jaccard_median_', h,'_mesh140_', td, '.1D', sep='')
        write.table(grp_med_out, outname, row.names=FALSE, col.names=FALSE, quote=FALSE)
    }
}
