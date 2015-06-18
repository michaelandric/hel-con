# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 02:22:43 2015

@author: andric
"""

import os
import sys
import time
import numpy as np
import graph_evals as ge


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


if __name__ == "__main__":

    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    top_dir = '%s/graph_analyses' % os.environ['hel']
    if not os.path.exists(top_dir):
        print 'What is going on here?'
        print 'Where is the top_dir?'
        sys.exit(1)

    for thresh_dens in [.05, .10, .15, .20]:
        for ss in subj_list:
            ss_deg_dir = os.path.join(top_dir, '%s/degrees' % ss)
            if not os.path.exists(ss_deg_dir):
                os.makedirs(ss_deg_dir)
            proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
            graph_dir = os.path.join(top_dir, '%s/graphs' % ss)
            for session in range(1, 3):
                print 'Doing %s %s %s' % (thresh_dens, ss, session)
                print time.ctime()
                ts_name = os.path.join(proc_dir,
                                       'task_sess_%d_%s_gm_mskd.txt' %
                                       (session, ss))
                graph_outname = 'task_sess_%d_%s.dens_%s.edgelist.gz' % \
                    (session, ss, thresh_dens)
                gr = ge.Graphs(ss, ts_name, thresh_dens, graph_dir)

                n_nodes = file_len(ts_name)
                edge_list = os.path.join(graph_dir, graph_outname)
                nx_graph = gr.make_networkx_graph(n_nodes, edge_list)
                degrees = np.array(nx_graph.degree().values())
                suffx = 'degrees.txt'
                deg_fname = os.path.join(ss_deg_dir,
                                         'task_sess_%d_%s.dens_%s.%s' %
                                         (session, ss, thresh_dens, suffx))
                np.savetxt(deg_fname, degrees, fmt='%i')
