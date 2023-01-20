#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Count and export redundancy of sequences found in a fasta file.

Warning: may crash by using the whole memory.

Usage:
    %program <input_file> <output_file> [data_column]"""

import sys
import re
from collections import defaultdict

try:
    from Bio import SeqIO
except:
    print("This program requires the Biopython library")
    sys.exit(0)

try:
    fasta_file = sys.argv[1]  # Input fasta file
    out_file = sys.argv[2]    # Outpout file
except:
    print(__doc__)
    sys.exit(0)

d = defaultdict(int)

fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')
for seq in fasta_sequences:
    d[str(seq.seq)] += 1

print("There where %s different sequences" % (len(d)))
fasta_sequences.close()

dd = [(x[1], x[0]) for x in d.items()]
dd.sort(reverse=True)

with open(out_file, "w") as f:
    for x in dd:
        f.write(str(x[1]) + "\t" + str(x[0]) + "\n")

