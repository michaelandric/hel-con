# -*- coding: utf-8 -*-
"""
Created Jul 15 2016.

(AFNI doesn't work in 3+)
@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def fsl_maths(log, corrp, statimg, outname):
    """Threshold via FSL procedure."""
    cmdargs = split('fslmaths {} -thr 0.95 -bin -mul {} {}'.format(
        corrp, statimg, outname))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def cluster(log, inputf, clustindx, lmax, clustsize):
    """Cluster via FSL procedure."""
    cmdargs = split('cluster --in={} --thresh=0.005 --oindex={} \
                    --olmax={}.txt --osize={} --mm'.format(
                        inputf, clustindx, lmax, clustsize))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Wrap the methods for execution."""
    logfile = setup_log(os.path.join(os.environ['hel'], 'logs',
                                     'thresh_cluster_fsl'))
    logfile.info('Threshold and cluster.')
    outdir = os.path.join(os.environ['hel'], 'graph_analyses',
                          'randomise_global_connectivity')

    os.chdir(outdir)
    for subclust_n in range(2, 4):
        prefx = 'knnward_clst1_subclust{}'.format(subclust_n)
        corrctd_p = '{}_4Dfile_n10000_clustere_corrp_tstat2.nii.gz'.format(
            prefx)
        stat = '{}_4Dfile_n10000_tstat2.nii.gz'.format(prefx)
        outfilename = '{}_thresh_4Dfile_n10000_clustere_corrp_tstat2'.format(
            prefx)
        fsl_maths(logfile, corrctd_p, stat, outfilename)
        clust_in = '{}.nii.gz'.format(outfilename)
        clst_indx = '{}_cluster_index'.format(outfilename)
        lmax_f = '{}_lmax.txt'.format(outfilename)
        clst_sz = '{}_cluster_size'.format(outfilename)
        cluster(logfile, clust_in, clst_indx, lmax_f, clst_sz)

if __name__ == '__main__':
    main()
