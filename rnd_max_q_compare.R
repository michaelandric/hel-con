setwd('~/Documents/workspace/hel/group_rnd_modularity/')
library(dplyr)
subjects <- c()
s_nums = seq(1, 19)[seq(1,19) != 9]
for (s in s_nums)
{
    subjects <- c(subjects, paste('hel', s, sep=''))
}

conditions <- seq(2)
condition_names = c("A", "B")
# thresholds <- c(20, 15, 10, 5)  #These are densities. % of complete graph
thresholds <- c(10, 5)  #These are densities. % of complete graph

# Real data
setwd('~/Documents/workspace/hel/group_modularity/')
dat5 <- read.table('max_q_values_density0.05_array.txt')
dat10 <- read.table('max_q_values_density0.1_array.txt')
dat15 <- read.table('max_q_values_density0.15_array.txt')
dat20 <- read.table('max_q_values_density0.2_array.txt')
dat <- rbind(stack(dat20), stack(dat15), stack(dat10), stack(dat5))$values

condition_vec <- rep(rep(condition_names, each=length(subjects)), length(thresholds))
subjects_vec <- rep(rep(subjects, length(conditions)), length(thresholds))
thresh_levels <- as.factor(rep(thresholds, each = length(subjects) * length(conditions)))
mod_score_frame <- tbl_df(data.frame(dat, condition_vec, subjects_vec, thresh_levels))
colnames(mod_score_frame) <- c("modularity", "condition", "subject", "thresh")


setwd('~/Documents/workspace/hel/group_rnd_modularity/')
rnd_dat5 <- read.table('rnd_max_q_values_density0.05_array.txt')
rnd_dat10 <- read.table('rnd_max_q_values_density0.1_array.txt')