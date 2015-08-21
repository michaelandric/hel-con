# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 18:00:07 2015

@author: andric
"""

import os
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph
import general_procedures as gp


def cluster_subreg(ss, nclust):
    """These will be used for undump"""
    anat_dir = os.path.join(os.environ['hel'], ss, 'volume.%s.anat' % ss)
    ijk = os.path.join(anat_dir, '%s_gm_mask_frac_bin_ijk.txt' % ss)
    master = os.path.join(anat_dir, '%s_gm_mask_frac_bin.nii.gz' % ss)

    proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
    ts_name = os.path.join(proc_dir, 'task_sess_2_%s_gm_mskd.txt' % ss)
    msk_name = os.path.join(os.environ['hel'], ss, 'volume.%s.anat' % ss,
                            '%s_Clust_msk_glob_conn_origspace.txt' % ss)
    msk = np.loadtxt(msk_name)
    clusters = np.unique(msk)[np.unique(msk) != 0]
    ts = np.loadtxt(ts_name)
    ts_corr = np.corrcoef(ts)
    outnames = []
    for cl in clusters:
        clst_dat = ts_corr[np.where(msk == cl)]
        nvox_in_clst = clst_dat.shape[0]
        neighb = int(round(np.sqrt(nvox_in_clst)))
        knn = kneighbors_graph(ts_corr[np.where(msk == cl)], neighb)
        w = AgglomerativeClustering(n_clusters=nclust,
                                    connectivity=knn, linkage="ward")
        w.fit(clst_dat)

        outlabels = np.zeros(ts.shape[0])
        outlabels[np.where(msk == cl)] = w.labels_ + 1

        out_pref = '%s_Clust_msk_glob_conn_knnward_clst%d' % (ss, cl)
        out_dir = os.path.join(os.environ['hel'], 'graph_analyses',
                               ss, 'global_connectivity')
        cl_outname = os.path.join(out_dir, out_pref)
        outnames.append(cl_outname)
        np.savetxt(cl_outname, outlabels, fmt='%d')
        gp.undump(ss, ijk, cl_outname, out_dir, master)

        return outnames


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 19):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    for ss in subj_list:
        out_dir = os.path.join(os.environ['hel'], 'graph_analyses',
                               ss, 'global_connectivity')
        outs = cluster_subreg(ss, 4)

        anat_dir = os.path.join(os.environ['hel'], ss, 'volume.%s.anat' % ss)
        extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')
        premat = os.path.join(anat_dir, '%s_gm_mask_frac_bin_flirted.mat' % ss)
        for oo in outs:
            fname = '%s.ijk+orig' % oo
            nii_fname = '%s.ijk.nii.gz' % oo
            gp.converttoNIFTI(out_dir, fname, nii_fname)
            out_fl = '%s.ijk_flirted' % oo
            gp.applywarpFLIRT(ss, out_dir, nii_fname,
                              extrt1, out_fl, premat, 'nn')
            fn_coef = os.path.join(anat_dir,
                                   'T1_to_MNI_nonlin_coeff.nii.gz')
            in_fn = '%s.nii.gz' % out_fl
            out_fn = '%s.ijk_fnirted_MNI2mm' % oo
            gp.applywarpFNIRT(ss, out_dir, in_fn, out_fn, fn_coef)
            maskn = 'group_avg_gm_mask_frac_bin_fnirted_MNI2mm_thr0.5.nii.gz'
            mask = os.path.join(os.environ['hel'], 'group_anat', maskn)
            gp.maskdump(out_dir, mask, '%s.nii.gz' % out_fn, '%s.txt' % out_fn)
