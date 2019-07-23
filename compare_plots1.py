
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import ompy as om
import sys
import scipy.ndimage
import copy
import seaborn as sns


sns.set()

sns.set_context("paper")
# sns.set_context("talk")

# sns.set(font_scale=1.2) # Bigger than normal fonts
# sns.set(font_scale=1.2)
# sns.set(rc={'figure.figsize':(5.5,6.5)})
sns.set_style("ticks", { 'axes.grid': False})
plt.rcParams["axes.labelsize"] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.loc'] = 'best'

def projectEx(mat, Ex_select):
    Ex = mat.Ex
    mat = mat.values
    idEx = np.argmin(np.abs(Ex-Ex_select))
    py = mat[idEx,:]
    return py


# def slice_plot(ax, Ex, fg_exp, fg_err, fg_sim, fg_sim_err=None, fg_sim2=None):
#     ax.text(0.05, 0.9, "Ex = \n{:.0f} keV".format(Ex),
#             horizontalalignment='left',
#             verticalalignment='center',
#             transform=ax.transAxes,
#             size="small")

#     Eg_exp = fg_exp.Eg
#     Eg_sim = fg_sim.Eg

#     py = projectEx(fg_exp, Ex_select=Ex)
#     pyerr = projectEx(fg_err, Ex_select=Ex)
#     ax.errorbar(Eg_exp, py, yerr=pyerr, fmt="o--", label="exp", markersize='3')

#     py = projectEx(fg_sim, Ex_select=Ex)
#     # pyerr = projectEx(fg_sim_err,Ex_select=Ex)
#     # ax.errorbar(Eg_sim,py,yerr=pyerr,fmt="o-", label="sim")
#     ax.plot(Eg_sim, py, "o--", label="sim", markersize='3')
# #     py = projectEx(fg_sim,Ex_select=Ex)
# #     ax.plot(Eg_sim,py,"s", alpha=0.5, label ="sim")
#     ax.set_xlim(max(0, Eg_cut-200), Ex+300)
#     ax.legend(loc="upper right")
#     ax.set_xlim((0,5000))
#     # plt.savefig("does_it_work-Ex{}.pdf".format(Ex))


def map_iterator_to_grid(counter, Nx):
    # Returns i, j coordinate pairs to map a single iterator onto a 2D grid for subplots.
    # Counts along each row from left to right, then increments row number
    i = counter // Nx
    j = counter % Nx
    return i, j


# def main_fg(iteration, fsim_base):
#     fg_sim = om.Matrix()
#     fg_sim.load(fsim_base+"/folded_rhotot_test_low_Ex/fg.rsg")
#     # fg_sim.plot()

#     # fg_sim_err = om.Matrix()
#     # fg_sim_err.load(fbase+"folded_rhotot_test_low_Ex/fgerr.rsg")
#     # fg_sim_err.plot()

#     fg_exp = om.Matrix()
#     fg_exp.load("/home/fabiobz/Desktop/Masterthesis/239Pu_OsloMethod_20180802/rhotot_T0.415/fg.rsg")
#     # fg_exp.plot()

#     fg_err = om.Matrix()
#     fg_err.load("/home/fabiobz/Desktop/Masterthesis/239Pu_OsloMethod_20180802/rhotot_T0.415/fgerr.rsg")
#     # fg_err.plot()

#     Nx, Ny = 3, 2
#     Ntot = Nx * Ny
#     fig, axes = plt.subplots(Ny, Nx, sharey=True, sharex=True,
#                              gridspec_kw={'hspace': 0, 'wspace': 0})
#     Exs = np.linspace(2600, 4000, Ntot)

#     for i in range(Ntot):
#         i_plt, j_plt = map_iterator_to_grid(i, Nx=Nx)
#         ax = axes[i_plt,j_plt]
#         Ex_plt = Exs[i]
#         slice_plot(ax, Ex_plt, fg_exp, fg_err, fg_sim)
#     try:
#         fig.suptitle(str(sys.argv[1]))
#     except IndexError:
#         plot_title = ("Differences between exp (1Gen) and iteration {}").format(iteration)
#         fig.suptitle(plot_title)
#         pass


#     fig.savefig("does_it_work_fg_{}.pdf".format(iteration))


