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

    for ss in subj_list:
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        
        deg_dir = os.path.join(os.environ['hel'], 'graph_analyses', ss, 'degrees')
        ijk_name = os.path.join(anat_dir,
                                '%s_gm_mask_frac_bin_ijk.txt' % ss)
        master_file = os.path.join(anat_dir,
                                   '%s_gm_mask_frac_bin.nii.gz' % ss)
        for i in range(1, 3):
            for thr in [.05, .1, .15, .2]:
                deg_name = 'task_sess_%s_%s.dens_%s.degrees.txt' % (i, ss, thr)
                deg_file = os.path.join(deg_dir, deg_name)
                gp.undump(ss, ijk_name, deg_file, deg_dir, master_file)
