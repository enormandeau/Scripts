#!/usr/bin/env python

### DO NOT USE THIS SCRIPT
# Instead, use 'fasta_reservoir_sampling.py'

"""Extract approximately n random sequences from a fasta file. To be sure to get
the exact desired number of sequences, boost the number of wanted sequences by a
certain amount. Eg:

150% for 300 sequences or less
120% for 1000 sequences or less
110% for 10000 sequences or less
105% for 100000 sequences or less

Then use fasta_extract_n_sequences.py to extract the exact number of sequences.

Usage:
    %program <input_file> n <output_file>"""

# Importing modules
import sys
import re
import random

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
    n_sequences = SeqIO.convert(fasta_file, "fasta", "/dev/null", "fasta")

    if n_sequences < n:
        print("There are %i sequences in the file, will extract all sequences" % (n_sequences))
        n_sequences = n

    odd = float(n) / n_sequences
    print("Treating %s\nwanted: %i, in file: %i, odd"  % (fasta_file, n, n_sequences, odd))

    fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')
    seq_num = 0

    with open(result_file, "w") as f:
        for seq in fasta_sequences:
            r = random.random()
            if r <= odd:
                SeqIO.write([seq], f, "fasta")
            seq_num += 1

