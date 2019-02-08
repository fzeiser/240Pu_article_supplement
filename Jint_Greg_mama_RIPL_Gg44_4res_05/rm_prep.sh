#!/bin/bash

rm -irf results
rm -irf folded_rhotot
rm Run0001.root
rm Param0001.dat
find . -name 'RAINIER_copy*' -exec rm {} \;
find . -name 'slurm-*' -exec rm {} \;
#rm slurm-*
rm 1Gen.m
rm ExEg.m

