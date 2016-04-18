# -*- coding: utf-8 -*-
"""
Created on Fri May 29 17:34:54 2015

@author: andric
"""

import os
import time
import numpy as np
import graph_evals as ge
# import networkx as nx


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


if __name__ == '__main__':

    os.chdir(os.environ['hel'])
    print (os.getcwd())

    top_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    if not os.path.exists(top_dir):
        os.makedirs(top_dir)

    niter = 100
    mod_loc = 'modularity'

    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]

    for ss in subj_list:
        graph_dir = os.path.join(top_dir, '{}/subrun_graphs'.format(ss))
        if not os.path.exists(graph_dir):
            os.makedirs(graph_dir)        

        mod_dir = os.path.join(top_dir, '{}/subrun_modularity'.format(ss))
        if not os.path.exists(mod_dir):
            os.makedirs(mod_dir)        

        trees_all_levl_dir = os.path.join(top_dir,
                                          '{}/subrun_hierarchy_trees'.format(ss))
        if not os.path.exists(trees_all_levl_dir):
            os.makedirs(trees_all_levl_dir)        

        random_dir = os.path.join(top_dir, '{}/subrun_random'.format(ss))
        if not os.path.exists(random_dir):
            os.makedirs(random_dir)

        random_graph_dir = random_dir+'/subrun_graphs/'
        if not os.path.exists(random_graph_dir):
            os.makedirs(random_graph_dir)

        rand_mod_dir = os.path.join(random_dir, mod_loc)
        if not os.path.exists(rand_mod_dir):
            os.makedirs(rand_mod_dir)

        proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')

        for r in [1, 3]:
            if r is 1:
                session = 'first'
            if r is 3:
                session = 'second'
            ts_nameA = os.path.join(proc_dir,
                                    'task_r0{}_hel1_gm_mskd.txt'.format(r))
            ts_nameB = os.path.join(proc_dir,
                                    'task_r0{}_hel1_gm_mskd.txt'.format(r+3))
            tsA = np.loadtxt(ts_nameA)
            tsB = np.loadtxt(ts_nameB)
            ts_file = np.column_stack([tsA, tsB])
            n_nodes = file_len(ts_nameA)

            for thresh_dens in [.15]:
                print ('Thresh: {}'.format(thresh_dens))
                print (time.ctime())
                graph_outname = 'task_{}_{}.dens_{}.edgelist.gz'.format(
                    session, ss, thresh_dens)
                gr = ge.Graphs(ss, ts_file, thresh_dens, graph_dir)

                # making graph:
                print ('Making graph... '+time.ctime())
                avg_r = np.zeros(1)
                edg_lst = os.path.join(graph_dir, graph_outname)
                avg_r[0] = gr.make_graph(edg_lst)
                avg_r_val_name = 'Avg_rval_task_{}_{}.dens_{}.txt'.format(
                    session, ss, thresh_dens)
                avg_r_out = os.path.join(graph_dir, avg_r_val_name)
                np.savetxt(avg_r_out, avg_r, fmt='%.4f')

                # modularity and trees
                graph_pref = 'task_{}_{}.dens_{}.edgelist'.format(
                    session, ss, thresh_dens)
                com = ge.CommunityDetect(os.path.join(graph_dir, graph_pref))
                com.zipper('unzip')
                com.convert_graph()
                com.zipper('zip')
                Qs = np.zeros(niter)
                nmods = np.zeros(niter)
                trees = np.zeros(n_nodes*niter).reshape(n_nodes, niter)
                hierar_suff = 'task_{}_{}.dens_{}.trees_hierarchy'.format(
                    session, ss, thresh_dens)
                for i in range(niter):
                    print ('iter {}'.format(i))
                    hierarchy_tr_name = 'iter{}.{}'.format(i, hierar_suff)
                    hierarchy_tr_filename = os.path.join(trees_all_levl_dir,
                                                         hierarchy_tr_name)
                    Qs[i] = com.get_modularity(hierarchy_tr_filename)
                    tr, n_m = com.get_hierarchical(hierarchy_tr_filename)
                    if len(tr) == trees.shape[0]-1:
                        tr = np.append(tr, tr[len(tr)-1])
                    trees[:, i] = tr
                    nmods[i] = n_m
                Qs_outname = 'task_{}_{}.dens_{}.Qval'.format(
                    session, ss, thresh_dens)
                np.savetxt(os.path.join(mod_dir, Qs_outname), Qs, fmt='%.4f')
                trees_outname = 'task_{}_{}.dens_{}.trees'.format(
                    session, ss, thresh_dens)
                np.savetxt(os.path.join(mod_dir, trees_outname),
                           trees, fmt='%i')
                nmods_outname = 'task_{}_{}.dens_{}.nmods'.format(
                    session, ss, thresh_dens)
                np.savetxt(os.path.join(mod_dir, nmods_outname),
                           nmods, fmt='%i')
                bin_file = '{}.bin'.format(graph_pref)
                os.remove(os.path.join(graph_dir, bin_file))
