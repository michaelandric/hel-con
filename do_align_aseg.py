# -*- coding: utf-8 -*-
"""
Created on Wed May 11 18:44:32 2016

@author: andric
"""

import os
from shlex import split
from subprocess import call
from subprocess import STDOUT

def aseg_align(anat, transmat, aseg, outname):
    """Aligning the freesurfer segmentation in the volume
    to the EPI data"""
    stdf = open('stdout_files/stdout_from_asegalign.txt', 'w')
    cmdargs = split('3dAllineate -master {} -1Dmatrix_apply {} \
                    -input {} -prefix {}'.format(anat, transmat, aseg, outname))
    call(cmdargs, stdout=stdf, stderr=STDOUT)
    stdf.close()

def main():
    """calling the aseg_align as main"""
    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]
    for subject in subj_list:
        subject_dir = os.path.join(os.environ['hel'], subject)
        aseg = os.path.join(subject_dir,
                            'freesurfer_{ss}/{ss}/SUMA'.format(ss=subject),
                            'aparc.a2009s+aseg_rank.nii')
        anat = os.path.join(subject_dir, 'volume.{}.nii.gz'.format(subject))
        transmat = os.path.join(subject_dir, 'preprocessing',
                                '{}_SurfVol_Alnd_Exp.A2E.1D'.format(subject))
        outname = os.path.join(subject_dir, 'preprocessing',
                               'aparc.a2009s+aseg_rank_{}_allin'.format(subject))
        aseg_align(anat, transmat, aseg, outname)


if __name__ == '__main__':
    main()
