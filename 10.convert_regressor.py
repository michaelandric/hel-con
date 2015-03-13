#!/usr/bin/evn python
__author__ = 'andric'

import sys
import os
import numpy as np
from scipy import stats

def zscore_input(infile, type):
    """
    This is to take the wavrd Task file input and normalize
    :param infile: The wavrd (task convolved with GAMMA function) input
    :param type: Either "zrange" (z-score) or "ones" for -1 to 1 interval
    :return: Normalized input design
    """
    indat = np.loadtxt(infile)
    if type == 'zrange':
        normed = stats.zscore(indat)
    elif type == 'ones':
        normed = (((indat-np.min(indat)) / (np.max(indat) - np.min(indat))*2)-1)

    return normed

if __name__ == '__main__':

    if len(sys.argv) < 4:
        sys.stderr.write("You done screwed up! \n"
                         "Usage: %s <INPUT FILE> <TYPE> <OUTPUT NAME> \n" %
                         (os.path.basename(sys.argv[0]),))

    infle = sys.argv[1]
    type_of_normed = sys.argv[2]
    outname = sys.argv[3]

    outfile = zscore_input(infle, type_of_normed)
    np.savetxt(outname, outfile, fmt='%.3f')
