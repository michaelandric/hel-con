#!/usr/bin/env python

import os
import numpy as np


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


if __name__ == '__main__':

subj_list = []
for i in range(1, 20):
    subj_list.append('hel%d' % i)
subj_list.remove('hel9')   # because this is bad subj

vox_counts = np.empty(len(subj_list))

for i, ss in enumerate(subj_list):
    ff = '%s/%s/preprocessing/task_sess_2_%s_gm_mskd.txt' % (os.environ['hel'], ss, ss)
    if os.path.exists(ff):
        vox_counts[i] = file_len(ff)
    else:
        print '%s does not exist, sucka!' % ff
