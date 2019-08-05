#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract sequences from a fasta file and group them in output files.

Groups of 'number' sequences are formed.
Output file names will begin by 'stub'.

Usage:
    %program <input_file> <number> <stub>"""

import sys
import re

try:
    from Bio import SeqIO
except:
    print("This program requires the Biopython library")
    sys.exit(0)

try:
    fasta_file = sys.argv[1]        # Input fasta file
    nb_sequences = int(sys.argv[2]) # Number of sequences per group
    result_file = sys.argv[3]       # Output fasta filename stub eg: my_genes
except:
    print(__doc__)
    sys.exit(0)

fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')
end = False
group_count = 0
total_seq = 0

while True:
    group_count += 1
    with open(result_file + str("%04i.fasta" % group_count), "w") as f:
        for i in range(nb_sequences):
            try:
                name = ""
                seq = next(fasta_sequences)
                total_seq += 1
            except:
                print("All sequences treated")
                if total_seq % nb_sequences != 0:
                    print("WARNING: Number of sequences not a multiple of %i"\)
                           % nb_sequences
                sys.exit(0)
            f.write(">" + seq.name + "\n" + str(seq.seq) + "\n")

