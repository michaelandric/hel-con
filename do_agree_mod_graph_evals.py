# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 12:09:08 2015

@author: andric
"""

import os
import numpy as np
import graph_evals as ge

niter = 100
grp_conn_dir = os.path.join(os.environ['hel'],
                            'graph_analyses', 'group_modularity')

mod_dir = os.path.join(grp_conn_dir, 'modularity_iters')
if not os.path.exists(mod_dir):
    os.makedirs(mod_dir)
trees_all_levl_dir = os.path.join(grp_conn_dir, 'hierarchy_trees')
if not os.path.exists(trees_all_levl_dir):
    os.makedirs(trees_all_levl_dir)

n_nodes = 23155

"""for thresh_dens in [.05, .10, .15, .20]:
    el_suff = 'dens_%s.agreement.thr.edgelist' % thresh_dens
    for session in range(1, 3):
        el_name = 'group_task_sess_%d.%s' % (session, el_suff)
        edg_list = os.path.join(grp_conn_dir, el_name)
        com = ge.CommunityDetect(edg_list)
        com.convert_graph()

        Qs = np.zeros(niter)
        nmods = np.zeros(niter)
        trees = np.zeros(n_nodes*niter).reshape(n_nodes, niter)
        hierar_suff = 'group_task_sess_%d.dens_%s.trees_hierarchy' % \
            (session, thresh_dens)
        for i in xrange(niter):
            print 'iter %d' % i
            hierarchy_tr_name = 'iter%d.%s' % (i, hierar_suff)
            hierarchy_tr_filename = os.path.join(trees_all_levl_dir,
                                                 hierarchy_tr_name)
            Qs[i] = com.get_modularity(hierarchy_tr_filename)
            tr, n_m = com.get_hierarchical(hierarchy_tr_filename)
            if len(tr) == trees.shape[0]-1:
                tr = np.append(tr, tr[len(tr)-1])
            trees[:, i] = tr
            nmods[i] = n_m
        Qs_outname = 'task_sess_%d.dens_%s.Qval' % \
            (session, thresh_dens)
        np.savetxt(os.path.join(mod_dir, Qs_outname), Qs, fmt='%.4f')
        trees_outname = 'task_sess_%ddens_%s.trees' % \
            (session, thresh_dens)
        np.savetxt(os.path.join(mod_dir, trees_outname),
                   trees, fmt='%i')
        nmods_outname = 'task_sess_%d.dens_%s.nmods' % \
            (session, thresh_dens)
        np.savetxt(os.path.join(mod_dir, nmods_outname),
                   nmods, fmt='%i')
        bin_file = '%s.bin' % edg_list
        os.remove(bin_file)"""

for thresh_dens in [.05, .10, .15, .20]:
    el_suff = 'dens_%s.agreement.thr.edgelist' % thresh_dens

    el_name = 'group_task_2sess_%s' % el_suff
    edg_list = os.path.join(grp_conn_dir, el_name)
    com = ge.CommunityDetect(edg_list)
    com.convert_graph()

    Qs = np.zeros(niter)
    nmods = np.zeros(niter)
    trees = np.zeros(n_nodes*niter).reshape(n_nodes, niter)
    hierar_suff = 'group_task_2sess_dens_%s.trees_hierarchy' % thresh_dens
    for i in xrange(niter):
        print 'iter %d' % i
        hierarchy_tr_name = 'iter%d.%s' % (i, hierar_suff)
        hierarchy_tr_filename = os.path.join(trees_all_levl_dir,
                                             hierarchy_tr_name)
        Qs[i] = com.get_modularity(hierarchy_tr_filename)
        tr, n_m = com.get_hierarchical(hierarchy_tr_filename)
        if len(tr) == trees.shape[0]-1:
            tr = np.append(tr, tr[len(tr)-1])
        trees[:, i] = tr
        nmods[i] = n_m
    Qs_outname = 'task_2sess_dens_%s.Qval' % thresh_dens
    np.savetxt(os.path.join(mod_dir, Qs_outname), Qs, fmt='%.4f')
    trees_outname = 'task_2sess_dens_%s.trees' % thresh_dens
    np.savetxt(os.path.join(mod_dir, trees_outname),
               trees, fmt='%i')
    nmods_outname = 'task_2sess_dens_%s.nmods' % thresh_dens
    np.savetxt(os.path.join(mod_dir, nmods_outname),
               nmods, fmt='%i')
    bin_file = '%s.bin' % edg_list
    os.remove(bin_file)
