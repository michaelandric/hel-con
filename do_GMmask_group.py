# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 12:27:17 2015
Make group gray matter mask
@author: andric
"""

import os
import general_procedures as gp
from shlex import split
from subprocess import call, STDOUT


def calc_mask_thr(stdout_dir, mask_name, thresh, out_name):
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_epireg.txt' % stdout_dir, 'w')
    cmdargs = split("3dcalc -a %s -expr 'ispositive(a-%s)' \
        -prefix %s" % (mask_name, thresh, out_name))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    grp_dir = '%s/group_anat' % os.environ['hel']
    if not os.path.exists(grp_dir):
        os.makedirs(grp_dir)

    subj_masks = []
    for ss in subj_list:
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        ss_msk = '%s_gm_mask_frac_bin_fnirted_MNI2mm.nii.gz' % ss
        subj_masks.append(os.path.join(anat_dir, ss_msk))
    subj_masks_strlist = ' '.join(subj_masks)
    grp_msk_pref = os.path.join(grp_dir,
                                'group_avg_gm_mask_frac_bin_fnirted_MNI2mm')
    grp_msk_fname = '%s.nii.gz' % grp_msk_pref
    gp.avgepis('group', subj_masks_strlist, grp_dir, grp_msk_fname)

    st_out_dir = os.path.join(grp_dir, 'stdout_dir')
    thr = .34
    out_mask_thr_name = '%s_thr%s.nii.gz' % (grp_msk_pref, thr)
    calc_mask_thr(st_out_dir, grp_msk_fname, thr, out_mask_thr_name)
