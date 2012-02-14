#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Formating multiple microarray data files into one data matrix.

Usage:
    %program <input_file> <output_file>

<input_file>  contains one data file name per line
<output_file> is the name of the output data file"""

import sys
import os

TEMP = "._ma_temp_file_"

try:
    input_namefile = sys.argv[1] # Input file containing filenames, one per line
    output_file = sys.argv[2]     # Output microarray data file
except:
    print __doc__
    sys.exit(0)

with open(input_namefile) as f:
    filenames = [x.strip() for x in f.readlines() if x.strip() != ""]

for f in filenames:
    os.system(str("markers_extract_to_file.py %s 'Begin Data' 'End Data' %s%s") % 
              (f, f, TEMP))

data = []

filenames = [x + TEMP for x in filenames]
for f in filenames:
    with open(f) as in_f:
        lc = -1
        for line in in_f:
            lc += 1
            if line.strip() != "":
                l = line.strip().split("\t")
                f_data = [l[8], l[9], l[20], l[21], l[32]]
                try:
                    data[lc] += f_data
                except:
                    data.append(f_data)

os.system(str("touch %s") % (output_file))
with open(output_file, "w") as out_f:
    for d in data:
        l = "\t".join(d) + "\n"
        out_f.write(l)

os.system(str("rm *%s") % (TEMP))
