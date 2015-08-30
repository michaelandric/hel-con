setwd('/Users/andric/Documents/workspace/hel/group_global_connectivity/')
library(clue)
clst_prts <- read.table('group_Clust_msk_glob_conn_knnward_clst1')
clst_rows <- rowSums(clst_prts)

clst_prts <- clst_prts[which(clst_rows > 0), ]
clcon <- cl_consensus(hclust(dist(clst_prts), method = 'ward.D2'))
cl_ensem <- cl_ensemble(hclust(as.dist(clst_prts), method = 'ward.D2'))
cons_ensem <- cl_consensus(cl_ensem)

ag <- read.table('agreement_group_Clust_msk_glob_conn_knnward_clst1')
cl_agensem <- cl_ensemble(hclust(as.dist(ag), method = 'ward.D2'))
ag_cons <- cl_consensus(cl_agensem)
