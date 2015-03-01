#!/usr/bin/env python

"""This contains functions for both stand-alone 'FAST' and calculating the mask."""

import sys
import os
import time
from shlex import split
from subprocess import call, STDOUT

class MaskMaker:

    def __init__(self, anat, ss):
        print 'Initializing... '+time.ctime()+'\nAnatomy: '+anat
        self.brain = anat
        self.subjid = ss

    def run_fast(self):
        """
        Takes the brain without extension
        """
        print 'Running fast... '+time.ctime()
        f = open('stdout_files/stdout_from_fast.txt', 'w')
        fastargs = split('fast -t 1 -n 4 -H 0.4 -I 4 -l 20.0 -g -o %s_fast_out %s' % (self.brain, self.brain))
        call(fastargs, stdout=f, stderr=STDOUT)
        f.close()

    def mask_calc(self):
        """
        Doing 3dcalc to get the gray matter mask
        """
        print 'Calculating mask... '+time.ctime()
        f = open('stdout_files/stdout_from_3dcalc_mask.txt', 'w')
        calcargs = split("3dcalc -a T1_subcort_seg.nii.gz \
                            -b %s_fast_out_seg_1.nii.gz \
                            -c %s_fast_out_seg_2.nii.gz \
                            -expr 'step(a+b+c)' \
                            -prefix %s_GMmask" % (self.brain, self.brain, self.subjid))
        call(calcargs, stdout=f, stderr=STDOUT)
        f.close()

    def resample_func(self, automask):
        """
        resample to functional resolution
        """
        print 'Resampling to correct functional space... '+time.ctime()
        f = open('stdout_files/stdout_from_3dresample.txt', 'w')
        resargs = split('3dresample -master %s -inset %s_GMmask+orig -prefix %s_GMmask_resampled' % (automask, self.subjid, self.subjid))
        call(resargs, stdout=f, stderr=STDOUT)
        f.close()

if __name__ == "__main__":

    subj_list = ['hel14', 'hel15', 'hel16']
    for ss in subj_list:
        os.chdir(os.environ['hel']+'/%s/volume.%s.anat' % (ss, ss))

        stdfdir = os.environ['hel']+'/%s/volume.%s.anat/stdout_files' % (ss, ss)
        if not os.path.exists(stdfdir):
            os.makedirs(stdfdir)

        print os.getcwd()
        print sys.version
        mm = MaskMaker('T1_biascorr_brain', ss)
        mm.run_fast()
        mm.mask_calc()
        mask = os.environ['hel']+'/%s/preprocessing/automask_d1_%s+orig' % (ss, ss)
        mm.resample_func(mask)




