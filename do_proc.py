# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:55:40 2015

@author: andric
"""

import os
import general_procedures as gp


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    """
    mask_dir = '%s/group_anat' % (os.environ['hel'])
    mask_pref = 'group_avg_gm_mask_frac_bin_fnirted_MNI4mm_thr0.5'
    mask_fname = os.path.join(mask_dir, '%s.nii.gz' % mask_pref)
    ijk_fname = os.path.join(mask_dir, '%s_ijk.txt' % mask_pref)
    """
    mask_dir = '%s/data/standard' % os.environ['FSLDIR']
    mask_fname = os.path.join(mask_dir, 'MNI152_T1_2mm_brain_mask_dil1.nii.gz')

    in_suff = 'ijk_fnirted_MNI2mm.nii.gz'
    out_suff = 'ijk_fnirted_MNI2mm.txt'

    for ss in subj_list:
        conn_dir = os.path.join(os.environ['hel'], ss, 'global_connectivity')
        st_odir = os.path.join(conn_dir, 'stdout_dir')

        for session in range(1, 3):
            in_pref = 'avg_corrZ_task_sess_%d_%s' % (session, ss)
            in_fname = os.path.join(conn_dir, '%s.%s' % (in_pref, in_suff))
            out_fname = os.path.join(conn_dir, '%s.%s' % (in_pref, out_suff))
            gp.maskdump(st_odir, mask_fname, in_fname, out_fname)
