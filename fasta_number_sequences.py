#!/usr/bin/env python3

"""Change the names of fasta sequences in a file and number them.

Usage:
    %program <input> <output> [<stub> <spaces> <first_num>]

Parameters between brackets '[]' are optional:

<input>       path to input file
<output>      path to output file

<stub>   common part of name for all sequences (default: 'seq_')
<spaces>  number of spaces including zeros for sequence number (default: 4)
<first_num>   number from which numbering shoud start (derault: 1)"""

import sys

try:
    in_file = open(sys.argv[1])
    out_file = open(sys.argv[2], "w")
except:
    print(__doc__)
    sys.exit(1)

try:
    stub = sys.argv[3]
except:
    stub = "seq_"

try:
    num_spaces = int(sys.argv[4])
except:
    num_spaces = 4

try:
    first_num = int(sys.argv[5])
except:
    first_num = 1

n = first_num -1
zero_format = "%0" + str(num_spaces) + "i"
for line in in_file:
    if line.startswith(">"):
        n += 1
        number = str(zero_format % int(n))
        new = str(">%s%s\n") % (stub, number)
        out_file.write(new)
    else:
        out_file.write(line)

in_file.close()
out_file.close()

