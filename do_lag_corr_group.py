# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 16:39:09 2015

@author: andric
"""

import os
import numpy as np


def corr_complete(mat):


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    graph_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    suff = 'ijk_fnirted_MNI4mm_thr0.5.txt'
    nvox = 20071
    lag_mat = np.empty((nvox, len(subj_list)))
    for i, ss in enumerate(subj_list):
        sspref = 'ccf_lag_out_%s_gm_mskd.%s' % (ss, suff)
        ss_mat = os.path.join(graph_dir, ss, 'global_connectivity', sspref)
        lag_mat[:, i] = np.loadtxt(ss_mat)
