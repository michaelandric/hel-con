# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 14:52:34 2015

@author: andric
"""

import shutil
import os
import glob


subj_list = []
for i in range(1, 20):
    subj_list.append('hel%d' % i)
subj_list.remove('hel9')   # because this is bad subj

ava_dir = os.path.join(os.environ['hel'], 'ava')
for ss in subj_list:
    proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
    for i in range(1, 3):
        ava_files = glob.glob('%s/ava_task_sess_*_%s_gm_mskd.txt.ijk+orig.*' % (proc_dir, ss))
        for f in ava_files:
            shutil.copy2(f, ava_dir)
