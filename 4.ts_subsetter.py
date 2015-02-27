#!/usr/bin/env python
"""
This subsets the time series so later don't have to read in the entire thing
"""
import os
import sys
import time
import numpy as np
import pandas as pd



def TSsubsetter(inputTS, state):
    """
    This is to grab a section of the time series
    :param inputTS: The input time series
    :param state: Either Task or Rest
    :return: Writes to file the subset of the time series
    """
    if state=='Rest':
        subsection = [(79,100),(211,243),(351,361),(471,485),(524,539),(615,631),(705,727),(805,826),(937,969),(1077,1087),(1197,1211),(1250,1265),(1341,1357),(1431,1451)]
        section = [i for j in (range(x[0]+2, x[1]+1) for x in subsection) for i in j]
    elif state=='Task':
        subsection = [(2,78),(101,210),(244,350),(362,470),(486,523),(540,614),(632,704),(728,804),(827,936),(970,1076),(1088,1196),(1212,1249),(1266,1340),(1358,1430)]
        section = [i for j in (range(x[0]+4, x[1]+1) for x in subsection) for i in j]
    else:
        print 'Where is state? Task? Rest? We done here. This will fail now.'+time.ctime()
        sys.exit()
    ts = np.loadtxt(inputTS)
    subsetts = pd.DataFrame(ts).iloc[:,section]
    return subsetts

if __name__ == '__main__':

    subj_list=['hel18']:
    for ss in subj_list:
        os.chdir(os.environ['hel']+'/%s/connectivity/' % ss)
        print os.getcwd()+' is the current dir'+time.ctime()
        for state in ['Task', 'Rest']:
            inputTSname = 'cleanTScat_%s.allruns_GMmask_dump' % ss
            #state = 'Task'   # should be "Task" or "Rest"
            outname = '%s_%s.csv' % (state, inputTSname)
            TSout = TSsubsetter(inputTSname, state)
            TSout.to_csv(outname, header=False, index=False)
            print 'TS subset written. We done.'+time.ctime()


