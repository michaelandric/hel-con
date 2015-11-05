# density hist for Weisfeiler Lehman similarity
library(dplyr)
library(ggplot2)
setwd('~/Documents/workspace/hel/group_modularity_thr0.5msk/')
kv <- as.numeric(read.table('wl_similarity_diffthr8_dens_0.15.wl_simval3'))
pv <- tbl_df(read.table('wl_similarity_diffthr8_dens_0.15.perm_vec_all'))
pv2 <- tbl_df(data.frame(pv, kv))
names(pv) <- 'similarity'

#print(qplot(similarity, data = pv, geom="density", fill=T, alpha=I(.90), main=paste("Density of W-L similarity", sep=""), xlab="Normalized W-L similarity") + scale_fill_manual(values = c("black")) + theme(panel.background = element_rect(fill="white")) + theme_bw() + geom_vline(xintercept = kv, color = "magenta4", size=1.25))
pdf('wl_similarity_plot.pdf')
print(qplot(similarity, data=pv, geom='density', fill=T, alpha=I(.90),
            main=paste('Density of W-L similarity', sep=''),
            xlab='Normalized W-L similarity') +
          scale_fill_manual(values = c('black')) +
          theme(panel.background = element_rect(fill='white')) +
          theme_bw() + geom_segment(aes(x=kv, y=0, xend=kv, yend=50),
                                    color='red', size=1.1))
dev.off()
