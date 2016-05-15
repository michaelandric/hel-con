# created May 15 2016
"""Calculate ROI stats from region masks."""

import os
import logging
import csv
import pandas as pd
from setlog import setup_log
from shlex import split
from subprocess import call


def calc_stat(mask_name, inputf, outname):
    """Get region stats.

    Calling as "3dROIstats -quiet -median -nzmean" will give 3 column output
    with 1) regular mean over all voxels in mask, 2) mean over non-zero voxels
    and 3) median over all voxels
    """
    logging.info('Input file: %s', inputf)
    outf = open(outname, 'w')
    cmdargs = split('3dROIstats -median -nzmean -mask {} {}'.format(
        mask_name, inputf))
    logging.info('Running: \n %s', cmdargs)
    call(cmdargs, stdout=outf)
    outf.close()


def stat_compile(subjectlist, region, outname, logdir):
    """Create table of stats.

    Region compilations of AFNI 3dROIstats outputs into a single file.
    """
    log = setup_log(os.path.join(logdir, '{}_stat_compile'.format(region)))
    log.info('Doing region: %s', region)
    statlist = []
    for subject in subjectlist:
        afnifile = os.path.join(os.environ['hel'], subject,
                                'preprocessing',
                                '{}_{}_stats.txt'.format(region, subject))
        with open(afnifile) as aff:
            caff = [line for line in csv.reader(aff, delimiter='\t')]
            statlist.append(caff[1])
    statframe = pd.DataFrame(statlist,
                             columns=['File', 'Sub-brick', 'Mean',
                                      'NZMean', 'Median'])
    statframe.to_csv(outname, index=False)
    log.info('Finished %s for stat_compile', region)


def main():
    """Getting region stats.

    Will adjust within calc_stat function.
    """
    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]
    region_list = ['lh_IFGOp',
                   'rh_IFGOp',
                   'rh_mid_occ_g',
                   'lh_sup_temp_g',
                   'rh_ant_occ_s',
                   'lh_ant_occ_s',
                   'lh_mid_occ_g',
                   'rh_sup_temp_g']
    for region in region_list:
        for subject in subj_list:
            subject_dir = os.path.join(os.environ['hel'], subject,
                                       'preprocessing')
            logfilename = os.path.join(subject_dir, 'calc_stat.log')
            logging.basicConfig(filename=logfilename, level=logging.INFO,
                                format='%(asctime)s %(message)s',
                                datefmt='%m/%d/%Y %I:%M:%S %p')
            chl = logging.StreamHandler()
            chl.setLevel(logging.INFO)
            logging.info('Subject: %s, region: %s', subject, region)
            tcorr = 'tcorr_prsn_{}_gm_mskd_Z+orig'.format(subject)
            input_stats = os.path.join(subject_dir, tcorr)
            mask_file = os.path.join(subject_dir, '{}_mask+orig'.format(region))
            outfname = os.path.join(subject_dir,
                                    '{}_{}_stats.txt'.format(region, subject))
            calc_stat(mask_file, input_stats, outfname)

        outtable = os.path.join(os.environ['hel'],
                                'graph_analyses/behav_correlate',
                                '{}_grouptable_raw.txt'.format(region))
        log_dir = os.path.join(os.environ['hel'],
                               'graph_analyses/behav_correlate')
        stat_compile(subj_list, region, outtable, log_dir)


if __name__ == '__main__':
    main()
