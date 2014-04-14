#!/usr/bin/env python
# cout sequence redondancy in a RAD file

"""Count and export redundancy of sequences found in a RAD file.

Warning: may crash by using the whole memory on large files

Usage:
    %program <input_file> <output_file> [data_column]"""

import sys
from collections import defaultdict

try:
    in_file = open(sys.argv[1])
    out_file = open(sys.argv[2], "w")
except:
    print __doc__
    sys.exit(0)

try:
    data_col = int(sys.argv[3])
except:
    data_col = 8

redundancy = defaultdict(int)
for line in in_file:
    seq = line.split("\t")[data_col]
    if seq.find(".") == -1 and seq.find("-") == -1:
        redundancy[seq] +=1

counts = [(x[1], x[0]) for x in redundancy.items()]
counts.sort(reverse=True)

for c in counts:
    out_file.write(str("%i\t%s\n") % (c[0], c[1]))

in_file.close()
out_file.close()

