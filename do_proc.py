# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:55:40 2015

@author: andric
"""

import os
import general_procedures as gp


if __name__ == '__main__':

    subj_list = ['hel{}'.format(i) for i in range(1, 20)]
    subj_list.remove('hel9')   # because this is bad subj

    top_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    for ss in subj_list:
        vol_dir_pref = '{}/volume.{}.anat'.format(ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        conn_dir = os.path.join(top_dir,
                                '{}/single_run_global_connectivity'.format(ss))
        st_odir = os.path.join(conn_dir, 'stdout_dir')
        if not os.path.exists(st_odir):
            os.makedirs(st_odir)
        ijk_name = os.path.join(anat_dir,
                                '{}_gm_mask_frac_bin_ijk.txt'.format(ss))
        master_file = os.path.join(anat_dir,
                                   '{}_gm_mask_frac_bin.nii.gz'.format(ss))

        first_name = os.path.join(conn_dir,
                                  'avg_corrZ_task_runs1and3_{}'.format(ss))
        second_name = os.path.join(conn_dir,
                                   'avg_corrZ_task_runs4and6_{}'.format(ss))

        gp.undump(ss, ijk_name, first_name, conn_dir, master_file)
        gp.undump(ss, ijk_name, second_name, conn_dir, master_file)
