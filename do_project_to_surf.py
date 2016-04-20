# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:59:05 2015

@author: andric
"""

import os
import general_procedures as gp

top_dir = os.path.join(os.environ['hel'], 'graph_analyses')
group_dir = os.path.join(top_dir, 'subrun_group_jaccard')

if __name__ == '__main__':

    subj_list = ['hel{}'.format(i) for i in range(1, 20) if i is not 9]

    for nom in ['1and4', '3and6']:
        for ss in subj_list:
            for thresh_dens in [.15]:
                for hemi in ['lh', 'rh']:
                    ss_dir = os.path.join(os.environ['hel'], ss)
                    proc_dir = os.path.join(ss_dir, 'preprocessing')
                    surfvol = os.path.join(proc_dir,
                                           '{}_SurfVol_Alnd_Exp+orig.'.format(ss))
                    jacc_dir = os.path.join(top_dir, ss, 'subrun_jaccard_res')
                    parent_pref = os.path.join(jacc_dir,
                                               'jacc_{}_{}_{}.ijk'.format(
                                               ss, thresh_dens, nom))
                    suma_dir = os.path.join(ss_dir,
                                            'freesurfer_{}'.format(ss), ss, 'SUMA')
                    spec = os.path.join(suma_dir,
                                        'mesh140_{}_{}.spec'.format(ss, hemi))
                    smoothwm = 'mesh140_{}.smoothwm.asc'.format(hemi)
                    pial = 'mesh140_{}.pial.asc'.format(hemi)
                    outname = os.path.join(jacc_dir,
                                           '{}_{}_mesh140.1D'.format(
                                           parent_pref, hemi))
                    gp.vol2surf_indiv(jacc_dir, spec, smoothwm, pial,
                                      '{}+orig'.format(
                                      parent_pref), surfvol, outname)