# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 13:06:28 2015

@author: andric
"""

import os
import time
import numpy as np
from shlex import split
from subprocess import call, STDOUT


def undump(subjid, ijk_coords, datafilename, data_dir, master_file):
    """
    :param subjid: Subject identifier
    :param ijk_coords: IJK coordinates. GIVE FULL PATH
    :param datafilename: name of the data file that you want to undump
    :param data_dir: File where the data live
    :param master_file: The master file for AFNI voxel resolution.
    GIVE FULL PATH
    Writes AFNI format Undumped file
    """
    print 'Doing undump... First pasting ijk to data'
    print time.ctime()
    ijkfile = np.loadtxt(ijk_coords)
    data = np.loadtxt(datafilename)
    data_ijk_outname = '%s.ijk' % datafilename
    np.savetxt(data_ijk_outname, np.column_stack([ijkfile, data]),
               fmt='%i %i %i %.4f')

    stdout_dir = os.path.join(data_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    print 'Doing 3dUndump... %s' % time.ctime()
    f = open('%s/stdout_from_undump.txt' % stdout_dir, 'w')
    cmdargs = split('3dUndump -prefix %s -ijk \
                    -datum %s -master %s %s' %
                    (data_ijk_outname, 'float',
                     master_file, data_ijk_outname))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()
    print 'Finished undump '
    print time.ctime()


def avgepis(ss, epi_list, work_dir, outpref):
    """
    Make average TS brain
    :param ss: Subject identifier
    :param epi_list: Include list of epis that you average over
    Writes to file a TS average brain
    """
    print 'Doing avgepis for %s -- ' % ss+time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_avgepis.txt' % stdout_dir, 'w')
    cmdargs = split('3dMean -prefix %s %s' % (outpref, epi_list))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def mean_epi(ss, infile, work_dir, outpref):
    """
    Average across TS mean brain to get one mean image.
    YOU SHOULD FIRST HAVE AN AVERAGE OF TS (MANY IMAGES)
    THIS IS WHAT YOU MAKE MEAN (ONE IMAGE).
    Serves registration purposes.
    :param ss: Subject identifier
    Writes to file AFNI mean brain (one image)
    """
    print 'Doing mean_epi for %s -- ' % ss
    print time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_mean_epi.txt' % stdout_dir, 'w')
    cmdargs = split('3dTstat -prefix %s -mean %s' % (outpref, infile))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def converttoNIFTI(work_dir, brain, prefix=None):
    """
    convert AFNI file to NIFTI
    """
    print 'Doing converttoNIFTI for %s -- ' % brain+time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_converttoNIFTI' % stdout_dir, 'w')
    if prefix is None:
        cmdargs = split('3dAFNItoNIFTI %s' % brain)
    elif prefix:
        cmdargs = split('3dAFNItoNIFTI -prefix %s %s' % (prefix, brain))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def epi_reg(ss, work_dir, epi, wholet1, extrt1, out):
    """
    Register epi to t1
    """
    print 'Doing epi_reg for %s -- ' % ss+time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_epireg.txt' % stdout_dir, 'w')
    cmdargs = split('epi_reg --epi=%s --t1=%s --t1brain=%s --out=%s' %
                    (epi, wholet1, extrt1, out))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def applywarpFLIRT(ss, work_dir, input, extrt1, out, premat, interp='nn'):
    """
    Warp via linear transformation via fsl FLIRT
    """
    print 'doing applywarpFLIRT for %s -- ' % ss+time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_applywarpFLIRT.txt' % stdout_dir, 'w')
    cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s --interp=%s' %
                    (input, extrt1, out, premat, interp))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def applywarpFNIRT(ss, work_dir, input, out, coeff, interp='nn'):
    """
    Warp via nonlinear transformation via fsl FNIRT
    """
    print 'Doing applywarpFNIRT for %s -- ' % ss+time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_applywarp.txt' % stdout_dir, 'w')
    cmdargs = split('applywarp -i %s \
                    -r %s/data/standard/MNI152_T1_2mm.nii.gz \
                    -o %s -w %s --interp=%s' %
                    (input, os.environ['FSLDIR'], out, coeff, interp))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()
