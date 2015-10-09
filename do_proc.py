# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:55:40 2015

@author: andric
"""

import os
import numpy as np
import general_procedures as gp


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    graph_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    t_dict = {'vals': 'float', 'lag': 'short'}

    for ss in subj_list:
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        conn_dir = os.path.join(graph_dir, '%s/global_connectivity' % ss)
        st_odir = os.path.join(conn_dir, 'stdout_dir')
        if not os.path.exists(st_odir):
            os.makedirs(st_odir)
        for lb in t_dict:
            corr_z_pref = 'ccf_%s_out_%s_gm_mskd' % (lb, ss)
            corr_z_fname = os.path.join(conn_dir, corr_z_pref)
            ijk_name = os.path.join(anat_dir,
                                    '%s_gm_mask_frac_bin_ijk.txt' % ss)
            master_file = os.path.join(anat_dir,
                                       '%s_gm_mask_frac_bin.nii.gz' % ss)
            gp.undump(ss, ijk_name, corr_z_fname, conn_dir,
                      master_file, t_dict[lb])
