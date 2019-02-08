from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from utilities import *

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
	strength = strength[np.all(strength,axis=1)] # delete "0" elments

	transextfile = open(folder+'/transext.nrm')
	transextlines = transextfile.readlines()
	transextfile.close()
	Next = len(transextlines)
	strengthext = np.zeros((Next, 2))
	for i in range(Next):
		transext_current = float(transextlines[i].split()[0])
		energy_current = a0 + i*a1 + 1e-8
		strengthext[i,:] = ( energy_current, transext_current/(2*np.pi*energy_current**3) )

	return strength, strengthext

folder = sys.argv[1]
strength, strengthext = readGSF(folder)
strengthext = strengthext[strengthext[:,0]>0]

header="# E y"
np.savetxt('strength_export.txt', strength,
            header=header)
np.savetxt('strengthext_export.txt', strengthext,
            header=header)
