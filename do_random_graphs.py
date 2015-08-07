# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 17:21:11 2015

@author: andric
"""

import os
import numpy as np
import graph_evals as ge


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

    subj_list = ['hel19']
    for ss in subj_list:
        ss_dir = '%s/%s' % (top_dir, ss)
        proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')

        rand_graph_dir = '%s/random' % ss_dir
        if not os.path.exists(rand_graph_dir):
            os.makedirs(rand_graph_dir)

        for session in range(1, 3):
            ts_name = os.path.join(proc_dir,
                                   'task_sess_%d_%s_gm_mskd.txt' %
                                   (session, ss))
            ts_file = np.loadtxt(ts_name)
            n_nodes = file_len(ts_name)

            for thresh_dens in [.05, .10]:
                gr = ge.Graphs(ss, 'none', thresh_dens, rand_graph_dir)

                Qs = np.zeros(niter)
                nmods = np.zeros(niter)
                trees = np.zeros(n_nodes*niter).reshape(n_nodes, niter)
                hierar_suff = 'rnd_sess_%d_%s.dens_%s.trees_hierarchy' % \
                    (session, ss, thresh_dens)

                for i in range(niter):
                    grph_out_pref = 'rnd_graph_sess_%d_%s.dens_%s.edgelist' \
                                    % (session, ss, thresh_dens)
                    rgrph_outname = os.path.join(rand_graph_dir, grph_out_pref)
                    gr.make_random_graph(n_nodes, rgrph_outname)
                    com = ge.CommunityDetect(rgrph_outname)
                    com.convert_graph()

                    hierarchy_tr_name = 'iter%d.%s' % (i, hierar_suff)
                    hierarchy_tr_filename = os.path.join(rand_graph_dir,
                                                         hierarchy_tr_name)
                    Qs[i] = com.get_modularity(hierarchy_tr_filename)
                    tr, n_m = com.get_hierarchical(hierarchy_tr_filename)
                    if len(tr) == trees.shape[0]-1:
                        tr = np.append(tr, tr[len(tr)-1])
                    trees[:, i] = tr
                    nmods[i] = n_m
                    os.remove(rgrph_outname)
                    os.remove(hierarchy_tr_filename)
                    bin_file = '%s.bin' % rgrph_outname
                    os.remove(bin_file)
                Qs_outname = 'rnd_sess_%d_%s.dens_%s.Qval' % \
                    (session, ss, thresh_dens)
                np.savetxt(os.path.join(rand_graph_dir, Qs_outname),
                           Qs, fmt='%.4f')
                trees_outname = 'rnd_sess_%d_%s.dens_%s.trees' % \
                    (session, ss, thresh_dens)
                np.savetxt(os.path.join(rand_graph_dir, trees_outname),
                           trees, fmt='%i')
                nmods_outname = 'rnd_sess_%d_%s.dens_%s.nmods' % \
                    (session, ss, thresh_dens)
                np.savetxt(os.path.join(rand_graph_dir, nmods_outname),
                           nmods, fmt='%i')
