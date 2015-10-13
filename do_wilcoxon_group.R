# Doing Wilcoxon signed-rank test
setwd('/cnari/normal_language/HEL/ccf_cor')
subjects <- c()
s_nums = seq(1, 19)[seq(1,19) != 9]
for (s in s_nums)
{
        subjects <- c(subjects, paste('hel', s, sep=''))
}

nvox <- 262245
group_mat <- matrix(ncol=length(subjects), nrow=nvox)
lb <- 'lag'
for (ss in 1:length(subjects))
{
    group_mat[, ss] <- read.table(paste('ccf_abs_',lb,'_out_',subjects[ss],'_gm_mskd.ijk_fnirted_MNI2mm.txt', sep=''))$V1
}

oo <- apply(group_mat, 1, wilcox.test, correct=FALSE)
med_vals <- apply(group_mat, 1, median)
pvals <- sapply(seq_along(1:nvox), function(i)oo[[i]]$p.value[[1]]) 
stats <- sapply(seq_along(1:nvox), function(i)oo[[i]]$statistic[[1]]) 

write.table(stats, paste('ccf_abs_',lb,'_out_group_gm_mskd_wilcox_stats', sep=''), row.names=F, col.names=F, quote=F)
write.table(pvals, paste('ccf_abs_',lb,'_out_group_gm_mskd_wilcox_pvals', sep=''), row.names=F, col.names=F, quote=F)
write.table(med_vals, paste('ccf_abs_',lb,'_out_group_gm_mskd_median_vals', sep=''), row.names=F, col.names=F, quote=F)
