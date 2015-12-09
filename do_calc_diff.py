# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 16:10:25 2015

@author: andric
"""

import os
import logging
from shlex import split
from subprocess import call

def calc(input1, input2, outpref):
    """
    3dcalc -a Corr_subj01R+tlrc -expr 'atanh(a)' -prefix Corr_subj01_Z
    """
    logging.info('Doing 3dcalc for %s' % outpref)
    cmd = split("3dcalc -a %s -b %s -expr 'a-b' -prefix %s" %
                (input1, input2, outpref))
    call(cmd)


ava_dir = os.path.join(os.environ['hel'], 'ava')
logging.basicConfig(filename='%s/calc_diff.log' % ava_dir, level=logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

for thr in [.05, .1, .15, .2]:
    ava1 = ('%s/ava_smth_deg_corr_sess_1_dens_%s_out.ijk_Z+tlrc' %
            (ava_dir, thr))
    ava2 = ('%s/ava_smth_deg_corr_sess_2_dens_%s_out.ijk_Z+tlrc' %
            (ava_dir, thr))
    outpref = ('%s/ava_smth_deg_corr_diff_dens_%s_out.ijk_Z' % (ava_dir, thr))
    calc(ava1, ava2, outpref)

logging.info('3dcalc done.')
