#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 17:55:22 2015

@author: andric
"""

import os
from subprocess import call, STDOUT
from shlex import split

ss = 'hel4'

proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
wholet1 = os.path.join(anat_dir, 'T1_biascorr.nii.gz')
extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')
# epi_brain = "'%s/pb02_trim_despiked_%sr03+orig.[241]'" % (proc_dir, ss)
# epi_nii_pref = '%s/pb02_%s_regslice' % (proc_dir, ss)
# epi_nii_pref = '%s/pb01_%s_regslice' % (proc_dir, ss)
# epi = '%s.nii.gz' % epi_nii_pref
# epi_reg_out = os.path.join(anat_dir, 'flirt4_bbr_epi2anat_%s_reg' % ss)
# epi_reg_out = os.path.join(anat_dir, 'flirt3_nobbr_epi2anat_%s_reg' % ss)
wm_edge = os.path.join(anat_dir, 'epi2anat_%s_reg_fast_wmedge.nii.gz' % ss)

f = open('%s/stdout_files/stdout_from_applywarp_tests.txt' % anat_dir, 'w')
# cmdargs = split('flirt -in %s -ref %s -dof 6 -cost bbr -wmseg %s \
#                 -omat %s.mat -o %s' %
#                 (epi, wholet1, wm_edge, epi_reg_out, epi_reg_out))
# cmdargs = split('flirt -in %s -ref %s -wmseg %s \
#                -omat %s.mat -o %s' %
#                (epi, extrt1, wm_edge, epi_reg_out, epi_reg_out))
top_dir = '%s/graph_analyses' % os.environ['hel']
mod_dir = os.path.join(top_dir, '%s/modularity' % ss)
epi_nii_pref = os.path.join(mod_dir, 'task_sess_%d_%s.dens_%s.maxq_tree.ijk' %
                            (2, ss, '0.05'))
in_fl = '%s.nii.gz' % epi_nii_pref
premat = os.path.join(anat_dir, '%s_GMmask_frac_bin_flirted.mat' % ss)
interp = 'nn'
out_fl = os.path.join(anat_dir,
                      'flirttest_task_sess_%d_%s.dens_%s.maxq_tree.ijk' %
                      (2, ss, '0.05'))
cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s --interp=%s' %
                (in_fl, extrt1, out_fl, premat, interp))
call(cmdargs, stdout=f, stderr=STDOUT)

fn_coef = os.path.join(anat_dir, 'T1_to_MNI_nonlin_coeff.nii.gz')
out_fn = os.path.join(anat_dir,
                      'fnirttest_task_sess_%d_%s.dens_%s.maxq_tree.ijk' %
                      (2, ss, '0.05'))
cmdargs2 = split('applywarp -i %s \
                 -r %s/data/standard/MNI152_T1_2mm.nii.gz -o %s \
                 -w %s --interp=%s' %
                 ('%s.nii.gz' % out_fl, os.environ['FSLDIR'],
                  out_fn, fn_coef, interp))
call(cmdargs2, stdout=f, stderr=STDOUT)
f.close()
