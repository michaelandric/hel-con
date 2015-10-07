# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 15:06:08 2015

@author: andric
"""

import os
import numpy as np
from subprocess import call, STDOUT


def clust_msk(stdoutdir, infile, thresh, vxl, outmskpref):
    """
    cluster correct a result
    """
    f = open('%s/stdout_files/stdout_from_3dclust.txt' % stdoutdir, 'w')
    clst1d = open('%s.txt' % outmskpref, 'w')
    cl_args = "3dclust -1Dformat -nosum -1dindex 1 -1tindex 1 \
                -2thresh -%.3f %.3f -dxyz=1 \
                -savemask %s 1.44 %.1f %s" % \
              (thresh, thresh, outmskpref, vxl, infile)
    call(cl_args, stdout=clst1d, stderr=f, shell=True)
    clst1d.close()
    f.close()


def thresh_clust(stdoutdir, msk, infile, outfilepref):
    """
    create masked thresholded map
    """
    f = open('%s/stdout_files/stdout_from_thresh_clust.txt' % stdoutdir, 'w')
    tc_args = "3dcalc -a %s -b '%s[1]' -expr 'ispositive(a)*b*-1' \
                -prefix %s" % (msk, infile, outfilepref)
    call(tc_args, stdout=f, stderr=STDOUT, shell=True)
    f.close()


if __name__ == '__main__':

    graph_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    conn_dir = os.path.join(graph_dir, 'group_global_connectivity')

#    thresh_dict = {2.898: 234}
    thresh_dict = {3.965: 71, 3.222: 156}

    for thr in thresh_dict:
        for cl in range(1, 4):
            maskfname = 'consensus_prtn_knnward_clst%d_mskd' % cl
            maskf = os.path.join(graph_dir, 'group_global_connectivity',
                                 maskfname)
            msk = np.loadtxt(maskf)
            subclusters = np.unique(msk[msk != 0])
            for clst in subclusters:
                inf = os.path.join(conn_dir,
                                   'knnward_clst%d_mskd_subclust%d_corrZ' %
                                   (cl, clst))
                omskpref = '%s_%s_%s_mask' % (inf, thr, thresh_dict[thr])
                clust_msk(conn_dir, '%s+tlrc' % inf,
                          thr, thresh_dict[thr], omskpref)
                out_thr_clust = '%s_%s_%s_vals' % (inf, thr, thresh_dict[thr])
                thresh_clust(conn_dir, '%s+tlrc' % omskpref,
                             '%s+tlrc' % inf, out_thr_clust)
