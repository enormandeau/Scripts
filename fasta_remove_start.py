#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract sequences from a fasta file if the begining of their name is not in a 'remove' file.

Remove file contains one sequence name per line.

Usage:
    %program <input_file> <remove_file> <output_file>"""

import sys
import re

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)

try:
    fasta_file = sys.argv[1]  # Input fasta file
    remove_file = sys.argv[2] # Input remove file, one gene name per line
    result_file = sys.argv[3] # Output fasta file
except:
    print __doc__
    sys.exit(0)

remove = set()
with open(remove_file) as f:
    for line in f:
        line = line.strip()
        if line != "":
            remove.add(line)

fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')

with open(result_file, "w") as f:
    for seq in fasta_sequences:
        name = seq.id
        to_remove = False
        for r in remove:
            if name.startswith(r):
                to_remove = True
        if to_remove == False and len(str(seq.seq)) > 0:
            SeqIO.write([seq], f, "fasta")

