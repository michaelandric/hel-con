# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 00:27:56 2015

@author: andric
"""

import os
import numpy as np


def rw_corr_coeff(A, B):
    """
    inspiration from
    https://stackoverflow.com/questions/30143417/computing-the-correlation-coefficient-between-two-multi-dimensional-arrays
    """
    # Rowwise mean of input arrays & subtract from input arrays themeselves
    A_mA = A - A.mean(1)[:,None]
    B_mB = B - B.mean(1)[:,None]

    # Sum of squares across rows
    ssA = (A_mA**2).sum(1)
    ssB = (B_mB**2).sum(1)
    return (A_mA*B_mB).sum(1) / (np.sqrt(ssA*ssB))


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    ava_dir = os.path.join(os.environ['hel'], 'ava')
    graph_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    grp_deg_dir = os.path.join(graph_dir, 'group_degrees')

    sfx = 'txt.ijk_fnirted_MNI4mm_thr0.5.txt'

    for thr in [.05, .1, .15, .2]:
        for r in range(1, 3):
            ava_name = 'ava_smth_task_sess_%s_group_gm_mskd.%s' % (r, sfx)
            ava_mat = np.loadtxt(os.path.join(ava_dir, ava_name))
    
            deg_name = 'task_sess_%s_group.dens_%s.degrees.%s' % (r, thr, sfx)
            deg_mat = np.loadtxt(os.path.join(grp_deg_dir, deg_name))
            
            corr_out = rw_corr_coeff(ava_mat, deg_mat)
            outname = 'ava_smth_deg_corr_sess_%s_dens_%s_out' % (r, thr)
            outf = os.path.join(ava_dir, outname)
            np.savetxt(outf, corr_out, fmt='%.4f')
