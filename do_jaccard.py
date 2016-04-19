# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 13:51:22 2015

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


def jacc_evaluation(ss, density):
    """
    Get Jaccard similarity coefficient
    """
    tree_suff = 'maxq_tree'
    mod_dir = os.path.join(top_dir, ss, 'subrun_modularity')
    tree1_name = os.path.join(mod_dir,
                              'task_{}_{}.dens_{}.{}'.format(
                              'first', ss, density, tree_suff))
    tree2_name = os.path.join(mod_dir,
                              'task_{}_{}.dens_{}.{}'.format(
                              'second', ss, density, tree_suff))

    simil = ge.Similarity()
    return simil.jaccard_vw(tree1_name, tree2_name)


def median_simil_777filt(subj_list, thresh_dens, mask, nvox=185456):
    """
    Get median value across participants
    """
    def fltmedian(nr):
        if len(nr[nr == 777.]) / float(len(nr)) >= .5:
            return 777
        else:
            return np.median(nr[nr != 777])

    print ('Getting median at thresh {}'.format(thresh_dens))
    print (time.ctime())
    simil_vals = np.zeros((nvox, len(subj_list)))
    print (simil_vals.shape)
    print ('mask is \n{}'.format(mask))
    dat_suff = 'ijk_fnirted_MNI2mm.nii.gz'
    for i, ss in enumerate(subj_list):
        simil_dir = '{}/graph_analyses/{}/subrun_jaccard_res'.format(
            os.environ['hel'], ss)
        dat_name = 'jacc_{}_{}.{}'.format(ss, thresh_dens, dat_suff)
        dat_fname = os.path.join(simil_dir, dat_name)
        cmdargs = split('3dmaskdump -mask {} {}'.format(mask, dat_fname))
        dump_out = Popen(cmdargs, stdout=PIPE).communicate()
        out_dump = [dd for dd in dump_out[0].split('\n')]
        for n in range(len(out_dump)-1):
            simil_vals[n, i] = out_dump[n].split()[3]

    return np.apply_along_axis(fltmedian, axis=1, arr=simil_vals)


if __name__ == '__main__':

    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]

    top_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    if not os.path.exists(top_dir):
        print ('Where is the top_dir?')
        sys.exit(1)
    group_dir = os.path.join(top_dir, 'subrun_group_jaccard')
    if not os.path.exists(group_dir):
        os.makedirs(group_dir)

    for thresh_dens in [.15]:
        for ss in subj_list:
            indiv_res_dir = os.path.join(ss, 'subrun_jaccard_res')
            simil_dir = os.path.join(top_dir, indiv_res_dir)
            if not os.path.exists(simil_dir):
                os.makedirs(simil_dir)
            res = jacc_evaluation(ss, thresh_dens)
            simil_out_pref = 'jacc_{}_{}'.format(ss, thresh_dens)
            simil_outf = os.path.join(simil_dir, simil_out_pref)
            np.savetxt(simil_outf, res, fmt='%.4f')

            vol_dir_pref = os.path.join(ss, 'volume.{}.anat'.format(ss))
            anat_dir = os.path.join(os.environ['hel'], vol_dir_pref)
            ijk_name = os.path.join(anat_dir,
                                    '{}_gm_mask_frac_bin_ijk.txt'.format(ss))
            master_file = os.path.join(anat_dir,
                                       '{}_gm_mask_frac_bin.nii.gz'.format(ss))
            gp.undump(ss, ijk_name, simil_outf, simil_dir,
                      master_file, 'float')

            epi_nii_pref = '{}.ijk'.format(simil_outf)
            epi_afni = '{}+orig'.format(epi_nii_pref)
            gp.converttoNIFTI(simil_dir, epi_afni, epi_nii_pref)

            extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')
            premat = os.path.join(anat_dir,
                                  '{}_gm_mask_frac_bin_flirted.mat'.format(ss))
            in_fl = '{}.nii.gz'.format(epi_nii_pref)
            out_fl = '{}_flirted'.format(epi_nii_pref)
            gp.applywarpFLIRT(ss, simil_dir, in_fl, extrt1,
                              out_fl, premat)

            fn_coef = os.path.join(anat_dir,
                                   'T1_to_MNI_nonlin_coeff.nii.gz')
            in_fn = '{}.nii.gz'.format(out_fl)
            out_fn = '{}_fnirted_MNI2mm'.format(epi_nii_pref)
            gp.applywarpFNIRT(ss, simil_dir, in_fn, out_fn,
                              fn_coef)

        # now getting median value across all ss
        mask_dir = os.path.join(os.environ['hel'], 'group_anat')
        mask_pref = 'group_avg_gm_mask_frac_bin_fnirted_MNI2mm_thr0.34'
        mask_fname = os.path.join(mask_dir, '{}.nii.gz'.format(mask_pref))
        group_simil = median_simil_777filt(subj_list, thresh_dens, mask_fname)

        group_out_name = 'jaccard_group_median_dens_{}'.format(thresh_dens)
        group_out_fname = os.path.join(group_dir, group_out_name)
        np.savetxt(group_out_fname, group_simil, fmt='%.4f')

        ijk_n = '{}_ijk.txt'.format(mask_pref)
        ijk_f = os.path.join(mask_dir, ijk_n)
        gp.undump('group', ijk_f, group_out_fname,
                  group_dir, mask_fname, 'float')
