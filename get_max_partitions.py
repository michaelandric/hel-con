# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:52:58 2015
lil code to write out the partition
corresponding to maximum modularity value

@author: andric
"""

import os
import numpy as np
import graph_evals as ge

grp_conn_dir = os.path.join(os.environ['hel'],
                            'graph_analyses', 'group_modularity_thr0.5msk')
mod_dir = grp_conn_dir

if __name__ == '__main__':

    for thresh_dens in [.05, .10, .15, .20]:
        gr = ge.Graphs('group', 'agreement_stuff',
                       thresh_dens, grp_conn_dir)

        qsuff = 'agreement.nothr.Qval'
        pref = 'group_task_2sess'
        q_fname = '%s_dens_%s.%s' % (pref, thresh_dens, qsuff)
        qval, iter_max = gr.max_q(os.path.join(mod_dir, q_fname))
        tsuff = 'agreement.nothr.mod_arr'
        trees_fname = '%s_dens_%s.%s' % (pref, thresh_dens, tsuff)
        trees = np.loadtxt(os.path.join(mod_dir, trees_fname))
        best_tree = trees[:, iter_max]+1
        best_tree_fname = '%s_dens_%s.maxq_tree' % (pref, thresh_dens)
        np.savetxt(os.path.join(mod_dir, best_tree_fname),
                   best_tree, fmt='%i')
