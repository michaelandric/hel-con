#!/usr/bin/python

import os
from itertools import *

os.chdir('/Users/andric/Documents/workspace/hel/PAU_SUMA')
print os.getcwd()

region_dict = {"G_front_inf-Orbital":3947660 , "G_front_inf-Opercular":6558940, "G_front_inf-Triangul":9231540, "G_front_middle":11822220, "G_pariet_inf-Angular":14433300, "G_pariet_inf-Supramar":3957860, "G_temp_sup-G_T_transv":14433340, "G_temp_sup-Lateral":14433500, "G_temp_sup-Plan_polar":3988545, "G_temp_sup-Plan_tempo":1346585, "G_and_S_cingul-Ant":15386, "G_precuneus":9180185, "G_cuneus":1316020, "S_calcarine":11842623, "G_oc-temp_med-Lingual":9221340, "S_temporal_transverse":3947741, "S_temporal_sup":3988703} 

nnodes = 196002
for h in ['lh', 'rh']:
    for reg in region_dict:
        print reg
        fname = 'mesh140_%s.aparc.a2009s.annot.niml.dset' % h
        with open(fname) as f:
            a = f.read().split('\n')

        nodelist = []
        for i in xrange(12, 12+nnodes):
            nodelist.append(int(a[i]))

        r = islice(count(), nnodes)
        i1, i2 = tee(r)

        outname = '%s_%s.nodes.1D' % (h, reg)
        outv = []
        fout = open(outname, 'w')
        for i in i1:
            if nodelist[i] == region_dict[reg]:
                outv.append(1)
            else:
                outv.append(0)
        fout.write('\n'.join(map(str, outv)))
        fout.close()
