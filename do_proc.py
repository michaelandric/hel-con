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
    mask = os.path.join(os.environ['hel'], 'group_anat',
                        'MNI152_T1_2mm_brain_mask_dil1.nii.gz')

    for ss in subj_list:
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        conn_dir = os.path.join(graph_dir, '%s/global_connectivity' % ss)
        st_odir = os.path.join(conn_dir, 'stdout_dir')
        if not os.path.exists(st_odir):
            os.makedirs(st_odir)
        for lb in t_dict:
            epi_nii_pref = os.path.join(conn_dir,
                                        'ccf_%s_out_%s_gm_mskd.ijk' % (lb, ss))
            out_fn = '%s_fnirted_MNI2mm' % epi_nii_pref
            gp.maskdump(conn_dir, mask, '%s.nii.gz' % out_fn,
                        '%s.txt' % out_fn)
