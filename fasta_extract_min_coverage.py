#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract fasta sequences that are above a minimal coverage.

Usage:
    %program <input_file> <min_coverage> <output_file>"""

import sys
import re

try:
    from Bio import SeqIO
except:
    print("This program requires the Biopython library")
    sys.exit(0)

try:
    fasta_file = sys.argv[1]      # Input fasta file
    min_coverage = int(sys.argv[2]) # Minimum coverage of sequence
    result_file = sys.argv[3]     # Output fasta file
except:
    print(__doc__)
    sys.exit(0)

fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')

with open(result_file, "w") as f:
    for seq in fasta_sequences:
        if int(seq.name.split("_")[2]) >= min_coverage:
            SeqIO.write([seq], f, "fasta")

