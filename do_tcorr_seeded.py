# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 16:34:22 2016.

Re-mod with intra-subject corr from regions
May 17 2016

Setting up 3dTcorr1D
@author: andric
"""

import os
from setlog import setup_log
from shlex import split
from subprocess import call
from subprocess import PIPE
from subprocess import STDOUT


def bucket(log, workdir, subj_list, outname):
    """Bucket individuals' tcorr values into one dataset."""
    log.info('Doing bucket...')
    log.info('work directory: %s', workdir)

    tcorr_dir = os.path.join(os.environ['hel'], 'tcorr_group')
    input_set = []
    for subj in subj_list:
        fname = 'tcorr_prsn_{}_gm_mskd_Z_fnirted_MNI2mm.nii.gz'.format(subj)
        input_set.append(os.path.join(tcorr_dir, fname))
    input_set = ' '.join(input_set)

    cmd = split('3dbucket -prefix {} {}'.format(outname, input_set))
    log.info('cmd: \n%s', cmd)
    call(cmd, stdout=PIPE, stderr=STDOUT)


def tcorr(log, inbucket, seedfile, outname):
    """Correlate func data against seed."""
    log.info('Doing 3dTcorr1D...')
    cmd = split('3dTcorr1D -prefix {} {} {}'.format(outname, inbucket,
                                                    seedfile))
    log.info('cmd: \n%s', cmd)
    call(cmd, stdout=PIPE, stderr=STDOUT)


if __name__ == '__main__':
    SUBJECTLIST = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]
    WORKDIR = os.path.join(os.environ['hel'], 'graph_analyses/behav_correlate')
    LOGFILE = setup_log(os.path.join(WORKDIR, 'calc_mask'))
    LOGFILE.info('Doing tcorr1D')

    INBUCKET = os.path.join(WORKDIR, 'tcorr_prsn_gm_mskd_Z_bucket')
    SEED_PREFS = ['lh_highlevel', 'lh_ttg', 'lh_vis_ctx']
    for seed in SEED_PREFS:
        outcorr = os.path.join(WORKDIR, 'wgc_sess_1_{}_corr')
        tcorr(LOGFILE, '{}+tlrc.'.format(INBUCKET),
              os.path.join(WORKDIR, '{}.txt'.format(seed)), outcorr)
