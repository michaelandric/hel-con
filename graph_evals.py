# -*- coding: utf-8 -*-
"""
Created on Fri May 29 16:29:43 2015

@author: andric
"""

import os
import sys
import time
import numpy as np
import networkx as nx
import bct
from shlex import split
from subprocess import call, STDOUT, PIPE, Popen
from sklearn.metrics import normalized_mutual_info_score
from sklearn.metrics import adjusted_rand_score


class Graphs(object):

    def __init__(self, subjid, inputTS, thresh_density,
                 graph_dir, edgelist_name):
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
        self.graph_dir = graph_dir
        self.el_name = edgelist_name
        print 'Initializing. -- '+time.ctime()

    def make_graph(self):
        """
        Makes graph by pairwise correlation
        Threshold at density
        Returns average correlation among values
        """
        print 'Now making graph -- '+time.ctime()
        n_vox = self.input.shape[0]
        compl_graph = int((n_vox*(n_vox-1))/2)
        n_edges = int(compl_graph*self.dens)
        print 'Input is read. '
        print 'Now getting the correlation matrix. '+time.ctime()
        corrmat = np.corrcoef(self.input)
        corrmat_ut = np.nan_to_num(np.triu(corrmat, k=1))
        print 'Starting sort. -- '+time.ctime()
        corrsrtd = np.sort(corrmat_ut[corrmat_ut > 0], kind='mergesort')
        print 'Sort done. \nThresholding... -- '+time.ctime()
        threshd = corrsrtd[-n_edges:]
        print 'Thresholding done. \nNow getting edge indices -- '+time.ctime()
        ix = np.searchsorted(threshd, corrmat_ut, 'right')
        n, v = np.where(ix)
        inds = np.array(zip(n, v), dtype=np.int32)
        print 'Got graph edges. \nWriting it to file -- '+time.ctime()
        np.savetxt(self.el_name, inds, fmt='%d')
        print 'Graph edgelist written out. \nDONE. -- '+time.ctime()
        return np.mean(threshd)

    def make_networkx_graph(self, n_nodes):
        # setting it up for further use
        g = nx.Graph()
        g.add_nodes_from(range(n_nodes))
        ed = nx.read_edgelist(os.path.join(self.graph_dir, self.el_name),
                              nodetype=int)
        g.add_edges_from(ed.edges())
        return g

    def nx_get_modularity(self, graph):
        """
        Gets modularity louvain
        Uses bct package
        Returns communities and modularity value
        at highest level
        :param graph: Input graph via networkx
        :return c: communities
        :return q: modularity value
        """
        c, q = bct.modularity_louvain_und(nx.adjacency_matrix(graph).toarray())
        return (c, q)

    def max_q(self, fname):
        """
        Get the maximum modularity value
        :param fname: File name containing Q values
        :return : max q value, iteration with max q value
        """
        print 'Getting max q value -- %s' % time.ctime()
        q_vals = np.loadtxt(fname)
        iter_max = q_vals.argmax()
        return (np.max(q_vals), iter_max)

    def max_nmod(self, fname, indx):
        """
        Get the maximum modularity value
        :param fname: File name containing Q values
        :param indx: corresponding index for max q
        :return : nmods at max q
        """
        print 'Getting max q value -- %s' % time.ctime()
        n_mods = np.loadtxt(fname)
        return n_mods[indx]

    def n_modules(self, tname):
        """
        Get the number of modules
        :param tname: File name for tree
        :return : number of modules > 1
        """
        from collections import Counter
        print 'Getting number of modules -- %s' % time.ctime()
        n_mods = np.zeros(100)
        tree = np.loadtxt(tname)
        cnts = np.array(Counter(tree[:, 1]).values())
        n_mods = len(cnts[np.where(cnts > 1)])
        return n_mods


