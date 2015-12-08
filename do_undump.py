# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 14:07:18 2015

@author: andric
"""

import os
import general_procedures as gp

if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    ava_dir = os.path.join(os.environ['hel'], 'ava')
    anat_dir = os.path.join(os.environ['hel'], 'group_anat')

    ijk_name = os.path.join(anat_dir,
                            'group_avg_gm_mask_frac_bin_fnirted_MNI4mm_thr0.5_ijk.txt')
    master_file = os.path.join(anat_dir,
                               'group_avg_gm_mask_frac_bin_fnirted_MNI4mm_thr0.5.nii.gz')

    for thr in [.05, .1, .15, .2]:
        for r in range(1, 3):
            ava_name = 'ava_smth_deg_corr_sess_%s_dens_%s_out' % (r, thr)
            ava_file = os.path.join(ava_dir, ava_name)
            gp.undump('group', ijk_name, ava_file, ava_dir, master_file, 'float')