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
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score, jaccard_similarity_score


class Graphs(object):

    def __init__(self, subjid, inputTS, thresh_density, graph_dir):
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
        print 'Initializing. -- '+time.ctime()

    def make_graph(self, el_name):
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
        np.savetxt(el_name, inds, fmt='%d')
        print 'Graph edgelist written out. \nDONE. -- '+time.ctime()
        return np.mean(threshd)

    def make_networkx_graph(self, n_nodes, el_name):
        # setting it up for further use
        g = nx.Graph()
        g.add_nodes_from(range(n_nodes))
        ed = nx.read_edgelist(os.path.join(self.graph_dir, el_name),
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

    def make_random_graph(self, nnodes, outname):
        rg = nx.fast_gnp_random_graph(nnodes, self.dens)
        nx.write_edgelist(rg, outname, data=False)


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

    def adj_rand(self, p1, p2):
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

    def normalized_MI(self, p1, p2):
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

    def snsc(self, input1, input2):
        """
        Get Single Node Set Consistency (SNSC)
        between two partitions
        Each input is a separate file, result of
        tree output from modularity function
        """
        coms1 = np.loadtxt(input1)
        coms2 = np.loadtxt(input2)
        mod_dict1 = {}
        mod_dict2 = {}
        for i in np.unique(coms1):
            mod_dict1[i] = [v for v, c in enumerate(coms1) if c == i]
        for i in np.unique(coms2):
            mod_dict2[i] = [v for v, c in enumerate(coms2) if c == i]

        preservation = np.zeros(len(coms2))
        """Return 777 if the community includes less than 20 voxels """
        for i in xrange(len(coms2)):
            if len(mod_dict2[coms2[i]]) < 20 or len(mod_dict1[coms1[i]]) < 20:
                preservation[i] = 777
            else:
                set2 = set(mod_dict2[coms2[i]])
                set1 = set(mod_dict1[coms1[i]])
                inter = len(set2.intersection(set1))
                preservation[i] = inter / float(len(mod_dict2[coms2[i]]))

        return preservation

    def jaccard_vw(self, input1, input2):
        """
        Jaccard similarity coefficient
        between two partitions at voxel-by-voxel
        Each input is a separate file, result of
        tree output from modularity function
        Similarity is intersection / union
        """
        coms1 = np.loadtxt(input1)
        coms2 = np.loadtxt(input2)
        mod_dict1 = {}
        mod_dict2 = {}
        for i in np.unique(coms1):
            mod_dict1[i] = [v for v, c in enumerate(coms1) if c == i]
        for i in np.unique(coms2):
            mod_dict2[i] = [v for v, c in enumerate(coms2) if c == i]

        jacc = np.zeros(len(coms2))
        """Return 777 if the community includes less than 20 voxels """
        for i in xrange(len(coms2)):
            if len(mod_dict2[coms2[i]]) < 20 or len(mod_dict1[coms1[i]]) < 20:
                jacc[i] = 777
            else:
                set2 = set(mod_dict2[coms2[i]])
                set1 = set(mod_dict1[coms1[i]])
                inter = len(set2.intersection(set1))
                union = len(set2.union(set1))
                jacc[i] = float(inter) / float(union)

        return jacc


def avg_global_connectivity(inputts, transform=True):
    """
    Construct correlation matrix and
    take average (Fisher transformed) correlation value
    at every row (i.e., voxel).
    :param inputts: Input time series
    in voxels (rows) x time points (cols)
    :return : avg correlation value at each voxels,
    default is Fisher z-transform
    """
    print 'Doing avg_global_connectivity '
    print time.ctime()
    print 'Input: %s' % inputts
    ts = np.loadtxt(inputts)
    ts_corr = np.corrcoef(ts)
    corr_avg = np.nanmean(ts_corr, axis=1)
    # in case there were 0 rows f'n things up
    corr_avg[np.isnan(corr_avg)] = 0
    if transform is True:
        return np.arctanh(corr_avg)
    else:
        return corr_avg


def seeded_connectivity(seedts, inputts, transform=True):
    """
    Correlate seed time series against every other
    """
    print 'Doing seed correlation'
    print time.ctime()
    print 'Input ts: %s' % inputts
    ts = np.loadtxt(inputts)
    seed = np.loadtxt(inputts)
    


def dummyvar(cis, return_sparse=False):
    '''
    This is an efficient implementation of matlab's "dummyvar" command
    using sparse matrices.
    input: partitions, NxM array-like containing M partitions of N nodes
        into <=N distinct communities
    output: dummyvar, an NxR matrix containing R column variables (indicator
        variables) with N entries, where R is the total number of communities
        summed across each of the M partitions.
        i.e.
        r = sum((max(len(unique(partitions[i]))) for i in range(m)))
    '''
    # num_rows is not affected by partition indexes
    n = np.size(cis, axis=0)
    m = np.size(cis, axis=1)
    r = np.sum((np.max(len(np.unique(cis[:, i])))) for i in range(m))
    nnz = np.prod(cis.shape)

    ix = np.argsort(cis, axis=0)
    # s_cis=np.sort(cis,axis=0)
    # FIXME use the sorted indices to sort by row efficiently
    s_cis = cis[ix][:, xrange(m), xrange(m)]

    mask = np.hstack((((True,),)*m,(s_cis[:-1,:]!=s_cis[1:,:]).T))
    indptr, = np.where(mask.flat)
    indptr = np.append(indptr, nnz)

    import scipy.sparse as sp
    dv = sp.csc_matrix((np.repeat((1, ), nnz),
                        ix.T.flat, indptr), shape=(n, r))
    return dv.toarray()


def agreement(ci, buffsz=None):
    """
    Takes as input a set of vertex partitions CI of
    dimensions [vertex x partition]. Each column in CI contains the
    assignments of each vertex to a class/community/module. This function
    aggregates the partitions in CI into a square [vertex x vertex]
    agreement matrix D, whose elements indicate the number of times any two
    vertices were assigned to the same class.

    In the case that the number of nodes and partitions in CI is large
    (greater than ~1000 nodes or greater than ~1000 partitions), the script
    can be made faster by computing D in pieces. The optional input BUFFSZ
    determines the size of each piece. Trial and error has found that
    BUFFSZ ~ 150 works well.

    Inputs,     CI,     set of (possibly) degenerate partitions
                BUFFSZ, optional second argument to set buffer size

    Outputs:    D,      agreement matrix
    """
    m, n = ci.shape

    if buffsz is None:
        buffsz = 1000
    # noticed this is where there is a bug
    # used 'n' instead of 'm'
    # corrected it: 9.June.2015
    if m <= buffsz:
        ind = dummyvar(ci)
        D = np.dot(ind, ind.T)
    else:
        a = np.arange(0, n, buffsz)
        b = np.arange(buffsz, n, buffsz)
        if len(a) != len(b):
            b = np.append(b, m)
        D = np.zeros((m, m))
        for i, j in zip(a, b):
            y = ci[:, i:j+1]
            ind = dummyvar(y)
            D += np.dot(ind, ind.T)

    np.fill_diagonal(D, 0)
    return D
