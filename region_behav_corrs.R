# differ particpants by correlations
library(dplyr)
setwd('/Users/andric/Documents/workspace/hel/behav_correlations_etc/')
subjects <- c()
s_nums = seq(1, 19)[seq(1,19) != 9]
for (s in s_nums)
{
    subjects <- c(subjects, paste('hel', s, sep=''))
}

region_list <- c('lh_IFGOp',
                 'rh_IFGOp',
                 'lh_ant_occ_s',
                 'rh_ant_occ_s',
                 'lh_sup_temp_g',
                 'rh_sup_temp_g',
                 'lh_mid_occ_g',
                 'rh_mid_occ_g')

behav <- read.table('/Users/andric/Documents/HEL/questions/scores.txt', header=TRUE)
scores <- behav$SCORE[s_nums]

for (region in region_list){
    print(region)
    print(summary(read.csv(paste(region,'_grouptable_raw.csv', sep=''))))
}

# reg_dat <- read.csv(paste(region, '_grouptable_raw.csv', sep=''))
for (region in region_list){
    reg_dat <- read.csv(paste(region,'_grouptable_raw.csv', sep=''))
    cor_pval <- cor.test(scores, reg_dat$NZMean)$p.value
    if (cor_pval <= .05){
        print(region)
        print(cor.test(scores, reg_dat$NZMean))}
    else{
        next
    }
}



mod_dir <- c('/Users/andric/Documents/workspace/hel/group_modularity/')
for (td in seq(0.05, .2, .05)){
    q_vals <- read.table(paste(mod_dir, 'max_q_values_density',td,'_array.txt', sep=''))
    names(q_vals) <- c('view1', 'view2')
    print(cor.test(scores, q_vals$view1))
}


