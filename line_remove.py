#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Remove lines starting with elements contained in a 'remove' file.

Remove file contains one name per line.

Usage:
    %program <input_file> <remove_file> <output_file>"""

import sys

try:
    in_file = open(sys.argv[1])  # Input file
    remove_file = sys.argv[2]    # Input remove file, one name per line
    out_file = sys.argv[3]       # Output file
except:
    print __doc__
    sys.exit(0)

remove = set()
with open(remove_file) as f:
    for line in f:
        line = line.strip()
        if line != "":
            remove.add(line)

lines = [l.strip() for l in in_file.readlines()]

with open(out_file, "w") as f:
    for line in lines:
        name = line.split("\t")[0]
        if name not in remove:
            f.write(line + "\n")
