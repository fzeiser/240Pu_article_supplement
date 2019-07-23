import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("Pu240_dsdE.txt")
Ex = data[:,1]
xs_neb = data[:,-3]

Sn = 6.5
Ex += Sn

plt.plot(Ex,xs_neb)
plt.xlabel(r'$E_x$ [MeV]',fontsize="medium")
plt.ylabel(r'\sigma, Non-Elastic Breakup',fontsize="medium")
plt.savefig("Pu240_dsdE.png")
plt.show()