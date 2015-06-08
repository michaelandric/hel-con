# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:50:07 2015

@author: andric
"""

import os
import sys
import time
import numpy as np
from subprocess import Popen, PIPE
from shlex import split
import graph_evals as ge
import general_procedures as gp


def snsc_evaluation(ss, density):
    """
    Get Single Node Set Consistency (SNSC) value
    """
    tree_suff = 'maxq_tree'
    mod_dir = os.path.join(top_dir, '%s/modularity' % ss)
    tree1_name = os.path.join(mod_dir,
                              'task_sess_%d_%s.dens_%s.%s' %
                              (1, ss, density, tree_suff))
    tree2_name = os.path.join(mod_dir,
                              'task_sess_%d_%s.dens_%s.%s' %
                              (2, ss, density, tree_suff))

    simil = ge.Similarity()
    return simil.snsc(tree1_name, tree2_name)


def median_simil_777filt(subj_list, thresh_dens, mask, nvox=157440):
    """
    Get median value across participants
    """
    def fltmedian(nr):
        if len(nr[nr == 777.]) / float(len(nr)) >= .5:
            return 777
        else:
            return np.median(nr[nr != 777])

    print 'Getting median at thresh %s' % thresh_dens
    print time.ctime()
    simil_vals = np.zeros((nvox, len(subj_list)))
    print simil_vals.shape
    print 'mask is \n%s' % mask
    dat_suff = 'ijk_fnirted_MNI2mm.nii.gz'
    for i, ss in enumerate(subj_list):
        simil_dir = '%s/graph_analyses/%s/snsc_res' % \
            (os.environ['hel'], ss)
        dat_name = 'snsc_%s_%s.%s' % (ss, thresh_dens, dat_suff)
        dat_fname = os.path.join(simil_dir, dat_name)
        cmdargs = split('3dmaskdump -mask %s %s' % (mask, dat_fname))
        dump_out = Popen(cmdargs, stdout=PIPE).communicate()
        out_dump = [dd for dd in dump_out[0].split('\n')]
        for n in xrange(len(out_dump)-1):
            simil_vals[n, i] = out_dump[n].split()[3]

    return np.apply_along_axis(fltmedian, axis=1, arr=simil_vals)


if __name__ == '__main__':

    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    top_dir = '%s/graph_analyses' % os.environ['hel']
    if not os.path.exists(top_dir):
        print 'What is going on here?'
        print 'Where is the top_dir?'
        sys.exit(1)
    group_dir = os.path.join(top_dir, 'group_snsc')
    if not os.path.exists(group_dir):
        os.makedirs(group_dir)

    for thresh_dens in [.05, .10, .15, .20]:
        for ss in subj_list:
            snsc_dir = os.path.join(top_dir, '%s/snsc_res' % ss)
            if not os.path.exists(snsc_dir):
                os.makedirs(snsc_dir)
            res = snsc_evaluation(ss, thresh_dens)
            snsc_out_pref = 'snsc_%s_%s' % (ss, thresh_dens)
            snsc_outf = os.path.join(snsc_dir, snsc_out_pref)
            np.savetxt(snsc_outf, res, fmt='%.4f')

            vol_dir_pref = '%s/volume.%s.anat' % (ss, ss)
            anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
            ijk_name = os.path.join(anat_dir,
                                    '%s_GMmask_frac_bin_ijk.txt' % ss)
            master_file = os.path.join(anat_dir,
                                       '%s_GMmask_frac_bin+orig' % ss)
            gp.undump(ss, ijk_name, snsc_outf, snsc_dir, master_file, 'float')

            epi_nii_pref = '%s.ijk' % snsc_outf
            epi_afni = '%s+orig' % epi_nii_pref
            gp.converttoNIFTI(snsc_dir, epi_afni, epi_nii_pref)

            extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')
            premat = os.path.join(anat_dir,
                                  '%s_GMmask_frac_bin_flirted.mat' % ss)
            in_fl = '%s.nii.gz' % epi_nii_pref
            out_fl = '%s_flirted' % epi_nii_pref
            gp.applywarpFLIRT(ss, snsc_dir, in_fl, extrt1,
                              out_fl, premat)

            fn_coef = os.path.join(anat_dir,
                                   'T1_to_MNI_nonlin_coeff.nii.gz')
            in_fn = '%s.nii.gz' % out_fl
            out_fn = '%s_fnirted_MNI2mm' % (epi_nii_pref)
            gp.applywarpFNIRT(ss, snsc_dir, in_fn, out_fn,
                              fn_coef)

        # now getting median value across all ss
        mask_dir = '%s/group_anat' % (os.environ['hel'])
        mask_pref = 'group_avg_GMmask_frac_bin_fnirted_MNI2mm_thr0.34'
        mask_fname = os.path.join(mask_dir, '%s.nii.gz' % mask_pref)
        group_simil = median_simil_777filt(subj_list, thresh_dens, mask_fname)

        group_out_name = 'snsc_group_median_dens_%s' % thresh_dens
        group_out_fname = os.path.join(group_dir, group_out_name)
        np.savetxt(group_out_fname, group_simil, fmt='%.4f')

        ijk_n = '%s_ijk.txt' % mask_pref
        ijk_f = os.path.join(mask_dir, ijk_n)
        gp.undump('group', ijk_f, group_out_fname,
                  group_dir, mask_fname, 'float')
