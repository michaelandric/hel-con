# -*- coding: utf-8 -*-
"""
Created Jul 5 2016.

(AFNI doesn't work in 3+)
@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
import numpy as np
from setlog import setup_log


def make_design_mat(subj_list):
    """Build design matrix for FSL process.

    Makes what fsl docs call 'design.mat'
    """
    n_subj = len(subj_list)
    design_arr = np.array(np.zeros(n_subj**2)).reshape(n_subj, n_subj)
    np.fill_diagonal(design_arr, 1)
    onecolumn = np.array([1]*len(subj_list) + [-1]*len(subj_list))
    return np.column_stack((onecolumn, np.vstack((design_arr, design_arr))))


def make_design_grp(subj_list):
    """Build group design file for fsl.

    This makes what fsl docs call 'design.grp'
    """
    return np.array(range(1, len(subj_list)+1) * 2)


def make_design_contr(subj_list):
    """Get the contr vector.

    This makes what fsl docs call 'design.con'
    """
    outarr = np.array([1] + ([0]*len(subj_list))).reshape(1, -1)
    return outarr


def fsl_randomise(log, inputf, outpref):
    """Randomise in fsl."""
    try:
        cmdargs = split('randomise -i {} -o {} -d design.mat \
                        -t design.con -e design.grp -m mask -T'.format(
                            inputf, outpref))
        proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
        log.info(proc.stdout.read())
    except proc as err:
        print('SOMETHING BROKE ---------- randomise NOT WORKING: ', err.value)


def main():
    """Call methods to get fsl randomise."""
    subjectlist = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]
    workdir = os.path.join(os.environ['hel'], 'graph_analyses',
                           'randomise_global_connectivity')
    logfile = setup_log(os.path.join(os.environ['hel'], 'logs',
                                     'randomise_ttest'))
    logfile.info('Doing design files...')
    descon_outf = os.path.join(workdir, 'design.con')
    np.savetxt(descon_outf, make_design_contr(subjectlist), fmt='%i')
    desgrp_outf = os.path.join(workdir, 'design.grp')
    np.savetxt(desgrp_outf, make_design_grp(subjectlist), fmt='%i')
    desmat_outf = os.path.join(workdir, 'design.mat')
    np.savetxt(desmat_outf, make_design_mat(subjectlist), fmt='%i')
    os.chdir(workdir)
    logfile.info('Now in working directory: %s', os.getcwd())
    infile = os.path.join(workdir, 'wgc_PairedT_4Dfile')
    outname = os.path.join(workdir, 'wgc_PairedTres')
    fsl_randomise(logfile, infile, outname)

if __name__ == '__main__':
    main()
