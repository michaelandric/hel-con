# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:05:42 2015

Grab the TS of interest via 3dTcat
Then dump that to text file for further analysis.

Update: Tues Apr 12 2016
Addressing whether being in scanner longer gives effect
Compare runs 1 & 4 to 3 & 6
@author: andric
"""

import os
import sys
import time
from shlex import split
from subprocess import call, STDOUT


def TScat(stdout_dir, input_list, out_pref):
    """
    Takes inputs as list (with sub-bricks indicated)
    """
    f = open('%s/stdout_from_TScat.txt' % stdout_dir, 'w')
    cmdargs = split('3dTcat -prefix %s %s' % (out_pref, ' '.join(input_list)))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close

def TScat_single(stdout_dir, input_sub, out_pref):
    """
    Takes one input (with sub-bricks indicated)
    """
    f = open('%s/stdout_from_TScat.txt' % stdout_dir, 'w')
    cmdargs = split('3dTcat -prefix {} {}'.format(out_pref, input_sub))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close

def maskdump(stdout_dir, mask, in_pref, out_pref):
    outf = open(out_pref, 'w')
    f = open('%s/stdout_from_maskdump.txt' % stdout_dir, 'w')
    cmdargs = split('3dmaskdump -mask %s -noijk %s' % (mask, in_pref))
    call(cmdargs, stdout=outf, stderr=f)
    outf.close()
    f.close()


def get_ijk(outname, mask=None):
    print ('Getting IJK coordinates... '.format+time.ctime())
    if mask is None:
        print ('NOTT USING MASK. HUH?')
        call("3dmaskdump {} | awk '{print $1, $2, $3}' > {}".format(
             (mask, outname)), shell=True)
    else:
        print ('USING MASK: {}'.format(mask))
        call("3dmaskdump -mask {} {} | awk '{print $1, $2, $3}' > {}".format(
             (mask, mask, outname)), shell=True)
    print ('DONE. {}'.format(time.ctime()))


def build_inputlist(subjid, proc_dir, sess):
    """
    :param subjid: This is the subject id
    :param sess: Is session 1 or 2
    Each person saw the same set of videos twice
    in same order

    subs currently reflect task (movie)
    corresponding to each run (why there are 3 in subs list)
    """
    inp_list = []
    runs = range(1, 4)
    subs = ['9..78, 108..210', '9..108, 123..229',
            '9..40, 63..131, 155..220']
    sub_dct = dict(zip(runs, subs))
    if sess == 1:
        for r in runs:
            f = "'%s/cleanTS_%sr0%d_smth4mm_Liresamp4mm_gm_mskd+orig[%s]'" % \
                (proc_dir, subjid, r, sub_dct[r])
            inp_list.append(f)
    elif sess == 2:
        for r in runs:
            f = "'%s/cleanTS_%sr0%d_smth4mm_Liresamp4mm_gm_mskd+orig[%s]'" % \
                (proc_dir, subjid, int(r+3), sub_dct[r])
            inp_list.append(f)

    return inp_list

    

if __name__ == '__main__':
    subj_list = ['hel19']
    for ss in subj_list:
        print ('Doing subject {}'.format(ss))
        print (time.ctime())
        preproc_dir = os.path.join(os.environ['hel'],
                                   '%s/preprocessing/' % ss)
        if not os.path.exists(preproc_dir):
            print ('Problem with paths.')
            print ('Shut down!')
            sys.exit(1)

        stdout_dir = os.path.join(preproc_dir, 'stdout_files/')
        if not os.path.exists(stdout_dir):
            os.makedirs(stdout_dir)
        
        runs = [1, 3, 4, 6]
        subs = ['9..78, 108..210', '9..40, 63..131, 155..220']
        sub_dct = dict(zip(runs[:2], subs))
        sub_dct.update(dict(zip(runs[2:], subs)))
        for r in runs:
            f = "'{}/cleanTS_{}r0{}_smth4mm_Liresamp4mm_gm_mskd+orig[{}]'".format(
            preproc_dir, ss, int(r), sub_dct[r])
            cat_out_name = os.path.join(preproc_dir,
                                        'task_r0{}_{}_gm_mskd'.format(r, ss))
            TScat_single(stdout_dir, f, cat_out_name)

            mask_dir = '%s/%s/volume.%s.anat/' % (os.environ['hel'], ss, ss)
            mask_pref = os.path.join(mask_dir, '%s_gm_mask_frac_bin' % ss)
            mask = '%s.nii.gz' % mask_pref
            in_name = '{}+orig'.format(cat_out_name)
            ts_outname = '{}.txt'.format(cat_out_name)
            maskdump(stdout_dir, mask, in_name, ts_outname)
