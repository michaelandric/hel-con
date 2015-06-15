# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 12:15:41 2015

@author: andric
"""

import os
import sys
import time
from shlex import split
from subprocess import call, STDOUT


class Masker(object):

    def __init__(self, anat, ss, stdout_dir):
        print 'Initializing... '+time.ctime()+'\nAnatomy: '+anat
        self.master_brain = anat
        self.subjid = ss
        self.stdoutdir = stdout_dir

    def allineate(self, trans_mat, input, outpref):
        """
        Use the Alnd_Exp transform to get freesurfer
        parcells to exp anat
        """
        f = open('%s/stdout_from_allineate.txt' % self.stdoutdir, 'w')
        cmdargs = split('3dAllineate -master %s -1Dmatrix_apply %s \
                        -input %s -prefix %s -final NN' %
                        (self.master_brain, trans_mat, input, outpref))
        call(cmdargs, stdout=f, stderr=STDOUT)
        f.close()

    def resample_reorient(self, inset, out_pref):
        f = open('%s/stdout_from_3dresample.txt' % self.stdoutdir, 'w')
        cmdargs = split("3dresample -master %s -prefix %s \
            -inset %s" % (self.master_brain, out_pref, inset))
        call(cmdargs, stdout=f, stderr=STDOUT)
        f.close()

    def mask_calc(self, subcort, lhribbon, rhribbon, aseg, outpref):
        """
        Doing 3dcalc to get the gray matter mask
        """
        print 'Calculating mask... '+time.ctime()
        f = open('%s/stdout_from_mask_calc.txt' % self.stdoutdir, 'w')
        calc_args = split("3dcalc -a %s -b %s -c %s -d %s \
                          -expr 'ispositive(ispositive(a) + equals(b,8) \
                          + equals(b,47) + ispositive(c) + ispositive(d))' \
                          -prefix %s" %
                          (subcort, aseg, lhribbon, rhribbon, outpref))
        call(calc_args, stdout=f, stderr=STDOUT)
        f.close()

    def resample(self, in_pref, out_pref):
        f = open('%s/stdout_from_3dresample.txt' % self.stdoutdir, 'w')
        cmdargs = split("3dresample -dxyz 4.0 4.0 4.0 -prefix %s \
            -rmode 'Li' -inset %s+orig" % (out_pref, in_pref))
        call(cmdargs, stdout=f, stderr=STDOUT)
        f.close()

    def fractionize(self, in_pref, out_pref, template):
        f = open('%s/stdout_from_3dfractionize.txt' % self.stdoutdir, 'w')
        cmdargs = split('3dfractionize -template %s+orig -input %s+orig \
            -prefix %s -clip 0.5' % (template, in_pref, out_pref))
        call(cmdargs, stdout=f, stderr=STDOUT)
        f.close()

    def mask_binary(self, in_pref, out_pref):
        f = open('%s/stdout_from_mask_binary.txt' % self.stdoutdir, 'w')
        cmdargs = split("3dcalc -a %s+orig -expr 'ispositive(a)' \
            -prefix %s.nii.gz" % (in_pref, out_pref))
        call(cmdargs, stdout=f, stderr=STDOUT)
        f.close()


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 19):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    for ss in ['hel19']:
        print 'Doing subject %s' % ss
        print time.ctime()
        ss_dir = os.path.join(os.environ['hel'],
                              '%s/' % ss)
        preproc_dir = '%s/preprocessing/' % ss_dir
        anat_dir = '%s/volume.%s.anat/' % (ss_dir, ss)
        stdout_dir = '%s/stdout_files/' % anat_dir
        for dir in [ss_dir, preproc_dir, anat_dir, stdout_dir]:
            if not os.path.exists(dir):
                print 'Problem with paths.'
                print '%s doesnt exist.' % dir
                print 'Shut down!'
                sys.exit(1)

        anat = os.path.join(ss_dir, 'volume.%s.nii.gz' % ss)

        msk = Masker(anat, ss, stdout_dir)

        alin_file_prefs = []
        suma_dir = '%s/freesurfer_%s/%s/SUMA/' % (ss_dir, ss, ss)
        for h in ['lh', 'rh']:
            alin_file_prefs.append('%s.ribbon' % h)
        alin_file_prefs.append('aseg')

        transmat = os.path.join(preproc_dir,
                                '%s_SurfVol_Alnd_Exp.A2E.1D' % ss)
        for f in alin_file_prefs:
            infile = os.path.join(suma_dir, '%s.nii' % f)
            out_pref = os.path.join(anat_dir, '%s_Alnd_Exp.nii.gz' % f)
            msk.allineate(transmat, infile, out_pref)

        subcort_seg = os.path.join(anat_dir, 'T1_subcort_seg.nii.gz')
        subcort_reorient = os.path.join(anat_dir,
                                        'T1_subcort_seg_reorient.nii.gz')
        msk.resample_reorient(subcort_seg, subcort_reorient)

        aseg = os.path.join(anat_dir, 'aseg_Alnd_Exp.nii.gz')
        lh_ribbon = os.path.join(anat_dir, 'lh.ribbon_Alnd_Exp.nii.gz')
        rh_ribbon = os.path.join(anat_dir, 'rh.ribbon_Alnd_Exp.nii.gz')
        outpref_mask = os.path.join(anat_dir, '%s_gm_mask.nii.gz' % ss)
        msk.mask_calc(subcort_reorient, lh_ribbon, rh_ribbon,
                      aseg, outpref_mask)

        frac_in_pref = os.path.join(anat_dir, '%s_gm_mask' % ss)
        frac_out_pref = '%s_frac' % frac_in_pref
        func_resamp_pref = 'cleanTS_%sr01_smth4mm_Liresamp4mm' % ss
        resamp_tmpl = os.path.join(preproc_dir, func_resamp_pref)
        msk.fractionize('%s.nii.gz' % frac_in_pref,
                        '%s.nii.gz' % frac_out_pref, resamp_tmpl)

        binary_out_pref = '%s_bin' % frac_out_pref
        msk.mask_binary(frac_out_pref, binary_out_pref)
