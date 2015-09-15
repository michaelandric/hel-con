# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 17:17:08 2015

@author: andric
"""

import os
import string
from shlex import split
from subprocess import call, STDOUT


def calc_overlap(ss_list, thresh):
    tcorr_dir = os.path.join(os.environ['hel'], 'tcorr_group')
    conj_dir = os.path.join(tcorr_dir, 'conjunctions')
    stdoutdir = os.path.join(conj_dir, 'stdout_dir')
    if not os.path.exists(stdoutdir):
        os.makedirs(stdoutdir)

    f = open('%s/stdout_from_3dcalc_conj.txt' % stdoutdir)
    input_list = []
    expr_list = []
    thr = thresh
    for i, ss in enumerate(ss_list):
        fname = 'tcorr_prsn_%s_gm_mskd_Z_fnirted_MNI2mm.nii.gz' % ss
        outcalc_pref = '%s_above_r%s' % (fname.split('.')[0], thr)
        cmdargs = split("3dcalc -prefix %s \
                        -a %s -expr 'ispositive(a-.1)'" %
                        (os.path.join(conj_dir, outcalc_pref),
                         os.path.join(tcorr_dir, fname)))
        call(cmdargs, stdout=f, stderr=STDOUT)
        input_list.append('-%s %s+orig' % (string.ascii_lowercase[i],
                                           os.path.join(conj_dir,
                                                        outcalc_pref)))
        expr_list.append(string.ascii_lowercase[i])
    inputstr = ' '.join(input_list)
    exprstr = '+'.join(expr_list)

    outpref = 'conj_tcorr_prsn_above_r%s' % thr
    conj_cmds = split("3dcalc -prefix %s %s -expr '%s'" %
                      (outpref, inputstr, exprstr))
    call(conj_cmds, stdout=f, stderr=STDOUT)
    f.close()


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj
