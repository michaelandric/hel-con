# -*- coding: utf-8 -*-
"""
Created Jul 5 2016.

(AFNI doesn't work in 3+)
@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def mergefsl(log, file_list, outname):
    """Merge files with fslmerge."""
    cmdargs = split('fslmerge -t {} {}'.format(outname, file_list))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def make_file_list(subj_list):
    """Make list of files."""
    graph_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    suffx = 'ijk_fnirted_MNI2mm.nii.gz'
    filelist = []
    for i in range(1, 3):
        for subj in subj_list:
            subj_dir = os.path.join(graph_dir, subj, 'global_connectivity')
            fname = 'avg_corrZ_task_sess_{}_{}.{}'.format(i, subj, suffx)
            filelist.append(os.path.join(subj_dir, fname))

    return ' '.join(filelist)


def main():
    """Wrap methods to main call."""
    subjectlist = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]
    logfile = setup_log(os.path.join(os.environ['hel'], 'logs',
                                     'randomise_setup_fslmerge'))
    logfile.info('Setup for randomise.')
    logfile.info('Making a 4D data set by combining images')
    outdir = os.path.join(os.environ['hel'], 'graph_analyses',
                          'randomise_global_connectivity')
    outfilename = os.path.join(outdir, 'wgc_PairedT_4Dfile')
    mergefsl(logfile, make_file_list(subjectlist), outfilename)

if __name__ == '__main__':
    main()
