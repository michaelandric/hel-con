# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 21:49:46 2015

@author: andric
"""

import os
import sys
import numpy as np
from itertools import combinations
from sklearn.metrics import normalized_mutual_info_score


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


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
    group_siml_dir = os.path.join(top_dir, 'group_similarity')
    if not os.path.exists(group_siml_dir):
        os.makedirs(group_siml_dir)

    niter = 100
    n_unique = (niter*(niter-1)) / 2.
    n_vox = 157440
    n_subj = len(subj_list)

    tree_suff = 'maxq_tree.ijk_fnirted_MNI2mm.txt'
    for thresh_dens in [.05, .10, .15, .20]:
        sess1_mat = np.empty(n_vox*len(subj_list))
        sess1_mat = sess1_mat.reshape(n_vox, len(subj_list))
        sess2_mat = np.empty(n_vox*len(subj_list))
        sess2_mat = sess2_mat.reshape(n_vox, len(subj_list))
        sess1_scores = np.empty((n_subj*(n_subj-1))/2.)
        sess2_scores = np.empty((n_subj*(n_subj-1))/2.)
        btwn_scores = np.empty((n_subj*(n_subj-1))/2.)
        for i, ss in enumerate(subj_list):
            mod_dir = os.path.join(top_dir, '%s/modularity' % ss)
            tree1_name = os.path.join(mod_dir,
                                      'task_sess_%d_%s.dens_%s.%s' %
                                      (1, ss, thresh_dens, tree_suff))
            in_tree1 = np.loadtxt(tree1_name)
            sess1_mat[:, i] = in_tree1

            tree2_name = os.path.join(mod_dir,
                                      'task_sess_%d_%s.dens_%s.%s' %
                                      (2, ss, thresh_dens, tree_suff))
            in_tree2 = np.loadtxt(tree2_name)
            sess2_mat[:, i] = in_tree2

        for i, c in enumerate(combinations(range(n_subj), 2)):
            v1 = sess1_mat[:, c[0]]
            v2 = sess1_mat[:, c[1]]
            sess1_scores[i] = normalized_mutual_info_score(v1, v2)
            v1 = sess2_mat[:, c[0]]
            v2 = sess2_mat[:, c[1]]
            sess2_scores[i] = normalized_mutual_info_score(v1, v2)
            v1 = sess1_mat[:, c[0]]
            v2 = sess2_mat[:, c[1]]
            btwn_scores[i] = normalized_mutual_info_score(v1, v2)
        sess1_pref = 'within_session%d_dens_%s_nmi.txt' % (1, thresh_dens)
        sess1_fname = os.path.join(group_siml_dir, sess1_pref)
        sess2_pref = 'within_session%d_dens_%s_nmi.txt' % (2, thresh_dens)
        sess2_fname = os.path.join(group_siml_dir, sess2_pref)
        btwn_pref = 'between_dens_%s_nmi.txt' % thresh_dens
        btwn_fname = os.path.join(group_siml_dir, btwn_pref)
        np.savetxt(sess1_fname, sess1_scores, fmt='%.4f')
        np.savetxt(sess2_fname, sess2_scores, fmt='%.4f')
        np.savetxt(btwn_fname, btwn_scores, fmt='%.4f')
