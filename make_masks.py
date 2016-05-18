# Created May 14 2016
"""Making region masks."""

import os
from setlog import setup_log
from shlex import split
from subprocess import call
from subprocess import STDOUT
from subprocess import PIPE


def calc_mask(log, inputf, region_num, outname):
    """Using this to make a region mask.

    Volumes are already done in Freesurfer parcellation
    """
    cmdargs = split('3dcalc -prefix {} -a {} \
                     -expr "step(equals(a, {}))"'.format(outname, inputf,
                                                         region_num))
    log.info('calc_mask command: \n%s', cmdargs)
    call(cmdargs, stdout=PIPE, stderr=STDOUT)


def main():
    """Making anat region masks.

    There are different region indices for different subjects. Many reasons
    made it this way, but somewhat due to different freesurfer versions
    and different degrees of editing, i.e., running standalone
    autorecon2 and autorecon3 that did not always behave in uniform way.

    """
    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]
    reg_d = {'lh_ttg': (74, 73, 74, 76, 77),
             'rh_ttg': (152, 150, 151, 151, 152),
             'lh_planum_temp': (77, 76, 77, 79, 80),
             'rh_planum_temp': (155, 153, 154, 154, 155),
             'lh_vis_calcarine': (85, 84, 85, 88, 88),
             'rh_vis_calcarine': (163, 161, 162, 163, 163)}
    subj_d = dict(zip(subj_list, [0] + [1] + [2] + [3]*7 + [4]*8))
    for region in reg_d:
        for subject in subj_list:
            subject_dir = os.path.join(os.environ['hel'], subject,
                                       'preprocessing')
            if subject == 'hel1' or subject == 'hel2' or subject == 'hel3':
                year = 2005
            else:
                year = 2009
            aparcname = 'aparc.a{}s+aseg_rank_{}_allin_resamp+orig'.format(
                year, subject)
            inputfile = os.path.join(subject_dir, aparcname)
            regionnumber = reg_d[region][subj_d[subject]]
            outfname = os.path.join(subject_dir, '{}_mask'.format(region))
            log = setup_log(os.path.join(subject_dir, 'calc_mask'))
            log.info('Doing calc_mask...')
            calc_mask(log, inputfile, regionnumber, outfname)

if __name__ == '__main__':
    main()
