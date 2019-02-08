from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from utilities import *
import seaborn as sns
import matplotlib.ticker as ticker

Bn=6.534000 # MeV

sns.set()
# sns.set_context("paper")
sns.set_context("paper",
                font_scale=1.4,
                rc={'legend.loc' : 'best', 'figure.figsize':(5.5,5.5)})
#sns.set(rc={'figure.figsize':(5.5,6.5)})
sns.set_style("ticks", { 'axes.grid': False})
# plt.rcParams['legend.loc'] = 'best'

# Cross section factor for formula strength = xsec*factor/Egamma
xsec_factor = 8.68e-8

def readGSF(folder):

	# import fgteo.rsg to get the calibration
	folded1, cal, E_array, tmp = read_mama_2D(folder+"/fgteo.rsg")

	# Constants for energy binning
	if(cal["a0x"] != cal["a0y"]
		or cal["a1x"] != cal["a1y"]
		or cal["a2x"] != cal["a2y"]):
		raise ValueError("Calibration coefficients for the axes don't match")

	a0 =  cal["a0x"]/1e3 # in MeV
	a1 = cal["a1x"]/1e3 # in MeV

	strengthfile = open(folder+'/strength.nrm', 'r')
	strengthlines = strengthfile.readlines()
	strengthfile.close()
	N = len(strengthlines)
	strength = np.zeros((N,3))
	for i in range(N):
		words = strengthlines[i].split()
		if i < int(N/2):
			strength[i,0] = a0 + i*a1 # Energy coordinate
			strength[i,1] = float(words[0]) # Strength coordinate
		else:
			strength[i-int(N/2),2] = float(words[0]) # Strength uncertainty (this way due to horrible file format!)

	transextfile = open(folder+'/transext.nrm')
	transextlines = transextfile.readlines()
	transextfile.close()
	Next = len(transextlines)
	strengthext = np.zeros((Next, 2))
	for i in range(Next):
		transext_current = float(transextlines[i].split()[0])
		energy_current = a0 + i*a1 + 1e-8
		strengthext[i,:] = ( energy_current, transext_current/(2*np.pi*energy_current**3) )

	# comptonfile = open(folder+'/187Re_gamma_n.dat', 'r')
	# comptonlines = comptonfile.readlines()
	# comptonfile.close()
	# Ncompton = len(comptonlines)
	# comptonstrength = np.zeros((Ncompton,3))
	# for i in range(Ncompton):
	# 	words = comptonlines[i].split()
	# 	comptonstrength[i,0] = float(words[3])
	# 	comptonstrength[i,1] = float(words[0]) * xsec_factor / comptonstrength[i,0]
	# 	comptonstrength[i,2] = np.sqrt(float(words[1])**2 + float(words[2])**2) * xsec_factor / comptonstrength[i,0] # Energy, strength, uncertainty (sqrt(stat^2 + sys^2))

	return strength, strengthext

# strength, strengthext = readGSF("rhored0.3_T0.435/rhotot_t0.415")

# # read all strength in (requirment)
# #                      (-> rhored)
# list_of_dirs = []
# for (dirpath, dirnames, filenames) in os.walk("."):
# 	for dirname in dirnames:
# 		if "rhored" in dirpath:
# 			list_of_dirs.append(os.sep.join([dirpath, dirname]))

# strength_arr = np.zeros((len(list_of_dirs),len(strength),3))
# strengthext_arr = np.zeros((len(list_of_dirs),len(strengthext),2))

# for i, folder in enumerate(list_of_dirs):
# 	strength_, strengthext_ = readGSF(folder)
# 	strength_arr[i,:,:] = np.copy(strength_)
# 	strengthext_arr[i,:,:] = np.copy(strengthext_)

# # find min/max, see
# # http://tretherington.blogspot.com/2015/04/some-stuff-import-numpy-as-npa-np.html
# abc = np.dstack(strength_arr)

# # Get the index values for the minimum and maximum values
# maxIndex = np.argmax(abc, axis=2)
# print(maxIndex)
# minIndex = np.argmin(abc, axis=2)

# # Create column and row position arrays
# nRow, nCol = np.shape(strength)
# col, row = np.meshgrid(range(nCol), range(nRow))

# # Index out the maximum and minimum values from the stacked array based on row
# # and column position and the maximum value
# maxValue = abc[row, col, maxIndex]
# minValue = abc[row, col, minIndex]

# print(maxValue)


# load other data
# format: header line with "Eg(MeV)  f(MeV^-3)   f_Err(MeV^-3)"
exp1 = np.loadtxt('other_data/gSF_239Pu_gurevich_1976_g_abs.txt', skiprows=0)
exp2 = np.loadtxt('other_data/gSF_239Pu_moraes_1993_g_abs.txt', skiprows=0)

