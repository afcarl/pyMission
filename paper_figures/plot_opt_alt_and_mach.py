# Simultaneous optimization of Altitude and Mach to reproduce figure 10 in the paper.

from __future__ import division
import os
import time
from subprocess import call

import numpy as np

import matplotlib
#matplotlib.use('Agg')
import matplotlib.pylab
import matplotlib.pylab as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx


from openmdao.lib.casehandlers.api import CaseDataset

###########################
# USER SPECIFIED INPUTS:

#fuel_guess = 200000.0
fuel_guess = 100000
x_range = 1000.0 * 1.852

# END USER SPECIFIED INPUTS
###########################

# Read in the openmdao final dataset.
cds1 = CaseDataset('opt_alt_and_mach_final.bson', 'bson')
final_data = cds1.data.fetch() # results
final_data = final_data[-1] # Get last case. Earlier cases are sub-iterations.

# Constants are stored here
x_init = np.array(cds1.simulation_info['constants']['SysXBspline.x_init'])

# Variables are stored in the cases.
dist = np.array(final_data['SysXBspline.x'])
altitude = np.array(final_data['SysHBspline.h'])
speed = np.array(final_data['SysSpeed.v'])
mach = np.array(final_data['SysMVBspline.M'])
eta = np.array(final_data['SysTripanCMSurrogate.eta'])
gamma = np.array(final_data['SysGammaBspline.Gamma'])
temp = np.array(final_data['SysTemp.temp'])
alpha = np.array(final_data['SysTripanCLSurrogate.alpha'])
rho = np.array(final_data['SysRho.rho'])
throttle = np.array(final_data['SysTau.tau'])
lift_c = np.array(final_data['SysCLTar.CL'])
fuel = np.array(final_data['SysFuelWeight.fuel_w'])
thrust = np.array(final_data['SysCTTar.CT_tar'])
drag_c = np.array(final_data['SysTripanCDSurrogate.CD'])

# various scaling params
dist = dist/(1e3 * 1.852)*1e6
thrust *= 0.225
altitude *= 3.28
speed *= 1.94 * 1e2
fuel *= 0.225/1e3 * 1e5
thrust *= 0.225/1e3 * 1e6


subfig, subax = plt.subplots(8, 1, sharex=True)

dist /= 1000

lines = []

values = [altitude, gamma, mach, alpha,
          lift_c, lift_c/drag_c,
          thrust, fuel]
labels = [' Alt ($10^3$ ft)',
          'Path Angle (deg)', 'Mach', 'AoA (deg)',
          '$C_L$', '$L/D$',
          'Thrust ($10^3$ lb)', 'Fuel ($10^3$ lb)']
#limits = [[-5, 30],
          #[-6, 25], [0.1, 0.9], [-2.3, 4.3],
          #[0.1, 0.7], [0, 35],
          #[-25, 250], [-2, 22]]
#ticks = [[0, 25],
          #[-3, 22], [0.2, 0.85], [-2, 4],
          #[0.15, 0.65], [5, 30],
          #[0, 225], [0, 20]]
limits = [[-5, 35],
          [-6, 20], [0.1, 0.9], [-2.3, 3.3],
          [0.1, 0.75], [0, 12],
          [-25, 250], [-2, 22]]
ticks = [[0, 25],
          [-3, 15], [0.2, 0.85], [-2, 3],
          [0.15, 0.7], [5, 10],
          [0, 225], [0, 20]]
#colorVal = scalarMap.to_rgba(1)

for i, a in enumerate(subax):
    retLine, = a.plot(dist, values[i])
    lines.append(retLine)
    a.spines['top'].set_visible(False)
    a.spines['right'].set_visible(False)
    if i < 7:
        a.spines['bottom'].set_visible(False)
        a.get_yaxis().tick_left()
        a.set_xticks([])
    else:
        a.get_yaxis().tick_left()
        #a.set_xticks([0.0, 1.0])
    a.set_ylabel(r'%s' %(labels[i]), rotation='horizontal', fontsize=10)
    a.set_xlim(-0.05, 1.05)
    a.set_yticks(ticks[i])
    a.set_ylim(limits[i])
    for tick in a.yaxis.get_major_ticks():
        tick.label.set_fontsize(10)
    subfig.subplots_adjust(left=0.25, right=0.98, top=0.98, bottom=0.05,
                        wspace=0.05, hspace=0.05)
a.set_xlabel(r'Normalized Range', fontsize=10)
#subfig.savefig('./Results/SciTech_CarpetRange.png')
subfig.savefig('./plots/SciTech_CarpetRange.png')
matplotlib.pylab.show()
print 'done'