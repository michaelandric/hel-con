# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 14:48:05 2015

Implementing routine to do cross-correlation
Will use the normalized version as in R's "ccf" function

@author: andric
"""

import os
import numpy as np


def ccf_xcorr(a, b, mode='same'):
    """
    https://gist.github.com/werediver/e5348bf945aeecfc5a2a
    https://stats.stackexchange.com/questions/116330/proper-normalized-cross-correlation
    """
    a = np.asarray(a)
    b = np.asarray(b)

    a = a - a.mean()
    b = b - b.mean()

    r = np.correlate(a, b, mode)

    r /= np.sqrt(np.correlate(a, a) * np.correlate(b, b))
    lag_max = int(len(r) / 2)
    lags = np.asarray(xrange(-lag_max, lag_max + len(r) % 2))

    sl = 2 / np.sqrt(len(r))

    return r, lags, sl


def ccf_xcorr_matapply(v, mode='same'):
    """
    https://gist.github.com/werediver/e5348bf945aeecfc5a2a
    https://stats.stackexchange.com/questions/116330/proper-normalized-cross-correlation

    This version meant for use with numpy.apply_along_axis
    it takes one mat and splits them
    """
    ts_length = 547
    a = np.asarray(v[:ts_length])
    b = np.asarray(v[ts_length:])

    r = np.correlate(a, b, mode)

    r /= np.sqrt(np.correlate(a, a) * np.correlate(b, b))
    lag_max = int(len(r) / 2)
    lags = np.asarray(xrange(-lag_max, lag_max + len(r) % 2))

#    subsets correspond to taking lags -4 to 4
    r = r[269:278]
    lags = lags[269:278]
    lags[np.isnan(r)] = 0
    r[np.isnan(r)] = 0
    return (r.max(), lags[r.argmax()])


if __name__ == '__main__':
    subj_list = []
    for i in range(1, 20):
        subj_list.append('hel%d' % i)
    subj_list.remove('hel9')   # because this is bad subj

    for ss in subj_list:
        ss_dir = os.path.join(os.environ['hel'], ss)
        proc_dir = os.path.join(ss_dir, 'preprocessing')
        anat_dir = os.path.join(ss_dir, 'volume.%s.anat' % ss)
        conn_dir = os.path.join(os.environ['hel'], 'graph_analyses',
                                '%s/global_connectivity' % ss)

        ts1_fname = os.path.join(proc_dir, 'task_sess_1_%s_gm_mskd.txt' % ss)
        ts2_fname = os.path.join(proc_dir, 'task_sess_2_%s_gm_mskd.txt' % ss)
        ts1 = np.loadtxt(ts1_fname)
        ts2 = np.loadtxt(ts2_fname)
        outcor = np.apply_along_axis(ccf_xcorr_matapply, 1,
                                     np.array(np.hstack([ts1, ts2])))
        outname_v = 'ccf_vals_out_%s_gm_mskd' % ss
        outfname_v = os.path.join(conn_dir, outname_v)
        np.savetxt(outfname_v, np.arctanh(outcor[:, 0]), fmt='%.4f')
        outname_lag = 'ccf_lag_out_%s_gm_mskd' % ss
        outfname_lag = os.path.join(conn_dir, outname_lag)
        np.savetxt(outfname_lag, outcor[:, 1], fmt='%i')
