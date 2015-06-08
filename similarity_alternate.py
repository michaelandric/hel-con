# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 21:25:56 2015

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

    n_vox = 157440
    n_subj = len(subj_list)

    tree_suff = 'maxq_tree.ijk_fnirted_MNI2mm.txt'
    for thresh_dens in [.05, .10, .15, .20]:

        btwn_mat = np.empty(n_vox*(n_subj*2))
        btwn_mat = btwn_mat.reshape(n_vox, n_subj*2)
        btwn_scores = np.empty((n_subj*(n_subj-1))/2.)

        fr = 0
        st = n_subj
        for session in range(1, 3):
            sess_mat = np.empty(n_vox*n_subj)
            sess_mat = sess_mat.reshape(n_vox, n_subj)
            sess_scores = np.empty((n_subj*(n_subj-1))/2.)
            for i, ss in enumerate(subj_list):
                mod_dir = os.path.join(top_dir, '%s/modularity' % ss)
                tree_name = os.path.join(mod_dir,
                                         'task_sess_%d_%s.dens_%s.%s' %
                                         (session, ss, thresh_dens, tree_suff))
                in_tree = np.loadtxt(tree_name)
                sess_mat[:, i] = in_tree
            for i, c in enumerate(combinations(range(n_subj), 2)):
                v1 = sess_mat[:, c[0]]
                v2 = sess_mat[:, c[1]]
                sess_scores[i] = normalized_mutual_info_score(v1, v2)
            sess_pref = 'within_session%d_dens_%s_nmi.txt' % \
                (session, thresh_dens)
            sess_fname = os.path.join(group_siml_dir, sess_pref)
            np.savetxt(sess_fname, sess_scores, fmt='%.4f')

            btwn_mat[:, fr:st]
            fr = fr + n_subj
            st = st + n_subj

        for i, c in enumerate(combinations(range(n_subj), 2)):
            v1 = btwn_mat[:, c[0]]
            v2 = btwn_mat[:, (c[1]+n_subj)]
            btwn_scores[i] = normalized_mutual_info_score(v1, v2)
        btwn_pref = 'between_dens_%s_nmi.txt' % thresh_dens
        btwn_fname = os.path.join(group_siml_dir, btwn_pref)
        np.savetxt(btwn_fname, btwn_scores, fmt='%.4f')
