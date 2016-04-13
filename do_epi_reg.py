# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:01:31 2015

@author: andric
"""

import os
import general_procedures as gp


if __name__ == '__main__':
    subj_list = ['hel{}'.format(i) for i in range(1, 20)]
    subj_list.remove('hel9')   # because this is bad subj

    graph_dir = os.path.join(os.environ['hel'], 'graph_analyses')

    for ss in subj_list:
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        wholet1 = os.path.join(anat_dir, 'T1_biascorr.nii.gz')
        extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')

        premat = os.path.join(anat_dir,
                              '{}_gm_mask_frac_bin_flirted.mat'.format(ss))
        
        conn_dir = os.path.join(graph_dir,
                                '{}/single_run_global_connectivity'.format(ss))

        first_name = os.path.join(conn_dir,
                                  'avg_corrZ_task_runs1and3_{}.ijk'.format(ss))
        second_name = os.path.join(conn_dir,
                                   'avg_corrZ_task_runs4and6_{}.ijk'.format(ss))

        name_list = [first_name, second_name]
        for epi_nii_pref in name_list:
            gp.converttoNIFTI(conn_dir, '{}+orig'.format(epi_nii_pref),
                              epi_nii_pref)
            in_fl = '{}.nii.gz'.format(epi_nii_pref)
            out_fl = '{}_flirted'.format(epi_nii_pref)
            gp.applywarpFLIRT(ss, conn_dir, in_fl, extrt1,
                              out_fl, premat, 'trilinear')

            fn_coef = os.path.join(anat_dir,
                                   'T1_to_MNI_nonlin_coeff.nii.gz')
            in_fn = '{}.nii.gz'.format(out_fl)
            out_fn = '{}_fnirted_MNI2mm'.format(epi_nii_pref)
            gp.applywarpFNIRT(ss, conn_dir, in_fn, out_fn,
                              fn_coef, 'trilinear')
