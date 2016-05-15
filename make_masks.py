# Created May 14 2016
"""Making region masks."""

import os
import logging
from shlex import split
from subprocess import call
from subprocess import STDOUT
from subprocess import PIPE


def calc_mask(log_file_name, inputf, region_num, outname):
    """Using this to make a region mask.

    Volumes are already done in Freesurfer parcellation
    """
    logging.basicConfig(filename=log_file_name, level=logging.INFO)
    chl = logging.StreamHandler()
    chl.setLevel(logging.INFO)

    logging.info('Input file: %s', inputf)
    cmdargs = split('3dcalc -prefix {} -a {} \
                     -expr "step(equals(a, {}))"'.format(outname, inputf,
                                                         region_num))
    call(cmdargs, stdout=PIPE, stderr=STDOUT)


def main():
    """Making anat region masks.

    There are different region indices for different subjects. Many reasons
    made it this way, but somewhat due to different freesurfer versions
    and different degrees of editing, i.e., running standalone
    autorecon2 and autorecon3 that did not always behave in uniform way.

    """
    subj_list = ['hel{}'.format(i) for i in range(1, 19) if i is not 9]
    reg_d = {'lh_ant_occ_s': (101, 100, 101, 103, 103),
             'rh_ant_occ_s': (179, 177, 177, 178, 178),
             'lh_mid_occ_g': (56, 55, 56, 62, 63),
             'rh_mid_occ_g': (134, 132, 133, 137, 138),
             'lh_sup_temp_g': (75, 74, 75, 77, 78),
             'rh_sup_temp_g': (153, 151, 152, 152, 153),
             'lh_IFGOp': (47, 46, 47, 55, 56),
             'rh_IFGOp': (125, 123, 124, 130, 131)}
    subj_d = dict(zip(subj_list, [0] + [1] + [2] + [3]*7 + [4]*7))
    for region in reg_d:
        for subject in subj_list:
            subject_dir = os.path.join(os.environ['hel'], subject,
                                       'preprocessing')
            logfilename = os.path.join(subject_dir,
                                       'preprocessing', 'calc_mask.log')
            if subject == 'hel1' or subject == 'hel2' or subject == 'hel3':
                year = 2005
            else:
                year = 2009
            aparcname = 'aparc.a{}s+aseg_rank_{}_allin_resamp+orig'.format(
                year, subject)
            inputfile = os.path.join(subject_dir, aparcname)
            regionnumber = reg_d[region][subj_d[subject]]
            outfname = os.path.join(subject_dir, '{}_mask'.format(region))
            calc_mask(logfilename, inputfile, regionnumber, outfname)

if __name__ == '__main__':
    main()
