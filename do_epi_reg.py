# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:01:31 2015

@author: andric
"""

import os
import numpy as np
import general_procedures as gp


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 19):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    graph_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    for cl in [2, 3]:
        maskfname = 'consensus_prtn_knnward_clst%d_mskd' % cl
        maskf = os.path.join(graph_dir, 'group_global_connectivity',
                             maskfname)
        msk = np.loadtxt(maskf)
        subclusters = np.unique(msk[msk != 0])

        for ss in subj_list:
            conn_dir = os.path.join(graph_dir, '%s/global_connectivity' % ss)
            proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
            vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
            anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
            wholet1 = os.path.join(anat_dir, 'T1_biascorr.nii.gz')
            extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')

            premat = os.path.join(anat_dir,
                                  '%s_gm_mask_frac_bin_flirted.mat' % ss)
            for session in range(1, 3):
                for clst in subclusters:
                    epi_pref = 'knnward_clst%d_mskd_subclust%d_corrZ_sess_%s_%s.ijk' % \
                               (cl, clst, session, ss)
                    epi_nii_pref = os.path.join(conn_dir, epi_pref)
                    gp.converttoNIFTI(conn_dir, '%s+orig' % epi_nii_pref,
                                      epi_nii_pref)
                    in_fl = os.path.join(proc_dir, '%s.nii.gz' % epi_nii_pref)
                    out_fl = os.path.join(proc_dir, '%s_flirted' % epi_nii_pref)
                    gp.applywarpFLIRT(ss, proc_dir, in_fl, extrt1,
                                      out_fl, premat)

                    fn_coef = os.path.join(anat_dir,
                                           'T1_to_MNI_nonlin_coeff.nii.gz')
                    in_fn = '%s.nii.gz' % out_fl
                    out_fn = os.path.join(conn_dir,
                                          '%s_fnirted_MNI2mm' % epi_nii_pref)
                    gp.applywarpFNIRT(ss, conn_dir, in_fn, out_fn,
                                      fn_coef)
