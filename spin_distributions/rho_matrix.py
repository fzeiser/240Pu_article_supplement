from numpy import pi, sin
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.ticker as ticker
import os
import seaborn as sns
from matplotlib.colors import LogNorm

# sns.set()
plt.rcParams["axes.labelsize"] = 15

#plt.rcParams["savefig.directory"] = os.chdir(os.path.dirname(__file__))

# reaction = "238U(d,p)"
# reaction = "232Th(d,p)"
reaction = "239Pu(d,p)"

# fig, ax = plt.subplots()

# setting the parameters
if reaction == "238U(d,p)":
	#238U(d,p)239U
	A  = 239
	a  = 26.67
	E1 = -0.31
	Sn = 4.806
	Q  = 2.581
	E_beam = 15.
	I0 = 0

elif reaction == "232Th(d,p)":
	#232Th(d,p)233Th
	A  = 233
	a  = 25.98
	E1 = -0.58
	Sn = 4.786
	Q  = 2.561
	E_beam = 12.
	I0 = 0

elif reaction == "239Pu(d,p)":
	#232Th(d,p)233Th
	A  = 240
	a  = 25.16
	E1 = 0.12
	Sn = 6.534
	Q  = 4.309
	E_beam = 12.
	I0 = 1/2.

else:
	print "WARNING"
	exit()

if reaction == "238U(d,p)":
	filename = "u238-pop-j.dat"

elif reaction == "232Th(d,p)":
	filename = "th232-pop-j.dat"

elif reaction == "239Pu(d,p)":
	# filename = "pu239-pop-j.dat"
	filename = "pu239-pop-j_125deg.dat"
###################################################


########################
## Gregory:
Ex =[]
spinpar = []
Nspins=12+1 # Number of spins in the file provided

# with open('Pu_SpinParity_12MeVnew.txt') as f:
with open('Pu_SpinParity12MeV_RIPL.txt') as f:
    lines=f.readlines()
    for line in lines:
    	if line.startswith("#"):
    		continue
    	if line[:7]=="NEnergy":
    		Ex_ = line.split(' ')
    		Ex_=Ex_[1]
    		Ex.append(Ex_)
    		continue
        myarray = np.fromstring(line, dtype=float, sep=' ')
		# myarray[1] = myarray[1] + myarray[2] # add both parities
        spinpar.append(myarray)

Ex=np.asarray(Ex,dtype=float)
# print spinpar
spinpar=np.asarray(spinpar).reshape((-1,Nspins,3))
Ex=np.flipud(Ex) # Get ascending order of Ex
spinpar=np.flipud(spinpar) # Get ascending order of Ex

xs = np.loadtxt("Pu240_dsdE.txt")[:,2]
xs = np.flipud(xs) # Get ascending order of Ex
for i in range(len(spinpar)):
	spinpar[i,:,:] *= xs[i]

# format: spinpar[Ex,J,col], where col= J, pi+, pi-
spinparPos = np.copy(spinpar[:,:,1]) # First column was positive parity in Gregs file
spinparNeg = np.copy(spinpar[:,:,2])

spinpar[:,:,1]= spinpar[:,:,1] + spinpar[:,:,2] # add both parities
spinpar = np.delete(spinpar, 2, 2)

spinpar_hist = spinpar[:,:,1]
# print spinpar_hist[0,:]

for i in range(len(spinparPos)):
	print Ex[i],  np.sum(spinpar_hist[i,:])

xmin = 0
xmax = Nspins
ymin = Ex[0]
ymax = Ex[-1]

interactive(True)

fig = plt.figure(1)
ax = fig.add_subplot(111)
plt.imshow(np.flipud(spinpar_hist),interpolation="none",extent=[xmin, xmax, ymin, ymax] )
plt.colorbar()
ax.set_xlabel("Spin")
ax.set_ylabel("Ex")
plt.show()


