#!/usr/bin/env python

"""Add sequence name before quality string if missing.

Usage:
    %program <input_file> <output_file>"""

import sys

try:
    in_file = sys.argv[1]
    out_file = sys.argv[2]
except:
    print __doc__
    sys.exit(0)

with open(in_file) as f:
    with open(out_file, "w") as out_f:
        for line in f:
            if line.startswith("@"):
                out_f.write(line)
                temp = line.replace("@", "+")
            elif line.startswith("+"):
                out_f.write(temp)
            else:
                out_f.write(line)

