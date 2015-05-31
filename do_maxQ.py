# -*- coding: utf-8 -*-
"""
Created on Sun May 31 10:35:21 2015

@author: andric
"""

import os
import sys
import time
import numpy as np
import graph_evals as ge
from scipy.stats import wilcoxon


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
    group_Q_dir = os.path.join(top_dir, 'group_modularity')
    if not os.path.exists(group_Q_dir):
        os.makedirs(group_Q_dir)

    for thresh_dens in [.05, .10, .15, .20]:
        q_array = np.zeros(len(subj_list)*2).reshape(len(subj_list), 2)
        nmod_array = np.zeros(len(subj_list)*2).reshape(len(subj_list), 2)
        for i, ss in enumerate(subj_list):
            proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
            graph_dir = os.path.join(top_dir, '%s/graphs' % ss)
            mod_dir = os.path.join(top_dir, '%s/modularity' % ss)
            for session in range(1, 3):
                ts_name = os.path.join(proc_dir,
                                       'task_sess_%d_%s.txt' % (session, ss))
                graph_outname = 'task_sess_%d_%s.dens_%s.edgelist.gz' % \
                    (session, ss, thresh_dens)
                gr = ge.Graphs(ss, ts_name, thresh_dens, graph_dir,
                               os.path.join(graph_dir, graph_outname))
                q_fname = 'task_sess_%d_%s.dens_%s.Qval' % \
                    (session, ss, thresh_dens)
                qval, indx = gr.max_q(os.path.join(mod_dir, q_fname))
                q_array[i, session-1] = qval
                nmod_fname = 'task_sess_%d_%s.dens_%s.nmods' % \
                    (session, ss, thresh_dens)
                nmods = gr.max_nmod(os.path.join(mod_dir, nmod_fname), indx)
                nmod_array[i, session-1] = nmods

        q_out_report = []
        nmod_out_report = []
        print 'Wilcox tests.. %s' % time.ctime()
        qstat, qp = wilcoxon(q_array[:, 0], q_array[:, 1])
        q_out_report.append('Density %s, Wilcoxon: %s, p-val %s' %
                            (thresh_dens, qstat, qp))
        nstat, nmods_p = wilcoxon(nmod_array[:, 0], nmod_array[:, 1])
        nmod_out_report.append('Density %s, Wilcoxon: %s, p-val %s' %
                               (thresh_dens, nstat, nmods_p))
        out_qrep_fname = 'max_q_values_density%s_report.txt' % thresh_dens
        outqf = open(os.path.join(group_Q_dir, out_qrep_fname), 'w')
        outqf.write('\n'.join(q_out_report))
        outqf.close()
        out_nmodrep_fname = 'max_q_n_mods_density%s_report.txt' % thresh_dens
        outnmf = open(os.path.join(group_Q_dir, out_nmodrep_fname), 'w')
        outnmf.write('\n'.join(nmod_out_report))
        outnmf.close()
        q_array_fname = 'max_q_values_density%s_array.txt' % thresh_dens
        np.savetxt(os.path.join(group_Q_dir, q_array_fname),
                   q_array, fmt='%.4f')
        nmod_array_fname = 'max_q_n_mods_density%s_array.txt' % thresh_dens
        np.savetxt(os.path.join(group_Q_dir, nmod_array_fname),
                   nmod_array, fmt='%.4f')
