# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:44:58 2015

@author: andric
"""

import os
import general_procedures as gp


subj_list = []
for i in range(1, 19):
    subj_list.append('hel%d' % i)
subj_list.remove('hel9')   # because this is bad subj

conn_dir = os.path.join(os.environ['hel'],
                        'graph_analyses/group_global_connectivity')
mask = os.path.join(os.environ['FSLDIR'],
                    'data/standard/MNI152_T1_2mm_brain_mask_dil1.nii.gz')

for ss in subj_list:
    input_name = os.path.join(conn_dir, 'ttest_avg_corrZ')
    out_name = '%s_fwhm_est_out' % input_name
    gp.fwhm_est('%s+tlrc' % input_name, out_name, mask)

