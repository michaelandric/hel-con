# Calculate sorensen-dice similarity 

library(dplyr)

lat_new <- read.table('/home/cnari/cnari_projects/normal_language/HEL/graph_analyses/randomise_global_connectivity/wgc_cluster_index_lh_lat.txt')$V1
lat_old <- read.table('/home/cnari/cnari_projects/normal_language/HEL/graph_analyses/group_global_connectivity/Clust_mask_lh_lat.txt')$V1

num <- length(intersect(which(lat_new == 1), which(lat_old == 1)))*2
denom <- length(which(lat_new == 1)) + length(which(lat_old == 1))
print(num/denom)

