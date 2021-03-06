# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 17:12:16 2015

@author: andric
"""

import os
from shlex import split
from subprocess import call, STDOUT


def t_test(stdoutdir, ss_list, outpref):
    """
    test between conditions
    """
    top_dir = '%s/graph_analyses' % os.environ['hel']
    a_sets = []
    b_sets = []
    for ss in ss_list:
        pref_a = 'avg_corrZ_task_sess_1_%s.ijk_fnirted_MNI2mm.nii.gz' % ss
        pref_b = 'avg_corrZ_task_sess_2_%s.ijk_fnirted_MNI2mm.nii.gz' % ss
        a_sets.append(os.path.join(top_dir, ss, 'global_connectivity', pref_a))
        b_sets.append(os.path.join(top_dir, ss, 'global_connectivity', pref_b))
    a_sets = ' '.join(a_sets)
    b_sets = ' '.join(b_sets)

    f = open('%s/stdout_from_3dttest++.txt' % stdoutdir, 'w')
    cmdargs = split('3dttest++ -setA %s -labelA sess_1 -setB %s -labelB sess_2 \
                    -mask %s/MNI152_T1_2mm_brain_mask_dil1.nii.gz \
                    -paired -prefix %s' %
                    (a_sets, b_sets,
                     '%s/data/standard' % os.environ['FSLDIR'], outpref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def t_test_subruns(stdoutdir, ss_list, outpref):
    """
    testing 1st and 3rd runs versus 4th and 6th
    """
    top_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    a_sets = []
    b_sets = []
    for ss in ss_list:
        pref_a = 'mean_avg_corrZ_task_runs1and4_{}+tlrc'.format(ss)
        pref_b = 'mean_avg_corrZ_task_runs3and6_{}+tlrc'.format(ss)

        a_sets.append(os.path.join(top_dir, ss,
                                   'single_run_global_connectivity', pref_a))
        b_sets.append(os.path.join(top_dir, ss,
                                   'single_run_global_connectivity', pref_b))
    a_sets = ' '.join(a_sets)
    b_sets = ' '.join(b_sets)

    f = open(os.path.join(stdoutdir, 'stdout_from_3dttest++.txt'), 'w')
    cmdargs = split('3dttest++ -setA {} -labelA sess_1and3 -setB {} -labelB sess_4and6 \
                    -mask {} -paired -prefix {}'.format(
                    a_sets, b_sets,
                    os.path.join(os.environ['FSLDIR'],
                                 'data/standard', 
                                 'MNI152_T1_2mm_brain_mask_dil1.nii.gz'),
                    outpref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def t_test_subruns_mean_diff(stdoutdir, ss_list, outpref):
    """
    testing 1st and 3rd run diff average with 4th and 6th diff
    """
    top_dir = os.path.join(os.environ['hel'], 'graph_analyses')
    a_sets = []
    for ss in ss_list:
        pref_a = 'mean_diff_corrZ_task_{}+tlrc'.format(ss)
        a_sets.append(os.path.join(top_dir, ss,
                                   'single_run_global_connectivity', pref_a))
    a_sets = ' '.join(a_sets)

    f = open(os.path.join(stdoutdir, 'stdout_from_3dttest++.txt'), 'w')
    cmdargs = split('3dttest++ -setA {} -labelA mean_diffs \
                    -mask {} -prefix {}'.format(
                    a_sets, 
                    os.path.join(os.environ['FSLDIR'],
                                 'data/standard', 
                                 'MNI152_T1_2mm_brain_mask_dil1.nii.gz'),
                    outpref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def t_test_subclust(stdoutdir, ss_list, cl, clst, outpref):
    """
    test between conditions
    """
    top_dir = '%s/graph_analyses' % os.environ['hel']
    suff = 'ijk_fnirted_MNI2mm.nii.gz'
    a_sets = []
    b_sets = []
    for ss in ss_list:
        pref_a = 'knnward_clst%d_mskd_subclust%d_corrZ_sess_1_%s.%s' % \
                 (cl, clst, ss, suff)
        pref_b = 'knnward_clst%d_mskd_subclust%d_corrZ_sess_2_%s.%s' % \
                 (cl, clst, ss, suff)
        a_sets.append(os.path.join(top_dir, ss,
                                   'global_connectivity', pref_a))
        b_sets.append(os.path.join(top_dir, ss,
                                   'global_connectivity', pref_b))
    a_sets = ' '.join(a_sets)
    b_sets = ' '.join(b_sets)

    f = open('%s/stdout_from_3dttest++.txt' % stdoutdir, 'w')
    cmdargs = split('3dttest++ -setA %s -labelA sess_1 -setB %s -labelB sess_2 \
                    -mask %s/MNI152_T1_2mm_brain_mask_dil1.nii.gz \
                    -paired -prefix %s' %
                    (a_sets, b_sets,
                     '%s/data/standard' % os.environ['FSLDIR'], outpref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def tcorr_t_test(stdoutdir, ss_list, outpref):
    """
    Testing whether biaseless ISC values
    differ from 0
    """
    a_set = []
    tcorr_dir = os.path.join(os.environ['hel'], 'tcorr_group')
    for ss in ss_list:
        pref = 'tcorr_prsn_%s_gm_mskd_Z_fnirted_MNI2mm.nii.gz' % ss
        a_set.append(os.path.join(tcorr_dir, pref))
    a_set = ' '.join(a_set)

    f = open('%s/stdout_from_3dttest++.txt' % stdoutdir, 'w')
    cmdargs = split('3dttest++ -setA %s \
                    -mask %s/MNI152_T1_2mm_brain_mask_dil1.nii.gz \
                    -prefix %s' %
                    (a_set, '%s/data/standard' % os.environ['FSLDIR'],
                     outpref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def tcorr_ccf_t_test(stdoutdir, ss_list, outpref):
    """
    Testing whether biaseless ISC values
    differ from 0
    """
    corr_dir = os.path.join(os.environ['hel'], 'ccf_cor')
    a_set = []
    for ss in ss_list:
        pref = 'ccf_abs_vals_out_%s_gm_mskd.ijk_fnirted_MNI2mm.nii.gz' % ss
        a_set.append(os.path.join(corr_dir, pref))
    a_set = ' '.join(a_set)

    f = open('%s/stdout_from_3dttest++.txt' % stdoutdir, 'w')
    cmdargs = split('3dttest++ -setA %s \
                    -mask %s/MNI152_T1_2mm_brain_mask_dil1.nii.gz \
                    -prefix %s' %
                    (a_set, '%s/data/standard' % os.environ['FSLDIR'],
                     outpref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()
    
def ava_main(stdoutdir, ss_list, outpref):
    """
    Test ava in each task_sess_1 (VIEW1) and task_sess_2 (VIEW2)
    """
    ava_dir = os.path.join(os.environ['hel'], 'ava')
    a_set = []
    b_set = []
    for ss in ss_list:
        pref_a = 'ava_smth_task_sess_1_%s_gm_mskd.txt.ijk_fnirted_MNI2mm.nii.gz' % ss
        pref_b = 'ava_smth_task_sess_2_%s_gm_mskd.txt.ijk_fnirted_MNI2mm.nii.gz' % ss
        a_set.append(os.path.join(ava_dir, pref_a))
        b_set.append(os.path.join(ava_dir, pref_b))
    a_set = ' '.join(a_set)
    b_set = ' '.join(b_set)
    f = open('%s/stdout_from_3dttest++.txt' % stdoutdir, 'w')
    cmdargs = split('3dttest++ -setA %s -labelA ava_sess_1 -setB %s -labelB ava_sess_2 \
                    -mask %s/MNI152_T1_2mm_brain_mask_dil1.nii.gz \
                    -paired -prefix %s' %
                    (a_set, b_set,
                     '%s/data/standard' % os.environ['FSLDIR'], outpref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()    
    

if __name__ == '__main__':
    subj_list = ['hel{}'.format(i) for i in range(1, 20)]
    subj_list.remove('hel9')   # because this is bad subj

    out_dir = os.path.join(os.environ['hel'], 'graph_analyses',
                           'group_single_run_global_connectivity')
    stdout_dir = os.path.join(out_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)

    outpref = os.path.join(out_dir, 'mean_diff_ttest_subruns')
    t_test_subruns_mean_diff(stdout_dir, subj_list, outpref)
