#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Formating perch array design file from 1008 spots to 6048 spots format.

Usage:
    %program <input_file> <output_file>"""

import sys
import os

try:
    input_file = sys.argv[1]  # Input array design file with 1008 spots
    output_file = sys.argv[2] # Output array design file with 6048 spots
except:
    print __doc__
    sys.exit(0)

with open(input_file) as f:
    lines = [l for l in f.read().split("\n") if l !=""]

results = [lines[0] + "\n"]
data = lines[1:] * 3

for l in data:
    results.append(l + "\n")
    ll = l.split("\t")
    ll[1] = str(int(ll[1]) + 1)
    ll = "\t".join(ll)
    results.append(ll + "\n")

with open(output_file, "w") as f:
    f.writelines(results)

