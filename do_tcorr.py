# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 12:32:50 2015

@author: andric
"""

import os
from shlex import split
from subprocess import call, STDOUT
import general_procedures as gp


def tcorr(stdoutdir, outpref, epi1, epi2):
    f = open('%s/stdout_from_tcorrelate.txt' % stdoutdir, 'w')
    cmdargs = split('3dTcorrelate -polort -1 -spearman \
                    -prefix %s %s %s' % (outpref, epi1, epi2))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def fishertransform(stdoutdir, inputcor, outpref):
    f = open("%s/stdout_from_fishertransform.txt" % stdoutdir, "w")
    cmdargs = split("3dcalc -a %s -expr 'atanh(a)' \
                    -prefix %s" % (inputcor, outpref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 19):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    for ss in subj_list:
        proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
        epi1_fname = os.path.join(proc_dir, 'task_sess_1_%s_gm_mskd+orig' % ss)
        epi2_fname = os.path.join(proc_dir, 'task_sess_2_%s_gm_mskd+orig' % ss)
        out_pref = os.path.join(proc_dir, 'tcorr_%s_gm_mskd' % ss)
        stdout_dir = os.path.join(proc_dir, 'stdout_files')
        if not os.path.exists(stdout_dir):
            os.makedirs(stdout_dir)
#        tcorr(stdout_dir, out_pref, epi1_fname, epi2_fname)
        trans_out = '%s_Z' % out_pref
        fishertransform(stdout_dir, '%s+orig' % out_pref, trans_out)
        gp.converttoNIFTI(proc_dir, '%s+orig' % trans_out, trans_out)
