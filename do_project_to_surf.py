# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:59:05 2015.

@author: andric
"""

import os
import general_procedures as gp


WORKDIR = os.path.join(os.environ['hel'], 'graph_analyses',
                       'randomise_global_connectivity')

for subclust_n in range(2, 4):
    prefx = 'knnward_clst1_subclust{}'.format(subclust_n)
    fname = '{}_thresh_4Dfile_n10000_clustere_corrp_tstat2'.format(prefx)
    parent_pref = os.path.join(WORKDIR, fname)
    if os.path.exists('{}.nii.gz'.format(parent_pref)):
        for hemi in ['lh', 'rh']:
            outname = '{}_{}_pn1.0_MNI_N27.1D'.format(parent_pref, hemi)
            gp.vol2surf_mni(WORKDIR, hemi, '{}.nii.gz'.format(parent_pref),
                            '1.0', outname)
    else:
        print('There is no {}+tlrc.HEAD'.format(parent_pref))
        print('On to the next one.')
