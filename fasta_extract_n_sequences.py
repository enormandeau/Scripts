#!/usr/bin/env python
"""Extract the first n sequences from a fasta file. 

Usage:
    %program <input_file> n <output_file>"""

# Importing modules
import sys
import re

try:
    from Bio import SeqIO
except:
    print("This program requires the Biopython library")
    sys.exit(0)

# Parsing user input
try:
    fasta_file = sys.argv[1]  # Input fasta file
    n = int(sys.argv[2]) # Number of sequences wanted
    result_file = sys.argv[3] # Output fasta file
except:
    print(__doc__)
    sys.exit(0)

# Main
if __name__ == '__main__':
    fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')
    seq_num = 0

    with open(result_file, "w") as f:
        while seq_num < n:
            seq = next(fasta_sequences)
            SeqIO.write([seq], f, "fasta")
            seq_num += 1

