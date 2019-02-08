import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("t_chi_hist.dat")

plt.step(data[:,0],data[:,1])

plt.show()