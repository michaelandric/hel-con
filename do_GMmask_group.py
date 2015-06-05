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

    grp_dir = '%s/group_anat' % os.environ['hel']
    if not os.path.exists(grp_dir):
        os.makedirs(grp_dir)

    subj_masks = []
    for ss in subj_list:
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        epi_nii_pref = os.path.join(anat_dir, '%s_GMmask' % ss)
        epi_in_pref = '%s+orig' % epi_nii_pref
        gp.converttoNIFTI(anat_dir, epi_in_pref, epi_nii_pref)

        in_fn = '%s.nii.gz' % epi_nii_pref
        out_fn = '%s_fnirted_MNI2mm' % (epi_nii_pref)
        fn_coef = os.path.join(anat_dir,
                               'T1_to_MNI_nonlin_coeff.nii.gz')
#        gp.applywarpFNIRT(ss, anat_dir, in_fn, out_fn, fn_coef, 'nn')

        ss_msk = '%s_GMmask_fnirted_MNI2mm.nii.gz' % ss
        subj_masks.append(os.path.join(anat_dir, ss_msk))
        subj_masks_in = ' '.join(subj_masks)
    grp_msk_pref = 'group_avg_GMmask_fnirted_MNI2mm'
    grp_msk_fname = os.path.join(grp_dir, grp_msk_pref)
    gp.avgepis('group', subj_masks, grp_dir, grp_msk_fname)

    in_frac_fname = '%s+orig' % grp_msk_fname
    out_frac_pref = '%s_frac' % grp_msk_fname
    template = '%s/data/standard/MNI152_T1_2mm.nii.gz' % os.environ['hel']
    gp.fractionize(grp_dir, in_frac_fname, out_frac_pref, template)
