# -*- coding: utf-8 -*-
"""
Created on Thu May 28 16:13:53 2015

@author: andric
"""

import os
import sys
import time
from shlex import split
from subprocess import call, STDOUT


def blur_fwhm(stdout_dir, in_pref, out_pref, fwhm):
    """
    """
    f = open('%s/stdout_from_3dmerge.txt' % stdout_dir, 'w')
    cmdargs = split('3dmerge -1blur_fwhm %s -doall \
        -datum float -prefix %s %s+orig' % (fwhm, out_pref, in_pref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def resample(stdout_dir, in_pref, out_pref):
    f = open('%s/stdout_from_3dresample.txt' % stdout_dir, 'w')
    cmdargs = split("3dresample -dxyz 4.0 4.0 4.0 -prefix %s \
        -rmode 'Li' -inset %s+orig" % (out_pref, in_pref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def fractionize(stdout_dir, in_pref, out_pref, template):
    f = open('%s/stdout_from_3dfractionize.txt' % stdout_dir, 'w')
    cmdargs = split('3dfractionize -template %s+orig -input %s+orig \
        -prefix %s -clip 0.5' % (template, in_pref, out_pref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def mask_binary(stdout_dir, in_pref, out_pref):
    f = open('%s/stdout_from_mask_binary.txt' % stdout_dir, 'w')
    cmdargs = split("3dcalc -a %s+orig -expr 'ispositive(a)' \
        -prefix %s" % (in_pref, out_pref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def calc_masked_dat(stdout_dir, a_pref, b_pref, out_pref):
    f = open('%s/stdout_from_calc_masked_dat.txt' % stdout_dir, 'w')
    cmdargs = split("3dcalc -a %s+orig -b %s+orig \
        -expr 'a*b' -datum float \
        -prefix %s" % (a_pref, b_pref, out_pref))
    call(cmdargs, stdout=f, stderr=STDOUT)


if __name__ == '__main__':

    subj_list = ['hel19']
    for ss in subj_list:
        print 'Doing subject %s' % ss
        print time.ctime()
        preproc_dir = os.path.join(os.environ['hel'],
                                   '%s/preprocessing/' % ss)
        if not os.path.exists(preproc_dir):
            print 'Problem with paths.'
            print 'Shut down!'
            sys.exit(1)

        stdout_dir = os.path.join(preproc_dir, 'stdout_files/')
        if not os.path.exists(stdout_dir):
            os.makedirs(stdout_dir)

        func_dat_pref = os.path.join(preproc_dir, 'cleanTS_%sr01' % ss)
        fwhm_size = '4.0'
        out_blur_pref = '%s_smth4mm' % func_dat_pref
        blur_fwhm(stdout_dir, func_dat_pref, out_blur_pref, fwhm_size)

        out_resample_pref = '%s_Liresamp4mm' % out_blur_pref
        resample(stdout_dir, out_blur_pref, out_resample_pref)

        anat_dir = os.path.join(os.environ['hel'],
                                '%s/volume.%s.anat' % (ss, ss))
        frac_in_pref = os.path.join(anat_dir, '%s_GMmask' % ss)
        frac_out_pref = '%s_frac' % frac_in_pref
        fractionize(stdout_dir, frac_in_pref, frac_out_pref, out_resample_pref)

        binary_out_pref = '%s_bin' % frac_out_pref
        mask_binary(stdout_dir, frac_out_pref, binary_out_pref)

        calc_mask_a = binary_out_pref
        calc_mask_out_pref = '%s_mskd' % out_resample_pref
        calc_masked_dat(stdout_dir, calc_mask_a,
                        out_resample_pref, calc_mask_out_pref)

        for i in range(2, 7):
            print 'Doing %s -- run %s ' % (ss, i)
            print time.ctime()
            preproc_dir = os.path.join(os.environ['hel'],
                                       '%s/preprocessing/' % ss)
            if not os.path.exists(preproc_dir):
                print 'Problem with paths.'
                print 'Shut down!'
                sys.exit(1)

            stdout_dir = os.path.join(preproc_dir, 'stdout_files/')
            if not os.path.exists(stdout_dir):
                os.makedirs(stdout_dir)

            func_dat_pref = os.path.join(preproc_dir,
                                         'cleanTS_%sr0%s' % (ss, i))
            out_blur_pref = '%s_smth4mm' % func_dat_pref
            blur_fwhm(stdout_dir, func_dat_pref, out_blur_pref, fwhm_size)

            out_resample_pref = '%s_Liresamp4mm' % out_blur_pref
            resample(stdout_dir, out_blur_pref, out_resample_pref)

            calc_mask_out_pref = '%s_mskd' % out_resample_pref
            calc_masked_dat(stdout_dir, calc_mask_a,
                            out_resample_pref, calc_mask_out_pref)
