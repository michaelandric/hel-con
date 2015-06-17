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
    mask_dir = '%s/group_anat' % (os.environ['hel'])
    mask_n = 'group_avg_gm_mask_frac_bin_fnirted_MNI2mm_thr0.34.nii.gz'
    mask_fname = os.path.join(mask_dir, mask_n)
    for ss in subj_list:
        mod_dir = os.path.join(top_dir, '%s/modularity' % ss)
        st_odir = os.path.join(mod_dir, 'stdout_dir')
        if not os.path.exists(st_odir):
            os.makedirs(st_odir)
        for session in range(1, 3):
            for thresh_dens in [.05, .10, .15, .20]:
                best_tree_name = 'task_sess_%d_%s.dens_%s.maxq_tree' % \
                    (session, ss, thresh_dens)
                in_fn_pref = '%s.ijk_fnirted_MNI2mm' % best_tree_name
                in_fn = os.path.join(mod_dir, '%s.nii.gz' % in_fn_pref)
                out_fname = os.path.join(mod_dir, '%s.txt' % in_fn_pref)
                gp.maskdump(st_odir, mask_fname, in_fn, out_fname)
