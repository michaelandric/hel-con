# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 03:01:21 2015

Revised Apr 12 2016

@author: andric
"""

import os
import numpy as np
import graph_evals as ge


if __name__ == '__main__':

    subj_list = ['hel{}'.format(i) for i in range(1, 20)]
    subj_list.remove('hel9')   # because this is bad subj

    top_dir = os.path.join(os.environ['hel'], 'graph_analyses')

    for ss in subj_list:
        proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
        conn_dir = os.path.join(top_dir,
                                '{}/single_run_global_connectivity'.format(ss))
        if not os.path.exists(conn_dir):
            os.makedirs(conn_dir)
        for r in [1, 3, 4, 6]:
            ts_name = os.path.join(proc_dir,
                                   'task_r0{}_{}_gm_mskd'.format(r, ss))
            agc = ge.avg_global_connectivity(ts_name)
            out_name = 'avg_corrZ_task_r0{}_{}'.format(r, ss)
            out_fname = os.path.join(conn_dir, out_name)
            np.savetxt(out_fname, agc, fmt='%.4f')
