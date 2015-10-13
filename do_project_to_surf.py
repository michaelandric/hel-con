# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:59:05 2015

@author: andric
"""

import os
import general_procedures as gp

conn_dir = os.path.join(os.environ['hel'], 'ccf_cor')

if __name__ == '__main__':

    subj_list = []
    for i in range(1, 19):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    pn = '1.0'

    for hemi in ['lh', 'rh']:
        print 'Doing %s ' % hemi
        parent_pref = os.path.join(conn_dir,
                                   'ccf_abs_lag_out_group_gm_mskd_wilcox_bucket')
        outname = '%s_%s_pn%s_MNI_N27.1D' % (parent_pref, hemi, pn)
        gp.vol2surf_mni(conn_dir, hemi, '%s+tlrc' % parent_pref,
                        pn, outname)
