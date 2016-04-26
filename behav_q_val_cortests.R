# check whether correlation betweewn behavior scores and modularity vals
library(dplyr)

setwd('/Users/andric/Documents/workspace/hel/group_modularity/')
subjects <- c()
s_nums = seq(1, 19)[seq(1,19) != 9]
for (s in s_nums)
{
    subjects <- c(subjects, paste('hel', s, sep=''))
}

behav <- read.table('/Users/andric/Documents/HEL/questions/scores.txt', header=TRUE)
scores <- behav$SCORE[s_nums]

for (td in seq(.05, .2, .05))
{
    print(td)
    q_vals <- read.table(paste('max_q_values_density',td,'_array.txt', sep=''))
    names(q_vals) <- c('view1', 'view2')
    print(cor.test(scores, q_vals$view1))
    print(cor.test(scores, q_vals$view2))
}

