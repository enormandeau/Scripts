#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract sequences from a fasta file if their name is in a 'wanted' file.

Wanted file contains one sequence name per line.

Usage:
    %program <input_file> <wanted_file> <output_file>"""

import sys
import re

try:
    from Bio import SeqIO
except:
    print("This program requires the Biopython library")
    sys.exit(0)

try:
    fasta_file = sys.argv[1]  # Input fasta file
    wanted_word = sys.argv[2] # Word to be found in the sequence name
    result_file = sys.argv[3] # Output fasta file
except:
    print(__doc__)
    sys.exit(0)

fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')

with open(result_file, "w") as f:
    for seq in fasta_sequences:
        name = seq.name
        if  wanted_word in name and len(str(seq.seq)) > 0:
            wanted.remove(name) # Output only the first appearance for a name
            SeqIO.write([seq], f, "fasta")

