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


def cluster(inputf):
    """Cluster the permutation."""
    try:
        cmdargs = split('3dclust -quiet -1Dformat -nosum -1dindex 1 -1tindex 1 \
                        -dxyz=1 -2thresh -2.896 2.896 \
                        1.44 2 {}'.format(inputf))
        proc = Popen(cmdargs, stdout=PIPE)
        ppp = proc.stdout.read().split('\n')
    except proc as err:
        print('SOMETHING BROKE ---------- cluster NOT WORKING: ', err.value)
        print(inputf)

    if 'NO CLUSTERS' in ppp[0]:
        clustsize = 0
    else:
        clustsize = int(ppp[0].split()[0])

    return clustsize


def read_perms():
    """Read the permutation orders."""
    perm_a_name = os.path.join(os.environ['hel'], 'graph_analyses',
                               'group_modularity_thr0.5msk', 'perm_mat_a.txt')
    perm_b_name = os.path.join(os.environ['hel'], 'graph_analyses',
                               'group_modularity_thr0.5msk', 'perm_mat_b.txt')
    with open(perm_a_name) as a:
        prm_afile = a.read().splitlines()
    with open(perm_b_name) as b:
        prm_bfile = b.read().splitlines()

    return (prm_afile, prm_bfile)


def setup_files(setdict, indxa, indxb):
    """Iterate through indices to set files from permutations."""
    suffx = 'ijk_fnirted_MNI2mm.nii.gz'
    afiles = []
    bfiles = []
    for i in indxa:
        subj = setdict[i][0]
        sess = setdict[i][1]
        fname = 'avg_corrZ_task_sess_{}_{}.{}'.format(sess, subj, suffx)
        fpath = os.path.join(os.environ['hel'], 'graph_analyses',
                             subj, 'global_connectivity', fname)
        afiles.append(fpath)
    for i in indxb:
        subj = setdict[i][0]
        sess = setdict[i][1]
        fname = 'avg_corrZ_task_sess_{}_{}.{}'.format(sess, subj, suffx)
        fpath = os.path.join(os.environ['hel'], 'graph_analyses',
                             subj, 'global_connectivity', fname)
        bfiles.append(fpath)

    return (afiles, bfiles)


def do_perms_exact_half(log, n_perms, setdict):
    """Permute half the participants."""
    from itertools import combinations
    from collections import Counter
    combos_list = list(combinations(range(1, 19), 9))
    shuffle(combos_list)
    first_inds = range(1, 19)

    cluster_list = []
    for i in range(n_perms):
        kept = list((Counter(first_inds) - Counter(combos_list[i])).elements())
        a_perm_indx = kept + [i+18 for i in list(combos_list[i])]
        b_perm_indx = list((Counter(range(1, 37)) -
                            Counter(a_perm_indx)).elements())
        a_files, b_files = setup_files(setdict, a_perm_indx, b_perm_indx)
        aset = ' '.join(a_files)
        bset = ' '.join(b_files)
        outf = os.path.join(os.environ['hel'], 'graph_analyses',
                            'perms_global_connectivity', 'perm{}'.format(i))
        t_test(log, aset, bset, outf)
        cluster_list.append(cluster('{}+tlrc'.format(outf)))
    return cluster_list


def do_perms_at_least_half(log, n_perms, setdict):
    """Permute the groups.

    Re-design where at least half the participants
    have to be swapped between session 1 and session 2.
    """
    from collections import Counter
    permuted_a, permuted_b = read_perms()
    perms_indxs = range(len(permuted_a))
    shuffle(perms_indxs)

    first_inds = Counter(range(1, 19))
    cluster_list = []
    for n, i in enumerate(perms_indxs):
        if len(cluster_list) > n_perms:
            break
        a_perm_indx = map(int, permuted_a[i].split())
        b_perm_indx = map(int, permuted_b[i].split())
        a_inds = Counter(a_perm_indx)
        if len(list((first_inds & a_inds).elements())) < 9:
            a_files, b_files = setup_files(setdict, a_perm_indx, b_perm_indx)
            aset = ' '.join(a_files)
            bset = ' '.join(b_files)
            outf = os.path.join(os.environ['hel'], 'graph_analyses',
                                'perms_global_connectivity',
                                'perm{}'.format(n))
            t_test(log, aset, bset, outf)
            cluster_list.append(cluster('{}+tlrc'.format(outf)))

    return cluster_list


def do_perms(log, n_perms, setdict):
    """Do AFNI functions on permutation."""
    permuted_a, permuted_b = read_perms()
    perms_indxs = range(len(permuted_a))
    shuffle(perms_indxs)

    cluster_list = []
    for i in range(n_perms):
        a_perm_indx = map(int, permuted_a[perms_indxs[i]].split())
        b_perm_indx = map(int, permuted_b[perms_indxs[i]].split())
        a_files, b_files = setup_files(setdict, a_perm_indx, b_perm_indx)
        aset = ' '.join(a_files)
        bset = ' '.join(b_files)
        outf = os.path.join(os.environ['hel'], 'graph_analyses',
                            'perms_global_connectivity', 'perm{}'.format(i))
        t_test(log, aset, bset, outf)
        cluster_list.append(cluster('{}+tlrc'.format(outf)))
    return cluster_list


def output_clusterlist(clustlist):
    """Sort and write out cluster list from permutations."""
    clustout = '\n'.join(map(str, clustlist))
    clusters_outf = os.path.join(os.environ['hel'], 'graph_analyses',
                                 'perms_global_connectivity',
                                 'clustersize_permutations.txt')
    outf = open(clusters_outf, 'w')
    outf.write(clustout)
    outf.close()


def main():
    """Wrap function calls."""
    logfile = setup_log(os.path.join(os.environ['hel'], 'logs',
                                     'perm_t_test'))
    logfile.info('Started do_perm_t_test.py')

    subjectlist = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]

    sets = zip(subjectlist, [1]*18) + zip(subjectlist, [2]*18)
    set_dict = dict(zip(range(1, len(sets)+1), sets))

    n_permut = 5
    output_clusterlist(do_perms_exact_half(logfile, n_permut, set_dict))

if __name__ == '__main__':
    main()
