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
import scipy.stats
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

    def get_inds(self, data):
        """
        This derives correlation matrix for data and returns thresholded indices
        :param data: Input TS
        :return: The indices that pass density threshold
        """
        rows = data.shape[0]
        data = np.array(data)
        ms = data.mean(axis=1)[(slice(None,None,None),None)]
        datam = data - ms
        datass = np.sqrt(scipy.stats.ss(datam,axis=1))
        temp = np.dot(datam[0:], datam[0].T)
        out_rs = np.array((temp / (datass[0:]*datass[0]))[1:])
        n = 1
        mtinds = np.arange(1, rows)
        for i in xrange(1, rows):
            temp = np.dot(datam[i:], datam[i].T)
            out_rs = np.append(out_rs, (temp / (datass[i:]*datass[i]))[1:])
            n = n+rows
            mtinds = np.append(mtinds, np.arange(n+i, rows*(i+1)))
        blank = np.array(np.zeros(rows**2).reshape(rows,rows))
        nin = mtinds[out_rs.argsort()[int((rows*(rows-1)/2) * (1-self.dens)):]]
        blank.ravel()[nin] = 1
        inds = zip(np.where(blank)[0], np.where(blank)[1])
        return inds

    def make_graph(self, outname):
        print 'Now making graph -- '+time.ctime()
        ts = pd.read_csv(self.input, header=None)
        print 'Input is read. \nNow getting the thresholded indices. '+time.ctime()
        inds = self.get_inds(ts)
        print 'Indices done. '+time.ctime()
        G = nx.Graph()
        print 'Graph initialized. \nAdding edges -- '+time.ctime()
        for ii in inds:
            G.add_edge(ii[0], ii[1])
        print 'Graph complete. \nWriting it to file -- '+time.ctime()
        nx.write_edgelist(G, outname, data=False)
        print 'Graph edgelist written out. \nDONE. -- '+time.ctime()

    def convert_graph(self, graph):
        '''This is to convert graph from text to binary file for community detection'''
        f = open('stdout_files/stdout_from_convert.txt', 'w')
        print 'Converting edgelist to binary for community detection -- '+time.ctime()
        cmdargs = split('community_convert -i '+graph+'  -o '+graph+'.bin')
        call(cmdargs, stdout=f, stderr=STDOUT)
        print 'Conversion done. -- '+time.ctime()
        f.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.stderr.write("You done fucked up! \n"
                         "Usage: %s <SUBJECT ID> <CONDITION ID> <THRESH DENSITY> \n" %
                        (os.path.basename(sys.argv[0]),))

    subjid = sys.argv[1]
    condition = sys.argv[2]
    thresh_density = sys.argv[3]

    os.chdir('/mnt/lnif-storage/urihas/MAstdstt/%s' % subjid)
    print os.getcwd()
    graph_outname = '/mnt/lnif-storage/urihas/MAstdstt/%s/graphs/%s.%s.dens_%s.edgelist' % (subjid, subjid, condition, thresh_density)
    GR = GRAPHS(subjid, condition, thresh_density)
    GR.make_graph(graph_outname)
    GR.convert_graph(graph_outname)
