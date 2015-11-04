#!/usr/bin/env python
"""
Uses the powerlaw package
See here: http://arxiv.org/abs/1305.0215
"""

import numpy as np
import os
import powerlaw
import matplotlib.pyplot as plt

os.chdir('/Users/andric/Documents/workspace/hel/group_modularity_thr0.5msk')
degs = np.loadtxt('degrees_group_task_diff_thr8_component_dens_0.15.vals')
degs_pos = degs[degs > 0]

results = powerlaw.Fit(degs_pos)

font = {'family':'sans-serif','size':14, 'sans-serif': ['Arial']}
plt.rc('font',**font)
#plt.rc('legend',**{'fontsize':14})
fig1 = results.plot_ccdf(linewidth=3, label='Degrees of difference component', color='purple')
results.power_law.plot_ccdf(ax=fig1, linewidth=2, color='orange', linestyle='--', label='Power law fit')
results.truncated_power_law.plot_ccdf(ax=fig1, linewidth=2, color='g', label='Truncated power law fit')
fig1.set_ylabel(u"p(X≥x)")
fig1.set_xlabel(r"Degree values")
handles, labels = fig1.get_legend_handles_labels()
leg = fig1.legend(handles, labels, loc=3)
leg.draw_frame(False)
plt.savefig('Degree_diff_comp_fit.pdf', dpi=300, transparent=True)
plt.close()


results2 = powerlaw.Fit(degs_pos, xmin=1)
fig1 = results2.plot_ccdf(linewidth=4, label='Degrees of difference component', color='purple')
results2.power_law.plot_ccdf(ax=fig1, linewidth=2, color='orange', linestyle='--', label='Power law fit')
#results2.lognormal.plot_ccdf(ax=fig1, linewidth=1, color='cyan', linestyle='--', label='Lognormal fit')
results2.truncated_power_law.plot_ccdf(ax=fig1, linewidth=2, color='g', label='Truncated power law fit')
fig1.set_ylabel(u"p(X≥x)")
fig1.set_xlabel(r"Degree values")
handles, labels = fig1.get_legend_handles_labels()
leg = fig1.legend(handles, labels, loc=3, fontsize=13)
leg.draw_frame(False)
plt.savefig('Degree_diff_comp_fit2.pdf', dpi=300, transparent=True)
plt.close()

