# -*- coding: utf-8 -*-
"""
Created on Wed May 11 18:44:32 2016.

@author: andric
"""

import os
from shlex import split
from subprocess import call
from subprocess import STDOUT


def aseg_align(anat, transmat, aseg, outname):
    """Aligning the freesurfer segmentation.

    Volume to the EPI data.
    """
    stdf = open('stdout_files/stdout_from_asegalign.txt', 'w')
    cmdargs = split('3dAllineate -master {} -1Dmatrix_apply {} \
                    -input {} -prefix {} \
                    -final NN'.format(anat, transmat, aseg, outname))
    call(cmdargs, stdout=stdf, stderr=STDOUT)
    stdf.close()


def resampler(tcorr_dat, aparc_name):
    """Resample from anat to epi space."""
    stdf = open('stdout_files/stdout_from_resampler.txt', 'w')
    cmdargs = split('3dresample -master {} -rmode NN -input {}+orig \
                    -prefix {}_resamp'.format(tcorr_dat, aparc_name,
                    aparc_name))
    call(cmdargs, stdout=stdf, stderr=STDOUT)
    stdf.close()


def main():
    """calling the aseg_align as main."""
    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]
    for subject in subj_list:
        if subject == 'hel1' or subject == 'hel2' or subject == 'hel3':
            year = 2005
        else:
            year = 2009
        subject_dir = os.path.join(os.environ['hel'], subject)
        aseg = os.path.join(os.environ['hel'], 'freesurfdir',
                            '{}/SUMA'.format(subject),
                            'aparc.a{}s+aseg_rank.nii.gz'.format(year))
        anat = os.path.join(subject_dir, 'volume.{}.nii.gz'.format(subject))
        transmat = os.path.join(subject_dir, 'preprocessing',
                                '{}_SurfVol_Alnd_Exp.A2E.1D'.format(subject))
        outname = os.path.join(subject_dir, 'preprocessing',
                               'aparc.a{}s+aseg_rank_{}_allin'.format(
                                year, subject))
        aseg_align(anat, transmat, aseg, outname)

        tcorr_dat = os.path.join(subject_dir, 'preprocessing',
                                 'tcorr_prsn_{}_gm_mskd_Z+orig'.format(
                                    subject))
        resampler(tcorr_dat, outname)


if __name__ == '__main__':
    main()
