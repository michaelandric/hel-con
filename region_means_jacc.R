# get mean within region

library(dplyr)
library(ggplot2)
subjects <- c()
s_nums = seq(1, 19)[seq(1,19) != 9]
for (s in s_nums)
{
    subjects <- c(subjects, paste('hel', s, sep=''))
}

region_list <- c('G_front_inf-Orbital',
                 'G_front_inf-Opercular',
                 'G_front_inf-Triangul',
                 'G_front_middle',
                 'G_pariet_inf-Angular',
                 'G_pariet_inf-Supramar',
                 'G_temp_sup-G_T_transv',
                 'G_temp_sup-Lateral',
                 'G_temp_sup-Plan_polar',
                 'G_temp_sup-Plan_tempo',
                 'G_and_S_cingul-Ant',
                 'G_precuneus', 'G_cuneus',
                 'S_calcarine',
                 'G_oc-temp_med-Lingual',
                 'S_temporal_transverse',
                 'S_temporal_sup')

# nodedir <- paste('/Users/andric/Documents/workspace/hel/PAU_SUMA/')
nodedir <- paste('/cnari/normal_language/HEL/freesurfdir/PAU/SUMA/')
# jaccdir <- paste('/Users/andric/Documents/workspace/hel/group_jaccard/')
graphdir <- paste('/cnari/normal_language/HEL/graph_analyses/')

pdf('/cnari/normal_language/HEL/graph_analyses/group_jaccard/jacc_region_barplots.pdf')
par(mfrow=c(2, 2))
for (h in c('lh', 'rh'))
{
    for (reg in region_list)
    {
        reg_dat_vec <- c()
        reg_name_vec <- c()
        dens_vec <- c()
        rnodes <- read.table(paste(nodedir, h, '_',
                                   reg, '.nodes.1D', sep=''))$V1
        for (td in seq(.05, .2, .05))
        {
            ss_mat <- matrix(nrow=196002, ncol=length(subjects))
            for (ss in 1:length(subjects))
            {
                ss_mat[, ss] <- read.table(paste(graphdir, subjects[ss],
                                                 '/jaccard_res/jacc_', subjects[ss], '_', td, '.ijk_', h, '_mesh140.1D', sep=''))$V2
            }
            rnode_set <- filter(data.frame(ss_mat), rnodes==1)
            rnode_set[rnode_set==777] = NA
            reg_dat_vec <- c(reg_dat_vec, as.numeric(colMeans(rnode_set, na.rm=TRUE)))
            # print(reg_dat_vec)
            reg_name_vec <- c(reg_name_vec, rep(reg, length(subjects)))
            dens_vec <- c(dens_vec, rep(td, length(subjects)))
        }
        dframe <- data.frame(reg_dat_vec, dens_vec, reg_name_vec)
        colnames(dframe) <- c('dat', 'density', 'region')
        reg_smr <- summarise(group_by(dframe, density), reg_val= mean(dat))
        print(qplot(x=density, y=reg_val, data=reg_smr,
                    geom="bar", stat="identity", main=paste(h, reg), xlab="density", ylab="region mean"))
    }
}
dev.off()

#                avgs <- mean(apply(reg_dat, 2, mean))
#                sem <- (sd(reg_dat))/(sqrt(length(reg_dat)))
