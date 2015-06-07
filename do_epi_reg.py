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

    top_dir = '%s/graph_analyses' % os.environ['hel']
    interpol = 'nn'
    for ss in subj_list:
        proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
        mod_dir = os.path.join(top_dir, '%s/modularity' % ss)
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        wholet1 = os.path.join(anat_dir, 'T1_biascorr.nii.gz')
        extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')
#        gp.converttoNIFTI(proc_dir, epi_brain, epi_nii_pref)

        premat = os.path.join(anat_dir, '%s_GMmask_frac_bin_flirted.mat' % ss)
        for session in range(1, 3):
            for thresh_dens in [.05, .10, .15, .20]:
                epi_nii_pref = '%s/task_sess_%d_%s.dens_%s.maxq_tree.ijk' % \
                    (mod_dir, session, ss, thresh_dens)
                in_fl = '%s.nii.gz' % epi_nii_pref
                out_fl = '%s_flirted' % epi_nii_pref
                gp.applywarpFLIRT(ss, mod_dir, in_fl, extrt1,
                                  out_fl, premat, interpol)
                fn_coef = os.path.join(anat_dir,
                                       'T1_to_MNI_nonlin_coeff.nii.gz')
                in_fn = '%s.nii.gz' % out_fl
                out_fn = '%s_fnirted_MNI2mm' % (epi_nii_pref)
                gp.applywarpFNIRT(ss, mod_dir, in_fn, out_fn,
                                  fn_coef, interpol)
