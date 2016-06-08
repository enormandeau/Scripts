#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract only the first occurence of each sequences, based on the name.

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
    fasta_file = sys.argv[1]  # Input fasta file
    result_file = sys.argv[2] # Output fasta file
except:
    print __doc__
    sys.exit(0)

seen = set()
fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')

with open(result_file, "w") as f:
    for seq in fasta_sequences:
        name = seq.id
        if name not in seen and len(str(seq.seq)) > 0:
            seen.add(name)
            SeqIO.write([seq], f, "fasta")

