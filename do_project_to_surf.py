# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:59:05 2015

@author: andric
"""

import os
import general_procedures as gp

graph_dir = os.path.join(os.environ['hel'], 'graph_analyses')
mod_dir = os.path.join(graph_dir, 'group_modularity')

if __name__ == '__main__':

    subj_list = []
    for i in range(1, 19):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    pn = '1.0'
    for thresh_dens in [.05, .10, .15, .20]:
        for session in range(1, 3):
            for hemi in ['lh', 'rh']:
                print 'Doing %s ' % hemi
                parent_pref = os.path.join(mod_dir,
                                           'group_task_sess_%d.dens_%s.agreement.nothr.mods.ijk' % thresh_dens)
                outname = '%s_%s_pn%s_MNI_N27.1D' % (parent_pref, hemi, pn)
                gp.vol2surf_mni(mod_dir, hemi, '%s+tlrc' % parent_pref,
                                pn, outname)
