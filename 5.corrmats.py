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
        self.dens = float(thresh_density)
        self.input = inputTS
        print 'Initializing. -- '+time.ctime()

    def make_graph(self, outname):
        """
        Getting the graph by reading the time series input.
        Doing Pearson's correlation. Sort values then threshold by density.
        Find the indices for thresholded values.
        Make binary graph with those as edges.
        Write the list of edges to file.
        :param outname: Outname for the graph
        :return: Writes to text file the outname
        """
        print 'Now making graph -- '+time.ctime()
        ts = pd.read_csv(self.input, header=None).T   # transposing this
        n_vox = ts.shape[1]
        compl_graph = int((n_vox*(n_vox-1))/2)
        n_edges = int(compl_graph*self.dens)
        print 'Input is read. \nNow getting the correlation matrix. '+time.ctime()
        corrmat = np.corrcoef(ts)
        corrmat_ut = np.nan_to_num(np.triu(corrmat, k=1))
        print 'Starting sort. -- '+time.ctime()
        corrsrtd = np.sort(corrmat_ut[corrmat_ut > 0], kind='mergesort')
        print 'Sort done. \nThresholding... -- '+time.ctime()
        threshd = corrsrtd[-n_edges:]
        print 'Thresholding done. \nNow getting edge indices -- '+time.ctime()
        ix = np.searchsorted(threshd, corrmat_ut, 'right')
        print 'Found in 1d '+time.ctime()
        n, v = np.where(ix)
        print 'Done getting where coords... '+time.ctime()
        inds = zip(n, v)
        G = nx.Graph()
        print 'Graph initialized. \nAdding edges -- '+time.ctime()
        G.add_edges_from(inds)
        print 'Graph complete. \nWriting it to file -- '+time.ctime()
        nx.write_edgelist(G, outname, data=False)
        print 'Graph edgelist written out. \nDONE. -- '+time.ctime()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.stderr.write("You done screwed up! \n"
                         "Usage: %s <SUBJECT ID> <CONDITION ID> <THRESH DENSITY> \n" %
                        (os.path.basename(sys.argv[0]),))

    subjid = sys.argv[1]
    condition = sys.argv[2]
    thresh_density = sys.argv[3]

    os.chdir(os.environ['hel']+'/%s/connectivity/' % subjid)
    print os.getcwd()
    inputTS = '%s_cleanTScat_%s.allruns_GMmask_dump.csv' % (condition, subjid)
    graph_outname = 'graphs/%s.%s.dens_%s.edgelist.gz' % (subjid, condition, thresh_density)
    GR = GRAPHS(subjid, inputTS, thresh_density)
    GR.make_graph(graph_outname)
