setwd('~/Documents/workspace/hel/group_similarity/')
library(dplyr)
library(ggplot2)

pdf('plotting_similarity_nmi.pdf')
for (td in seq(.05, .2, .05))
{
    within1 <- read.table(paste('within_session1_dens_',td,'_nmi.txt', sep=''))$V1
    within2 <- read.table(paste('within_session2_dens_',td,'_nmi.txt', sep=''))$V1
    between <- read.table(paste('between_dens_',td,'_nmi.txt', sep=''))$V1
    repnames <- c(rep("sess_1", length(within1)), rep("sess_2", length(within2)), rep("between", length(between)))
    nm_df <- tbl_df(data.frame(c(within1, within2, between), repnames))
    names(nm_df) <- c('NMI', 'Group')
    print(qplot(NMI, data = nm_df, geom="density", fill=Group, alpha=I(.66), xlim=c(0,1), main=paste("Density ",td*100,"%", sep=""), xlab="Normalized Mutual Information") + theme(panel.background = element_rect(fill="white")) + theme_bw())
}
dev.off()