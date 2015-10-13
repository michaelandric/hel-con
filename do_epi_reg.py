# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:01:31 2015

@author: andric
"""

import os
import general_procedures as gp


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 19):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    graph_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    conn_dir = os.path.join(os.environ['hel'], 'ccf_cor')

    t_dict = {'vals': 'trilinear', 'lag': 'nn'}
    for ss in subj_list:
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        wholet1 = os.path.join(anat_dir, 'T1_biascorr.nii.gz')
        extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')

        premat = os.path.join(anat_dir,
                              '%s_gm_mask_frac_bin_flirted.mat' % ss)
        for lb in t_dict:
            epi_nii_pref = os.path.join(conn_dir,
                                        'ccf_abs_%s_out_%s_gm_mskd.ijk' % (lb, ss))
            gp.converttoNIFTI(conn_dir, '%s+orig' % epi_nii_pref,
                              epi_nii_pref)
            in_fl = '%s.nii.gz' % epi_nii_pref
            out_fl = '%s_flirted' % epi_nii_pref
            gp.applywarpFLIRT(ss, conn_dir, in_fl, extrt1,
                              out_fl, premat, t_dict[lb])

            fn_coef = os.path.join(anat_dir,
                                   'T1_to_MNI_nonlin_coeff.nii.gz')
            in_fn = '%s.nii.gz' % out_fl
            out_fn = '%s_fnirted_MNI2mm' % epi_nii_pref
            gp.applywarpFNIRT(ss, conn_dir, in_fn, out_fn,
                              fn_coef, t_dict[lb])
