setwd('~/Documents/workspace/hel/group_modularity/')
library(dplyr)
subjects <- c()
s_nums = seq(1, 19)[seq(1,19) != 9]
for (s in s_nums)
{
    subjects <- c(subjects, paste('hel', s, sep=''))
}

conditions <- seq(2)
condition_names = c("A", "B")
thresholds <- c(20, 15, 10, 5)  #These are densities. % of complete graph

# --- Doing modularity values ----
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

error_vec <- c()
medians_mat <- matrix(nrow = length(thresholds), ncol = length(conditions))

denom <- sqrt(length(subjects))
for (t in 1:length(thresholds))
{
    medians_mat[t,] <- tapply(mod_score_frame$modularity,
                              list(mod_score_frame$condition,
                                   mod_score_frame$thresh==thresholds[t]),
                              median)[,2]
    tmp <- subset(mod_score_frame, mod_score_frame$thresh == thresholds[t])
    tmp_mat <- matrix(tmp$modularity, ncol = length(conditions))
    tmp_means <- rowMeans(tmp_mat)
    for (i in conditions)
    {
        cond_tmp <- tmp_mat[,i]
        er <- sd(cond_tmp) / denom
        error_vec <- c(error_vec, er)
    }
}
error_vec_mat = matrix(error_vec, nrow = length(conditions), byrow = T)

attach(mod_score_frame)
aa <- tapply(modularity, list(condition, thresh), median)
trans_medians <- t(apply(medians_mat, 2, rev))
# trans_errs <- t(apply(error_vec_mat, 2, rev))
trans_errs <- t(apply(error_vec_mat, 1, rev))
ylim <- c(0, 1.11 * max(aa + trans_errs))
pdf('max_q_values_barplot_mediansofmax.pdf')
ab = barplot(aa, beside = TRUE, ylim = ylim, ylab = "Modularity (Q)")
segments(x0 = ab, x1 = ab, y0 = trans_medians, y1 = aa + trans_errs)
segments(x0 = ab - .2, x1 = ab + .2, y0 = trans_medians + trans_errs, y1 = trans_medians + trans_errs)
dev.off()


# ----- Doing n mods -----------
dat5 <- read.table('max_q_n_mods_density0.05_array.txt')
dat10 <- read.table('max_q_n_mods_density0.1_array.txt')
dat15 <- read.table('max_q_n_mods_density0.15_array.txt')
dat20 <- read.table('max_q_n_mods_density0.2_array.txt')
dat <- rbind(stack(dat20), stack(dat15), stack(dat10), stack(dat5))$values

condition_vec <- rep(rep(condition_names, each=length(subjects)), length(thresholds))
subjects_vec <- rep(rep(subjects, length(conditions)), length(thresholds))
thresh_levels <- as.factor(rep(thresholds, each = length(subjects) * length(conditions)))
mod_score_frame <- tbl_df(data.frame(dat, condition_vec, subjects_vec, thresh_levels))
colnames(mod_score_frame) <- c("modularity", "condition", "subject", "thresh")

error_vec <- c()
medians_mat <- matrix(nrow = length(thresholds), ncol = length(conditions))

denom <- sqrt(length(subjects))
for (t in 1:length(thresholds))
{
    medians_mat[t,] <- tapply(mod_score_frame$modularity,
                              list(mod_score_frame$condition,
                                   mod_score_frame$thresh==thresholds[t]),
                              median)[,2]
    tmp <- subset(mod_score_frame, mod_score_frame$thresh == thresholds[t])
    tmp_mat <- matrix(tmp$modularity, ncol = length(conditions))
    tmp_means <- rowMeans(tmp_mat)
    for (i in conditions)
    {
        cond_tmp <- tmp_mat[,i]
        # er <- (sd(cond_tmp - tmp_means)) / denom
        er <- sd(cond_tmp) / denom
        error_vec <- c(error_vec, er)
    }
}
error_vec_mat = matrix(error_vec, nrow = length(conditions), byrow = T)

attach(mod_score_frame)
aa <- tapply(modularity, list(condition, thresh), median)
trans_medians <- t(apply(medians_mat, 2, rev))
# trans_errs <- t(apply(error_vec_mat, 2, rev))
trans_errs <- t(apply(error_vec_mat, 1, rev))
ylim <- c(0, 1.11 * max(aa + trans_errs))
pdf('max_q_n_mods_barplot_mediansofmax.pdf')
ab = barplot(aa, beside = TRUE, ylim = ylim, ylab = "n modules")
segments(x0 = ab, x1 = ab, y0 = trans_medians, y1 = aa + trans_errs)
segments(x0 = ab - .2, x1 = ab + .2, y0 = trans_medians + trans_errs, y1 = trans_medians + trans_errs)
dev.off()