# Data from Stephan, resolving E1 and M1 part
data_stephan = np.genfromtxt("other_data/240Pu_ARC_data.csv",skip_header=0,delimiter=',')
data_stephan_E1 = []
data_stephan_M1 = []

# attribute relative error where error unknown
relativeErrorWhereUnknown = 0 #0.3
for i, (E, E1, M1, dE1, dM1) in enumerate(data_stephan):
    if(np.isfinite(E1)):
        if(np.isfinite(dE1)==False): dE1 = E1 * relativeErrorWhereUnknown
        data_stephan_E1.append( [E, E1, dE1] )
    if(np.isfinite(M1)):
        if(np.isfinite(dM1)==False): dM1 = M1 * relativeErrorWhereUnknown
        data_stephan_M1.append( [E, M1, dM1] )
data_stephan_E1 = np.array(data_stephan_E1)
data_stephan_M1 = np.array(data_stephan_M1)

# Plotting:
# fig, axes = plt.subplots(figsize=(10,9))
fig, axes = plt.subplots()

axes.tick_params("x", top="off")
axes.tick_params("y", right="off")
axes.yaxis.set_minor_locator(ticker.NullLocator())

# iBn = (np.abs(strengthext[:,0] - Bn)).argmin()
# plt.plot(strengthext[0:iBn,0], strengthext[:iBn,1], ":", color='red', label='Present work, extrapolated, r=0.3')
# plt.errorbar(strength[:,0], strength[:,1], yerr=strength[:,2], label="Present work, exp. data points, r=0.3", fmt='d', color='red')
# plt.errorbar(comptonstrength[:,0], comptonstrength[:,1], yerr=comptonstrength[:,2], label='Shizuma et.al. (2005)', fmt='.-', color='crimson')

# plt.fill_between(strength[:,0], minValue[:,1],maxValue[:,1], label="min/max")

# for i in range(len(strength_arr)):
# 	strength = strength_arr[i]
# 	strengthext = strengthext_arr[i]
# 	# label="Present work, exp. data points"
# 	id_plot = strength[:,1]>0
# 	if i == 0:
# 		label="1 sig on T_tot & T_red"
# 	else:
# 		label=""
# 	plt.errorbar(strength[id_plot,0], strength[id_plot,1], yerr=strength[id_plot,2], fmt='.-', color='red', alpha=0.15, label=label)
# 	plt.plot(strengthext[0:iBn,0], strengthext[:iBn,1], ":", color='red', alpha=0.3)

strength, strengthext = readGSF("rhotot_T0.415")
iBn = (np.abs(strengthext[:,0] - Bn)).argmin()
plt.errorbar(strength[:,0], strength[:,1], yerr=strength[:,2], label="Present work & extrapolation,\nintial analysis", fmt='d', color='red', zorder=0)
plt.plot(strengthext[0:iBn,0], strengthext[:iBn,1], ":", color='red'
         #, label='Present work, extrapolation'
         )

strength_export = strength[strength[:,1]>0]
np.savetxt("strength_export.txt",strength_export, header="E y yerr")

plt.errorbar(exp1[:,0],exp1[:,1],exp1[:,2],fmt="o",label="239Pu(g,abs), Gurevich et al.(1976)")
plt.errorbar(exp2[:,0],exp2[:,1],exp2[:,2],fmt="s",label="239Pu(g,abs), Moraes et al.(1993)")

plt.errorbar(data_stephan_E1[:,0],data_stephan_E1[:,1],data_stephan_E1[:,2],fmt=">",color="grey",label="240Pu, E1, Kopecky et al.(2017)")
plt.errorbar(data_stephan_M1[:,0],data_stephan_M1[:,1],data_stephan_M1[:,2],fmt="<",color="grey",label="240Pu, M1, Kopecky et al.(2017)")

plt.xlim([0,15])
plt.ylim([1e-8,5e-6])
plt.yscale('log')
plt.xlabel(r'$\gamma$-ray energy $E_\gamma$ [MeV]')
plt.ylabel(r'$\gamma$-ray strength [MeV$^{-3}$]')
# plt.text(0, 1e-7, '$^{187}\mathrm{Re}$', fontsize=30)
# plt.text(-1.5,1e-6, 'PRELIMINARY', alpha=0.1, fontsize=70, rotation=30)

handles, labels = axes.get_legend_handles_labels()
handles
axes.legend(handles, labels, numpoints=1, fancybox=True, framealpha=0.5)

fig.tight_layout()


plt.savefig('strength_pyplot.png')

# plt.show()



