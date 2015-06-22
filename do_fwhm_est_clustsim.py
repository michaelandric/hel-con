# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:44:58 2015

@author: andric
"""

import os
import numpy as np
import general_procedures as gp
from shlex import split
from subprocess import Popen, PIPE


def get_fwhm(mask, input):
    """
    Will return x, y, z as floats
    """
    cmds = split('3dFWHMx -mask %s -input %s' % (mask, input))
    p = Popen(cmds, stdout=PIPE).communicate()
    return map(float, p[0].split())


subj_list = []
for i in range(1, 19):
    subj_list.append('hel%d' % i)
subj_list.remove('hel9')   # because this is bad subj

group_conn_dir = os.path.join(os.environ['hel'],
                              'graph_analyses/group_global_connectivity')
# mask = os.path.join(os.environ['FSLDIR'],
#                     'data/standard/MNI152_T1_2mm_brain_mask_dil1.nii.gz')
mask = os.path.join(os.environ['hel'], 'group_anat',
                    'group_avg_gm_mask_frac_bin_fnirted_MNI2mm_thr0.34.nii.gz')

xyz_mat = np.zeros(len(subj_list)*3).reshape(len(subj_list), 3)

for i, ss in enumerate(subj_list):
    f_pref = 'avg_corrZ_task_sess_2_%s.ijk_fnirted_MNI2mm' % ss
    indv_conn_d = os.path.join(os.environ['hel'], 'graph_analyses',
                               ss, 'global_connectivity')
    input_pref = os.path.join(indv_conn_d, f_pref)
    x, y, z = get_fwhm(mask, '%s.nii.gz' % input_pref)
    xyz_mat[i, :] = [x, y, z]

avg_fwhm = np.mean(xyz_mat, axis=0)
print 'FWHM is:'
print avg_fwhm
out_pref = 'group_avg_corrZ_task_sess_2.ijk_fnirted_MNI2mm_fwhm_est_out'
out_name = os.path.join(group_conn_dir, out_pref)
np.savetxt(out_name, avg_fwhm.reshape(1, 3), fmt='%.4f %.4f %.4f')

gp.clustsim(avg_fwhm, group_conn_dir, mask)
