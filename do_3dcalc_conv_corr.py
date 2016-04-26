# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 18:56:36 2016

@author: andric
"""

import os
import logging
import subprocess
from shlex import split


def conv_corr_to_t(workdir, input, outname):
    logging.basicConfig(filename=os.path.join(workdir, 'conv_corr_to_t.log'),
                        level=logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)

    logging.info('work directory: {}'.format(workdir))
    cmd = split("3dcalc -a {} -expr 'a / (sqrt(((1-a^2) / (18-2))))' -prefix {}".format(input, outname))
    subprocess.call(cmd, stdout=subprocess.PIPE)



if __name__ == '__main__':

    workdir = os.path.join(os.environ['hel'], 'graph_analyses/behav_correlate')
    infile = os.path.join(workdir, 'tcorr_prsn_gm_mskd_Z_corr_with_behav+tlrc.')
    outf = os.path.join(workdir, 'tcorr_prsn_gm_mskd_Z_corr_with_behav_tvals')
    conv_corr_to_t(workdir, infile, outf)
    
    
