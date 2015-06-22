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
                            'graph_analyses', 'group_modularity')
mod_dir = os.path.join(grp_conn_dir, 'modularity_iters')

if __name__ == '__main__':

    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    for thresh_dens in [.05, .10, .15, .20]:
        gr = ge.Graphs('group', 'agreement_stuff',
                       thresh_dens, grp_conn_dir)
        q_fname = 'task_2sess_dens_%s.Qval' % thresh_dens
        qval, iter_max = gr.max_q(os.path.join(mod_dir, q_fname))
        trees_fname = 'task_2sess_dens_%s.trees' % thresh_dens
        trees = np.loadtxt(os.path.join(mod_dir, trees_fname))
        best_tree = trees[:, iter_max]+1
        best_tree_fname = 'task_2sess_dens_%s.maxq_tree' % thresh_dens
        np.savetxt(os.path.join(mod_dir, best_tree_fname),
                   best_tree, fmt='%i')
