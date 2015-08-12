# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 17:44:21 2015

@author: andric
"""

import os
import numpy as np
import pandas as pd


def get_clust_info(subj_list, conditions, maskname, method='mean'):
    print 'Getting cluster info'
    print 'Doing %s ' % method
    mask = np.loadtxt(maskname)
    mask = mask[:, 3]   # has ijk + data, just want data
    clusters = np.unique(mask)[np.unique(mask) != 0]
    vals = []
    for ss in subj_list:
        print 'Getting subject %s' % s
        