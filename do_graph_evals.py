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
    print os.getcwd()

    top_dir = '%s/graph_analyses' % os.environ['hel']
    if not os.path.exists(top_dir):
        os.makedirs(top_dir)

    niter = 100
    mod_loc = 'modularity'

    subj_list = ['hel19']
    for ss in subj_list:
        graph_dir = os.path.join(top_dir, '%s/graphs' % ss)
        if not os.path.exists(graph_dir):
            os.makedirs(graph_dir)
        mod_dir = os.path.join(top_dir, '%s/modularity' % ss)
        if not os.path.exists(mod_dir):
            os.makedirs(mod_dir)
        random_dir = os.path.join(top_dir, '%s/random' % ss)
        if not os.path.exists(random_dir):
            os.makedirs(random_dir)
        random_graph_dir = random_dir+'/graphs/'
        if not os.path.exists(random_graph_dir):
            os.makedirs(random_graph_dir)
        rand_mod_dir = os.path.join(random_dir, mod_loc)
        if not os.path.exists(rand_mod_dir):
            os.makedirs(rand_mod_dir)
        proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')

        for session in range(1, 3):
            ts_name = 'task_sess_%d_%s.txt' % (session, ss)
            ts_file = os.path.join(proc_dir, ts_name)
            n_nodes = file_len(ts_file)

            for thresh_dens in np.arange(.05, .1, .05):
                print 'Thresh: %s' % thresh_dens
                print time.ctime()
                graph_outname = 'task_sess_%d_%s.dens_%s.edgelist.gz' % \
                    (session, ss, thresh_dens)
                gr = ge.GRAPHS(ss, ts_file,
                               thresh_dens, graph_dir,
                               os.path.join(graph_dir, graph_outname))

                # making graph:
                print 'Making graph... '+time.ctime()
                avg_r = np.zeros(1)
                avg_r[0] = gr.make_graph()
                avg_r_val_name = 'Avg_rval_task_sess_%d_%s.dens_%s.txt' % \
                    (session, ss, thresh_dens)
                avg_r_out = os.path.join(graph_dir, avg_r_val_name)
                np.savetxt(avg_r_out, avg_r, fmt='%.4f')

                # get modularity and trees
                print 'Doing modularity evaluation... '
                print time.ctime()
                g = gr.make_networkx_graph(n_nodes)

                Qs = np.zeros(niter)
                trees = np.zeros(n_nodes*niter).reshape(n_nodes, niter)
                for i in xrange(niter):
                    trees[:, i], Qs[i] = gr.get_modularity(g)
                Qs_outname = 'task_sess_%d_%s.dens_%s.Qval' % \
                    (session, ss, thresh_dens)
                np.savetxt(os.path.join(mod_dir, Qs_outname), Qs, fmt='%.4f')
                trees_outname = 'task_sess_%d_%s.dens_%s.trees' % \
                    (session, ss, thresh_dens)
                np.savetxt(os.path.join(mod_dir, trees_outname),
                           trees, fmt='%i')
