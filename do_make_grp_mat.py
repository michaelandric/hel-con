# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:57:27 2015

@author: andric
"""

import os
import numpy as np

top_dir = '%s/graph_analyses' % os.environ['hel']
nvox = 262245
suff = 'maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt'

if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    top_dir = '%s/graph_analyses' % os.environ['hel']

    suff = 'ijk_fnirted_MNI2mm.txt'
    for clst in [2, 3]:
        # already did clst1
        grp_mat = np.zeros(nvox*len(subj_list))
        grp_mat = grp_mat.reshape(nvox, len(subj_list))
        for i, ss in enumerate(subj_list):
            conn_dir = os.path.join(top_dir, '%s/global_connectivity' % ss)
            f_name = '%s_Clust_msk_glob_conn_knnward_clst%d.%s' % \
                     (ss, clst, suff)
            in_fname = os.path.join(conn_dir, f_name)
            grp_mat[:, i] = np.loadtxt(in_fname)
        out_f_name = 'group_Clust_msk_glob_conn_knnward_clst%d' % clst
        out_f = os.path.join(top_dir,
                             'group_global_connectivity', out_f_name)
        np.savetxt(out_f, grp_mat, fmt='%i')
