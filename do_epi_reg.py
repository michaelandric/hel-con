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

    for ss in subj_list:
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        wholet1 = os.path.join(anat_dir, 'T1_biascorr.nii.gz')
        extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')

        premat = os.path.join(anat_dir,
                              '%s_gm_mask_frac_bin_flirted.mat' % ss)
        
        deg_dir = os.path.join(graph_dir, ss, 'degrees')
        for i in range(1, 3):
            for thr in [.05, .1, .15, .2]:
                epi_nii_pref = os.path.join(deg_dir,
                                            'task_sess_%s_%s.dens_%s.degrees.txt.ijk' %
                                            (i, ss, thr))
                gp.converttoNIFTI(deg_dir, '%s+orig' % epi_nii_pref,
                                  epi_nii_pref)
                in_fl = '%s.nii.gz' % epi_nii_pref
                out_fl = '%s_flirted' % epi_nii_pref
                gp.applywarpFLIRT(ss, deg_dir, in_fl, extrt1,
                                  out_fl, premat, 'nn')
    
                fn_coef = os.path.join(anat_dir,
                                       'T1_to_MNI_nonlin_coeff.nii.gz')
                in_fn = '%s.nii.gz' % out_fl
                out_fn = '%s_fnirted_MNI2mm' % epi_nii_pref
                gp.applywarpFNIRT(ss, deg_dir, in_fn, out_fn,
                                  fn_coef, 'nn')
