#!/usr/bin/env python

import os
import time
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import STDOUT

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
        fslargs = split('fsl_anat -i %s.nii.gz --weakbias' % self.t1pref)
        Popen(fslargs, stdout = f, stderr = STDOUT)
        f.close()
        print 'DONE. '+time.ctime()



if __name__ == "__main__":

    subj_list = ['hel12', 'hel13', 'hel14', 'hel15', 'hel16']

    for ss in subj_list:
        os.chdir(os.environ['hel']+'/%s' % ss)
        if not os.path.exists('stdout_files'):
            os.makedirs('stdout_files')
        anat = 'volume.%s' % ss
        FA = FSLANAT(anat)
        FA.AFNItoNIFTI()
        FA.fslanat()