'''
Gregory = np.array( [
	[0,0.0294837,0.0124131],
	[1,0.214675,0.0454649],
	[2,0.251857,0.0354277],
	[3,0.124301,0.0339191],
	[4,0.112906,0.00921398],
	[5,0.0727051,0.00664406],
	[6,0.0462221,0.0020912],
	[7,0.000943674,0.0011803],
	[8,0.000552348,0]
	])

print np.sum(Gregory[:,1]) + np.sum(Gregory[:,2])

spins = Gregory[:,0]
data_to_plot = Gregory[:,1] + Gregory[:,2]

scale = 1.
label = "Gregory, " + reaction + " x " + str(scale)

plt.plot(spins, scale*data_to_plot, "oy", label=label)

scale = 0.10
label = "Gregory, " + reaction + " x " + str(scale)

plt.plot(spins, scale*data_to_plot, "y--", label=label)

ax.set_xlabel('J')
# ax.set_ylabel('ylabel')

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, numpoints=1)

# plt.show()
'''


########################
## EB05

#cut-off parameters of EB06
rmi_red = 0.8
def sigma(U,A=A,a=a,E1=E1):
	sigma2 = np.sqrt(rmi_red) * 0.0146*A**(5./3.) * ( 1. + np.sqrt(1. + 4.*a*(U-E1)) ) / (2.*a)
	return np.sqrt(sigma2)

# Spin distribution of Gilbert and Cameron
def g(J,E=Sn):
	g = (2.*J+1.)/(2.*sigma(U=E)**2.) * np.exp( -(J+1./2.)**2. /(2.*(sigma(U=E))**2.) )
	return g

def g_arr(J,E=Sn):
    return np.array([g(j,E=E) for j in J])

EB06_mat = []
for E in Ex:
	EB06_mat.append(np.array([g(i,E=E) for i in range(Nspins)]))

EB06_mat = np.array(EB06_mat)
EB06_mat=np.flipud(EB06_mat) # Get ascending order of Ex

fig = plt.figure(2)
ax = fig.add_subplot(111)
plt.imshow(EB06_mat,interpolation="none",extent=[xmin, xmax, ymin, ymax])
ax.set_xlabel("Spin")
ax.set_ylabel("Ex")
plt.colorbar()
plt.show()

######################################
# both parities
import matplotlib.gridspec as gridspec
fig = plt.figure(11)
# Now, create the gridspec structure, as required
gs = gridspec.GridSpec(2,2, height_ratios=[2,8], width_ratios=[40,1])
ax = plt.subplot(gs[2]) # place it where it should be.
ax_cbar = plt.subplot(gs[3]) # place it where it should be.
ax_top = plt.subplot(gs[0]) # place it where it should be.

# Also make sure the margins and spacing are apropriate
gs.update(left=0.13, right=0.9, bottom=0.13, top=0.99, wspace=0.02, hspace=0.03)
# fig = plt.figure(11)
# ax = fig.add_subplot(111)
# scale = 2
# sns.set_context("paper", rc={"font.size":8*scale,"axes.titlesize":8*scale,"axes.labelsize":5*scale})

i_y_max_here = 20
ymax_here = Ex[-i_y_max_here]
xmax_here = 10
if xmax_here> Nspins: sys.exit()
neg = spinparNeg[:-i_y_max_here,:xmax_here][:,::-1]
pos = spinparPos[:-i_y_max_here,:xmax_here]
Ex_here = Ex[:-i_y_max_here]
hist = np.c_[neg,pos]
hist /= np.sum(hist,axis=1)[:,None]
print "\n Spin-Par hist\n", hist[:,:2*xmax_here]

import matplotlib.ticker as ticker
ax.xaxis.set_major_locator(ticker.MaxNLocator(4))
plt1= ax.imshow(np.flipud(hist),interpolation="none",extent=[-xmax_here, xmax_here, ymin, ymax_here], aspect="auto", cmap="BuPu")
my_xticks=["$" + str(xmax_here-1)+"^-$",
           "$" + str(xmax_here/2)+"^-$",
           "$" + str(1)+"^-$",
           "$" + str(1)+"^+$",
           "$" + str(xmax_here/2)+"^+$",
           "$" + str(xmax_here-1)+"^+$"]
ax.set_xticklabels(my_xticks)
ticks = [-9.5,-5.5,-1.5,1.5,5.5,9.5]
ax.set_xticks(ticks, minor=False)

