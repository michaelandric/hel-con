#!/usr/bin/env python
"""Getting the tree text file to AFNI via 3dUndump"""
__author__ = 'andric'

import sys
import os
import numpy as np
from shlex import split
from subprocess import call, STDOUT
from collections import Counter


def undump(undump_outname, datumtype, master, infile):
    fh = open('stdout_files/stdout_from_undump.txt', 'w')
    cmdargs = split('3dUndump -prefix %s -ijk -datum %s -master %s %s' % (undump_outname, datumtype, master, infile))
    call(cmdargs, stdout=fh, stderr=STDOUT)
    fh.close()


if __name__ == '__main__':

    if len(sys.argv) < 4:
        sys.stderr.write("You done fucked up! \n"
                         "Usage: %s <SUBJECT ID> <CONDITION ID> <THRESH DENSITY> \n" %
                         (os.path.basename(sys.argv[0]),))

    subjid = sys.argv[1]
    condition = sys.argv[2]
    thresh_density = sys.argv[3]

    os.chdir(os.environ['hel']+'/%s/connectivity/' % subjid)
    print os.getcwd()

    tree_hier_dir = 'tree_highest'
    mod_dir = 'modularity'
    q = np.loadtxt('%s/%s.%s.dens_%s.Qval' % (mod_dir, subjid, condition, thresh_density))
    maxiter = q.argmax()
    tree = np.loadtxt('%s/iter%s.%s.%s.dens_%s.tree_highest' % (tree_hier_dir, maxiter, subjid, condition, thresh_density), dtype=np.int32)
    tree1 = tree[:,1]
    cnts = Counter(tree1)
    modid = np.array(cnts.keys())[np.where(np.array(cnts.values())==1)]
    tree1[np.in1d(tree1, modid)] = 0

    ijk = np.loadtxt(os.environ['hel']+'/%s/volume.%s.anat/%s.ijk_GMmask_dump' % (subjid, subjid, subjid))
    ijktree = np.column_stack((ijk, tree1))
    ijktree_outname = '%s/%s.%s.dens_%s.tree_highest_max.ijk' % (mod_dir, subjid, condition, thresh_density)
    np.savetxt(ijktree_outname, ijktree, fmt='%i')

    if not os.path.exists('%s/stdout_files' % mod_dir):
        os.makedirs('%s/stdout_files' % mod_dir)
    master = 'cleanTScat_%s.allruns+orig.' % subjid
    undump(ijktree_outname, 'short', master, ijktree_outname)

