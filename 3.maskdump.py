#!/usr/bin/env python

import time
import os
from shlex import split
from subprocess import call, Popen, PIPE


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
    f = open('stdout_files/stderr_from_getijk.txt', 'w')
    dmpout = open('%s' % outname, 'w')
    if not mask==None:
        print 'USING MASK: '+mask
        dmpcmd = split('3dmaskdump -mask %s %s' % (mask, mask))
    else:
        print 'NOT USING MASK.'
        dmpcmd = split('3dmaskdump %s' % mask)
    print dmpcmd
    call(dmpcmd, stdout=dmpout, stderr=f)
    dmpout.close()
    f.close()
    ff = open(dmpout, 'r')
    fff = ff.readlines()
    a = []
    b = []
    c = []
    for line in fff:
        a.append(line.split()[0])
        b.append(line.split()[1])
        c.append(line.split()[2]+'\n')
    new = zip(a, b, c)
    newout = ""
    for line in new:
        newout += ' '.join(line)
    outf = open(outname, 'w')
    outf.write(newout)
    outf.close()
    print 'DONE. '+time.ctime()



if __name__ == '__main__':

    subj_list = ['hel19']
    for ss in subj_list:
        os.chdir(os.environ['hel']+'/%s/connectivity/' % ss)
        print os.getcwd()
        stdfdir = os.environ['hel']+'/%s/connectivity/stdout_files' % (ss)
        if not os.path.exists(stdfdir):
            os.makedirs(stdfdir)
        inimage = os.environ['hel']+'/%s/connectivity/cleanTScat_%s.allruns+orig' % (ss, ss)
        outname = os.environ['hel']+'/%s/connectivity/cleanTScat_%s.allruns_GMmask_dump' % (ss, ss)
        mask = os.environ['hel']+'/%s/volume.%s.anat/%s_GMmask_resampled+orig' % (ss, ss, ss)
        #maskdump(inimage, outname, mask)
        os.chdir(os.environ['hel']+'/%s/volume.%s.anat/' % (ss,ss))
        print os.getcwd()
        outname = '%s.ijk_GMmask_dump' % ss
        mask = '%s_GMmask_resampled+orig.BRIK.gz' % ss
        get_ijk(outname, mask)