from matplotlib.colorbar import Colorbar
cb = Colorbar(ax = ax_cbar, mappable = plt1, orientation = 'vertical')

idx = (np.abs(Ex - Sn)).argmin()-1
px = hist[idx]
x_array = np.linspace(0, 2.*xmax_here-1, 2.*xmax_here)
ax_top.plot(x_array,px,"bs")
ax_top.set_xlim(x_array[0]-0.5,x_array[-1]+0.5)

spins_array = np.linspace(-xmax_here+1,0,xmax_here)
spins_array_ = np.linspace(0,xmax_here-1,xmax_here)
spins_array = np.append(spins_array, spins_array_)

print "x_array:", x_array
print "spins_array:", spins_array
ax_top.plot(x_array,g_arr(np.abs(spins_array)/2., E=Sn),"g>")


ax_top.set_ylabel(r"$P(\,J^\pi)$")
ax_top.tick_params(labelsize=10)
ax_top.tick_params(axis="x", which='both', top=False, bottom=False,
                   labelbottom=False)
ax_top.text(14., 0.18,
            r"$E_x = {:.1f}$ MeV".format(Ex_here[idx]),
            fontsize=13)
ax_top.text(0.05, 0.7,
            r"(a)",
            fontsize=13, transform = ax_top.transAxes)

ax.set_xlabel(r"Spin-Parity $J^\pi$")
ax.set_ylabel(r"$E_x$")
ax.tick_params(labelsize=12)
ax_cbar.tick_params(labelsize=12)
ax.text(0.05, 0.9,
            r"(b)",
            fontsize=13, transform = ax.transAxes)

plt.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig("spins_norm_density.pdf")
plt.show()
#######################################




################
## "Projections" in 1D; Compare the data
fig = plt.figure(3)
ax3 = fig.add_subplot(111)
axis_color = 'lightgoldenrodyellow'

# Adjust the subplots region to leave some space for the sliders and buttons
fig.subplots_adjust(left=0.25, bottom=0.25)

spins = range(Nspins)
Ex_0 = Ex[0]
red_0 = 1.

# Draw the initial plot
# The 'line' variable is used for modifying the line later
ax3.plot(spins, g_arr(spins, E=Ex_0), "--", linewidth=1, color='red', label="EB06, def. Ex")
[lineEB06Int] = ax3.plot(spins, g_arr(spins, E=Ex_0), linewidth=1, color='red', label="EB05")
[lineGregInt] = ax3.plot(spins, red_0*spinpar_hist[0], linewidth=1, color='blue', label="Greg")
ax3.set_xlim([0, Nspins])
ax3.set_ylim([0, 0.4])
xlabel = "Ex chosen: " + "{:.2f}".format(Ex_0)
ax3.set_xlabel(xlabel)

# Define an axes area and draw a slider in it
# Ex_slider_ax  = fig.add_axes([0.25, 0.15, 0.65, 0.03], axisbg=axis_color) # axisbg depricated in matplotlib 2.0+
Ex_slider_ax  = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=axis_color)
Ex_slider = Slider(Ex_slider_ax, 'Ex', 1., 10.0, valinit=Ex_0)

# Draw another slider
red_slider_ax = fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=axis_color)
red_slider = Slider(red_slider_ax, 'Red. factor', 0.02, 1., valinit=red_0)

# Radiobutton
Ex_is_free = False
color_radios_ax = fig.add_axes([0.025, 0.5, 0.15, 0.15], facecolor=axis_color)
color_radios = RadioButtons(color_radios_ax, ('Ex_min=Greg', 'Ex free'), active=0)
def color_radios_on_clicked(label):
    global Ex_is_free
    if label=="Ex_min=Greg":
    	Ex_is_free = False
    if label=="Ex free":
    	Ex_is_free = True
    fig.canvas.draw_idle()
color_radios.on_clicked(color_radios_on_clicked)

