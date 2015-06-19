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


def undump(subjid, ijk_coords, datafilename, data_dir,
           master_file, dtype='short'):
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
    print 'Data type is %s' % dtype
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
                    (data_ijk_outname, dtype,
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


def flirt_solo(work_dir, epi, extrt1, wm_edge, epi_reg_out, interp=None):
    """
    Doing flirt
    """
    print 'doing flirt for %s -- ' % epi+time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_applywarpFLIRT.txt' % stdout_dir, 'w')
    if interp is None:
        cmdargs = split('flirt -in %s -ref %s -wmseg %s \
                    -omat %s.mat -o %s' %
                        (epi, extrt1, wm_edge, epi_reg_out, epi_reg_out))
    else:
        cmdargs = split('flirt -in %s -ref %s -wmseg %s \
                    -interp %s -omat %s.mat -o %s' %
                        (epi, extrt1, wm_edge, interp,
                         epi_reg_out, epi_reg_out))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close


def applywarpFLIRT(ss, work_dir, input, extrt1, out, premat, interp=None):
    """
    Warp via linear transformation via fsl FLIRT
    """
    print 'doing applywarpFLIRT for %s -- ' % ss+time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_applywarpFLIRT.txt' % stdout_dir, 'w')
    if interp is None:
        cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s' %
                        (input, extrt1, out, premat))
    else:
        cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s --interp=%s' %
                        (input, extrt1, out, premat, interp))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def applywarpFNIRT(ss, work_dir, input, out, coeff, interp=None):
    """
    Warp via nonlinear transformation via fsl FNIRT
    """
    print 'Doing applywarpFNIRT for %s -- ' % ss+time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_applywarp.txt' % stdout_dir, 'w')
    if interp is None:
        cmdargs = split('applywarp -i %s \
                        -r %s/data/standard/MNI152_T1_2mm.nii.gz \
                        -o %s -w %s' %
                        (input, os.environ['FSLDIR'], out, coeff))
    else:
        cmdargs = split('applywarp -i %s \
                        -r %s/data/standard/MNI152_T1_2mm.nii.gz \
                        -o %s -w %s --interp=%s' %
                        (input, os.environ['FSLDIR'], out, coeff, interp))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def fractionize(stdout_dir, in_pref, out_pref, template):
    f = open('%s/stdout_from_3dfractionize.txt' % stdout_dir, 'w')
    cmdargs = split('3dfractionize -template %s -input %s \
        -prefix %s -clip 0.5' % (template, in_pref, out_pref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def maskdump(stdout_dir, mask, in_pref, out_pref, noijk=True):
    outf = open(out_pref, 'w')
    f = open('%s/stdout_from_maskdump.txt' % stdout_dir, 'w')
    if noijk is True:
        cmdargs = split('3dmaskdump -mask %s -noijk %s' % (mask, in_pref))
    else:
        cmdargs = split('3dmaskdump -mask %s %s' % (mask, in_pref))
    call(cmdargs, stdout=outf, stderr=f)
    outf.close()
    f.close()


def get_ijk(outname, mask=None):
    print 'Getting IJK coordinates... '+time.ctime()
    if mask is None:
        print 'NOTT USING MASK. HUH?'
        call("3dmaskdump %s | awk '{print $1, $2, $3}' > %s" %
             (mask, outname), shell=True)
    else:
        print 'USING MASK: '+mask
        call("3dmaskdump -mask %s %s | awk '{print $1, $2, $3}' > %s" %
             (mask, mask, outname), shell=True)
    print 'DONE. '+time.ctime()


def vol2surf_mni(work_dir, hemi, parent, pn, outname):
    """
    Project to MNI surf.
    Make sure 'suma_dir' is set right
    """
    print 'Doing vol2surf_mni -- %s' % time.ctime()
    print os.getcwd()
    suma_dir = '/cnari/normal_language/apps/suma_MNI_N27'
    stdout_dir = '%s/stdout_files' % work_dir
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_vol2surf.txt' % stdout_dir, 'w')
    spec_fname = 'MNI_N27_%s.spec' % hemi
    spec = os.path.join(suma_dir, spec_fname)
    surf_a = '%s.smoothwm.gii' % hemi
    surf_b = '%s.pial.gii' % hemi
    surfvol_name = 'MNI_N27_SurfVol.nii'
    sv = os.path.join(suma_dir, surfvol_name)
    cmdargs = split('3dVol2Surf -spec %s \
                    -surf_A %s -surf_B %s \
                    -sv %s -grid_parent %s \
                    -map_func max -f_steps 10 -f_index voxels \
                    -f_p1_fr -%s -f_pn_fr %s \
                    -outcols_NSD_format -oob_index -1 -oob_value 0.0 \
                    -out_1D %s' % (spec, surf_a, surf_b, sv,
                                   parent, pn, pn, outname))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def vol2surf_indiv(work_dir, spec, smoothwm, pial,
                   parent, surfvol, outname):
    """
    """
    print 'Doing vol2surf_indiv -- %s' % time.ctime()
    print os.getcwd()
    stdout_dir = '%s/stdout_files' % work_dir
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_vol2surf.txt' % stdout_dir, 'w')
    cmdargs = split('3dVol2Surf -spec %s \
                    -surf_A %s -surf_B %s \
                    -sv %s -grid_parent %s \
                    -map_func max -f_steps 10 -f_index voxels \
                    -outcols_NSD_format -oob_index -1 -oob_value 0.0 \
                    -out_1D %s' %
                    (spec, smoothwm, pial, surfvol, parent, outname))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def resamp_with_master(stdout_dir, inset, master, out_pref):
    """
    resampling with master dset
    """
    print 'Doing resample -- %s' % time.ctime()
    print os.getcwd()
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_resamp.txt' % stdout_dir, 'w')
    cmdargs = split('3dresample -master %s -prefix %s -inset %s' %
                    (master, out_pref, inset))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()
