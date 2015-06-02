# Run this after "degree_fitting_pwr_funcs.R"
# (This accompanies 40.pwr_funcs.R and from 41.pwr_funcs_stats.R)
## It uses 'fitting*.txt' outputs from 40.pwr_funcs.R to do bar graphs that accompany group stats
library(gplots)   # this library only on servers 30 and 32
library(RColorBrewer)

graph_dir <- paste('/cnari/normal_language/HEL/graph_analyses/')
subjects <- c()
s_nums = seq(1, 19)[seq(1,19) != 9]
for (s in s_nums)
{
    subjects <- c(subjects, paste('hel', s, sep=''))
}

thresh_dens <- .05
conditions <- seq(2)
condition_names = c("Sess1", "Sess2")

dat_matA = matrix(nrow=length(subjects),ncol=length(conditions))
dat_matB = matrix(nrow=length(subjects),ncol=length(conditions))
dat_matG = matrix(nrow=length(subjects),ncol=length(conditions))

# setwd(paste("/mnt/tier2/urihas/Andric/steadystate/links_files5p/",sep=""))
for (ss in 1:length(subjects))
{
    deg_dir <- paste(graph_dir, subjects[ss], '/degrees/', sep='')
    for (i in conditions)
    {
        fitting_outn <- paste(deg_dir,
                              'fitting_cond',i,'_',subjects[ss],'.dens_',thresh_dens,'.txt', sep='')
        dat_matA[ss,i] = as.numeric(strsplit(levels(read.delim(fitting_outn)[1,])[4]," ")[[1]][4]) ## this is for alpha — shape
        dat_matB[ss,i] = as.numeric(strsplit(levels(read.delim(fitting_outn)[1,])[5]," ")[[1]][4]) ## this is for beta — scale ("exponent cutoff")
        dat_matG[ss,i] = as.numeric(strsplit(levels(read.delim(fitting_outn)[1,])[6]," ")[[1]][4]) ## this is for gamma — power law values
    }
}

error_vecG <- c()
error_vecB <- c()
error_vecA <- c()
denom <- sqrt(length(subjects))
for (i in conditions)
{
    # erG <- sd((dat_matG[,i] - rowMeans(dat_matG)) / sqrt(length(subjects)))
    erG <- sd(dat_matG[,i]) / denom
    error_vecG <- c(error_vecG, erG)
    # erB <- sd((dat_matB[,i] - rowMeans(dat_matB)) / sqrt(length(subjects)))
    erB <- sd(dat_matB[,i]) / denom
    error_vecB <- c(error_vecB, erB)
    # erA <- sd((dat_matA[,i] - rowMeans(dat_matA)) / sqrt(length(subjects)))
    erA <- sd(dat_matA[,i]) / denom
    error_vecA <- c(error_vecA, erA)   # These end up same order as condition_names ("Highly ordered, Some order, Random, Almost Random")
}

colnames(dat_matG) <- condition_names
colnames(dat_matB) <- condition_names
colnames(dat_matA) <- condition_names

aG <- apply(dat_matG, 2, mean)
aB <- apply(dat_matB, 2, mean)
aA <- apply(dat_matA, 2, mean)

thepal = colorRampPalette(brewer.pal(8,"Set2"))(8)
out_dir <- paste(graph_dir, 'group_degrees/', sep='')

pdf(paste(out_dir, 'Degrees_PowerLaw_bargraph.dens_',thresh_dens,'.pdf',sep=''))
ylimG <- c(1.15, 1.01 * max(aG + error_vecG))
plotaG <- barplot2(aG, beside = TRUE, ylim = ylimG, ylab = "Power law values", col = thepal, plot.grid = TRUE, xpd=F)
segments(x0 = plotaG, x1 = plotaG, y0 = aG, y1 = aG + error_vecG)
segments(x0 = plotaG - .2, x1 = plotaG + .2, y0 = aG + error_vecG, y1 = aG + error_vecG)
dev.off()

pdf(paste(out_dir, 'Degrees_ExpCutoff_bargraph.dens_',thresh_dens,'.pdf', sep=''))
ylimB <- c(0, 1.15 * max(aB + error_vecB))
plotaB <- barplot2(aB, beside = TRUE, ylim = ylimB, ylab = "Exponent cutoff values", col = thepal, plot.grid = TRUE)
segments(x0 = plotaB, x1 = plotaB, y0 = aB, y1 = aB + error_vecB)
segments(x0 = plotaB - .2, x1 = plotaB + .2, y0 = aB + error_vecB, y1 = aB + error_vecB)
dev.off()

pdf(paste(out_dir, 'Degrees_TruncPShape_bargraph.dens_',thresh_dens,'.pdf',sep=''))
ylimA <- c(0, 1.15 * max(aA + error_vecA))
plotaA <- barplot2(aA, beside = TRUE, ylim = ylimA, ylab = "Trunc Power Shape values", col = thepal, plot.grid = TRUE)
segments(x0 = plotaA, x1 = plotaA, y0 = aA, y1 = aA + error_vecA)
segments(x0 = plotaA - .2, x1 = plotaA + .2, y0 = aA + error_vecA, y1 = aA + error_vecA)
dev.off()
