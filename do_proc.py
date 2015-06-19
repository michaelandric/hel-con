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

    top_dir = '%s/graph_analyses' % os.environ['hel']
#    mask_dir = '%s/group_anat' % (os.environ['hel'])
#    mask_n = 'group_avg_gm_mask_frac_bin_fnirted_MNI4mm_thr0.34.nii.gz'
#    mask_fname = os.path.join(mask_dir, mask_n)
    for ss in subj_list:
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        conn_dir = os.path.join(top_dir, '%s/global_connectivity' % ss)
        st_odir = os.path.join(conn_dir, 'stdout_dir')
        if not os.path.exists(st_odir):
            os.makedirs(st_odir)
        for session in range(1, 3):
            corr_z_pref = 'avg_corrZ_task_sess_%s_%s' % (session, ss)
            corr_z_fname = os.path.join(conn_dir, corr_z_pref)
            ijk_name = os.path.join(anat_dir,
                                    '%s_gm_mask_frac_bin_ijk.txt' % ss)
            master_file = os.path.join(anat_dir,
                                       '%s_gm_mask_frac_bin.nii.gz' % ss)
            gp.undump(ss, ijk_name, corr_z_fname, conn_dir,
                      master_file)
