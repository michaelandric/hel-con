#!/usr/bin/env python

import os
import time
import sys
import commands
import time
import shutil
from optparse import OptionParser

class FSLANAT:

    def __init__(self, anat):
        print 'Initializing... '+time.ctime()+'\nAnatomy: '+anat
        self.t1pref = anat   # this is the T1 volume prefix
        print 'Got it.'

    def AFNItoNIFTI(self):
        print 'AFNItoNIFTI... '+time.ctime()
        f = open('stdout_files/stdout_from_afnitonifti_%s' % self.t1pref, 'w')
        cmdargs = split('3dAFNItoNIFTI %s+orig.' % self.t1pref)
        call(cmdargs, stdout = f, stderr = STDOUT)
        f.close()
        print 'DONE... '+time.ctime()

    def fslanat(self):
        print 'fslanat... '+time.ctime()
        f = open('stdout_files/stdout_from_fsl_anat_%s' % self.t1pref, 'w')
        fslargs = split('fsl_anat -i %s.nii.gz' % self.t1pref)
        Popen(fslargs, stdout = f, stderr = STDOUT)
        f.close()
        print 'DONE. '+time.ctime()



if __name__ == "__main__":

    subj_list = ['hel19']

    for ss in subj_list:
        os.chdir(os.environ['hel']+'/%s' % ss)   # set for localizers
        anat = 'volume.%s' % ss
        FA = FSLANAT(anat)
        FA.AFNItoNIFTI()
        FA.fslanat()
