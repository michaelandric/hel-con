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
                 'rh_mid_temp_g',
                 'lh_ttg',
                 'rh_ttg',
                 'lh_planum_tem',
                 'rh_planum_tem',
                 'lh_vis_ctx',
                 'rh_vis_ctx')

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


lh_highlev <- rowMeans(cbind(filter(region_frame,
                                    Region=='lh_sup_temp_s')$NZMean,
                             filter(region_frame, Region=='lh_ant_occ_s')$NZMean))
lh_lowlev <- rowMeans(cbind(filter(region_frame,
                                   Region=='lh_ttg')$NZMean,
                            filter(region_frame, Region=='lh_vis_ctx')$NZMean))
write.table(lh_highlev, 'lh_highlevel.txt', row.names=F, col.names=F, quote=F)
write.table(lh_lowlev, 'lh_lowlevel.txt', row.names=F, col.names=F, quote=F)
write.table(filter(region_frame, Region=='lh_ttg')$NZMean, 'lh_ttg.txt',
            row.names=F, col.names=F, quote=F)
write.table(filter(region_frame, Region=='lh_vis_ctx')$NZMean, 'lh_vis_ctx.txt',
            row.names=F, col.names=F, quote=F)


# Do modularity values correlate with high or low level region intra-corr?
moddir <- '/Users/andric/Documents/workspace/hel/group_modularity/'
for (td in seq(.05, .2, .05)){
    #print(td)
    q_vals <- read.table(paste(moddir, '/max_q_values_density',td,'_array.txt', sep=''))
    names(q_vals) <- c('View1', 'View2')
    attach(q_vals)
    for (levl in c('lh_highlev', 'lh_lowlev')){
        for (viewing in colnames(q_vals)){
            corrtest <- cor.test(get(levl), get(viewing))
            if (corrtest$p.value <= .05){
                print(c(td, levl, viewing))
                print(corrtest)
            }
            else{
                next
            }
        }
    }
    detach(q_vals)
}


# Do behavior scores correlate with region intra-subj corr?
for (levl in c('lh_highlev', 'lh_lowlev')){
    corrtest <- cor.test(get(levl), scores)
    if (corrtest$p.value <= .05){
        print(c(levl))
        print(corrtest)
    }
    else{
        next
    }
}

library(ggplot2)
pdf('region_qqplots.pdf')
ggplot(filter(region_frame, Region=='lh_ant_occ_s'), aes(sample=NZMean)) +
    theme_bw() + geom_point(stat='qq', size=4) + ggtitle('Q-Q plot lh_ant_occ_s')
ggplot(filter(region_frame, Region=='lh_ttg'), aes(sample=NZMean)) +
    theme_bw() + geom_point(stat='qq', size=4) + ggtitle('Q-Q plot lh_ttg')
ggplot(filter(region_frame, Region=='lh_planum_tem'), aes(sample=NZMean)) +
    theme_bw() + geom_point(stat='qq', size=4) + ggtitle('Q-Q plot lh_planum_tem')
ggplot(filter(region_frame, Region=='lh_vis_ctx'), aes(sample=NZMean)) +
    theme_bw() + geom_point(stat='qq', size=4) + ggtitle('Q-Q plot lh_vix_ctx')
ggplot(filter(region_frame, Region=='lh_sup_temp_s'), aes(sample=NZMean)) +
    theme_bw() + geom_point(stat='qq', size=4) + ggtitle('Q-Q plot lh_sup_temp_s')
dev.off()