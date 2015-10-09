# Doing Wilcoxon signed-rank test
setwd('/cnari/normal_language/HEL/graph_analyses/group_global_connectivity')
subjects <- c()
s_nums = seq(1, 19)[seq(1,19) != 9]
for (s in s_nums)
{
        subjects <- c(subjects, paste('hel', s, sep=''))
}

nvox <- 262245
group_mat <- matrix(ncol=length(subjects), nrow=nvox)
graph_dir <- paste('/cnari/normal_language/HEL/graph_analyses/', sep='')
lb <- 'lag'
for (ss in 1:length(subjects))
{
    ssdir <- paste(graph_dir, subjects[ss], 'global_connectivity', sep='/')
    group_mat[, ss] <- read.table(paste(ssdir, '/ccf_',lb,'_out_',subjects[ss],'_gm_mskd.ijk_fnirted_MNI2mm.txt', sep=''))$V1
}

oo <- apply(group_mat, 1, wilcox.test, correct=FALSE)
pvals <- sapply(seq_along(1:nvox), function(i)oo[[i]]$p.value[[1]]) 
stats <- sapply(seq_along(1:nvox), function(i)oo[[i]]$statistic[[1]]) 

write.table(stats, paste('ccf_',lb,'_out_group_gm_mskd_wilcox_stats', sep=''), row.names=F, col.names=F, quote=F)
write.table(pvals, paste('ccf_',lb,'_out_group_gm_mskd_wilcox_pvals', sep=''), row.names=F, col.names=F, quote=F)
