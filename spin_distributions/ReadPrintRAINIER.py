from numpy import pi, sin
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.ticker as ticker
import os
import seaborn as sns

########################
## Gregory:

def ReadSpinPar(filename, nSpins, flip_array):
    Ex =[]
    spinpar = []

    with open(filename) as f:
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
    spinpar=np.asarray(spinpar).reshape((-1,nSpins,3))

    if(flip_array):
        Ex=np.flipud(Ex) # Get ascending order of Ex
        spinpar=np.flipud(spinpar) # Get ascending order of Ex

    return Ex, spinpar

Nspins=12+1 # Number of spins in the file provided
Ex, spinpar= ReadSpinPar("Pu_SpinParity12MeV_RIPL.txt", Nspins, flip_array=True)
# format: spinpar[Ex,J,col], where col= J, pi+, pi- 

xs = np.loadtxt("Pu240_dsdE.txt")[:,2]
xs = np.flipud(xs) # Get ascending order of Ex
for i in range(len(spinpar)):
    spinpar[i,:,:] *= xs[i]

spinparPos = np.copy(spinpar[:,:,1]) # First column was positive parity in Gregs file
spinparNeg = np.copy(spinpar[:,:,2])
# print spinpar
# 
spinpar[:,:,1]= spinpar[:,:,1] + spinpar[:,:,2] # add both parities
spinpar = np.delete(spinpar, 2, 2)

#################################
## Plot per Parity
xmin = 0
xmax = Nspins
ymin = Ex[0]
ymax = Ex[-1]

# interactive(True)
spinpar_hist = spinparPos

fig = plt.figure(1)
ax = fig.add_subplot(111)
plt.imshow(np.flipud(spinpar_hist),interpolation="none",extent=[xmin, xmax, ymin, ymax] )
plt.colorbar()
ax.set_xlabel("Spin")
ax.set_ylabel("Ex")
# plt.show()

#######
spinpar_hist = spinparNeg

fig = plt.figure(2)
ax = fig.add_subplot(111)
plt.imshow(np.flipud(spinpar_hist),interpolation="none",extent=[xmin, xmax, ymin, ymax] )
plt.colorbar()
ax.set_xlabel("Spin")
ax.set_ylabel("Ex")
# plt.show()

#####
spinpar_hist = spinpar[:,:,1]

fig = plt.figure(3)
ax = fig.add_subplot(111)
plt.imshow(np.flipud(spinpar_hist),interpolation="none",extent=[xmin, xmax, ymin, ymax] )
plt.colorbar()
ax.set_xlabel("Spin")
ax.set_ylabel("Ex")
# plt.show()
#################################

def pwrite(fout, array):
    for row in array:
        head = str(int(row[0]))
        tail = " ".join(map(str, row[1:].tolist()))
        sout = head + " " +  tail + "\n"
        # print sout
        fout.write(sout)

