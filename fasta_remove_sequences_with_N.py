#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Remove sequences from a fasta file if they contain Ns.

Usage:
    %program <input_file>"""

import sys
import re

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)

try:
    fasta_file = sys.argv[1]  # Input fasta file
    output_good = sys.argv[1] + ".good"
    output_bad = sys.argv[1] + ".bad"
except:
    print __doc__
    sys.exit(0)

outgood = open(output_good, "w")
outbad = open(output_bad, "w")

for seq in SeqIO.parse(open(fasta_file),'fasta'):
    name = seq.id
    sequence = str(seq.seq)
    if not sequence.find("N") > -1:
        SeqIO.write([seq], outgood, "fasta")
    else:
        SeqIO.write([seq], outbad, "fasta")

outgood.close()
outbad.close()

