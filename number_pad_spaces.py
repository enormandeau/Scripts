#!/usr/bin/env python

"""Add spaces before numbers to pad them all to the same width

Usage:
    %program <input> <output> <spaces>

<spaces>  number of spaces including zeros for sequence number (default: 6)"""

import sys

try:
    in_file = open(sys.argv[1])
    out_file = open(sys.argv[2], "w")
except:
    print __doc__
    sys.exit[0]

try:
    num_spaces = int(sys.argv[3])
except:
    num_spaces = 6

for line in in_file:
    l = line.strip()
    if l != "":
        added_spaces = num_spaces - len(l)
        if added_spaces > 0:
            out_file.write(" " * added_spaces + l + "\n")
        else:
            out_file.write(line)

in_file.close()
out_file.close()

