# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 18:00:07 2015

@author: andric
"""

import os
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph
from sklearn.cluster import KMeans
from sklearn.feature_extraction import image
from sklearn.cluster import FeatureAgglomeration
import nibabel


ss = 'hel1'
proc_dir = os.path.join(os.environ['hel'], ss, 'preprocessing')
ts_name = os.path.join(proc_dir, 'task_sess_2_%s_gm_mskd.txt' % ss)
msk_name = os.path.join(os.environ['hel'], ss, 'volume.%s.anat' % ss,
                        '%s_Clust_msk_glob_conn_origspace.txt' % ss)
msk = np.loadtxt(msk_name)

ts = np.loadtxt(ts_name)
ts_corr = np.corrcoef(ts)
ts_corr[np.where(msk == 1)]

w = AgglomerativeClustering(n_clusters=4, linkage="ward")
w.fit(ts_corr[np.where(msk == 1)])

con = image.grid_to_graph(*ts_corr[np.where(msk == 1)].shape)
x = np.reshape(ts_corr[np.where(msk == 1)], (-1, 1))
ww = AgglomerativeClustering(n_clusters=4, connectivity=con, linkage="ward")
ww.fit(x)
label = np.reshape(ww.labels_, ts_corr[np.where(msk == 1)].shape)

feat = FeatureAgglomeration(n_clusters=4, linkage='ward')
feat.fit(ts_corr[np.where(msk == 1)])
feats = AgglomerativeClustering(n_clusters=4, connectivity=connectivity, linkage="ward")

knn = kneighbors_graph(ts_corr[np.where(msk == 1)], 9)
w = FeatureAgglomeration(n_clusters=4, connectivity=knn, linkage='ward')
ww = AgglomerativeClustering(n_clusters=4, connectivity=knn, linkage="ward")
ww.fit(ts_corr[np.where(msk == 1)])

k_means = KMeans(init='k-means++', n_clusters=4, n_init=10)
k_means.fit(ts_corr[np.where(msk == 1)])

outlabels = np.zeros(ts.shape[0])
outlabels[np.where(msk == 1)] = w.labels_+1
outlabels[np.where(msk == 1)] = ww.labels_+1
outlabels[np.where(msk == 1)] = k_means.labels_+1

out_pref = '%s_Clust_msk_glob_conn2_ward_3clst' % ss
out_pref = '%s_Clust_msk_glob_conn2_knnward' % ss
out_pref = '%s_Clust_msk_glob_conn2_kmeans' % ss
out_dir = os.path.join(os.environ['hel'], 'graph_analyses',
                       ss, 'global_connectivity')
np.savetxt(os.path.join(out_dir, out_pref), outlabels, fmt='%d')


msk = nibabel.load('/cnari/normal_language/HEL/hel1/volume.hel1.anat/hel1_Clust_msk_glob_conn_origspace.nii.gz')
shape = msk.shape
msk2 = msk
msk2.get_data()[np.where(msk2.get_data()==3)] = 0
msk2.get_data()[np.where(msk2.get_data()==2)] = 0
nifti_masker = input_data.NiftiMasker(memory='nilearn_cache',
                                      memory_level=1, mask_img=msk2,
                                      standardize=False)
mask = nifti_masker.mask_img.get_data().astype(np.bool)
shape = mask.shape
connectivity = image.grid_to_graph(n_x=shape[0], n_y=shape[1],
                                   n_z=shape[2], mask=mask)
ward = FeatureAgglomeration(n_clusters=4, connectivity=connectivity,
                            linkage='ward', memory='nilearn_cache')
ts_masked = nifti_masker.fit_transform(ts_corr)
ward.fit(ts_corr)
xyz = np.where(msk.get_data() == 1)
con = image.grid_to_graph(n_x=94, n_y=94, n_z=94)
con = image.grid_to_graph(n_x=shape[0], n_y=shape[1], n_z=shape[2], mask=msk)