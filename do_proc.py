# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:55:40 2015

@author: andric
"""

import os
import general_procedures as gp


if __name__ == '__main__':
    subj_list = []
    for i in range(2, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    mask_dir = '%s/group_anat' % (os.environ['hel'])
    mask_pref = 'group_avg_gm_mask_frac_bin_fnirted_MNI4mm_thr0.5'
    mask_fname = os.path.join(mask_dir, '%s.nii.gz' % mask_pref)
    ijk_fname = os.path.join(mask_dir, '%s_ijk.txt' % mask_pref)

    grp_conn_dir = os.path.join(os.environ['hel'],
                                'graph_analyses', 'group_modularity_thr0.5msk')

    st_odir = os.path.join(grp_conn_dir, 'stdout_dir')
    if not os.path.exists(st_odir):
        os.makedirs(st_odir)

    pref = 'group_task_diff_component'
    for thresh_dens in [.05, .10, .15, .20]:
        tree_fname = '%s_dens_%s.vals' % (pref, thresh_dens)
        best_tree_fname = os.path.join(grp_conn_dir, tree_fname)
        master_file = mask_fname
        gp.undump('group', ijk_fname, best_tree_fname, grp_conn_dir,
                  master_file)
