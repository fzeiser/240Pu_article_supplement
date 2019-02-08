#!/bin/bash

cp results/Run0001.root .
cp results/Param0001.dat .
cp -r ~/progs/RAINIER/Jint_Greg_mama_RIPL_Gg44_01/folded_rhotot .
root -l ../Analyze.C
