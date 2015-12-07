# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 00:27:56 2015

@author: andric
"""

import os
import numpy as np


nvox = 20071

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
        print('Doing deg mat thr: %s, run %s' % (thr, r))
        deg_mat = np.zeros(nvox*len(subj_list)).reshape(nvox, len(subj_list))
        for i, ss in enumerate(subj_list):
            deg_dir = os.path.join(graph_dir, ss, 'degrees')
            deg_name = 'task_sess_%s_%s.dens_%s.degrees.%s' % (r, ss, thr, sfx)
            deg_fname = os.path.join(deg_dir, deg_name)
            deg_mat[:, i] = np.loadtxt(deg_fname)
        out_fname = 'task_sess_%s_group.dens_%s.degrees.%s' % (r, thr, sfx)
        out_f = os.path.join(grp_deg_dir, out_fname)
        np.savetxt(out_f, deg_mat, fmt='%i')

for r in range(1, 3):
    print('Doing ava mat, run %s' % r)
    # ava_mat1 is smth data
    # ava_mat2 is not smth data
    ava_mat1 = np.zeros(nvox*len(subj_list)).reshape(nvox, len(subj_list))
    ava_mat2 = np.zeros(nvox*len(subj_list)).reshape(nvox, len(subj_list))
    for i, ss in subj_list:
        ava_name1 = 'ava_smth_task_sess_%s_%s_gm_mskd.%s' % (r, ss, sfx)
        ava_name2 = 'ava_task_sess_%s_%s_gm_mskd.%s' % (r, ss, sfx)
        ava_mat1[:, i] = np.loadtxt(os.path.join(ava_dir, ava_name1))
        ava_mat2[:, i] = np.loadtxt(os.path.join(ava_dir, ava_name2))
    out_ava1_name = 'ava_smth_task_sess_%s_group_gm_mskd.%s' % (r, sfx)
    out_ava2_name = 'ava_task_sess_%s_group_gm_mskd.%s' % (r, sfx)
    out_f1 = os.path.join(ava_dir, out_ava1_name)
    out_f2 = os.path.join(ava_dir, out_ava2_name)
    np.savetxt(out_f1, ava_mat1, fmt='%.4f')
    np.savetxt(out_f2, ava_mat2, fmt='%.4f')