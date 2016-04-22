# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:55:40 2015

@author: andric
"""

import os
import general_procedures as gp


if __name__ == '__main__':

    mask_dir = os.path.join(os.environ['hel'], 'group_anat')
    mask_pref = 'group_avg_gm_mask_frac_bin_fnirted_MNI4mm_thr0.5'
    mask_fname = os.path.join(mask_dir, '{}.nii.gz'.format(mask_pref))
    ijk_fname = os.path.join(mask_dir, '{}_ijk.txt'.format(mask_pref))

    grp_conn_dir = os.path.join(os.environ['hel'], 'graph_analyses',
                                'subrun_group_modularity_thr0.5msk')

    st_odir = os.path.join(grp_conn_dir, 'stdout_dir')
    if not os.path.exists(st_odir):
        os.makedirs(st_odir)

    thresh_dens = .15

    for session in ['first', 'second']:
        pref = 'group_task_sess_{}'.format(session)
        tree_fname = '{}.dens_{}.maxq_tree'.format(pref, thresh_dens)
        best_tree_fname = os.path.join(grp_conn_dir, tree_fname)
        master_file = mask_fname
        gp.undump('group', ijk_fname, best_tree_fname, grp_conn_dir,
                  master_file)
