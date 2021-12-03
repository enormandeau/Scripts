#!/usr/bin/env python3

"""Create random fasta sequences.

Usage:
    %program <length> <number> <output_file>"""

import sys
import re
from random import choice

try:
    seq_len = int(sys.argv[1])  # Length of sequences
    num_seq = int(sys.argv[2])  # Number of sequences
    result_file = sys.argv[3]   # Output fasta file
except:
    print(__doc__)
    sys.exit(0)

stub = "seq_"
num = 0

def out_name(stub, num):
    return ">" + stub + str("%i" % num) + "\n"

with open(result_file, "w") as f:
    for i in range(num_seq):
        num += 1
        seq = ""
        for j in range(seq_len):
            seq += (choice(["A", "C", "G", "T"]))
        f.write(out_name(stub, num))
        f.write(seq + "\n")
