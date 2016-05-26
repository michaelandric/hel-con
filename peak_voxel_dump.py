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
    coordinates, and an AFNI func dataset.
    If not obvious, coordinates and dataset should be in the
    same space.
    Arg: coords:
            This is a three value string, e.g.,
            '-44.0 34 12'
    Arg: dataset:
            This is the functional AFNI data that you
            from which you get the voxel's data.
    """
    log.info('Doing mask_dump_peak')
    cmdargs = split('3dmaskdump -noijk -dbox {} {}'.format(coords, dataset))
    proc = Popen(cmdargs, stdout=PIPE)
    return float(proc.stdout.read())


def build_serieslist(log, datadir, clust, coords, subjectlist):
    """separate function to get series for a cluster."""
    serieslist = []
    for i, subj in enumerate(subjectlist):
        log.info('Peak clust for %s, subj %s', clust, subj)
        fname = "'{}/avg_corrZ_task_{}_bucket+tlrc[{}]'".format(
            datadir, clust, i)
        serieslist.append(mask_dump_peak(log, coords, fname))
    return serieslist


def build_clust_dat(log, datadir, subjectlist, clustercoords):
    """Get peak vox data into table."""
    clust_col_names = []
    clust_dat = pd.Series()
    for clust in clustercoords:
        for seed in clustercoords[clust]:
            num_of_clusts = len(clustercoords[clust][seed])
            for subclust in range(num_of_clusts):
                clust_name = '{}_{}_{}'.format(clust, seed, subclust)
                clust_col_names.append(clust_name)
                coords = clustercoords[clust][seed][subclust]
                clust_series = build_serieslist(log, datadir, clust,
                                                coords, subjectlist)
                clust_dat = clust_dat.append(pd.Series(clust_series))
    return (clust_dat, clust_col_names)


def main():
    """Main call to dump.

    Dump the functional data with mask_dump_peak
    then build the data frame.
    """
    workdir = os.path.join(os.environ['hel'], 'graph_analyses/behav_correlate')
    subjectlist = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]
    clustercoords = {'diff': {'lh_highlevel':
                              ('-26.0 60.0 -46.0', '-12.0 48.0 76.0'),
                              'lh_vis_ctx':
                              ('-46.0 40.0 40.0',
                               '-12.0 70.0 64.0', '10.0 52.0 76.0')},
                     'sess_1': {'lh_vis_ctx':
                                (' -68.0 22.0 42.0',
                                 '-28.0 -70.0 8.0', '-60.0 62.0 -16.0',
                                 '52.0 28.0 62.0', '32.0 10.0 72.0',
                                 '14.0 52.0 22.0', '62.0 28.0 -20.0',
                                 '-44.0 10.0 -38.0', '-24.0 70.0 58.0',
                                 '20.0 -66.0 20.0', '64.0 18.0 42.0')},
                     'sess_2': {'lh_ttg':
                                ('14.0 82.0 10.0',
                                 '72.0 40.0 -8.0'),
                                'lh_vis_ctx':
                                ('8.0 -70.0 22.0', '6.0 48.0 48.0',
                                 '-12.0 94.0 2.0')}}
    logfile = setup_log(os.path.join(workdir, 'mask_dump_peak'))
    logfile.info('Doing mask_dump_peak')

    cluster_peaks, cluster_names = build_clust_dat(logfile, workdir,
                                                   subjectlist, clustercoords)
    total_num_clusts = len(list(chain(*clustercoords.values())))
    total_num_subjects = len(subjectlist)
    out_dat = pd.DataFrame(cluster_peaks.reshape(total_num_clusts,
                                                 total_num_subjects).T,
                           columns=cluster_names)
    outname = os.path.join(workdir, 'avg_corrZ_task_all_peak_voxel_data.csv')
    out_dat.to_csv(outname, index=False)

if __name__ == '__main__':
    main()
