# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:55:40 2015

@author: andric
"""

import os
import general_procedures as gp


if __name__ == '__main__':
    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]

    thresh_dens = .15
    top_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    mask_dir = os.path.join(os.environ['hel'], 'group_anat')
    mask_n = 'group_avg_gm_mask_frac_bin_fnirted_MNI4mm_thr0.5.nii.gz'
    mask_fname = os.path.join(mask_dir, mask_n)
    for ss in subj_list:
        anat_dir = os.path.join(os.environ['hel'], ss,
                                'volume.{}.anat'.format(ss))
        mod_dir = os.path.join(top_dir, ss, 'subrun_modularity')
        st_odir = os.path.join(mod_dir, 'stdout_dir')
        if not os.path.exists(st_odir):
            os.makedirs(st_odir)

        ijk_name = os.path.join(anat_dir,
                                '{}_gm_mask_frac_bin_ijk.txt'.format(ss))
        master_file = os.path.join(anat_dir,
                                   '{}_gm_mask_frac_bin.nii.gz'.format(ss))

        for session in ['first', 'second']:
            tree_name = os.path.join(mod_dir,
                                     'task_{}_{}.dens_{}.maxq_tree'.format(
                                     session, ss, thresh_dens))
            gp.undump(ss, ijk_name, tree_name, mod_dir, master_file, 'short')