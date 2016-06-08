#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract sequences from a fasta file if their name is in a 'wanted' file.

Wanted file contains one sequence name per line.
Insertions, represented by '*' are removed from the sequences.

Usage:
    %program <input_file> <wanted_file> <output_file>"""

import sys
import re
from Bio import SeqIO

fasta_file = sys.argv[1]  # Input fasta file
number_file = sys.argv[2] # Input interesting numbers file, one per line
result_file = sys.argv[3] # Output fasta file

wanted = set()
with open(number_file) as f:
    for line in f:
        line = line.strip()
        if line != "":
            wanted.add(line)

fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')

for seq in fasta_sequences:
    name = seq.id
    s = str(seq.seq)
    if name in wanted:
        f.write(">" + name + "\n" + s.replace("*", "") + "\n")

