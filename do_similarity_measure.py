# -*- coding: utf-8 -*-
"""
Created on Sun May 31 18:12:20 2015

@author: andric
"""

import os
import sys
import numpy as np
from itertools import combinations
from sklearn.metrics import normalized_mutual_info_score

if __name__ == '__main__':

    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    top_dir = '%s/graph_analyses' % os.environ['hel']
    if not os.path.exists(top_dir):
        print 'What is going on here?'
        print 'Where is the top_dir?'
        sys.exit(1)
    group_Q_dir = os.path.join(top_dir, 'group_modularity')
    if not os.path.exists(group_Q_dir):
        os.makedirs(group_Q_dir)

    niter = 100

    for thresh_dens in [.05, .10, .15, .20]:
        for i, ss in enumerate(subj_list):
            simil_dir = os.path.join(top_dir, '%s/similarity' % ss)
            if not os.path.exists(simil_dir):
                os.makedirs(simil_dir)
            proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
            mod_dir = os.path.join(top_dir, '%s/modularity' % ss)
            for session in range(1, 3):
                tree_fname = os.path.join(mod_dir,
                                          'task_sess_%d_%s.dens_%s.trees' %
                                          (session, ss, thresh_dens))
                tree_file = np.loadtxt(tree_fname)
                simil_scores = np.empty((niter*(niter-1)) / 2.)
                for i, c in enumerate(combinations(range(niter), 2)):
                    v1 = tree_file[:, c[0]]
                    v2 = tree_file[:, c[1]]
                    simil_scores[i] = normalized_mutual_info_score(v1, v2)
                simil_name = 'within_task_sess_%d_%s.dens_%s_nmi.txt' % \
                    (session, ss, thresh_dens)
                simil_fname = os.path.join(simil_dir, simil_name)
                np.savetxt(simil_fname, simil_scores, fmt='%.4f')

            simil_scores_b = np.empty((niter*(niter-1)) / 2.)
            trees_1_name = os.path.join(mod_dir,
                                        'task_sess_%d_%s.dens_%s.trees' %
                                        (1, ss, thresh_dens))
            trees_sess1 = np.loadtxt(trees_1_name)
            trees_2_name = os.path.join(mod_dir,
                                        'task_sess_%d_%s.dens_%s.trees' %
                                        (2, ss, thresh_dens))
            trees_sess2 = np.loadtxt(trees_2_name)
            for i, c in enumerate(combinations(range(niter), 2)):
                v1 = trees_sess1[:, c[0]]
                v2 = trees_sess2[:, c[1]]
                simil_scores_b[i] = normalized_mutual_info_score(v1, v2)
            simil_b_name = 'between_tasks_%s.dens_%s_nmi.txt' % \
                (ss, thresh_dens)
            simil_b_fname = os.path.join(simil_dir, simil_b_name)
            np.savetxt(simil_b_fname, simil_scores_b, fmt='%.4f')
