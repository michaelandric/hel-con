# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:01:31 2015

@author: andric
"""

import os
import general_procedures as gp


if __name__ == '__main__':
    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]

    graph_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    thresh_dens = .15
    for ss in subj_list:
        anat_dir = os.path.join(os.environ['hel'], ss,
                                'volume.{}.anat'.format(ss))

        wholet1 = os.path.join(anat_dir, 'T1_biascorr.nii.gz')
        extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')

        premat = os.path.join(anat_dir,
                              '{}_gm_mask_frac_bin_flirted.mat'.format(ss))
        mod_dir = os.path.join(graph_dir, ss, 'subrun_modularity')
        
        for session in ['first', 'second']:
            epi_nii_pref = os.path.join(mod_dir,
                                        'task_{}_{}.dens_{}.maxq_tree.ijk'.format(
                                        session, ss, thresh_dens))
            
            gp.converttoNIFTI('{}+orig'.format(epi_nii_pref),
                              epi_nii_pref)
            in_fl = '{}.nii.gz'.format(epi_nii_pref)
            out_fl = '{}_flirted'.format(epi_nii_pref)
            gp.applywarpFLIRT(ss, mod_dir, in_fl, extrt1,
                              out_fl, premat, 'nearestneighbour')

            fn_coef = os.path.join(anat_dir,
                                   'T1_to_MNI_nonlin_coeff.nii.gz')
            in_fn = '{}.nii.gz'.format(out_fl)
            out_fn = '{}_fnirted_MNI2mm'.format(epi_nii_pref)
            gp.applywarpFNIRT(ss, mod_dir, in_fn, out_fn,
                              fn_coef, 'nn')
