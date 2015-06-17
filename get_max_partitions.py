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

    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    top_dir = '%s/graph_analyses' % os.environ['hel']
    for ss in subj_list:
        proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
        mod_dir = os.path.join(top_dir, '%s/modularity' % ss)

        for session in range(1, 3):
            ts_name = os.path.join(proc_dir,
                                   'task_sess_%d_%s_gm_mskd.txt' %
                                   (session, ss))
            graph_dir = os.path.join(top_dir, '%s/graphs' % ss)
            for thresh_dens in [.05, .10, .15, .20]:
                gr = ge.Graphs(ss, ts_name, thresh_dens, graph_dir)
                q_fname = 'task_sess_%d_%s.dens_%s.Qval' % \
                    (session, ss, thresh_dens)
                qval, iter_max = gr.max_q(os.path.join(mod_dir, q_fname))
                trees_fname = 'task_sess_%d_%s.dens_%s.trees' % \
                    (session, ss, thresh_dens)
                trees = np.loadtxt(os.path.join(mod_dir, trees_fname))
                best_tree = trees[:, iter_max]+1
                best_tree_fname = 'task_sess_%d_%s.dens_%s.maxq_tree' % \
                    (session, ss, thresh_dens)
                np.savetxt(os.path.join(mod_dir, best_tree_fname),
                           best_tree, fmt='%i')
