import numpy as np
import sys
from scipy import interpolate


def readNLDtot(folder):
  nld = np.loadtxt(folder+"/talys_nld_cnt.txt", usecols=(0,3))
  return nld

def log_interp1d(xx, yy):
    """ Interpolate a 1-D function.logarithmically """
    logy = np.log(yy)
    lin_interp = interpolate.interp1d(xx, logy, kind='linear')
    log_interp = lambda zz: np.exp(lin_interp(zz))
    return log_interp


def WriteRAINIERnldTable(fname, Ex, nld, sigma, a=None):
    '''
    Takes nld and write it in a format readable for RAINIER

    input:
    fname: outputfilename
    x: Excitation energy in MeV
    nld: nld for above discretes [in 1/MeV]
    sigma: spin-cut
    a: level density parameter a
    '''
    if a is None:
        a = np.zeros(len(Ex))

    fh = open(fname, "w")

    def write_arr(arr):
        # write array to file that resembles the CERN ROOT arrays
        for i, entry in enumerate(arr):
            if i!=(len(arr)-1):
                fh.write(str(entry)+",\n")
            else:
                fh.write(str(entry)+"\n};\n")

    fh.write("#include \"TGraph.h\"\n\n")
    fh.write("double adETable[] = {\n")
    write_arr(Ex)
    fh.write("const int nETable = sizeof(adETable)/sizeof(double);\n\n")

    fh.write("double adRho[] = {")
    write_arr(nld)
    fh.write("TGraph *grRho = new TGraph(nETable,adETable,adRho);\n\n")

    fh.write("double adLDa[] = {\n")
    write_arr(a)
    fh.write("TGraph *grLDa = new TGraph(nETable,adETable,adLDa);\n\n")

    fh.write("double adJCut[] = {\n")
    write_arr(sigma)
    fh.write("TGraph *grJCut = new TGraph(nETable,adETable,adJCut);\n\n")

    print("Wrote nld fro RAINIER to {}".format(fname))

    fh.close()


def sigma2(U,A,a,E1, rmi_red=1):
    #cut-off parameters of EB05
    sigma2 = np.sqrt(rmi_red) * 0.0146*A**(5./3.) * ( 1. + np.sqrt(1. + 4.*a*(U-E1)) ) / (2.*a)
    return sigma2


def sigma(U,A,a,E1, rmi_red=1):
    return np.sqrt(sigma2(U,A,a,E1, rmi_red=1))


if __name__ == '__main__':
  # Parameters for 240Piu
  Sn=6.534
  Ecrit=1.03
  A=240
  a=25.16
  E1=0.12

  folder = sys.argv[1]
  nld = readNLDtot(folder)

  # id_Ecrit = np.abs(nld[:,0]-Ecrit).argmin()
  # id_Sn = np.abs(nld[:,0]-Sn).argmin()
  # nld = nld[Ecrit:id_Sn+1,:]

  binwidth = 0.05
  Earr = np.linspace(Ecrit, Sn, num=int((Sn-Ecrit)/binwidth))
  fnld = log_interp1d(nld[:,0],nld[:,1])
  nld_interp = fnld(Earr)

  WriteRAINIERnldTable("nld_new.dat", Earr, nld_interp, sigma(U=Earr, A=A, a=a,E1=E1), a=None)

  header="# Ex[MeV] nld[MeV^-1]"
  np.savetxt("nld_new.txt", np.c_[Earr,nld_interp], header=header)

  # import matplotlib.pyplot as plt
  # plt.semilogy(Earr, nld_new, "o-")
  # plt.show()

# header="# E y"
# np.savetxt('strength_export.txt', strength,
#             header=header)
# np.savetxt('strengthext_export.txt', strengthext,
#             header=header)
