#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 17:55:22 2015

@author: andric
"""

import os
from subprocess import call, STDOUT
from shlex import split

ss = 'hel2'

proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
wholet1 = os.path.join(anat_dir, 'T1_biascorr.nii.gz')
extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')
epi_brain = "'%s/pb02_trim_despiked_%sr03+orig.[241]'" % (proc_dir, ss)
# epi_nii_pref = '%s/pb02_%s_regslice' % (proc_dir, ss)
epi_nii_pref = '%s/pb01_%s_regslice' % (proc_dir, ss)
epi = '%s.nii.gz' % epi_nii_pref
# epi_reg_out = os.path.join(anat_dir, 'flirt4_bbr_epi2anat_%s_reg' % ss)
epi_reg_out = os.path.join(anat_dir, 'flirt3_nobbr_epi2anat_%s_reg' % ss)
wm_edge = os.path.join(anat_dir, 'epi2anat_%s_reg_fast_wmedge.nii.gz' % ss)

f = open('%s/stdout_from_flirt3_test.txt' % anat_dir, 'w')
# cmdargs = split('flirt -in %s -ref %s -dof 6 -cost bbr -wmseg %s \
#                 -omat %s.mat -o %s' %
#                 (epi, wholet1, wm_edge, epi_reg_out, epi_reg_out))
cmdargs = split('flirt -in %s -ref %s -wmseg %s \
                -omat %s.mat -o %s' %
                (epi, extrt1, wm_edge, epi_reg_out, epi_reg_out))
call(cmdargs, stdout=f, stderr=STDOUT)
f.close()
