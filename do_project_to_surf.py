# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:59:05 2015

@author: andric
"""

import os
import general_procedures as gp

#mod_dir = os.path.join(os.environ['hel'],
#                       'graph_analyses', 'group_modularity_thr0.5msk')
tcorr_dir = os.path.join(os.environ['hel'], 'tcorr_group')

if __name__ == '__main__':

    subj_list = []
    for i in range(1, 19):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    pn = '1.0'

    for hemi in ['lh', 'rh']:
        print 'Doing %s ' % hemi
        parent_pref = os.path.join(tcorr_dir,
                                           'ttest_tcorr_prsn_Z_vals')
        outname = '%s_%s_pn%s_MNI_N27.1D' % (parent_pref, hemi, pn)
        gp.vol2surf_mni(tcorr_dir, hemi, '%s+tlrc' % parent_pref,
                        pn, outname)
