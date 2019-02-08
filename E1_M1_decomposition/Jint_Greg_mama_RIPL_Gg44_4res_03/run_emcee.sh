#!/bin/bash
python -u ../curve_fit_emcee.py | tee >(awk '!/\r\[NoLog!\]/' >log.txt)
