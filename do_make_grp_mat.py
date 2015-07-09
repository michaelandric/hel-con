# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:57:27 2015

@author: andric
"""

import os
import numpy as np

top_dir = '%s/graph_analyses' % os.environ['hel']
nvox = 20071
suff = 'maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt'

if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    top_dir = '%s/graph_analyses' % os.environ['hel']

    for thresh_dens in [.05]:
        for session in range(1, 3):
            grp_mat = np.zeros(nvox*len(subj_list))
            grp_mat = grp_mat.reshape(nvox, len(subj_list))
            for i, ss in enumerate(subj_list):
                mod_dir = os.path.join(top_dir, '%s/modularity' % ss)
                f_name = 'task_sess_%s_%s.dens_%s.%s' % (session, ss,
                                                         thresh_dens, suff)
                in_fname = os.path.join(mod_dir, f_name)
                grp_mat[:, i] = np.loadtxt(in_fname)
            out_f_name = 'group_task_sess_%s.dens_%s.%s' % (session,
                                                            thresh_dens, suff)
            out_f = os.path.join(top_dir,
                                 'group_modularity_thr0.5msk', out_f_name)
            np.savetxt(out_f, grp_mat, fmt='%i')
