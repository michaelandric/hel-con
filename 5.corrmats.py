#!/usr/bin/env python
"""This is to determine the graphs.
Principal method is using Pearson correlation and binary matrices"""
__author__ = 'andric'

import sys
import os
import time
import pandas as pd
import numpy as np
import networkx as nx
from shlex import split
from subprocess import call, STDOUT


class GRAPHS:

    def __init__(self, subjid, inputTS, thresh_density):
        """
        Initialize for hel
        :param subjid: subject identifier
        :param inputTS: the time series for input
        :param thresh_density: This is the threshold
        :return:
        """
        self.ss = subjid
        self.dens = thresh_density
        self.input = inputTS
        print 'Initializing. -- '+time.ctime()


    def make_graph(self, outname):
        print 'Now making graph -- '+time.ctime()
        ts = pd.read_csv(self.input).T
        print 'Time series loaded \nStarting correlation -- '+time.ctime()
        corrmat = ts.corr()
        print 'Correlation matrix done. -- '+time.ctime()
        corrmatUT = np.triu(corrmat)
        np.fill_diagonal(corrmatUT, 0)
        print 'Starting sort. -- '+time.ctime()
        corrsrtd = np.sort(corrmatUT[corrmatUT !=0], kind='mergesort')
        print 'Sort done. \nThresholding... -- '+time.ctime()
        threshd = corrsrtd[int(len(corrsrtd)*(1.-float(self.dens))):]
        print 'Thresholding done. \nNow getting edge indices -- '+time.ctime()
        ix = np.in1d(corrmatUT.ravel(), threshd).reshape(corrmatUT.shape)
        inds = zip(np.where(ix)[0], np.where(ix)[1])
        G = nx.Graph()
        print 'Graph initialized. \nAdding edges -- '+time.ctime()
        for ii in inds:
            G.add_edge(ii[0], ii[1])
        print 'Graph complete. \nWriting it to file -- '+time.ctime()
        nx.write_edgelist(G, outname, data=False)
        print 'Graph edgelist written out. \nDONE. -- '+time.ctime()

