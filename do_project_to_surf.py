# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:59:05 2015.

@author: andric
"""

import os
import general_procedures as gp


WORKDIR = os.path.join(os.environ['hel'], 'graph_analyses',
                       'randomise_global_connectivity')

fname = 'wgc_PairedTres_n10000_clustere_corrp_tstat2_vals'
parent_pref = os.path.join(WORKDIR, fname)
if os.path.exists('{}+tlrc.HEAD'.format(parent_pref)):
    for hemi in ['lh', 'rh']:
        outname = '{}_{}_pn1.0_MNI_N27.1D'.format(parent_pref, hemi)
        gp.vol2surf_mni(WORKDIR, hemi, '{}+tlrc'.format(parent_pref),
                        '1.0', outname)
else:
    print('There is no {}+tlrc.HEAD'.format(parent_pref))
    print('On to the next one.')
