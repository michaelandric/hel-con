# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:01:31 2015

@author: andric
"""

import os
import general_procedures as gp


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

#    for ss in subj_list:
    for ss in ['hel19']:
        proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
        epi_brain = "'%s/pb02_%sr06_ricorTS+orig[241]'" % (proc_dir, ss)
        epi_nii_pref = '%s/pb02_%s_regslice' % (proc_dir, ss)
        gp.converttoNIFTI(proc_dir, epi_brain, epi_nii_pref)

        epi = '%s.nii.gz' % epi_nii_pref
        anat_dir = os.path.join(os.environ['hel'], 'volume.%s.anat' % ss)
        wholet1 = os.path.join(anat_dir, 'T1_biascorr.nii.gz')
        extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')
        epi_reg_out = os.path.join(anat_dir, 'epi2anat_%s_reg' % ss)
        gp.epi_reg(ss, anat_dir, epi, wholet1, extrt1, epi_reg_out)
