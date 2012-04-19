#!/usr/bin/env python

"""Change the names of fasta sequences in a file to make retrieving matepairs
possible.

Usage:
    %program <input> <output>

<input>       path to input fasta file
<output>      path to output fasta file"""

import sys

try:
    in_file = open(sys.argv[1])
    out_file = open(sys.argv[2], "w")
except:
    print __doc__
    sys.exit[0]

n = 1
mate = 1
change = 1
for line in in_file:
    if line.startswith(">"):
        new = str(">%i\n") % (n)
        out_file.write(">sequence" + str(n) + "_" + str(mate) + "\n")
        mate += change
        change *= -1
        if mate == 1:
            n += 1
    else:
        out_file.write(line)

in_file.close()
out_file.close()

