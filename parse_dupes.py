#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Parse the result of the unix fdupes program

fdupes finds duplicated files in a given set of directories.

Usage:
    %program <input_file> <min_bytes> <output_file>"""

import sys
import re

try:
    in_file = open(sys.argv[1])  # Input fdupes file
    min_bytes = int(sys.argv[2]) # Input minimum number of bytes to use
    out_file = sys.argv[3]       # Output edited dfupes file
except:
    print __doc__
    sys.exit(0)

lines = [l.strip() for l in in_file.readlines()]

new_file = False
with open(out_file, "w") as f:
    for line in lines:
        if line == "":
            if new_file == True:
                f.write("\n")
            new_file = False
        elif new_file == True:
            f.write(line + "\n")
        elif new_file == False and len(re.findall("[0-9]+\ bytes", line)) > 0:
            bytes = int(line.split()[0])
            if bytes >= min_bytes:
                f.write(line + "\n")
                new_file = True

