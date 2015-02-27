#!/usr/bin/env python
"""This is to convert edgelists to binary encoding for louvain community detection.
Then to run community detection."""
__author__ = 'andric'

import sys
import os
import time
from shlex import split
from subprocess import call, STDOUT

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

    def get_modularity(self, tree_out, modscore):
        """
        Do community detection with Louvain algorithm.
        :param tree_out:
        :param modscore:
        :return: Writes tree and modscore to separate files.
        """
        f = open(tree_out, 'w')
        m = open(modscore, 'w')
        cmdargs = split('community -l -1 '+self.graphname+'.bin')
        call(cmdargs, stdout=f, stderr=m)
        f.close()
        m.close()


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
        Qdir = 'Qvals'
        niter = 100
        print 'Doing community detection. \nNumber of iterations: %s -- ' % niter+time.ctime()
        if not os.path.exists(treedir):
            os.makedirs(treedir)
        if not os.path.exists(Qdir):
            os.makedirs(Qdir)
        for n in xrange(niter):
            tree_outname = '%s/iter%s.%s.%s.dens_%s.tree' % (treedir, n, subjid, condition, thresh_density)
            modscorename = '%s/iter%s.%s.%s.dens_%s.Qval' % (Qdir, n, subjid, condition, thresh_density)
            cm.get_modularity(tree_outname, modscorename)
