#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Extract lines starting with elements contained in a 'wanted' file.

Wanted file contains one name per line.

Usage:
    %program <input_file> <wanted_file> <output_file>"""

import sys

try:
    in_file = open(sys.argv[1])  # Input file
    wanted_file = sys.argv[2]    # Input wanted file, one name per line
    out_file = sys.argv[3]       # Output file
except:
    print __doc__
    sys.exit(0)

wanted = set()
with open(wanted_file) as f:
    for line in f:
        line = line.strip()
        if line != "":
            wanted.add(line)

lines = [l.strip() for l in in_file.readlines()]

with open(out_file, "w") as f:
    for line in lines:
        name = line.split("\t")[0]
        if name in wanted:
            f.write(line + "\n")
            #wanted.remove(name)
