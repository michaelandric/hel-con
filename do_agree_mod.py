# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 14:53:20 2015

@author: andric
"""

import os
import sys
import time
import numpy as np
import bct


if __name__ == '__main__':

    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    top_dir = '%s/graph_analyses' % os.environ['hel']
    if not os.path.exists(top_dir):
        print 'Where is the top_dir?'
        sys.exit(1)
    group_dir = os.path.join(top_dir, 'group_agreement')
    if not os.path.exists(group_dir):
        os.makedirs(group_dir)

    nvox = 157440
    n_subj = len(subj_list)
    tree_suff = 'maxq_tree.ijk_fnirted_MNI2mm.txt'

    for thresh_dens in [.05, .10, .15, .20]:
        for session in range(1, 3):
            print 'Doing Thresh %s Session %s' % (thresh_dens, session)
            print time.ctime()
            group_mat = np.empty(nvox*n_subj).reshape(nvox, n_subj)
            for i, ss in enumerate(subj_list):
                mod_dir = os.path.join(top_dir, '%s/modularity' % ss)
                tree_name = os.path.join(mod_dir,
                                         'task_sess_%d_%s.dens_%s.%s' %
                                         (session, ss, thresh_dens, tree_suff))
                tree = np.loadtxt(tree_name)
                group_mat[:, i] = tree
            out_fname = os.path.join(group_dir,
                                     'group_task_sess_%d.dens_%s.%s' %
                                     (session, thresh_dens, tree_suff))
            np.savetxt(out_fname, group_mat, fmt='%i')

            """Below was failed attempts at running
            all of this in python.
            Was getting memory error doing bct.agreement

            print 'Group mat made. Getting agreement...'
            print time.ctime()
            ag = bct.agreement(group_mat, buffsz=150)
            print 'Agreement found. Getting modularity...'
            print time.ctime()
            ci, q = bct.modularity_louvain_und(ag)
            print 'Modularity soltion done.'
            print time.ctime()
            out_name = 'group_agr_mod_task_sess_%d_dens_%s' % \
                (session, thresh_dens)
            out_fname = os.path.join(group_dir, out_name)
            np.savetxt('%s.tree' % out_fname, ci, fmt='%i')
            np.savetxt('%s.Qval' % out_fname, q, fmt='%.4f')
            """