def get_differences(iteration, fname_exp, fname_sim, mtype, Eg_bins,
                    fname_sim2=None, fname_exp_err=None):
    matrix_exp = om.Matrix()
    matrix_exp.load(fname_exp)

    matrix_sim = om.Matrix()
    matrix_sim.load(fname_sim)

    if fname_sim2 is not None:
        matrix_sim2 = om.Matrix()
        matrix_sim2.load(fname_sim2[0])
        matrixes = [matrix_exp, matrix_sim, matrix_sim2]
    else:
        matrixes = [matrix_exp, matrix_sim]

    if fname_exp_err is not None:
        matrix_exp_err = om.Matrix()
        matrix_exp_err.load(fname_exp_err)
        matrixes.append(matrix_exp_err)

    for matrix in matrixes:
        matrix.values = om.rebin_matrix(matrix.values,
                                        matrix.Eg, Eg_bins,
                                        rebin_axis=1)
        matrix.Eg = Eg_bins
        matrix.values = om.rebin_matrix(matrix.values,
                                        matrix.Ex, Eg_bins,
                                        rebin_axis=0)
        matrix.Ex = Eg_bins

        idx = abs(matrix.Eg-Eg_cut).argmin()
        matrix.values[:,:idx] = 0

    # if mtype == "allGen":
    #     matrix_exp.values = om.rebin_matrix(matrix_exp.values,
    #                                         matrix_exp.Eg, matrix_sim.Eg,
    #                                         rebin_axis=1)
    #     matrix_exp.Eg = matrix_sim.Eg
    #     sigma = 1.5
    # if mtype == "1Gen":
    #     # matrix_exp.values = om.rebin_matrix(matrix_exp.values,
    #     #                                     matrix_exp.Eg, matrix_sim.Eg[::2],
    #     #                                     rebin_axis=1)
    #     # matrix_exp.Eg = matrix_sim.Eg[::2]

    #     matrix_sim.values = om.rebin_matrix(matrix_sim.values,
    #                                         matrix_sim.Eg, matrix_exp.Eg,
    #                                         rebin_axis=1)
    #     matrix_sim.Eg = matrix_exp.Eg
    #     sigma = 0.

    # matrix_sim.plot()

    def my_projection(Ex, matrix, plot=True, sigma=0, fmt="o--",
                      linewidth=1, **kwargs):
        matrix = copy.deepcopy(matrix)
        Eg_max = Ex+100
        idx = abs(matrix.Eg-Eg_max).argmin()
        matrix.values[:, idx:] = 0
        py = projectEx(matrix, Ex_select=Ex)
        if sigma > 0:
            py = scipy.ndimage.gaussian_filter1d(py, sigma)
        py /= np.sum(py)

        if plot:
            ax.plot(matrix.Eg/1e3, py, fmt, markersize='3', **kwargs)
        return py

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    def slice_plot(ax, Ex, mtype, ax_diff=None):
        ax.text(0.05, 0.9, "Ex = \n{:.2f} MeV".format(Ex/1e3),
                horizontalalignment='left',
                verticalalignment='center',
                transform=ax.transAxes,
                size="medium")
        if mtype == "allGen":
            pyexp = my_projection(Ex, matrix_exp, label="exp.", color="black",
                          zorder=20)
        elif mtype == "1Gen":
            # py = projectEx(matrix_exp, Ex_select=Ex)
            # pyerr = projectEx(matrix_exp_err, Ex_select=Ex)
            # ax.errorbar(matrix_exp.Eg, py,
            #             yerr=pyerr, fmt="o--", label="exp", markersize='3',
            #             color=colors[0],
            #             zorder=20)
            pyexp = my_projection(Ex, matrix_exp, label="exp.", color="black",
                          zorder=20)
        pysim = my_projection(Ex, matrix_sim,
                      label="sim.#{}".format(iteration),
                      color=colors[2],
                      fmt="s--")
        if fname_sim2 is not None:
            pysim2 = my_projection(Ex, matrix_sim2,
                          label="sim.#{}".format(fname_sim2[1]),
                          color=colors[3],
                          fmt="^--")
        ax.set_xlim(max(0, Eg_cut)/1e3, (Ex+300)/1e3)
        ax.set_ylim(0.001, 0.18)
        # py_sim1 = my_projection(matrix_sim1, label="sim1")
        ax.set_xlabel(r"$E_\gamma$ [MeV]")
        ax.xaxis.set_major_locator(MaxNLocator(4))
        # ax.set_ylabel(r"$P(E_\gamma)$ [arb. units]")
        if ax_diff is not None:
            ax_diff.plot(matrix.Eg/1e3, pysim/pyexp, "s--", color=colors[2])
            ax_diff.plot(matrix.Eg/1e3, pysim2/pyexp, "^--" ,color=colors[3])
            ax_diff.set_ylim(0,2.5)

    Nx, Ny = 3, 2
    Ntot = Nx * Ny
    fig, axes = plt.subplots(Ny, Nx, sharey=True, sharex=True,
                             gridspec_kw={'hspace': 0, 'wspace': 0})
    fig_diff, axes_diff = plt.subplots(Ny, Nx, sharey=True, sharex=True,
                                       gridspec_kw={'hspace': 0, 'wspace': 0})
    Exs = np.linspace(2600, 4000, Ntot)
    for i in range(Ntot):
        i_plt, j_plt = map_iterator_to_grid(i, Nx=Nx)
        ax = axes[i_plt, j_plt]
        ax_diff = axes_diff[i_plt, j_plt]
        Ex = Exs[i]
        slice_plot(ax, Ex, mtype, ax_diff)
        if i==Ntot-1:
            ax.legend()
    for ax in [axes[0, 0], axes[1, 0]]:
        ax.set_ylabel(r"$P(E_\gamma)$")
    if mtype == "allGen":
        fig.suptitle("All Generations")
        fig.savefig("does_it_work_allGen_{}.pdf".format(iteration))
        fig_diff.savefig("diff_allGen_{}.pdf".format(iteration))
    if mtype == "1Gen":
        fig.suptitle(r"$1^\mathrm{st}$ Generation")
        fig.savefig("does_it_work_fg_{}.pdf".format(iteration))
        fig_diff.savefig("diff_fg_{}.pdf".format(iteration))

    Exs = matrix_sim.Ex
    Ex_min = 2500
    Ex_max = 4000
    id1 = abs(Exs-Ex_min).argmin()
    id2 = abs(Exs-Ex_max).argmin()
    Exs = Exs[id1:id2+1]

    chi2s = np.zeros(len(Exs))
    for i, Ex in enumerate(Exs):
        py_exp = my_projection(Ex, matrix_exp, plot=False)
        py_sim = my_projection(Ex, matrix_sim, plot=False)
        chi2 = np.sum((py_exp-py_sim)**2)
        chi2s[i] = chi2
    return chi2s


