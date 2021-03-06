## 14/April/2014. AVA script implementing AVA analysis as reported in Davis et al.
## Link to original paper is http://dx.doi.org/10.1093/cercor/bhs416
## Dec 2015. updated version by MJA
library(pastecs)
ssname <- commandArgs(trailingOnly=T)
s <- c(.5, 1, .5)   # this for smoothing
s <- s/sum(s)

tps_func <- function(x, s)
{
    xflt <- na.omit(filter(x, sides=2, s)) 
    tps <- turnpoints(xflt)
    peaksLocation <- which(tps$peaks==TRUE)
    pitsLocation <- which(tps$pits==TRUE)
    peaks_vec <- xflt[peaksLocation]
    pits_vec <- xflt[pitsLocation]
    varPeaks <- var(peaks_vec)
    varPits <- var(pits_vec)
    logratio <- log(varPeaks/varPits)
    return(logratio)
}

# Do AVA for each of the two time series
for (i in seq(2))
{
    inPath <- paste(Sys.getenv('hel'), ssname, 'preprocessing/', sep='/')
    inName <- paste('task_sess_',i,'_',ssname,'_gm_mskd.txt', sep='')
    inFile <- paste(inPath, inName, sep='')
    outPath <- inPath
    outName <- paste('ava_smth_task_sess_',i,'_',ssname,'_gm_mskd.txt', sep='')
    outFile <- paste(outPath, outName, sep='')

    myts <- as.matrix(read.table(inFile))
    outvec <- apply(myts, 1, tps_func, s)
    outvec[is.na(outvec)] <- 0

    write.table(round(outvec, 4), outFile, row.names=FALSE, col.names=FALSE)
}
