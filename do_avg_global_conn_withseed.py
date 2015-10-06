# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 16:12:26 2015

@author: andric
"""

import os
import numpy as np
import time


def corr_coeff2(A, B):
    """
    need same col dimension for A and B
    """
    # Rowwise mean of input arrays & subtract from
    # input arrays themeselves
    A_mA = A - A.mean(1)[:, None]
    B_mB = B - B.mean(1)[:, None]

    # Sum of squares across rows
    ssA = (A_mA**2).sum(1)
    ssB = (B_mB**2).sum(1)

    # Finally get corr coeff
    return np.dot(A_mA, B_mB.T)/np.sqrt(np.dot(ssA[:, None], ssB[None]))


def seed_global_connectivity(ts, seed, transform=True):
    """
    correlate seed time series against every other
    """
    print 'Doing avg_global_connectivity '
    print time.ctime()
#    n_tps = ts.shape[0]
#    seed_corr = np.corrcoef(ts, seed)[n_tps, :-1]
    seed_corr = corr_coeff2(ts, seed[None, :])
    # in case there were 0 rows f'n things up
    seed_corr[np.isnan(seed_corr)] = 0
    if transform is True:
        return np.arctanh(seed_corr)
    else:
        return seed_corr

if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    for cl in [2, 3]:
        outn_pref = 'knnward_clst%d_mskd' % cl

        for ss in subj_list:
            ss_dir = os.path.join(os.environ['hel'], ss)
            proc_dir = os.path.join(ss_dir, 'preprocessing')
            anat_dir = os.path.join(ss_dir, 'volume.%s.anat' % ss)
            conn_dir = os.path.join(os.environ['hel'], 'graph_analyses',
                                    '%s/global_connectivity' % ss)
            maskf_name = '%s_consensus_prtn_knnward_clst%d_mskd_origspace.txt' % (ss, cl)
            mask_file = os.path.join(anat_dir, maskf_name)
            m = np.loadtxt(mask_file)
            subclusters = np.unique(m[m != 0])
            for session in range(1, 3):
                ts_name = os.path.join(proc_dir,
                                       'task_sess_%d_%s_gm_mskd.txt' %
                                       (session, ss))
                ts = np.loadtxt(ts_name)
                for clst in subclusters:
                    seed = np.mean(ts[np.where(m == clst)[0], :], axis=0)
                    sgc = seed_global_connectivity(ts, seed)
                    outname = '%s_subclust%d_corrZ_sess_%d_%s' % \
                              (outn_pref, clst, session, ss)
                    outfname = os.path.join(conn_dir, outname)
                    np.savetxt(outfname, sgc, fmt='%.4f')
