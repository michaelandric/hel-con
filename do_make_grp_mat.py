# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:57:27 2015

revision April 2016 for subrun modularity

@author: andric
"""

import os
import numpy as np

top_dir = (os.environ['hel'], 'graph_analyses')
nvox = 20071
suff = 'maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt'

if __name__ == '__main__':
    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]

    thresh_dens = .15
    for session in ['first', 'second']:
        grp_mat = np.zeros(nvox*len(subj_list))
        grp_mat = grp_mat.reshape(nvox, len(subj_list))
        for i, ss in enumerate(subj_list):
            mod_dir = os.path.join(top_dir, ss, 'subrun_modularity')
            f_name = 'task_{}_{}.dens_{}.{}'.format(
                session, ss, thresh_dens, suff)
            in_fname = os.path.join(mod_dir, f_name)
            grp_mat[:, i] = np.loadtxt(in_fname)
        out_f_name = 'group_task_sess_{}.dens_{}.{}'.format(
            session, thresh_dens, suff)
        out_f = os.path.join(top_dir,
                             'subrun_group_modularity_thr0.5msk', out_f_name)
        np.savetxt(out_f, grp_mat, fmt='%i')
