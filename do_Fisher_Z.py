# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 16:04:36 2015

@author: andric
"""

import os
import logging
from shlex import split
from subprocess import call


def fisher_Z(inpref):
    """
    3dcalc -a Corr_subj01R+tlrc -expr 'atanh(a)' -prefix Corr_subj01_Z
    """
    logging.info('Doing fisher_Z for %s' % inpref)
    cmd = split("3dcalc -a %s+tlrc -expr 'atanh(a)' -prefix %s_Z" % (inpref, inpref))
    call(cmd)


ava_dir = os.path.join(os.environ['hel'], 'ava')
logging.basicConfig(filename='%s/fisher_Z.log' % ava_dir, level=logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

for thr in [.05, .1, .15, .2]:
    for r in range(1, 3):
        ava_pref = ('%s/ava_smth_deg_corr_sess_%s_dens_%s_out.ijk' %
                    (ava_dir, r, thr))
        fisher_Z(ava_pref)
logging.info('fisher_Z done.')
