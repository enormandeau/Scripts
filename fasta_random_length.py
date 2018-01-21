#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create random fasta sequences.

Usage:
    %program <length> <variance> <number> <output_file>"""

import sys
import re
import random

try:
    seq_len = int(sys.argv[1])  # Length of sequences
    seq_var = int(sys.argv[2])  # Variance of length
    num_seq = int(sys.argv[3])  # Number of sequences
    result_file = sys.argv[4]   # Output fasta file
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
        seq = [] 
        variance = random.randint(-seq_var, seq_var)
        for j in range(seq_len + variance):
            seq.append(random.choice(["A", "C", "G", "T"]))
        f.write(out_name(stub, num))
        f.write("".join(seq) + "\n")

