#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract fasta sequences that are at or above a minimal length.

Usage:
    %program <input_file> <output_file>"""

import sys

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)

try:
    fasta_file = sys.argv[1]  # Input fasta file
    min_len = int(sys.argv[2]) # Minimum length of sequences to be counted
except:
    print __doc__
    sys.exit(0)

count = 0
fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')

for seq in fasta_sequences:
    if len(str(seq.seq)) >= min_len:
        count += 1

print count, "sequences where longer than", min_len, "nucleotides"

