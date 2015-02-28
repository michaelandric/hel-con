#!/usr/bin/env python
"""This is to convert edgelists to binary encoding for louvain community detection.
Then to run community detection."""
__author__ = 'andric'

import sys
import os
import time
import numpy as np
from shlex import split
from subprocess import call, STDOUT, PIPE, Popen

class COMMUN:

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
        :return: Writes to file the binary formatted graph for Louvain community detection
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
            f = open('stdout_files/stdout_from_convert.txt', 'w')
            print 'Converting edgelist to binary for community detection -- '+time.ctime()
            cmdargs = split('community_convert -i '+self.graphname+'  -o '+self.graphname+'.bin')
            call(cmdargs, stdout=f, stderr=STDOUT)
            f.close()
            print 'Conversion done. -- '+time.ctime()
        elif os.path.exists(self.graphname+'.gz'):
            print 'You need to unzip the graph! '+time.ctime()
        else:
            print 'Cannot find the graph. Check your configuration and inputs. \nFlaming... '+time.ctime()

    def get_modularity(self, tree_out):
        """
        Do community detection with Louvain algorithm.
        :param tree_out:
        :return: Q value, also writes tree to file.
        """
        fh = open(tree_out, 'w')
        cmdargs = split('community -l -1 '+self.graphname+'.bin')
        m = Popen(cmdargs, stdout=fh, stderr=PIPE).communicate()
        fh.close()
        return float(m[1])


if __name__ == '__main__':

    if len(sys.argv) < 4:
        sys.stderr.write("You done fucked up! \n"
                         "Usage: %s <SUBJECT ID> <CONDITION ID> <THRESH DENSITY> \n" %
                         (os.path.basename(sys.argv[0]),))

    subjid = sys.argv[1]
    condition = sys.argv[2]
    thresh_density = sys.argv[3]

    os.chdir(os.environ['hel']+'/%s/connectivity/' % subjid)
    print os.getcwd()
    graph = 'graphs/%s.%s.dens_%s.edgelist' % (subjid, condition, thresh_density)
    cm = COMMUN(graph)
    cm.zipper('unzip')
    cm.convert_graph()
    cm.zipper('zip')
    # Below for doing modularity
    treedir = 'trees'
    mod_dir = 'modularity'
    niter = 100
    Qs = np.array(np.zeros(niter))
    print 'Doing community detection. \nNumber of iterations: %s -- ' % niter+time.ctime()
    if not os.path.exists(treedir):
        os.makedirs(treedir)
    if not os.path.exists(mod_dir):
        os.makedirs(mod_dir)
    for n in xrange(niter):
        tree_outname = '%s/iter%s.%s.%s.dens_%s.tree' % (treedir, n, subjid, condition, thresh_density)
        Qs[n] = cm.get_modularity(tree_outname)
    np.savetxt('%s/%s.%s.dens_%s.Qval' % (mod_dir, subjid, condition, thresh_density), Qs, fmt='%.5f')
