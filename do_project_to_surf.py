# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:59:05 2015

@author: andric
"""

import os
import general_procedures as gp

mod_dir = os.path.join(os.environ['hel'],
                       'graph_analyses', 'group_modularity_thr0.5msk')

if __name__ == '__main__':

    subj_list = []
    for i in range(1, 19):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    pn = '1.0'

    for hemi in ['lh', 'rh']:
        for thresh_dens in [.05, .10, .15]:
            fname = 'group_task_diff_thr8_component_dens_%s.vals_sig.ijk' % \
                    thresh_dens
            parent_pref = os.path.join(mod_dir, fname)
            outname = '%s_%s_pn%s_MNI_N27.1D' % (parent_pref, hemi, pn)
            gp.vol2surf_mni(mod_dir, hemi, '%s+tlrc' % parent_pref,
                            pn, outname)