class CommunityDetect(object):
    """
    Using the cpp versionso of the louvain community detection
    This interacts with Popen to read in and out parameters.
    Hopefully in future I will have this in cython
    Or something

    """

    def __init__(self, edgelist):
        """
        Methods for converting text file edgelist to binary format.
        Doing community detection.
        :param edgelist: The graph
        """
        self.graphname = edgelist

    def zipper(self, method):
        """
        Unzip / zip the graph file for use with Louvain tools.
        :param file: This graph to be unzipped/zipped
        :param method: Either "zip" or "unzip"
        :return: Writes to file the binary formatted graph
        for Louvain community detection
        """
        try:
            if method == 'zip':
                print 'Zipping up %s -- ' % self.graphname+time.ctime()
                cmds = split('gzip %s' % self.graphname)
                call(cmds)
                print 'DONE. '+time.ctime()
            elif method == 'unzip':
                print 'Unzipping  %s -- ' % self.graphname+time.ctime()
                cmds = split('gunzip %s.gz' % self.graphname)
                call(cmds)
                print 'DONE. '+time.ctime()
        except IOError:
            print 'zipper not working. No file? Flaming... '+time.ctime()
            sys.exit()

    def convert_graph(self):
        """
        This is to convert graph for community detection
        :param graph: The graph made in previous function
        :return: Will convert to binary for Louvain algorithm and write to file
        """
        if os.path.exists(self.graphname):
            print 'Converting edgelist to binary for community detection'
            print time.ctime()
            cmdargs = split('community_convert -i %s -o %s.bin' %
                            (self.graphname, self.graphname))
            call(cmdargs)
            print 'Conversion done. -- '+time.ctime()
        elif os.path.exists(self.graphname+'.gz'):
            print 'You need to unzip the graph! '+time.ctime()
        else:
            print 'Cannot find the graph. Check config and inputs.'
            print 'Flaming... '+time.ctime()

    def get_modularity(self, tree_out):
        """
        Do community detection with Louvain algorithm.
        :param tree_out:
        :return: Q value, also writes tree to file.
        """
        fh = open(tree_out, 'w')
        cmdargs = split('community -l -1 %s.bin' % self.graphname)
        m = Popen(cmdargs, stdout=fh, stderr=PIPE).communicate()
        fh.close()
        return float(m[1])

    def get_hierarchical(self, tree_all_levels):
        """
        Find the highest level. Get the tree at that level.
        Write tree to file. Find the number of modules at that level.
        :param tree_all_levels: the entire tree comprising every level
        (from community detection)
        :param tr_outname: Output name for tree at highest hierarchical level
        :retrun mods: The modules tree at highest hierarchical level
        :return n_mods: number of modules at
        highest hierarchical level (> 1)
        """
        from collections import Counter
        cmdargs = split('hierarchy -n %s' % tree_all_levels)
        print cmdargs
        p = Popen(cmdargs, stdout=PIPE).communicate()
        h = int(p[0].split()[3]) - 1
        print 'Getting hierarchy -- '+time.ctime()
        cmdargs = split('hierarchy -l %d %s' % (h, tree_all_levels))
        tree = Popen(cmdargs, stdout=PIPE).communicate()
        stree = [tt for tt in tree[0].split('\n')]
        mods = np.array(np.zeros(len(stree)-1), dtype=np.int)
        for i in xrange(len(mods)):
            mods[i] = stree[i].split()[1]
        cnts = np.array(Counter(mods).values())
        n_mods = len(cnts[np.where(cnts > 1)])
        print time.ctime()
        return (mods, n_mods)


class Similarity(object):

    def adj_rand(p1, p2):
        """
        Return the Adjusted Rand Index
        across two partitions
        :param p1: partition 1
        :param p2; partition 2
        :return : Adjusted Rand Score
        """
        if len(p1) != len(p2):
            print 'Subject needs a fix'
            if len(p1) < len(p2):
                p1 = np.append(p1, p1[len(p1)-1])
            elif len(p2) < len(p1):
                p2 = np.append(p2, p2[len(p2)-1])

        ari = adjusted_rand_score(p1, p2)
        return ari

    def normalized_MI(p1, p2):
        """
        Return the normalized mutual information
        across two partitions
        :param p1: partition 1
        :param p2; partition 2
        :return : normalized mutual information score
        """
        if len(p1) != len(p2):
            print 'Subject needs a fix'
            if len(p1) < len(p2):
                p1 = np.append(p1, p1[len(p1)-1])
            elif len(p2) < len(p1):
                p2 = np.append(p2, p2[len(p2)-1])

        nmi = normalized_mutual_info_score(p1, p2)
        return nmi
