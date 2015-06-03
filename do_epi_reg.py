# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:01:31 2015

@author: andric
"""

import os
import general_procedures as gp


if __name__ == '__main__':
    subj_list = []
    for i in range(2, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj
    subj_list.remove('hel2')   # because already did hel2

    """subj_list = []
    for i in range(15, 20):
        subj_list.append('hel%d' % i)
    """

    top_dir = '%s/graph_analyses' % os.environ['hel']
    interpol = 'trilinear'
    for ss in ['hel1']:
        proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
        conn_dir = os.path.join(top_dir, '%s/global_connectivity' % ss)
        vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
        anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
        wholet1 = os.path.join(anat_dir, 'T1_biascorr.nii.gz')
        extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')
        epi_brain = "'%s/pb02_trim_despiked_%sr03+orig.[241]'" % (proc_dir, ss)
        epi_nii_pref = '%s/pb02_%s_regslice' % (proc_dir, ss)
#        gp.converttoNIFTI(proc_dir, epi_brain, epi_nii_pref)

        epi = '%s.nii.gz' % epi_nii_pref
        epi_reg_out = os.path.join(anat_dir, 'epi2anat_%s_reg' % ss)
        gp.epi_reg(ss, anat_dir, epi, wholet1, extrt1, epi_reg_out)

        for session in range(1, 3):
            epi_nii_pref = '%s/avg_corrZ_task_sess_%d_%s.ijk' % \
                (conn_dir, session, ss)
            epi_in_pref = '%s+orig' % epi_nii_pref
#            gp.converttoNIFTI(conn_dir, epi_in_pref, epi_nii_pref)

            in_fl = '%s.nii.gz' % epi_nii_pref
            premat = os.path.join(anat_dir, 'epi2anat_%s_reg.mat' % ss)
            out_fl = '%s_flirted_%s' % (epi_nii_pref, interpol)
#            gp.applywarpFLIRT(ss, anat_dir, in_fl,
#                              extrt1, out_fl, premat, interpol)

            in_fn = '%s.nii.gz' % out_fl
            out_fn = '%s_fnirted_MNI2mm_%s' % (epi_nii_pref, interpol)
            fn_coef = os.path.join(anat_dir, 'T1_to_MNI_nonlin_coeff.nii.gz')
#            gp.applywarpFNIRT(ss, anat_dir, in_fn,
#                              out_fn, fn_coef, interpol)
