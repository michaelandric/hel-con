# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:55:40 2015

@author: andric
"""

import os
import general_procedures as gp


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    top_dir = '%s/graph_analyses' % os.environ['hel']

    for ss in subj_list:
        conn_dir = os.path.join(top_dir, '%s/global_connectivity' % ss)
        ss_deg_dir = os.path.join(top_dir, '%s/degrees' % ss)
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        ijk_name = os.path.join(anat_dir,
                                '%s_GMmask_frac_bin_ijk.txt' % ss)
        master_file = os.path.join(anat_dir, '%s_GMmask_frac_bin+orig' % ss)
        for session in range(1, 3):
            agc_name = 'avg_corrZ_task_sess_%d_%s' % (session, ss)
            agc_fname = os.path.join(conn_dir, agc_name)
            gp.undump(ss, ijk_name, agc_fname, conn_dir, master_file)

        """for thresh_dens in [.05, .10, .15, .20]:
            for session in range(1, 3):
                deg_name = 'task_sess_%d_%s.dens_%s.degrees.txt' % \
                    (session, ss, thresh_dens)
                deg_fname = os.path.join(ss_deg_dir, deg_name)
                gp.undump(ss, ijk_name, deg_fname, ss_deg_dir, master_file)
        """
