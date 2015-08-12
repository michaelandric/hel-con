library(dplyr)
setwd('~/Documents/workspace/hel/group_global_connectivity/')
conditions <- c('1st View', '2nd View')
nn <- read.csv('avg_corrZ_sess2vals_Clust_mask.cluster_info.csv')
clusters <- unique(nn$cluster)
n_subj <- length(unique(nn$subject))

pdf('Cluster_means_avg_corrZ_sess2vals_Clust_mask.pdf')
for (cl in clusters)
{
    tmp <- filter(nn, cluster==cl)
    tmp_means <- tapply(tmp$val, tmp$condition, mean)
    # tmp_means <- tmp_means[c(1, 2, 4, 3)]
    error_vec <- c()
    for (i in seq(length(conditions)))
    {
        er <- sd(filter(tmp, condition==i)$val - tapply(tmp$val, tmp$subject, mean) / sqrt(n_subj))
        error_vec <- c(error_vec, er)
    }
    # error_vec <- error_vec[c(1, 2, 4, 3)]
    # ylim <- c(0, 1.21 * max(tmp_means + error_vec))
    ylim <- c(0, max(tmp_means + error_vec))
    # ab = barplot(tmp_means, beside = TRUE, ylim = ylim, ylab = "Avg. Global Connectivity")
    ab = barplot(tmp_means, beside = TRUE, ylim = ylim)
    segments(x0 = ab, x1 = ab, y0 = tmp_means, y1 = tmp_means + error_vec)
    segments(x0 = ab - .2, x1 = ab + .2, y0 = tmp_means + error_vec, y1 = tmp_means + error_vec)
    title(paste("Cluster",cl))
}
dev.off()