# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 14:35:31 2015

@author: andric
"""

import os
import general_procedures as gp


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 19):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    for ss in subj_list:
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        stdout_dir = os.path.join(anat_dir, 'stdout_files')
        matfile = os.path.join(anat_dir,
                               '%s_gm_mask_frac_bin_flirted.mat' % ss)
        inv_mat = os.path.join(anat_dir,
                               '%s_gm_mask_frac_bin_flirted_inv.mat' % ss)
        out_invwarp = os.path.join(anat_dir, '%s_out_invwarp.nii.gz' % ss)
        flrtd_brain = os.path.join(anat_dir,
                                   '%s_gm_mask_frac_bin_flirted.nii.gz' % ss)
        reg_msk = os.path.join(os.environ['hel'], 'graph_analyses',
                               'group_global_connectivity',
                               'Clust_mask.nii.gz')
        coeff = os.path.join(anat_dir, 'T1_to_MNI_nonlin_coeff.nii.gz')
        msk_out_pref = '%s_Clust_msk_glob_conn' % ss
        region_msk_out_flirt = os.path.join(anat_dir, '%s_flrtspace.nii.gz'
                                            % msk_out_pref)
        region_msk_out_orig = os.path.join(anat_dir, '%s_origspace.nii.gz'
                                           % msk_out_pref)
        msk_frac_bin_orig = os.path.join(anat_dir,
                                         '%s_gm_mask_frac_bin.nii.gz' % ss)
        final_msk_outpref = os.path.join(anat_dir,
                                         '%s_origspace.txt' % msk_out_pref)
        gp.mnispace_to_origspace(stdout_dir, matfile, inv_mat, out_invwarp,
                                 flrtd_brain, reg_msk, coeff,
                                 region_msk_out_flirt, region_msk_out_orig,
                                 msk_frac_bin_orig, final_msk_outpref)
