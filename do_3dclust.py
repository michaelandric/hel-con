# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 15:06:08 2015.

@author: andric
"""

import os
from setlog import setup_log
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def clust_msk(log, infile, thresh, vxl, outmskpref):
    """Cluster correct a stat result."""
    clst_info = open('%s.txt' % outmskpref, 'w')
    cmdargs = "3dclust -1Dformat -nosum -1dindex 1 -1tindex 1 \
                -2thresh -%.3f %.3f -dxyz=1 \
                -savemask %s 1.44 %.1f %s" % \
              (thresh, thresh, outmskpref, vxl, infile)
    log.info('cmd: \n%s', cmdargs)
    proc = Popen(cmdargs)
    outs, errs = proc.communicate()
    log.warning(errs)
    clst_info.write(outs)
    clst_info.close()


def thresh_clust(log, msk, infile, outfilepref):
    """Create masked thresholded map."""
    log.info('Doing thresh_clust')
    tcargs = split("3dcalc -a %s -b '%s[1]' -expr 'ispositive(a)*b*-1' \
        -prefix %s" % (msk, infile, outfilepref))
    log.info('cmd args: \n%s', tcargs)
    proc = Popen(tcargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


if __name__ == '__main__':

    THRESH_DICT = {2.898: 234}
    WORKDIR = os.path.join(os.environ['hel'], 'graph_analyses/behav_correlate')
    LOGFILE = setup_log(os.path.join(WORKDIR, 'clust_msk'))
    LOGFILE.info('Doing clustering')
    SEED_PREFS = ['lh_highlevel', 'lh_ttg', 'lh_vis_ctx']

    for thr in THRESH_DICT:
        for seed in SEED_PREFS:
            out_conv_corr = os.path.join(WORKDIR,
                                         'wgc_diff_{}_corr_tvals'.format(seed))
            clust_msk(LOGFILE, '{}+tlrc'.format(out_conv_corr),
                      thr, THRESH_DICT[thr], '{}_mask'.format(out_conv_corr))
            out_thr_clust = '{}_{}_{}'.format(out_conv_corr,
                                              thr, THRESH_DICT[thr])
            thresh_clust(LOGFILE, '{}_mask+tlrc'.format(out_conv_corr),
                         '{}+tlrc'.format(out_conv_corr), out_thr_clust)
