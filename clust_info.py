# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 17:44:21 2015

@author: andric
"""

import os
import numpy as np
import pandas as pd


def get_clust_info(subj_list, conditions, maskname, method='mean'):
    print 'Getting cluster info'
    print 'Doing %s ' % method
    mask = np.loadtxt(maskname)
    clusters = np.unique(mask[np.where(mask != 0)])
    vals = []

    suff = 'ijk_fnirted_MNI2mm.txt'

    for ss in subj_list:
        print 'Getting subject %s' % ss
        conn_dir = os.path.join(os.environ['hel'], 'graph_analyses',
                                ss, 'global_connectivity')

        for session in range(1, 3):
            in_pref = 'avg_corrZ_task_sess_%d_%s' % (session, ss)
            data_fname = os.path.join(conn_dir, '%s.%s' % (in_pref, suff))
            subj_dat = np.loadtxt(data_fname)
            for cl in clusters:
                if method is 'mean':
                    vals.append(np.mean(subj_dat[np.where(mask == cl)]))
                elif method is 'median':
                    vals.append(np.median(subj_dat[np.where(mask == cl)]))

    subj_vec = subj_list*(len(clusters)*len(conditions))
    cnd_set = np.tile(np.repeat(conditions, len(clusters)), len(subj_list))
    cond_vec = np.array(cnd_set, dtype=np.int16)
    cl_set = np.tile(np.tile(clusters, len(conditions)), len(subj_list))
    clust_vec = np.array(cl_set, dtype=np.int16)
    return np.column_stack([subj_vec, cond_vec, clust_vec, vals])


if __name__ == '__main__':

    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    conditions = range(1, 3)
    grp_conn_dir = os.path.join(os.environ['hel'],
                                'graph_analyses',
                                'group_global_connectivity')
    clust_mask = os.path.join(grp_conn_dir, 'Clust_mask.txt')
    col_names = ['subject', 'condition', 'cluster', 'val']
    res = get_clust_info(subj_list, conditions, clust_mask)
    out = pd.DataFrame(res, columns=col_names)
    out_fname = os.path.join(grp_conn_dir,
                             'avg_corrZ_sess2vals_Clust_mask.cluster_info.csv')
    out.to_csv(out_fname, index=False)
