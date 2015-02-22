#!/usr/bin/env python

import time
import os
from shlex import split
from subprocess import call


def maskdump(inimage, outname, mask=None):
    print 'Running maskdump... '+time.ctime()
    f = open('stdout_files/stderr_maskdump.txt', 'w')
    dmpout = open('%s' % outname, 'w')
    if not mask==None:
        print 'USING MASK: '+mask
        dmpcmd = split('3dmaskdump -mask %s -noijk %s' % (mask, inimage))
    else:
        print 'NOT USING MASK.'
        dmpcmd = split('3dmaskdump -noijk %s' % inimage)
    call(dmpcmd, stdout=dmpout, stderr=f)
    dmpout.close()
    f.close()
    print 'DONE. '+time.ctime()

if __name__ == '__main__':

    subj_list = ['hel19']
    for ss in subj_list:
        inimage = os.environ['hel']+'/%s/connectivity/cleanTScat_%s.allruns+orig' % (ss, ss)
        outname = os.environ['hel']+'/%s/connectivity/cleanTScat_%s.allruns_GMmask_dump' % (ss, ss)
        mask = os.environ['hel']+'/%s/volume.%s.anat/%s_GMmask_resampled+orig' % (ss, ss, ss)
        maskdump(inimage, outname, mask)