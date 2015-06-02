# fitting degree distributions
library(dplyr)
library(RColorBrewer)
graph_dir <- paste('/cnari/normal_language/HEL/graph_analyses/')
subjects <- c()
s_nums = seq(1, 19)[seq(1,19) != 9]
for (s in s_nums)
{
    subjects <- c(subjects, paste('hel', s, sep=''))
}

conditions <- seq(2)
thepal = colorRampPalette(brewer.pal(8,"Set2"))(8)

#library(brainwaver)
cutoff = 1

fitting <- function (degree.dist, nmax, fitting_outname) 
{
    n.regions <- length(degree.dist)
    tmp <- hist(degree.dist, breaks = c(0:nmax),plot=F)
    cum.dist <- 1 - cumsum(tmp$counts)/n.regions
    mu <- 1/(sum(degree.dist)/n.regions)
    nb <- length(degree.dist[degree.dist > 0])
    gamma <- 1 + nb/(sum(log(degree.dist[degree.dist > 0])))
    x <- degree.dist
    x <- x[x > 0]
    n <- length(x)
    fn <- function(p) -(-n * p * log(sum(x)/(n * p)) - n * log(gamma(p)) + 
                            (p - 1) * sum(log(x)) - n * p)
    out <- nlm(fn, p = 1, hessian = TRUE)
    alpha <- out$estimate
    beta <- sum(degree.dist)/(n.regions * alpha)
    AIC.exp <- -2 * (n.regions * log(mu) - mu * sum(degree.dist)) + 2
    AIC.pow <- -2 * (n.regions * log(gamma - 1) - gamma * sum(log(x))) + 2
    AIC.trunc <- -2 * (-out$minimum) + 2
    fitting <- "mu ="
    fitting <- paste(fitting, mu, sep = " ")
    fitting <- paste(fitting, "gamma = ", sep = "\n")
    fitting <- paste(fitting, gamma, sep = " ")
    fitting <- paste(fitting, "alpha = ", sep = "\n")
    fitting <- paste(fitting, alpha, sep = " ")
    fitting <- paste(fitting, "beta = ", sep = "\n")
    fitting <- paste(fitting, beta, sep = " ")
    fitting <- paste(fitting, "AIC exp = ", sep = "\n")
    fitting <- paste(fitting, AIC.exp, sep = " ")
    fitting <- paste(fitting, "AIC pow = ", sep = "\n")
    fitting <- paste(fitting, AIC.pow, sep = " ")
    fitting <- paste(fitting, "AIC trunc = ", sep = "\n")
    fitting <- paste(fitting, AIC.trunc, sep = " ")
    write.table(fitting, fitting_outname, row.names = FALSE, col.names = FALSE, 
                quote = FALSE)
    list(mu = mu, gamma = gamma, alpha = alpha, beta = beta)
}

deg_func <- function(x, fitting_outname)
{
    degree.dist = x[which(x > cutoff)]
    nmax = max(degree.dist)
    tmp = hist(degree.dist, breaks=c(cutoff:nmax),plot=F)
    cum.dist = 1-cumsum(tmp$counts)/length(degree.dist)
    # d = fitting(x, nmax, fitting_outname)
    d = fitting(degree.dist, nmax, fitting_outname)
    ptshape = d$alpha + d$gamma
    gamma.trace = 1-pgamma((0:nmax),shape=d$alpha,scale=d$beta) 
    Rsq = round((cor(log10(cum.dist)[1:(nmax-1)],
                     log10(gamma.trace)[1:(nmax-1)]))^2, 4)
    return(list("gamma.trace"=gamma.trace,
                "cum.dist"=cum.dist, "nmax"=nmax,
                "shape"=ptshape))
}


condition_names = c("Sess1", "Sess2")
thepalOrder = thepal[c(1,2)]

thresh_dens <- .05
out_dir <- paste(graph_dir, 'group_degrees/', sep='')
pdf(paste(out_dir,
          'Vers2deg_distribution_plotsGROUP',cutoff,'_dens_',thresh_dens,'.pdf', sep=''),
    paper='a4r', width=10.5)
par(mfrow=c(2,4))
for (ss in subjects)
{
    deg_dir <- paste(graph_dir, ss, '/degrees/', sep='')
    dat <- c()
    for (i in conditions)
    {
        in_name <- paste(deg_dir,
                         'task_sess_',i,'_',ss,'.dens_',thresh_dens,'.degrees.txt', sep='')
        dat <- c(dat, as.matrix(read.table(in_name)))
    }
    dat_matrix <- matrix(dat, ncol=length(conditions))
    rsquares <- c()
    for (i in conditions)
    {
        fitting_outn <- paste(deg_dir,
                              'fitting_cond',i,'_',ss,'.dens_',thresh_dens,'.txt', sep='')
        out <- deg_func(dat_matrix[,i], fitting_outn)
        Rsq <- round((cor(log10(out$cum.dist)[1:(out$nmax-2)],
                         log10(out$gamma.trace)[1:(out$nmax-2)]))^2, 4)
        rsquares <- c(rsquares, Rsq)
#        plot(log10(cutoff:(out$nmax-1)),
#             log10(out$cum.dist), pch=3,
#             xlab='log(k)', ylab='log(cumulative distribution)',
#             main=paste(ss,' ',condition_names[i],' // R^2=',
#                        round(Rsq, 4), sep=''))
#        plot(log10(cutoff:(out$nmax-1)),
#              log10(out$gamma.trace)[1:(out$nmax-1)],
#              lwd=2, col=thepalOrder[i])

        plot(log10(cutoff:(out$nmax-1)),
             log10(out$gamma.trace)[1:(out$nmax-1)],
             lwd=2, col=thepalOrder[i],
             xlab='log(k)', ylab='log(cumulative distribution)',
             main=paste(ss,' ',condition_names[i],' // R^2=',
                        round(Rsq, 4), sep=''))
        points(log10(cutoff:(out$nmax-1)),
             log10(out$cum.dist), pch=3)
    }
    rsquared_mat = matrix(rsquares, nrow=1, byrow=T)
}
dev.off()
