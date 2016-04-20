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


if __name__ == '__main__':

    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]

    top_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    for ss in subj_list:
        proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
        mod_dir = os.path.join(top_dir, ss, 'subrun_modularity')

        for r in [1, 3, 4, 6]:
            ts_name = os.path.join(proc_dir,
                                   'task_r0{}_{}_gm_mskd.txt'.format(r, ss))
            graph_dir = os.path.join(top_dir, ss, 'subrun_graphs')
            for thresh_dens in [.15]:
                pref = 'task_r0{}_{}.dens_{}'.format(r, ss, thresh_dens)
                gr = ge.Graphs(ss, ts_name, thresh_dens, graph_dir)
                q_fname = '{}.Qval'.format(pref)
                qval, iter_max = gr.max_q(os.path.join(mod_dir, q_fname))
                trees_fname = '{}.trees'.format(pref)
                trees = np.loadtxt(os.path.join(mod_dir, trees_fname))
                best_tree = trees[:, iter_max]+1
                best_tree_fname = '{}.maxq_tree'.format(pref)
                np.savetxt(os.path.join(mod_dir, best_tree_fname),
                           best_tree, fmt='%i')