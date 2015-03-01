#!/usr/bin/env python

import sys
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

def get_ijk(outname, mask=None):
    print 'Getting IJK coordinates... '+time.ctime()
    if not mask==None:
        print 'USING MASK: '+mask
        call("3dmaskdump -mask %s %s | awk '{print $1, $2, $3}' > %s" % (mask, mask, outname), shell=True)
    else:
        print 'NOT USING MASK.'
        call("3dmaskdump %s | awk '{print $1, $2, $3}' > %s" % (mask, outname), shell=True)
    print 'DONE. '+time.ctime()



if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.stderr.write("You messed up! \n"
                         "Usage: %s <SUBJECT ID> \n" %
                         (os.path.basename(sys.argv[0]),))

    subjid = sys.argv[1]

    os.chdir(os.environ['hel']+'/%s/connectivity/' % subjid)
    print os.getcwd()
    stdfdir = os.environ['hel']+'/%s/connectivity/stdout_files' % (subjid)
    if not os.path.exists(stdfdir):
        os.makedirs(stdfdir)

    inimage = os.environ['hel']+'/%s/connectivity/cleanTScat_%s.allruns+orig' % (subjid, subjid)
    outname = os.environ['hel']+'/%s/connectivity/cleanTScat_%s.allruns_GMmask_dump' % (subjid, subjid)
    mask = os.environ['hel']+'/%s/volume.%s.anat/%s_GMmask_resampled+orig' % (subjid, subjid, subjid)
    maskdump(inimage, outname, mask)
    os.chdir(os.environ['hel']+'/%s/volume.%s.anat/' % (subjid, subjid))
    print os.getcwd()
    outname = '%s.ijk_GMmask_dump' % subjid
    mask = '%s_GMmask_resampled+orig.BRIK.gz' % subjid
    get_ijk(outname, mask)