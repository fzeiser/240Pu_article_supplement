from __future__ import division
import numpy as np 
import matplotlib.pyplot as plt 
import sys
from utilities import *
import seaborn as sns
import matplotlib.ticker as ticker

# Level density at neutron separation energy
Bn=6.534000
Bnerr=0.001
rho_Bn=32700000.000000
rho_Bnerr=6500000.000000

sns.set()
# sns.set_context("paper")
sns.set_context("talk")
#sns.set(rc={'figure.figsize':(5.5,6.5)})
sns.set_style("ticks", { 'axes.grid': False})
plt.rcParams['legend.loc'] = 'best'

# import fgteo.rsg to get the calibration
folded1, cal, E_array, tmp = read_mama_2D("fgteo.rsg")

# Constants for energy binning
if(cal["a0x"] != cal["a0y"] 
	or cal["a1x"] != cal["a1y"] 
	or cal["a2x"] != cal["a2y"]):
	raise ValueError("Calibration coefficients for the axes don't match")  

a0 =  cal["a0x"]/1e3 # in MeV
a1 = cal["a1x"]/1e3 # in MeV

# Cross section factor for formula strength = xsec*factor/Egamma
xsec_factor = 8.68e-8

# Import data
fermigasfile = open('fermigas.cnt')
fermigaslines = fermigasfile.readlines()
fermigasfile.close()
Nfermi = len(fermigaslines)
energy = np.zeros(Nfermi)
fermigas = np.zeros(Nfermi)
for i in range(Nfermi):
	energy[i] = a0 + i*a1
	fermigas[i] = float(fermigaslines[i].split()[0])

rholevfile = open('rholev.cnt')
rholevlines = rholevfile.readlines()
rholevfile.close()
Nrholev = len(rholevlines)
rholev = np.zeros(Nrholev)
for i in range(Nrholev):
	rholev[i] = float(rholevlines[i].split()[0])

rholevfile = open('rholev.cnt')
rholevlines = rholevfile.readlines()
rholevfile.close()
Nrholev = len(rholevlines)
rholev = np.zeros(Nrholev)
for i in range(Nrholev):
	rholev[i] = float(rholevlines[i].split()[0])

rhopawfile = open('rhopaw.cnt')
rhopawlines = rhopawfile.readlines()
rhopawfile.close()
Nrhopaw = len(rhopawlines)
rhopaw = np.zeros((Nrhopaw,2))
for i in range(Nrhopaw):
	if i < int(Nrhopaw/2):
		rhopaw[i,0] = float(rhopawlines[i].split()[0])
	else:
		rhopaw[i-int(Nrhopaw/2),1] = float(rhopawlines[i].split()[0])

# Plotting, level density
fig, axes = plt.subplots()
plt.yscale('log')

axes.tick_params("x", top="off")
axes.tick_params("y", right="off")
axes.yaxis.set_minor_locator(ticker.NullLocator())

plt.plot(energy[energy>0], fermigas[energy>0], '--', color='grey', label='Constant-temperature model')
plt.hold('on')
plt.plot(energy[0:Nrholev], rholev, color='black', label='Known levels')
plt.errorbar(energy[0:Nrhopaw], rhopaw[:,0], yerr=rhopaw[:,1], fmt='.', markersize="15",color='midnightblue', label='Present work, exp. data points')
plt.errorbar(Bn, rho_Bn, yerr=rho_Bnerr, fmt='s', label=r'$\rho$ from neutron res. data', color='black')

plt.xlim([-0.2,7])
plt.ylim([1e-0, 1e8])
handles, labels = axes.get_legend_handles_labels()
axes.legend(handles, labels, numpoints=1)
# plt.legend(loc='upper left', fontsize=13)
plt.ylabel(r'Level density $\rho (E)$ [MeV$^{-1}$]')
plt.xlabel('Excitation energy [MeV]')
# plt.text(0, 1e5, '$^{240}\mathrm{Pu}$', fontsize=30)
plt.text(0,1e6, 'PRELIMINARY', alpha=0.1, fontsize=70, rotation=30)
plt.savefig('level_density_pyplot.png')
fig.tight_layout()
plt.show()