def sliders_on_changed(val):
    idx = (np.abs(Ex - Ex_slider.val)).argmin()
    if Ex_is_free:
    	lineEB06Int.set_ydata(g_arr(spins,E=Ex_slider.val))
    else:
    	lineEB06Int.set_ydata(g_arr(spins,E=Ex[idx]))
    # lineEB06.set_ydata(g_arr(spins,E=Ex[idx]))
    lineGregInt.set_ydata(red_slider.val*spinpar_hist[idx])
    xlabel = "Ex chosen: " + "{:.2f}".format(Ex[idx]) + "; Red: " + "{:.2f}".format(red_slider.val)
    ax3.set_xlabel(xlabel)
    fig.canvas.draw_idle()

Ex_slider.on_changed(sliders_on_changed)
red_slider.on_changed(sliders_on_changed)


handles, labels = ax.get_legend_handles_labels()
ax3.legend(handles, labels, numpoints=1)


############################
#### plot for paper
sns.set_context("paper")
sns.set(font_scale=1.2) # Bigger than normal fonts
sns.set_style("ticks")

fig = plt.figure(4)
ax = fig.add_subplot(111)

# red_art = 1

Ex_art =  Sn
idx = (np.abs(Ex - Ex_art)).argmin()
Ex_art = Ex[idx]
labelGreg = r'$g_\mathrm{pop}(J)$' + ' at $S_n$'
labelGregNeg = r'$g_\mathrm{pop}(J,\pi^-)$' + ' at $S_n$'
labelGregPos = r'$g_\mathrm{pop}(J,\pi^+)$' + ' at $S_n$'
# [lineGreg] = ax.plot(spins, red_art*spinpar_hist[idx], "^-",linewidth=1, color='blue', label=labelGreg)
normalization = np.sum(spinparPos[idx] + spinparNeg[idx])
[lineGreg] = ax.plot(spins, spinparNeg[idx]/normalization, "v--",linewidth=1, color='blue', label=labelGregNeg)
[lineGreg] = ax.plot(spins, spinparPos[idx]/normalization, "<-",linewidth=1, color='blue', label=labelGregPos)

print np.sum(spinparNeg[idx]), np.sum(spinparPos[idx])


Ex_art =  Sn # MeV
idx = (np.abs(Ex - Ex_art)).argmin()
Ex_art = Ex[idx]
labelEB06 = r"$g_\mathrm{int}$ (EB05) at $S_n$"
[lineEB06] = ax.plot(spins, g_arr(spins, E=Ex_art), "s-",linewidth=1, color='red', label = labelEB06)

Ex_art =  2. # MeV
idx = (np.abs(Ex - Ex_art)).argmin()
Ex_art = Ex[idx]
labelEB06 = r"$g_\mathrm{int}$ (EB05) at " + "{:.1f} MeV".format(Ex_art)
[lineEB06] = ax.plot(spins, g_arr(spins, E=Ex_art), "o:",linewidth=1, color='red', label = labelEB06)

# ax.set_xlabel("Spin",horizontalalignment="right", x=1, labelpad=05)
# ax.set_ylabel("g", y=1, labelpad=05)
ax.set_xlabel("Spin",horizontalalignment="right", x=1, labelpad=05)
ax.set_ylabel("g", y=0.5, labelpad=10)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, numpoints=1, loc=1)

ax.tick_params("x", top="off")
ax.tick_params("y", right="off")

plt.xlim(xmin=0,xmax=12)

# ax.xaxis.set_major_locator(ticker.AutoLocator())
plt.tight_layout()
plt.savefig("popToTot.pdf")

interactive(False)

plt.show()

############################
#### plot for paper
sns.set_context("paper")
sns.set(font_scale=1.2) # Bigger than normal fonts
sns.set_style("ticks")



fig = plt.figure(5)
ax = fig.add_subplot(111)


red_art = 0.08
Ex_art =  Sn
idx = (np.abs(Ex - Ex_art)).argmin()
Ex_art = Ex[idx]

Ex_art1 =  2.
idx1 = (np.abs(Ex - Ex_art1)).argmin()
Ex_art1 = Ex[idx1]

labelGreg = "{:.2f}".format(red_art) + " x populated levels"
labelEB06 = "all levels, EB05, rmi_red=" + "{:.2f}".format(rmi_red)
[lineEB06] = ax.plot(spins, g_arr(spins, E=Ex_art1), "o-",linewidth=1, color='red', label = labelEB06)
[lineGreg] = ax.plot(spins, red_art*spinpar_hist[idx], "^-",linewidth=1, color='blue', label=labelGreg)


