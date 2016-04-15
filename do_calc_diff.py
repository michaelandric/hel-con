# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 16:10:25 2015

Update Apr 15 2016 - Using to get
diff between runs

@author: andric
"""

import os
import logging
from shlex import split
from subprocess import call

def calc(input1, input2, outpref):
    """
    3dcalc -a Corr_subj01R+tlrc -expr 'atanh(a)' -prefix Corr_subj01_Z
    """
    logging.info('Doing 3dcalc for %s' % outpref)
    cmd = split("3dcalc -a {} -b {} -expr 'a-b' -prefix {}".format(input1,
                input2, outpref))
    call(cmd)


if __name__ == '__main__':
    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]

    sfx = 'ijk_fnirted_MNI2mm.nii.gz'
    for ss in subj_list:
        conn_dir = os.path.join(os.environ['hel'], 'graph_analyses',
                                '{}/single_run_global_connectivity'.format(ss))
        logging.basicConfig(filename=os.path.join(conn_dir, 'calc_diff.log'),
                            level=logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        f1 = os.path.join(conn_dir, 'avg_corrZ_task_r01_{}.{}'.format(ss, sfx))
        f3 = os.path.join(conn_dir, 'avg_corrZ_task_r03_{}.{}'.format(ss, sfx))
        calc(f1, f3, os.path.join(conn_dir, 'diff_avg_corrZ_task_runs1and3'))

        f4 = os.path.join(conn_dir, 'avg_corrZ_task_r04_{}.{}'.format(ss, sfx))
        f6 = os.path.join(conn_dir, 'avg_corrZ_task_r06_{}.{}'.format(ss, sfx))        
        calc(f4, f6, os.path.join(conn_dir, 'diff_avg_corrZ_task_runs4and6'))

    logging.info('3dcalc done')
