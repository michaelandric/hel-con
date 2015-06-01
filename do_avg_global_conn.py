# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 03:01:21 2015

@author: andric
"""

import os
import numpy as np
import graph_evals as ge


if __name__ == '__main__':

    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    top_dir = '%s/graph_analyses' % os.environ['hel']

    for ss in subj_list:
        proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
        conn_dir = os.path.join(top_dir, '%s/global_connectivity' % ss)
        if not os.path.exists(conn_dir):
            os.makedirs(conn_dir)
        for session in range(1, 3):
            ts_name = os.path.join(proc_dir,
                                   'task_sess_%d_%s.txt' % (session, ss))
            agc = ge.avg_global_connectivity(ts_name)
            out_name = 'avg_corrZ_task_sess_%d_%s' % (session, ss)
            out_fname = os.path.join(conn_dir, out_name)
            np.savetxt(out_fname, agc, fmt='%.4f')
