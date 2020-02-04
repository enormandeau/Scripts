#!/usr/bin/env python3
"""
Unwrap fasta file so that each sequence takes up only one line.

Usage:
    %program  input_file  output_file
"""

# Modules
import gzip
import sys

try:
    from Bio import SeqIO
except:
    print("This program requires the Biopython library")
    sys.exit(0)

# Defining functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

# Parse user input
try:
    in_file = myopen(sys.argv[1], "rt")
    out_file = myopen(sys.argv[2], "wt")
except:
    print(__doc__)
    sys.exit(0)

# Treat sequences
sequences = ([seq.id, seq.seq.tostring()] for seq in SeqIO.parse(in_file, 'fasta'))
with open(sys.argv[2], "w") as out_file:
    for seq in sequences:
        out_file.write(">" + seq[0] + "\n" + seq[1] + "\n")