# ax.set_xlabel("Spin",horizontalalignment="right", x=1, labelpad=05)
# ax.set_ylabel("g", y=1, labelpad=05)
ax.set_xlabel("Spin",horizontalalignment="right", x=1, labelpad=05)
ax.set_ylabel("g", y=0.5, labelpad=10)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, numpoints=1, loc=2)

ax.tick_params("x", top="off")
ax.tick_params("y", right="off")

# ax.xaxis.set_major_locator(ticker.AutoLocator())

# plt.savefig("popToTot.pdf")

interactive(False)

plt.show()

#####################################
# calculate the new type of reduction

def calcRed(rho_pop, rho_fin):
	# assume only dipole transitions, and equal probability for +- 1
	levels_sum = 0
	for i in range(len(rho_pop)):
		levels_sum_i = 0
		if i == 0:
			levels_sum_i += rho_fin[i+1]
		if i == len(rho_pop)-1:
			levels_sum_i += rho_fin[i-1] + rho_fin[i]
		else:
			levels_sum_i += rho_fin[i-1] + rho_fin[i] + rho_fin[+-1]
		levels_sum_i *= rho_pop[i]
		levels_sum += levels_sum_i
	return levels_sum


def calcRed2(rho_pop, rho_fin):
	# assume only dipole transitions, and equal probability for +- 1
	popfinal_ji = np.zeros((len(rho_fin),len(rho_fin)))
	popfinal_j = np.zeros(len(rho_fin))
	norms    = np.zeros(len(rho_fin))


	for i in range(len(rho_fin)):
	# hotfix: above take range of final states instead of populated states,
	# so that I don't get a error in the array lateron...
	# (shouldn't effect the results though...)
		if i == 0:
			norms[i] += rho_fin[i+1]
		if i == len(rho_fin)-1:
			norms[i] += rho_fin[i-1] + rho_fin[i]
		else:
			norms[i] += rho_fin[i-1] + rho_fin[i] + rho_fin[+-1]

		if norms[i]!= 0:
			norms[i] = 1./norms[i]
		else:
			norms[i] = 0
	# print norms

	for j in range(len(rho_fin)):
		for i in range(len(rho_pop)):
			popfinal_ji[j][i] = rho_pop[i] * rho_fin[j] * norms[i]
	# 		if i == 0:
	# 			popfinal_ji[j][i] += rho_pop[i+1] * rho_fin[j] * norms[i+1]
	# 		if i == len(rho_pop)-1:
	# 			popfinal_ji[j][i] += rho_pop[i-1] * rho_fin[j] * norms[i-1] + rho_pop[i] * rho_fin[j] * norms[i]
	# 		else:
	# 			popfinal_ji[j][i] += rho_pop[i-1] * rho_fin[i-1] * norms[i-1] + rho_pop[i] * rho_fin[i] * norms[i] + rho_pop[i+1] * rho_fin[i+1] * norms[i+1]
	# 		# if norms[i]!= 0:
	# 		# 	popfinal_ji[j][i] *= rho_pop[i]/norms[i]
	# 		# else:
	# 		# 	popfinal_ji[j][i] = 0
	# # print popfinal_ji

	# popfinal_j = popfinal_ji.sum(axis=1)
	for j in range(len(rho_fin)):
		if j == 0:
			popfinal_j[j] = popfinal_ji[j][j+1]
		if j == len(rho_fin)-1:
			popfinal_j[j] = popfinal_ji[j][j-1] + popfinal_ji[j][j]
		else:
			popfinal_j[j] = popfinal_ji[j][j-1] + popfinal_ji[j][j] + popfinal_ji[j][j+1]
	return popfinal_j



Nspins = 30
spins = range(Nspins)

Ex_ini =  Sn
idx_ini = (np.abs(Ex - Ex_ini)).argmin()
Ex_ini = Ex[idx]

Eg = 2.
Ex_fin =  Sn - Eg
idx_fin = (np.abs(Ex - Ex_fin)).argmin()
Ex_fin = Ex[idx]


