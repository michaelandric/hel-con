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
                 'rh_mid_occ_g',
                 'lh_sup_temp_s',
                 'rh_sup_temp_s',
                 'lh_mid_temp_g',
                 'rh_mid_temp_g')

behav <- read.table('/Users/andric/Documents/HEL/questions/scores.txt', header=TRUE)
scores <- behav$SCORE[s_nums]
scores_frame <- tbl_df(data.frame(subjects, scores))

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



region_frame <- data.frame()
for (region in region_list){
    reg_dat <- read.csv(paste(region,'_grouptable_raw.csv', sep=''))
    region_frame <- rbind(region_frame, reg_dat)
}

region_frame <- data.frame(rep(subjects, length(region_list)),
                           region_frame$NZMean, region_frame$Median,
                           rep(region_list, each=length(subjects)))

names(region_frame) <- c('Participant', 'NZMean', 'Median', 'Region')
region_frame <- tbl_df(region_frame)

#print(sort(tapply(region_frame$NZMean, list(region_frame$Region), sd)))
#print(sort(tapply(region_frame$NZMean, list(region_frame$Region), var)))

lh_ant_occ_s_dat <- filter(region_frame, Region == 'lh_ant_occ_s')
lh_ant_occ_s_high <- arrange(lh_ant_occ_s_dat, desc(NZMean))$Participant[1:9]
lh_ant_occ_s_low <- arrange(lh_ant_occ_s_dat, desc(NZMean))$Participant[10:18]

lh_sup_temp_s_dat <- filter(region_frame, Region == 'lh_sup_temp_s')
lh_sup_temp_s_high <- arrange(lh_sup_temp_s_dat, desc(NZMean))$Participant[1:9]
lh_sup_temp_s_low <- arrange(lh_sup_temp_s_dat, desc(NZMean))$Participant[10:18]

high_participants <- intersect(lh_sup_temp_s_high, lh_ant_occ_s_high)
low_participants <- intersect(lh_sup_temp_s_low, lh_ant_occ_s_low)
print(high_participants)
write.table(high_participants, 'high_participants.txt', row.names=F, col.names=F, quote=F)
print(low_participants)
write.table(low_participants, 'low_participants.txt', row.names=F, col.names=F, quote=F)
print(subjects[!subjects %in% low_participants & !subjects %in% high_participants])


for (region in region_list){
    reg_dat <- read.csv(paste(region,'_grouptable_raw.csv', sep=''))
    cor_pval <- cor.test(scores, reg_dat$NZMean)$p.value
    print(cor.test(scores, reg_dat$NZMean))}
    }
}
