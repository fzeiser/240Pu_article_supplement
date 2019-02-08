## Input files/results for the article:
F. Zeiser et al, "Corrections for restricted spin-ranges in the Oslo Method: The example of nuclear level density and $\gamma$-ray strength function from (d,p)$^{240}\mathrm{Pu}$"
(submitted)

## An overview:

The experimental analysis can be found in the `exp_analysis`. The `runMama.exp`script runs through the Oslo Method software, generating the first generations spectra from the particle-$\gamma$ coincidence matrix `alfna`

The files for each iteration can be found in the folder `Jint_Greg_mama_RIPL_Gg44_4res_XX`, where XX should be replace by the iteration number.

Decomposition into E1 and M1 contributions is performed for each iteration in the subfolders of `E1_M1_decomposition`. One would eg. cd into `E1_M1_decomposition/Jint_Greg_mama_RIPL_Gg44_4res_01` and run the fitting script: `python2 ../curve_fit/curve_fit_diff_evolution.py`.

The results are used as input to RAINIER, which we can see in `Jint_Greg_mama_RIPL_Gg44_4res_01`. This folder provides
- `settings.h`: All settings for RAINIER
- `results`: simulation results of RAINIER
- ExEg.m and 1Gen.m: analysis of the RAINIER simulation readable to Oslo-Method software
- `folded_rhotot`: Oslo-Method analysis of RAINIER results, automated via `OsloSim.sh`

On top level we also provide the `plotComparison_PRC` script, which we used to extract the corrected NLD and gSF inputs for the next iteration. It is currently set to produce the corresponding figure in the article. To analyze a different dataset, amend the data loaded to `OCL_Potel02` or redefine `current_dataset = OCL_Potel02`.
