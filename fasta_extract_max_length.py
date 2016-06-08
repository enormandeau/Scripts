#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract fasta sequences that are below a maximal length.

Usage:
    %program <input_file> <output_file>"""

import sys
import re

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)

try:
    fasta_file = sys.argv[1]      # Input fasta file
    max_length = int(sys.argv[2]) # Maximum length of sequence
    result_file = sys.argv[3]     # Output fasta file
except:
    print __doc__
    sys.exit(0)

fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')

with open(result_file, "w") as f:
    for seq in fasta_sequences:
        if len(str(seq.seq)) <= max_length:
            SeqIO.write([seq], f, "fasta")

