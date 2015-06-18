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

    subj_list = []
    for i in range(1, 19):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    for ss in subj_list:
        for thresh_dens in [.05, .10, .15, .20]:
            for hemi in ['lh', 'rh']:
                ss_dir = os.path.join(os.environ['hel'], ss)
                proc_dir = os.path.join(ss_dir, 'preprocessing')
                surfvol = os.path.join(proc_dir,
                                       '%s_SurfVol_Alnd_Exp+orig.' % ss)
                jacc_dir = os.path.join(top_dir, '%s/jaccard_res' % ss)
                parent_pref = os.path.join(jacc_dir,
                                           'jacc_%s_%s.ijk' % ss, thresh_dens)
                suma_dir = os.path.join(ss_dir,
                                        'freesurfer_%s' % ss, ss, 'SUMA')
                spec = os.path.join(suma_dir,
                                    'mesh140_%s_%s.spec' % (ss, hemi))
                smoothwm = os.path.join(suma_dir,
                                        'mesh140_%s.smoothwm.asc' % hemi)
                pial = os.path.join(suma_dir,
                                    'mesh140_%s.pial.asc' % hemi)
                outname = os.path.join(jacc_dir,
                                       '%s_%s_mesh140.1D' %
                                       parent_pref, hemi)
                gp.vol2surf_indiv(jacc_dir, spec, smoothwm, pial,
                                  '%s+orig' % parent_pref, surfvol, outname)