def WriteRAINIERTotPar():
    ##############################################
    # Some test -- write files to use with RAINIER
    # print population distribution for RAINIER
    # bin    Ex    Popul.    J= 0.0    J= 1.0  [...] J=9.0
    nJs = 10
    Jstart = 0
    Js = np.array(range(nJs)) + Jstart
    nRowsOffset = 0 # cut away the first x Rows
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
    spins_RAINIER[:,2] = xs # set population to the cross-sections cal. by Greg
    spins_RAINIER[:,nCollumsExtra:] = spinpar_hist[:,:nJs-len(spinpar_hist[0])]  # copy spins
        # spins_RAINIER[:,2] = 10. # set population to 1 (assumeing all excitations energies equally populated(?))
    # spins_RAINIER[:,nCollumsExtra:] = (spins_RAINIER[:,nCollumsExtra:].transpose()*spins_RAINIER[:,2]/np.sum(spins_RAINIER[:,nCollumsExtra:],axis=1)).transpose() # normalize (per bin) to given population
    spins_array_print = spins_RAINIER[nRowsOffset:,:]

    class prettyfloat(float):
        def __repr__(self):
            return "%0.2f" % self

    # # print "\n"
    # for i in range(len(spins_RAINIER)):
    #   print  "{0:.0f}\t{1:.2f}\t{2:.2f}\t{l[0]:.4f}".format(spins_RAINIER[i,0],spins_RAINIER[i,1], spins_RAINIER[i,2], l=spins_RAINIER[i,3:])
    # #     # for pop in spins_RAINIER[i,3:]:
    # #     #   print "\t{0:.0f}".format(pop)
    # #     x = map(prettyfloat, spins_RAINIER[i,3:])
    # #     print x
    # # # for i in range(len(spins_RAINIER)):
    # # #   print  "{0:.2f}".format(spins_RAINIER[i,1]) 
    # print spins_RAINIER[0,:]

    arr_Js_print =  [("J= " + "{0:.1f}".format(J)) for J in Js]
    arr_header = [("bin"),("Ex"),("Popul.")]  
    arr_header += arr_Js_print

    # Write spin distribution from Greg
    fout = open("Js2RAINER_Greg.txt","w")
    fout.write(" ".join(map(str, arr_header)))
    fout.write("\n")
    pwrite(fout, spins_array_print)
    fout.close()

    # #####################################
    # repeat for EB06
    # nJs = 23
    # Jstart = 0
    # Js = np.array(range(nJs)) + Jstart
    # nRowsOffset = 18 # cut away the first x Rows
    # nRows = len(spinpar_hist)
    # nCollumsExtra = 3 # 3 rows with "bin  Ex  Popul." added extra"
    # nCollums = nJs + nCollumsExtra 
    # nStartbin = 54-nRowsOffset # ust for easy copying to RAINIER file

    # spins_RAINIER = np.zeros((nRows,nCollums))
    # spins_RAINIER[:,0] =  np.array(range(nRows)) + nStartbin # copy bins
    # spins_RAINIER[:,1] = Ex # copy excitation energyies
    # spins_RAINIER[:,2] = 10. # set population to 1 (assumeing all excitations energies equally populated(?))

    # # Write spin distribution from EB06
    # EB06_mat = []
    # for E in Ex:
    #     EB06_mat.append(np.array([g(i,E=E) for i in Js]))
    # EB06_mat = np.array(EB06_mat)
    # spins_RAINIER[:,nCollumsExtra:] = EB06_mat  # copy spins
    # spins_RAINIER[:,nCollumsExtra:] = (spins_RAINIER[:,nCollumsExtra:].transpose()*spins_RAINIER[:,2]/np.sum(spins_RAINIER[:,nCollumsExtra:],axis=1)).transpose() # normalize (per bin) to given population
    # spins_array_print = spins_RAINIER[nRowsOffset:,:]

    # fout = open("Js2RAINER_EB06.txt","w")
    # fout.write(" ".join(map(str, arr_header)))
    # fout.write("\n")
    # pwrite(fout, spins_array_print)
    # fout.close()

def WriteRAINIERPerPar(nJs, nStartbin, h_negPar, h_posPar, popNorm):
    ##############################################
    # Some test -- write files to use with RAINIER
    # print population distribution for RAINIER
    # bin    Ex    Popul.    J= 0.0    J= 1.0  [...] J=9.0
    Jstart = 0
    Js = np.array(range(nJs)) + Jstart
    nRowsOffset = 0 # cut away the first x Rows
    nRows = len(h_negPar)
    nCollumsExtra = 3 # 3 rows with "bin  Ex  Popul." added extra"
    nCollums = 2*nJs + nCollumsExtra 
    nStartbin = nStartbin-nRowsOffset # ust for easy copying to RAINIER file

    bothParities = np.dstack((h_negPar,h_posPar))
    bothParities = bothParities.reshape(len(h_negPar), 2*len(h_negPar[0]))

    def FormPrintArray(spinpar_hist):
        spins_RAINIER = np.zeros((nRows,nCollums))
        # copying spinpar histogram into the historgram that shall be printed
        spins_RAINIER[:,0] =  np.array(range(nRows)) + nStartbin # copy bins
        spins_RAINIER[:,1] = Ex # copy excitation energyies
        spins_RAINIER[:,nCollumsExtra:] = spinpar_hist[:,:2*nJs-len(spinpar_hist[0])]  # copy spins
        spins_RAINIER[:,2] = popNorm # set population to popNorm
        spins_RAINIER[:,nCollumsExtra:] = (spins_RAINIER[:,nCollumsExtra:].transpose()*spins_RAINIER[:,2]/np.sum(spins_RAINIER[:,nCollumsExtra:],axis=1)).transpose() # normalize (per bin) to given population
        spins_array_print = spins_RAINIER[nRowsOffset:,:]
        return spins_array_print

    arrayPrint = FormPrintArray(bothParities)

    arr_Js_print =  [("J= " + "-{0:.1f}".format(J) + ", J= " + "+{0:.1f}".format(J)) for J in Js]
    arr_header = [("bin"),("Ex"),("Popul.")]  
    arr_header += arr_Js_print

    # Write spin distribution from Greg
    fout = open("Js2RAINER_perParity_Greg.txt","w")
    fout.write(" ".join(map(str, arr_header)))
    fout.write("\n\n")
    pwrite(fout, arrayPrint)
    fout.close()

# WriteRAINIERPerPar(nJs=10, nStartbin=24, h_negPar=spinparNeg, h_posPar=spinparPos, popNorm=10.)
WriteRAINIERPerPar(nJs=10, nStartbin=24, h_negPar=spinparNeg, h_posPar=spinparPos, popNorm=xs)