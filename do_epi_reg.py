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

    group_tcorr_dir = os.path.join(os.environ['hel'], 'tcorr_group')
    interpol = 'nn'
    for ss in subj_list:
        proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        wholet1 = os.path.join(anat_dir, 'T1_biascorr.nii.gz')
        extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')

        premat = os.path.join(anat_dir, '%s_gm_mask_frac_bin_flirted.mat' % ss)
        epi_nii_pref = 'tcorr_prsn_%s_gm_mskd_Z' % ss
        in_fl = os.path.join(proc_dir, '%s.nii.gz' % epi_nii_pref)
        out_fl = os.path.join(proc_dir, '%s_flirted' % epi_nii_pref)
        gp.applywarpFLIRT(ss, proc_dir, in_fl, extrt1,
                          out_fl, premat)

        fn_coef = os.path.join(anat_dir,
                               'T1_to_MNI_nonlin_coeff.nii.gz')
        in_fn = '%s.nii.gz' % out_fl
        out_fn = os.path.join(group_tcorr_dir,
                              '%s_fnirted_MNI2mm' % epi_nii_pref)
        gp.applywarpFNIRT(ss, group_tcorr_dir, in_fn, out_fn,
                          fn_coef)