if __name__ == "__main__":

    # use the same binning everywhere as used for the "exp" FG matrix
    # ensures also same binning as NLD and gSF
    fname_exp = "/home/fabiobz/Desktop/Masterthesis/239Pu_OsloMethod_20180802/rhotot_T0.415/fg.rsg"
    fg = om.Matrix(filename=fname_exp)
    Eg_bins = fg.Eg
    Eg_cut = 1000 # lower cut

    chi2s_ExEg_all_Ex = []
    chi2s_1Gen_all_Ex = []
    for i in range(1, 7):
        fname_exp = "/home/fabiobz/Desktop/Masterthesis/239Pu_OsloMethod_20180802/alfna_un"
        fsim_base = "../Jint_Greg_mama_RIPL_Gg44_4res_0" + str(i)
        it_compare = 3
        fsim2_base = "../Jint_Greg_mama_RIPL_Gg44_4res_0" + str(it_compare)
        chi2s = get_differences(i, fname_exp, fsim_base+"/ExEg.m",
                                mtype="allGen", Eg_bins=Eg_bins,
                                fname_sim2=[fsim2_base+"/ExEg.m", it_compare])
        chi2s_ExEg_all_Ex.append(chi2s.sum())

        fname_exp = "/home/fabiobz/Desktop/Masterthesis/239Pu_OsloMethod_20180802/rhotot_T0.415/fg.rsg"
        fname_exp_err = "/home/fabiobz/Desktop/Masterthesis/239Pu_OsloMethod_20180802/rhotot_T0.415/fgerr.rsg"
        chi2s = get_differences(i, fname_exp, fsim_base+"/1Gen.m",
                                mtype="1Gen", Eg_bins=Eg_bins,
                                fname_exp_err=fname_exp_err,
                                fname_sim2=[fsim2_base+"/1Gen.m", it_compare])
        chi2s_1Gen_all_Ex.append(chi2s.sum())

        # main_fg(i, fsim_base)

        # fig, ax = plt.subplots()
        # ax.plot(Exs, chi2s, "b", label="chi2s")
        # # ax.plot(Exs, chi2_1s, "r", label="chi2_1s")
        # ax.legend()
        # ax.set_xlabel(r"$E_x$ [keV]")
        # ax.set_ylabel(r"$\chi^2$ [arb. units]")
        # fig.suptitle("Differences between exp and simulation")

    fig_chi2s, ax_chis = plt.subplots()
    chi2s_ExEg_all_Ex = np.array(chi2s_ExEg_all_Ex)
    chi2s_1Gen_all_Ex = np.array(chi2s_1Gen_all_Ex)
    ax_chis.plot(range(1, 7), chi2s_ExEg_all_Ex*1.3*5, "o",
                 label="all generations")
    ax_chis.plot(range(1, 7), chi2s_1Gen_all_Ex*4, "s", label=r"$1^{\mathrm{st}}$ generation")
    chi2_diffevo = np.array([134.49, 211.12, 280.53, 295.47, 277.35])
    # ax_chis.plot(range(1, 6), chi2_diffevo/chi2_diffevo.min(), "s",
    #              label=r"gsf fit")
    ax_chis.set_xlabel("Iteration")
    ax_chis.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax_chis.set_ylabel(r"$\chi^2$ [arb. units]")
    ax_chis.legend(loc='upper center')
    fig_chi2s.suptitle("Differences between exp and simuation")
    fig_chi2s.savefig("chi2_per_iteration")

    plt.show()
