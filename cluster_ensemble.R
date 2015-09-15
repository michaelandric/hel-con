setwd('/Users/andric/Documents/workspace/hel/group_global_connectivity/')
library(clue)
clst_prts <- read.table('group_Clust_msk_glob_conn_knnward_clst1')
clst_rows <- rowSums(clst_prts)

clst_prts <- clst_prts[which(clst_rows > 0), ]

# hclust & dist on single participant (2967 x 262245)
# cl_ensemble the group from the indiv hclust solutions
# then cl_consensus the ensemble

clcon <- cl_consensus(hclust(dist(clst_prts), method = 'ward.D2'))
cl_ensem <- cl_ensemble(hclust(as.dist(clst_prts), method = 'ward.D2'))
cons_ensem <- cl_consensus(cl_ensem)

cl_agensem <- cl_ensemble(hclust(as.dist(ag), method = 'ward.D2'))
ag_cons <- cl_consensus(cl_agensem)


# below is the newest ('correct') version. no need for clue.
ag <- read.table('agreement_group_Clust_msk_glob_conn_knnward_clst1')
d <- dist(ag, method="canberra")
d_cl <- hclust(d, method='ward.D2')
rect_d_cl <- rect.hclust(d_cl, k=4)
ctree <- cutree(d_cl, k=4)
km <- kmeans(d_cl, 4)


solution_vec <- rep(0, length(clst_rows))
solution_vec[which(clst_rows > 0)] = km$cluster
write.table(solution_vec, 'kmeans_group_clst', row.names=F, col.names=F, quote=F)

solution_vec <- rep(0, length(clst_rows))
solution_vec[which(clst_rows > 0)] = ctree
write.table(solution_vec, 'wrd_group_clst', row.names=F, col.names=F, quote=F)