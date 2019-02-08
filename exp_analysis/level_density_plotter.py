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
sns.set_context("paper",
                font_scale=1.5,
                rc={'legend.loc' : 'best', 'figure.figsize':(5.5,5.5)})
# sns.set_context("talk")
# sns.set(rc={'figure.figsize':(5.5,5.5)})
sns.set_style("ticks", { 'axes.grid': False})
# plt.rcParams['legend.loc'] = 'best'

#


# Cross section factor for formula strength = xsec*factor/Egamma
xsec_factor = 8.68e-8

def readNLD(folder):
	# import fgteo.rsg to get the calibration
	folded1, cal, E_array, tmp = read_mama_2D(folder+"/fgteo.rsg")

	# Constants for energy binning
	if(cal["a0x"] != cal["a0y"]
		or cal["a1x"] != cal["a1y"]
		or cal["a2x"] != cal["a2y"]):
		raise ValueError("Calibration coefficients for the axes don't match")

	a0 =  cal["a0x"]/1e3 # in MeV
	a1 = cal["a1x"]/1e3 # in MeV



	# Import data
	fermigasfile = open(folder+"/fermigas.cnt")
	fermigaslines = fermigasfile.readlines()
	fermigasfile.close()
	Nfermi = len(fermigaslines)
	energy = np.zeros(Nfermi)
	fermigas = np.zeros(Nfermi)
	for i in range(Nfermi):
		energy[i] = a0 + i*a1
		fermigas[i] = float(fermigaslines[i].split()[0])

	rholevfile = open(folder+"/rholev.cnt")
	rholevlines = rholevfile.readlines()
	rholevfile.close()
	Nrholev = len(rholevlines)
	rholev = np.zeros(Nrholev)
	for i in range(Nrholev):
		rholev[i] = float(rholevlines[i].split()[0])

	rholevfile = open(folder+'/rholev.cnt')
	rholevlines = rholevfile.readlines()
	rholevfile.close()
	Nrholev = len(rholevlines)
	rholev = np.zeros(Nrholev)
	for i in range(Nrholev):
		rholev[i] = float(rholevlines[i].split()[0])

	rhopawfile = open(folder+'/rhopaw.cnt')
	rhopawlines = rhopawfile.readlines()
	rhopawfile.close()
	Nrhopaw = len(rhopawlines)
	rhopaw = np.zeros((Nrhopaw,2))
	for i in range(Nrhopaw):
		if i < int(Nrhopaw/2):
			rhopaw[i,0] = float(rhopawlines[i].split()[0])
		else:
			rhopaw[i-int(Nrhopaw/2),1] = float(rhopawlines[i].split()[0])

	return energy, fermigas, rholev, rhopaw, Nrholev, Nrhopaw


# Plotting, level density
fig, axes = plt.subplots()
plt.yscale('log')

axes.tick_params("x", top="off")
axes.tick_params("y", right="off")
axes.yaxis.set_minor_locator(ticker.NullLocator())
axes.xaxis.set_major_locator(ticker.MaxNLocator(5))
axes.yaxis.set_major_locator(ticker.LogLocator(numticks=5))

folder_rho_mid ="rhotot_T0.415"
energy, fermigas, rholev, rhopaw, Nrholev, Nrhopaw= readNLD(folder_rho_mid)
plt.plot(energy[23:], fermigas[23:], '--', color='grey', label='Constant-temperature model')
# plt.hold('on')
plt.plot(energy[0:Nrholev], rholev, color='black', label='Known levels (binned)')
plt.errorbar(Bn, rho_Bn, yerr=rho_Bnerr, fmt='s', markersize="4", label=r'$\rho$ from $D0$', color='black')

plt.errorbar(energy[0:Nrhopaw], rhopaw[:,0], yerr=rhopaw[:,1], fmt='d', markersize="5",color='red', label='Present work, exp. data points')

folder_rho_mid ="rhotot_T0.405"
energy, fermigas_low, rholev, rhopaw_low, Nrholev, Nrhopaw= readNLD(folder_rho_mid)

folder_rho_mid ="rhotot_T0.425"
energy, fermigas_high, rholev, rhopaw_high, Nrholev, Nrhopaw= readNLD(folder_rho_mid)

idx = np.abs(energy-2.825).argmin()+1
plt.fill_between(energy[0:idx], rhopaw_low[:idx,0], rhopaw_high[:idx,0], label=r"1$\sigma$ on $T_{CT}$", color="royalblue", alpha=0.2)

xmax = 7
idx = (np.abs(energy - xmax)).argmin()
expMax = np.argmax(rhopaw[:,0])
energy = energy[expMax:idx]
fermigas_low = fermigas_low[expMax:idx]
fermigas_high = fermigas_high[expMax:idx]
# print(energy, fermigas_low,  fermigas_high)
plt.fill_between(energy[energy>0], fermigas_low[energy>0], fermigas_high[energy>0], color="blue", alpha=0.1)

plt.xlim([-0.2,xmax])
plt.ylim([1e-0, 1e8])

handles, labels = axes.get_legend_handles_labels()
handles = [handles[-1], handles[2], handles[-2], handles[0], handles[1]]
labels = [labels[-1], labels[2], labels[-2], labels[0], labels[1]]

axes.legend(handles, labels, numpoints=1, framealpha=0.2)
# plt.legend(loc='upper left', fontsize=13)
plt.ylabel(r'Level density $\rho (E)$ [MeV$^{-1}$]')
plt.xlabel('Excitation energy [MeV]')
# plt.text(0, 1e5, '$^{240}\mathrm{Pu}$', fontsize=30)
# plt.text(0,1e6, 'PRELIMINARY', alpha=0.1, fontsize=70, rotation=30)
fig.tight_layout()
plt.savefig('level_density_pyplot.png')
plt.show()
