# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 16:34:22 2016

Setting up 3dTcorr1D
@author: andric
"""

import os
import logging
import subprocess
from shlex import split


def bucket(workdir, subj_list, outname):
    logging.basicConfig(filename=os.path.join(workdir, 'bucket.log'),
                        level=logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)

    logging.info('work directory: {}'.format(workdir))
    tcorr_dir = os.path.join(os.environ['hel'], 'tcorr_group')

    input_set = []
    for ss in subj_list:
        fname = 'tcorr_prsn_{}_gm_mskd_Z_fnirted_MNI2mm.nii.gz'.format(ss)
        input_set.append(os.path.join(tcorr_dir, fname))
    input_set = ' '.join(input_set)

    cmd = split('3dbucket -prefix {} {}'.format(outname, input_set))
    logging.info('cmd: \n{}'.format(cmd))
    subprocess.call(cmd, stdout=subprocess.PIPE)


def tcorr1D(inbucket, outname):
    logging.basicConfig(filename=os.path.join(workdir, '3dTcorr1D.log'),
                    level=logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)

    logging.info('doing 3dTcorr1D')
    scores = os.path.join(os.environ['hel'], 'questions', 'usable_scores.txt')
    cmd = split('3dTcorr1D -prefix {} {} {}'.format(outname, inbucket, scores))
    logging.info('cmd: \n{}'.format(cmd))
    subprocess.call(cmd, stdout=subprocess.PIPE)



if __name__ == '__main__':
    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]
    workdir = os.path.join(os.environ['hel'], 'graph_analyses/behav_correlate')

    outbucket = os.path.join(workdir, 'tcorr_prsn_gm_mskd_Z_bucket')
    bucket(workdir, subj_list, outbucket)

    outcorr = os.path.join(workdir, 'tcorr_prsn_gm_mskd_Z_corr_with_behav')
    tcorr1D('{}+tlrc.'.format(outbucket), outcorr)
