import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

# import seaborn as sns
# sns.set()

plt.rcParams["axes.labelsize"] = 15

fig, ax = plt.subplots()

def readGSFdata(files):
    """
    Reading gsf data from file
    Fileformat:
    # energy  y_obs   y_obs_err
    [entries]

    where type is (currently), either "E1", "M1", or "sum"

    Parameters
    ----------
    files : array, containing entires [[filepath1, type1], ...]
    filepath: string
        Path to data table
    typ: string
        Either "E1", "M1", or "sum"

    Returns
    -------
    data : pd datafram
        dataframe with the columns [x, type, y_obs, y_obs_err]
    """

    df = pd.DataFrame()
    for (filepath, typ, label) in files:
        data = np.loadtxt(filepath)
        df1= pd.DataFrame(data, columns=["x", "y", "y_err"])
        df1["typ"] = typ
        df1["label"] = label
        df = df.append(df1, ignore_index=True)
    return df


# some iterations
data = np.loadtxt("Jint_Greg_mama_RIPL_Gg44_4res_04/GSFTable_py.dat")
plt.semilogy(data[:,0],data[:,1]+data[:,2],"k-", label="this work, iteration 4")

try:
    folder= "Jint_Greg_mama_RIPL_Gg44_4res_01"
    exp = np.loadtxt(folder+"/strength_export.txt")
    plt.errorbar(exp[:,0],exp[:,1],yerr=exp[:,2],
                 fmt="o", alpha=0.5, color="tab:brown",
                 label="this work, initial")

    data = np.loadtxt(folder+"/GSFTable_py.dat")
    Sn=6.5
    idx = abs(data[:,0]-Sn).argmin()
    data = data[:idx,:]
    plt.semilogy(data[:,0],data[:,1]+data[:,2],"--",alpha=0.5,
                 color="tab:brown")
except:
    pass


# Array of files to be read
# with entries [filepath, type]
files = np.array([["misc/data/240Pu_E1_stephan.txt","E1", "E1, Kopecky et al. (2017)"],
    ["misc/data/240Pu_M1_stephan.txt","M1", "M1, Kopecky et al. (2017)"],
    ["misc/data/gSF_239Pu_gurevich_1976_g_abs.txt", "sum",r"$^{239}$Pu($\gamma$,abs), Gurevich et al. (1976)"],
    ["misc/data/gSF_239Pu_moraes_1993_g_abs.txt", "sum", r"$^{239}$Pu($\gamma$,abs), Moraes et al. (1976)"]])

data_obs = readGSFdata(files)

# plotting
data_obs = data_obs.groupby("label")
for name, df in data_obs:
    if df["typ"].iloc[0] == 'sum':
        fmt="s"
    elif df["typ"].iloc[0] == 'M1':
        fmt="^"
    elif df["typ"].iloc[0] == 'E1':
        fmt="v"
# df = data_obs.loc[data_obs['typ'] == 'sum']
    plt.errorbar(df["x"],df["y"],yerr= df["y_err"], fmt=fmt,
                 markerfacecolor='none',  label=name)

    # df = data_obs.loc[data_obs['typ'] == 'M1']
    # plt.errorbar(df["x"],df["y"],yerr= df["y_err"].values, fmt="o", alpha=0.3, label=df["label"].iloc[0])

    # # df = data_obs.loc[data_obs['typ'] == 'E1']
    # plt.errorbar(df["x"],df["y"],yerr= df["y_err"].values, fmt="o", alpha=0.3, label=df["label"].iloc[0])


# plt.semilogy(data[:,0],data[:,1],"k--")
# plt.semilogy(data[:,0],data[:,2],"k--")

# data = np.loadtxt("Jint_Greg_mama_RIPL_Gg44_4res_04_test_res/GSFTable_py.dat")
# plt.semilogy(data[:,0],data[:,1]+data[:,2],"b-", label="I4, 4 res + some extra")
# plt.semilogy(data[:,0],data[:,1],"b--")
# plt.semilogy(data[:,0],data[:,2],"b--")

# data = np.loadtxt("Jint_Greg_mama_RIPL_Gg44_04/GSFTable_py.dat")
# plt.semilogy(data[:,0],data[:,1]+data[:,2]+5e-8,"b-.", label="I4, 5 res +5e-8")
# plt.semilogy(data[:,0],data[:,1]+5e-8,"b:")
# plt.semilogy(data[:,0],data[:,2]+5e-8,"b:")

plt.legend(loc="best")

ax.xaxis.set_major_locator(ticker.MaxNLocator(5))
plt.tick_params(labelsize=13)
plt.rcParams["axes.labelsize"] = 15

plt.xlabel(r"$E_\gamma$ [MeV]")
plt.ylabel(r"$\gamma$SF [MeV$^{-3}$]")


plt.xlim((0,18))
plt.ylim((2e-8,5e-6))
plt.tight_layout()
# plt.savefig("gsfs_art.png")
plt.savefig("gsfs_art.pdf")

# plt.xlim((0,6.5))
# plt.ylim((2e-8,5e-7))
# plt.savefig("gsfs_art_zoom.png")
# plt.show()