# First
rho_pop = g_arr(spins, E=Ex_ini) # populated states: here, all
# rho_pop = np.ones(len(spins))/(len(spins)) # populated states: here, all
rho_fin = g_arr(spins, E=Ex_fin) # TODO: make sure, that this is really at the energy of final state
levels_sum1 = calcRed(rho_pop, rho_fin)
popfinal_j1 = calcRed2(rho_pop, rho_fin)

# Second
rho_pop = np.copy(spinpar_hist[idx_ini]) # populated states: here, calc Greg
rho_pop[:] = 0. # TODO : Comment out again
rho_pop[3:5] = 1. # TODO : Comment out again
rho_pop /= rho_pop.sum()
levels_sum2 = calcRed(rho_pop, rho_fin)
popfinal_j2 = calcRed2(rho_pop, rho_fin)

print """reachable levels, upon a constant, if \n populated levels from EB05: """, levels_sum1,
print "\n or Greg: ", levels_sum2
print "ratio:", levels_sum2/levels_sum1


print popfinal_j1, popfinal_j2
print "check normalization: ", popfinal_j1.sum(), popfinal_j2.sum()
print "something else: ", popfinal_j2.sum()/popfinal_j1.sum()
print "and p[3]/p[2]: ", popfinal_j2[3]/popfinal_j2[2]

fig = plt.figure(6)
ax = fig.add_subplot(111)

js = range(len(popfinal_j1))
[lineEB06] = ax.plot(js, popfinal_j1, "o-",linewidth=1, color='red',  label = labelEB06)
[lineGreg] = ax.plot(js, popfinal_j2, "^-",linewidth=1, color='blue', label=labelGreg)
[lineGregpop] = ax.plot(range(len(spinpar_hist[idx_ini])), spinpar_hist[idx_ini], "--",linewidth=1, color='blue', label="Greg, init pop")


#z plt.show()

## Some test -- write files to use with RAINIER
# print population distribution for RAINIER
# bin    Ex    Popul.    J= 0.0    J= 1.0  [...] J=9.0
nJs = 10
Jstart = 0
Js = np.array(range(nJs)) + Jstart
nRowsOffset = 18 # cut away the first x Rows
nRows = len(spinpar_hist)
nCollumsExtra = 3 # 3 rows with "bin  Ex  Popul." added extra"
nCollums = nJs + nCollumsExtra
nStartbin = 54-nRowsOffset # ust for easy copying to RAINIER file

# arr_JsStructure =  [(("J= " + "{0:.1f}".format(J)),"f4") for J in Js]
# arr_structure = [('bin', 'i4'),('Ex', 'f4'), ('Popul.', 'f4')]
# arr_structure += arr_JsStructure
# spins_RAINIER = np.zeros((nRows,nCollums),dtype=arr_structure)

spins_RAINIER = np.zeros((nRows,nCollums))
# copying spinpar histogram into the historgram that shall be printed
nRowsArrOrg = len(spinpar_hist[0]) # number of arrays in the histogram that shall be copied over
spins_RAINIER[:,0] =  np.array(range(nRows)) + nStartbin # copy bins
spins_RAINIER[:,1] = Ex # copy excitation energyies
spins_RAINIER[:,2] = 10. # set population to 1 (assumeing all excitations energies equally populated(?))
spins_RAINIER[:,nCollumsExtra:] = spinpar_hist[:,:nJs-len(spinpar_hist[0])]  # copy spins
spins_RAINIER[:,nCollumsExtra:] = (spins_RAINIER[:,nCollumsExtra:].transpose()*spins_RAINIER[:,2]/np.sum(spins_RAINIER[:,nCollumsExtra:],axis=1)).transpose() # normalize (per bin) to given population
spins_array_print = spins_RAINIER[nRowsOffset:,:]

class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

