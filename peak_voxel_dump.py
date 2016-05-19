# -*- coding: utf-8 -*-
"""
Created on Thurs May  19 2016.

@author: andric
"""

import os
import pandas as pd
from setlog import setup_log
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from itertools import chain


def mask_dump_peak(log, coords, dataset):
    """Dump the functional data at voxel coords.

    Generalize this to accept the log file,
    coordinates, and an AFNI func dataset
    """
    log.info('Doing mask_dump_peak')
    cmdargs = split('3dmaskdump -noijk -dbox {} {}'.format(coords, dataset))
    proc = Popen(cmdargs, stdout=PIPE)
    return float(proc.stdout.read())


def build_clust_dat(log, datadir, subjectlist, clustercoords):
    """Get peak vox data into table."""
    clust_col_names = []
    clust_dat = pd.Series()
    for clust in clustercoords:
        num_of_clusts = len(clustercoords[clust])
        for subclust in num_of_clusts:
            serieslist = []
            clust_name = '{}_{}'.format(clust, subclust)
            clust_col_names.append(clust_name)
            coords = clustercoords[clust][subclust]
            for i, subj in enumerate(subjectlist):
                log.info('Peak clust for %s, subj %s', clust, subj)
                fname = "'{}/avg_corrZ_task_diff_bucket+tlrc[{}]'".format(
                    datadir, i)
                serieslist.append(mask_dump_peak(log, coords, fname))
            clust_dat = clust_dat.append(pd.Series(serieslist))
    return (clust_dat, clust_col_names)


def main():
    """Main call to dump.

    Dump the functional data with mask_dump_peak
    then build the data frame.
    """
    workdir = os.path.join(os.environ['hel'], 'graph_analyses/behav_correlate')
    subjectlist = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]
    clustercoords = {'lh_highlevel': ('-26.0 60.0 -46.0', '-12.0 48.0 76.0'),
                     'lh_vis_ctx': ('-46.0 40.0 40.0', '-12.0 70.0 64.0',
                                    '10.0 52.0 76.0')}
    logfile = setup_log(os.path.join(workdir, 'mask_dump_peak'))
    logfile.info('Doing mask_dump_peak')

    cluster_peaks, cluster_names = build_clust_dat(logfile, workdir,
                                                   subjectlist, clustercoords)
    total_num_clusts = len(list(chain(*clustercoords.values())))
    total_num_subjects = len(subjectlist)
    out_dat = pd.DataFrame(cluster_peaks.reshape(total_num_clusts,
                                                 total_num_subjects).T,
                           columns=cluster_names)
    outname = os.path.join(workdir, 'avg_corrZ_task_diff_peak_voxel_data.csv')
    out_dat.to_csv(outname, index=False)

if __name__ == '__main__':
    main()
