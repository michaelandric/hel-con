#!/usr/bin/env python
"""Compare partitions"""
__author__ = 'andric'

import sys
import time
import numpy as np


class COMPARE:
    """
    Methods for comparing partition similarity
    """

    def adjRand(self, p1, p2):
        """
        Get the Adjusted Rand Score, adjusted as
        ARI = (RI - Expected_RI) / (max(RI) - Expected_RI)
        :param p1: Partition 1
        :param p2: Partition 2
        :return: Adjusted Rand score
        """
        ars = adjusted_rand_score(p1, p2)
        return ars

    def normalized_MI(self, p1, p2):
        """
        Get the Normalized Mutual Information
        :param p1: Partition 1
        :param p2: Partition 2
        :return: Normalized Mutual Information measure
        """
        nmi = normalized_mutual_info_score(p1, p2)
        return nmi



if __name__ == '__main__':

    if len(sys.argv) < 3:
    sys.stderr.write("You done screwed up! \n"
                     "Usage: %s <SUBJECT ID> <METHOD> \n" %
                     (os.path.basename(sys.argv[0]),))

    subjid = sys.argv[1]
    compare_method = sys.argv[2]
    niter = 100   # because I have 100 iterations of the modularity solution, one tree for each

    n_regions = 148
    # Building array of inputs. These are the trees of highest modularity
    tree_mat = np.array(np.zeros(niter*n_regions)).reshape(n_regions, niter)
    for n in xrange(niter):
        infile = 'tree_highest/%s_dens0.1_tree.iter%d.highesttree' % (subjid, n)
        tree_mat[:,n] = np.loadtxt(infile)[:,1]   # because these infile actually has one col for indices

    # Prepping output array
    n_combinations = ((niter**2)-niter)/2
    compare_out = np.array(np.zeros(n_combinations))

    cmp = COMPARE()

    if compare_method == 'ARI':
        from sklearn.metrics import adjusted_rand_score
        for combo in combinations(np.arange(100), 2):
            compare_out = cmp.adjRand(tree_mat[:,combo[0]], tree_mat[:,combo[1]])
    elif compare_method == 'NMI':
        from sklearn.metrics import normalized_mutual_info_score
        for combo in combinations(np.arange(100), 2):
            compare_out = cmp.normalized_MI(tree_mat[:,combo[0]], tree_mat[:,combo[1]])
    else:
        print 'Where is your method?? \nFlaming... '+time.ctime()
        sys.exit(1)

    return compare_out