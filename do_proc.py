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

    graph_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    t_dict = {'vals': 'float', 'lag': 'short'}

    mask_dir = '%s/group_anat' % (os.environ['hel'])
    mask_n = 'group_avg_gm_mask_frac_bin_fnirted_MNI4mm_thr0.5.nii.gz'
    mask_fname = os.path.join(mask_dir, mask_n)

    ava_dir = os.path.join(os.environ['hel'], 'ava')
    out_res_suff = 'ijk_fnirted_MNI4mm_thr0.5'
    for ss in subj_list:
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        st_odir = os.path.join(ava_dir, 'stdout_dir')
        if not os.path.exists(st_odir):
            os.makedirs(st_odir)
        for i in range(1, 3):
            epi_nii_pref = os.path.join(ava_dir,
                                        'ava_smth_task_sess_%s_%s_gm_mskd.txt' %
                                        (i, ss))
            in_resamp_pref = os.path.join(ava_dir,
                                          '%s.ijk_fnirted_MNI2mm' % epi_nii_pref)
            out_resamp_pref = os.path.join(ava_dir,
                                           '%s.%s' % (epi_nii_pref, out_res_suff))
            gp.resamp_with_master(ava_dir, '%s.nii.gz' % in_resamp_pref,
                                  mask_fname, '%s.nii.gz' % out_resamp_pref)
            out_fname = os.path.join(ava_dir, '%s.txt' % out_resamp_pref)
            gp.maskdump(st_odir, mask_fname,
                        '%s.nii.gz' % out_resamp_pref, out_fname)