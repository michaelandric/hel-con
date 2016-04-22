# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:59:05 2015

@author: andric
"""

import os
import general_procedures as gp


mod_dir = os.path.join(os.environ['hel'],
                       'graph_analyses', 'subrun_group_modularity_thr0.5msk')

if __name__ == '__main__':

    pn = '1.0'
    thresh_dens = .15
    for hemi in ['lh', 'rh']:
        for session in ['first', 'second']:
            print('Doing {} '.format(hemi))
            fname = 'group_task_sess_{}.dens_{}.maxq_tree.ijk'.format(
                session, thresh_dens)
            parent_pref = os.path.join(mod_dir, fname)
            outname = '{}_{}_pn{}_MNI_N27.1D'.format(parent_pref, hemi, pn)
            gp.vol2surf_mni(mod_dir, hemi, '{}+tlrc'.format(parent_pref),
                            pn, outname)