# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 12:27:17 2015
Make group gray matter mask
@author: andric
"""

import os
import general_procedures as gp

if __name__ == '__main__':
    subj_list = []
    for i in range(1, 19):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    for ss in ['hel1']:
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        epi_nii_pref = os.path.join(anat_dir, 'hel1_GMmask')
        epi_in_pref = '%s+orig' % epi_nii_pref
        gp.converttoNIFTI(anat_dir, epi_in_pref, epi_nii_pref)

        in_fn = '%s.nii.gz' % epi_nii_pref
        out_fn = '%s_fnirted_MNI2mm' % (epi_nii_pref)
        fn_coef = os.path.join(anat_dir,
                               'T1_to_MNI_nonlin_coeff.nii.gz')
        gp.applywarpFNIRT(ss, anat_dir, in_fn, out_fn, fn_coef, 'nn')