# # print "\n"
# for i in range(len(spins_RAINIER)):
# 	print  "{0:.0f}\t{1:.2f}\t{2:.2f}\t{l[0]:.4f}".format(spins_RAINIER[i,0],spins_RAINIER[i,1], spins_RAINIER[i,2], l=spins_RAINIER[i,3:])
# # 	# for pop in spins_RAINIER[i,3:]:
# # 	# 	print "\t{0:.0f}".format(pop)
# # 	x = map(prettyfloat, spins_RAINIER[i,3:])
# # 	print x
# # # for i in range(len(spins_RAINIER)):
# # # 	print  "{0:.2f}".format(spins_RAINIER[i,1])
# print spins_RAINIER[0,:]
def pwrite(fout, array):
	for row in array:
		head = str(int(row[0]))
		tail = " ".join(map(str, row[1:].tolist()))
		sout = head + " " +  tail + "\n"
		# print sout
		fout.write(sout)

arr_Js_print =  [("J= " + "{0:.1f}".format(J)) for J in Js]
arr_header = [("bin"),("Ex"),("Popul.")]
arr_header += arr_Js_print

# Write spin distribution from Greg
fout = open("Js2RAINER_Greg.txt","w")
fout.write(" ".join(map(str, arr_header)))
fout.write("\n")
pwrite(fout, spins_array_print)
fout.close()

#####################################
'''
nJs = 23
Jstart = 0
Js = np.array(range(nJs)) + Jstart
nRowsOffset = 18 # cut away the first x Rows
nRows = len(spinpar_hist)
nCollumsExtra = 3 # 3 rows with "bin  Ex  Popul." added extra"
nCollums = nJs + nCollumsExtra
nStartbin = 54-nRowsOffset # ust for easy copying to RAINIER file

spins_RAINIER = np.zeros((nRows,nCollums))
spins_RAINIER[:,0] =  np.array(range(nRows)) + nStartbin # copy bins
spins_RAINIER[:,1] = Ex # copy excitation energyies
spins_RAINIER[:,2] = 0.25 # set population to 1 (assumeing all excitations energies equally populated(?))

# Write spin distribution from EB06
EB06_mat = []
for E in Ex:
	EB06_mat.append(np.array([g(i,E=E) for i in Js]))
EB06_mat = np.array(EB06_mat)
spins_RAINIER[:,nCollumsExtra:] = EB06_mat  # copy spins
spins_RAINIER[:,nCollumsExtra:] = (spins_RAINIER[:,nCollumsExtra:].transpose()*spins_RAINIER[:,2]/np.sum(spins_RAINIER[:,nCollumsExtra:],axis=1)).transpose() # normalize (per bin) to given population
spins_array_print = spins_RAINIER[nRowsOffset:,:]

fout = open("Js2RAINER_EB06.txt","w")
fout.write(" ".join(map(str, arr_header)))
fout.write("\n")
pwrite(fout, spins_array_print)
fout.close()

'''

nJs = 23
Jstart = 0
Js = np.array(range(nJs)) + Jstart
nRowsOffset = 18 # cut away the first x Rows
Ex = np.linspace(-0.5,6.75,num=82)
print Ex
nRows = len(Ex)
nCollumsExtra = 3 # 3 rows with "bin  Ex  Popul." added extra"
nCollums = nJs + nCollumsExtra
nStartbin = 20-nRowsOffset # ust for easy copying to RAINIER file

spins_RAINIER = np.zeros((nRows,nCollums))
spins_RAINIER[:,0] =  np.array(range(nRows)) + nStartbin # copy bins
spins_RAINIER[:,1] = Ex # copy excitation energyies
spins_RAINIER[:,2] = 0.25 # set population to 1 (assumeing all excitations energies equally populated(?))


# Write spin distribution from EB06
EB06_mat = []
for E in Ex:
	EB06_mat.append(np.array([g(i,E=E) for i in Js]))
EB06_mat = np.array(EB06_mat)
spins_RAINIER[:,nCollumsExtra:] = EB06_mat  # copy spins
spins_RAINIER[:,nCollumsExtra:] = (spins_RAINIER[:,nCollumsExtra:].transpose()*spins_RAINIER[:,2]/np.sum(spins_RAINIER[:,nCollumsExtra:],axis=1)).transpose() # normalize (per bin) to given population
spins_array_print = spins_RAINIER[nRowsOffset:,:]

fout = open("Js2RAINER_EB06.txt","w")
fout.write(" ".join(map(str, arr_header)))
fout.write("\n")
pwrite(fout, spins_array_print)
fout.close()

