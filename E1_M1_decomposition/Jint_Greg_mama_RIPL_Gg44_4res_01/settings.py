import numpy as np
import random
from math import pi
import os

# Set random seed to get reproducible results
myseed = np.loadtxt("set_myseed.dat",dtype=int,comments="#")
np.random.seed(myseed)

# variables for emcee
nWalkers = 100
nSteps = 2000
nBurnin = 1500

# variables for differential evolution
n_runs_diff_evo = 1 # how often shall we run diff. evo.
mutation = (0.5,1.)
maxiter = 400
# maxiter = None  # uses the default max iterations
disp = False
strategy = "best1bin"

# Variables for emcee test
# how many runs
n_runs_synthetic_tot = 500
# force change of theta such that it lies within the boundaries
force_change = 0.001

strength_file = "strength_export.txt"

# parameter names
parameter_names_all = [
"GDR1_E", "GDR1_gamma", "GDR1_sigma",
"GDR2_E", "GDR2_gamma", "GDR2_sigma",
#"GDR_T",
"SLO1_E", "SLO1_gamma", "SLO1_sigma",
"SLO2_E", "SLO2_gamma", "SLO2_sigma",
"SLO3_E", "SLO3_gamma", "SLO3_sigma",
"T"
]

# initial guess; eg result from minimization
# initial guess; eg result from minimization
# try:
#     myfile = "popt_diff_evo.dat"
#     p0=np.loadtxt(myfile)
#     print "p0 directly taken from " + myfile
# except:
#     p0_all=[
#          # omega, Gamma, sigma
#          # MeV,   MeV,   mb
#             11.6, 6.8, 231,   # (E)GDR number 1
#             14.01, 5.23, 362,# (E)GDR number 2
#             #0.42,              # Common (E)GDR temperature in MeV
#             2.07, 0.31, 0.71,   # SLO number 1 (scissors 1)
#             2.59, 0.90, 0.86,   # SLO number 2 (scissors 2)
#             # 8.34, 7.8, 19.75  # SLO number 3
#             4.26, 2.46, 3.18,
#             0.28                #(E)GDR Temp
#             ]
p0_all=[
     # omega, Gamma, sigma
     # MeV,   MeV,   mb
        11.6, 6.8, 231,   # (E)GDR number 1
        14.01, 5.23, 362,# (E)GDR number 2
        #0.42,              # Common (E)GDR temperature in MeV
        2.07, 0.31, 0.71,   # SLO number 1 (scissors 1)
        2.59, 0.90, 0.0,   # SLO number 2 (scissors 2)
        # 8.34, 7.8, 19.75  # SLO number 3
        4.26, 2.46, 3.18,
        0.28                #(E)GDR Temp
        ]

# boundaries
# transform a boundary like this
# (12,15) -> None
# in order to take p0 instead and don't fit this parameter
p0_bounds_all=[
     # omega, Gamma, sigma
     # MeV,   MeV,   mb
    (9.,13.3), (3.,12), (150.,400.),     # (E)GDR number 1
    (12.8,15.8), (3.,12), (150.,450.),    # (E)GDR number 2
    #0.42,                        # Common (E)GDR temperature in MeV
    (1.,4), (0.3,3.), (0.2,2.),          # SLO number 1 (scissors 1)
    #(1,4), (0.3,3.), (0.2,2.),          # SLO number 2 (scissors 2)
    None, None, None,
    # 8.34, 7.8, 19.75            # SLO number 3
    # (4,7.5), (1,7), (1,15)
    (3.8,8.), (0.8,4.5), (2.,40.),
    (0.1,0.8)                       #(E)GDR Temp
    ]

p0_bounds =[]
# p0_bounds_fix =[]
p0 = []
p0_fix =[]
parameter_names = []
parameter_names_fix = []

for i, bound in enumerate(p0_bounds_all):
    if bound == None:
        p0_fix.append(p0_all[i])
        parameter_names_fix.append(parameter_names_all[i])
    elif len(bound)==2:
        p0.append(p0_all[i])
        p0_bounds.append(bound)
        parameter_names.append(parameter_names_all[i])
    else:
        exit()


p0= np.array(p0)
p0_bounds = np.array(p0_bounds)

# Hacks
# Uncomment to constrain maximum sigma of SLO3 "hardcode" in the functions
# definition (necessary in the emcee code, otherwise it wen really high)

try:
    _index = parameter_names.index("SLO3_sigma")
    SLO_constained_max_sigma = p0_bounds[_index,1] # comment out to ignore hack
except:
    pass

## Parameters for the nucleus
# A = 240          # (residual nucleus)
# calibration coefficients for the strength function file
# a0_strength =  -0.8296
# a1_strength =   0.1354


# Potential HACK: Skip some points
choice_skip = False
n_points_skip      = 3    # number of points that should be skipped
n_cutstart = -3   # first point to skipp, start counting from 1
n_cutcont   = n_cutstart + n_points_skip + 1
if n_cutstart<0 and n_cutcont>=0:
    n_cutcont=None
# Uncomment to readjust OCL data errors
# minimum error of ocl data
ocl_y_err_min = 0.05 # relative error

# for emcee
# The BM1 value may be constrained due to physical aguments (eg sum rule)
# Uncomment to constrain the maximum BM1 value
# BM1_max = 25.
# mult = 1.2
# BM1_max_emcee = BM1_max * mult
# print "Constrained BM1_max to ", BM1_max, "and for emcee to", BM1_max_emcee

# Some more plotting of results
bool_ploting = True

# some constant
#pi     = 3.14159265358979323846;   # defined by numpy
alpha            = 7.2973525664E-3 # approx. 1/137
value_protonmass = 938.272046 # in MeV/c^2
value_hbarc      = 197.32697 # in MeV fm
factor_BM1       = (9./(32. * pi**2 ) * 1/alpha
                    * (2.* value_protonmass / value_hbarc)**2. *1/10)

##########
## setting up directories
print("This file full path (following symlinks)")
full_path = os.path.realpath(__file__)
print(full_path + "\n")

print("This file directory and name")
path, filename = os.path.split(full_path)
print(path + ' --> ' + filename + "\n")

print("This file directory only")
filedir = os.path.dirname(full_path)
print(filedir)

cwd = os.getcwd()
###########
