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
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def bucket(log, subj_list, outname):
    """Bucket individuals' values into one dataset."""
    log.info('Doing bucket...')
    input_set = []
    suffx = 'ijk_fnirted_MNI2mm.nii.gz'
    for subj in subj_list:
        dat_dir = os.path.join(os.environ['hel'], 'graph_analyses',
                               subj, 'global_connectivity')
        fname = 'avg_corrZ_task_sess_2_{}.{}'.format(subj, suffx)
        input_set.append(os.path.join(dat_dir, fname))
    input_set = ' '.join(input_set)
    cmd = split('3dbucket -prefix {} {}'.format(outname, input_set))
    log.info('cmd: \n%s', cmd)
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def tcorr(log, inbucket, seedfile, outname):
    """Correlate func data against seed."""
    log.info('Doing 3dTcorr1D...')
    mask = os.path.join(os.environ['FSLDIR'], 'data/standard/',
                        'MNI152_T1_2mm_brain_mask_dil1.nii.gz')
    cmd = split('3dTcorr1D -prefix {} \
                -mask {} {} {}'.format(outname, mask, inbucket, seedfile))
    log.info('cmd: \n%s', cmd)
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def conv_corr_to_t(log, workdir, inputf, outname):
    """Convert correlation value to t value."""
    log.info('Doing convert corr to t')
    log.info('work directory: {}'.format(workdir))
    cmd = split("3dcalc -a {} -expr 'a / (sqrt(((1-a^2) / (18-2))))' \
                -prefix {}".format(inputf, outname))
    log.info('cmd: \n%s', cmd)
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Main call to do functions."""
    workdir = os.path.join(os.environ['hel'], 'graph_analyses/behav_correlate')
    logfile = setup_log(os.path.join(workdir, 'tcorr_conv_corr_to_t'))
    logfile.info('Doing tcorr1D')
    inbucket = os.path.join(workdir, 'avg_corrZ_task_diff_bucket')
    seed_prefs = ['lh_highlevel', 'lh_ttg', 'lh_vis_ctx']
    for seed in seed_prefs:
        outcorr = os.path.join(workdir, 'wgc_diff_{}_corr'.format(seed))
        tcorr(logfile, '{}+tlrc.'.format(inbucket),
              os.path.join(workdir, '{}.txt'.format(seed)), outcorr)

        out_conv_corr = '{}_tvals'.format(outcorr)
        conv_corr_to_t(logfile, workdir, '{}+tlrc'.format(outcorr),
                       out_conv_corr)

if __name__ == '__main__':
    main()
