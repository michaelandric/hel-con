# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:59:05 2015

@author: andric
"""

import os
import general_procedures as gp

top_dir = '%s/graph_analyses' % os.environ['hel']
group_dir = os.path.join(top_dir, 'group_jaccard')

if __name__ == '__main__':

    pn = '1.0'
    for thresh_dens in [.10, .15, .20]:
        for hemi in ['lh', 'rh']:
            print 'Doing %s %s' % (hemi, thresh_dens)
            parent_pref = os.path.join(group_dir,
                                       'jaccard_group_median_dens_%s.ijk'
                                       % thresh_dens)
            outname = '%s_%s_pn%s_MNI_N27.1D' % (parent_pref, hemi, pn)
            gp.vol2surf_mni(group_dir, hemi, '%s+tlrc' % parent_pref,
                            pn, outname)
