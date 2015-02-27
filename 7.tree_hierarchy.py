#!/usr/bin/env python
"""This parases the tree at the highest hierarchical level"""
__author__ = 'andric'

import sys
import os
import numpy as np
from subprocess import Popen, PIPE
from shlex import split
from time import ctime

class TreeParser(object):

    tree_all_levels = None

    def get_hierarchical(self, tree_all_levels, tr_outname, n_mods_name):
        cmdargs = split('hierarchy -n %s' % tree_all_levels)
        print 'Parsing trees to find highest hierarchical level -- '+ctime()
        print cmdargs
        p = Popen(cmdargs, stdout=PIPE).communicate()
        h = int(p[0].split()[3]) - 1
        print 'Done parsing trees -- '+ctime()
        print 'Highest level: %s ' % h
        print 'Getting hierarchy -- '+ctime()
        cmdargs = split('hierarchy -l %d %s' % (h, tree_all_levels))
        tree = Popen(cmdargs, stdout=PIPE).communicate()
        f = open(tr_outname, 'w')
        f.write(tree[0])
        f.close()
        print ctime()+' :::\n'
        print 'Done writing the tree. '+ctime()

        mods = []
        for x in xrange(len(tree[0].split('\n'))-1):
            mods.append(tree[0].split('\n')[x].split()[1])
        m2 = map(int, mods)
        s2 = set(m2)
        toremove = []
        for mod_id in s2:
            if m2.count(mod_id) < 2:
                toremove.append(mod_id)
        for mod_id in toremove:
            s2.remove(mod_id)
        # n_mods = str(len(set(mods)))   # this would be the total number of modules
        n_mods = str(len(set(s2)))   # this is the total number of modules > 1 voxel
        print ctime()+' :::\n'
        print n_mods+' is the numbere of modules (> 1 voxel)'
        ff = open(n_mods_name, 'w')
        ff.write(n_mods+'\n')
        ff.close()
        print 'Done writing N_mods '+ctime()

if __name__ == '__main__':

    if len(sys.argv) < 4:
        sys.stderr.write("You done fucked up! \n"
                         "Usage: %s <SUBJECT ID> <CONDITION ID> <THRESH DENSITY> \n" %
                         (os.path.basename(sys.argv[0]),))

    subjid = sys.argv[1]
    condition = sys.argv[2]
    thresh_density = sys.argv[3]
    niter = 100   # because I have 100 iterations of the modularity solution, one tree for each

    tp = TreeParser()

    os.chdir(os.environ['hel']+'/%s/connectivity/' % subjid)
    print os.getcwd()
    treedir = 'trees'
    tree_hier_dir = 'tree_highest'
    n_mods_dir = 'n_mods'
    if not os.path.exists(tree_hier_dir):
        os.makedirs(tree_hier_dir)
    if not os.path.exists(n_mods_dir):
        os.makedirs(n_mods_dir)

    for n in xrange(niter):
        main_tree = '%s/iter%s.%s.%s.dens_%s.tree' % (treedir, n, subjid, condition, thresh_density)
        tree_out = '%s/iter%s.%s.%s.dens_%s.tree_highest' % (tree_hier_dir, n, subjid, condition, thresh_density)
        n_mods_name = '%s/iter%s.%s.%s.dens_%s.n_mods' % (tree_hier_dir, n, subjid, condition, thresh_density)
        tp.get_hierarchical(main_tree, tree_out, n_mods_name)