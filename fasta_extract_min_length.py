#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract fasta sequences that are above a minimal length.

Usage:
    %program <input_file> <min_length> <output_file>"""

import sys
import re

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)

try:
    fasta_file = sys.argv[1]      # Input fasta file
    min_length = int(sys.argv[2]) # Minimum length of sequence
    result_file = sys.argv[3]     # Output fasta file
except:
    print __doc__
    sys.exit(0)

fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')

with open(result_file, "w") as f:
    for seq in fasta_sequences:
        if len(seq.seq.tostring()) >= min_length:
            SeqIO.write([seq], f, "fasta")

