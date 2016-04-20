# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 12:30:50 2015

Assign bin identifiers to SNSC values

@author: andric
"""


import os
from itertools import dropwhile
import numpy as np


def iscomment(s):
    return s.startswith('#')


def assigner(inputname, outname):
    """
    orig range is .4, .6
    But only relevant for 5% dens thresh
    Modified for 'stratified_2' with
    lowered by .5, so range is .35, .55
    """
    vertvals = []
    f = open(inputname, "r")

    for line in dropwhile(iscomment, f):
        vertvals.append(line.split()[1])

    vertvals = map(float, vertvals)

    binvals = np.zeros(len(vertvals))

    for i, v in enumerate(vertvals):
        if v == 777:
            binvals[i] = 4
        elif v < .35:
            binvals[i] = 5
        elif v > .35 and v <= .4:
            binvals[i] = 6
        elif v > .4 and v <= .45:
            binvals[i] = 7
        elif v > .45 and v <= .5:
            binvals[i] = 8
        elif v > .5 and v <= .55:
            binvals[i] = 9
        elif v > .55:
            binvals[i] = 10

    binvals = map(int, binvals)

    outdat = ''
    for i, v in enumerate(binvals):
        outdat += str(i)+' '+str(v)+'\n'

    outf = open(outname, 'w')
    outf.write(outdat)
    outf.close()


if __name__ == "__main__":

    os.chdir(os.path.join(os.environ['hel'], 'graph_analyses',
                          'subrun_group_jaccard'))

    for nom in ['1and4', '3and6']:
        for h in ['lh', 'rh']:
            for td in [.15]:
                pref = 'subrun_group_jaccard_median_{}_mesh140_{}_{}'.format(h, td, nom)
                inname = '{}.1D'.format(pref)
                outname = '{}.stratified_2.1D'.format(pref)
                assigner(inname, outname)
