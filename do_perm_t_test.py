# -*- coding: utf-8 -*-
"""
Created Jul 5 2016.

(AFNI doesn't work in 3+)
@author: andric
"""

import os
from shlex import split
from setlog import setup_log
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from random import shuffle


def t_test(log, a_sets, b_sets, outpref):
    """T test in afni."""
    log.info('Doing t_test.')
    cmdargs = split('3dttest++ -setA %s -labelA sess_1 -setB %s -labelB sess_2 \
                    -mask %s/MNI152_T1_2mm_brain_mask_dil1.nii.gz \
                    -paired -prefix %s' %
                    (a_sets, b_sets,
                     '%s/data/standard' % os.environ['FSLDIR'], outpref))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def shuffle_indx(indx):
    """Shuffle the index."""
    g = indx[:]
    shuffle(g)
    return tuple(g)


def gen_perms(nset, nperms):
    """Generate permutated indices.

    Arg: nset
        number of items shuffling around
    Arg: nperms
        number of permutations
    """
    perms = []
    while len(perms) < nperms:
        shuf = shuffle_indx(range(nset))
        if shuf not in perms:
            perms.append(shuf)
    return perms


def setup_files(setdict, indx):
    """Iterate through indices to set files from permutations."""
    suffx = 'ijk_fnirted_MNI2mm.nii.gz'
    files = []
    for i in indx:
        subj = setdict[i][0]
        sess = setdict[i][1]
        fname = 'avg_corrZ_task_sess_{}_{}.{}'.format(sess, subj, suffx)
        fpath = os.path.join(os.environ['hel'], 'graph_analyses',
                             subj, 'global_connectivity', fname)
        files.append(fpath)
    return files


def main():
    """Wrap function calls."""
    logfile = setup_log(os.path.join(os.environ['hel'], 'logs',
                                     'perm_t_test'))
    logfile.info('Started do_perm_t_test.py')

    subjectlist = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]

    sets = zip(subjectlist, [1]*18) + zip(subjectlist, [2]*18)
    set_dict = dict(zip(range(len(sets)), sets))

    n_permutations = 2
    perm_list = gen_perms(len(set_dict), n_permutations)
    for n, perm_indx in enumerate(perm_list):
        testfiles = setup_files(set_dict, perm_indx)
        aset = ' '.join(testfiles[:18])
        bset = ' '.join(testfiles[18:])
        t_test(logfile, aset, bset, 'perm{}'.format(n))
