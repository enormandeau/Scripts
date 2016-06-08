#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Replace fasta sequences that are above a minimal length.

Usage:
    %program <input_file> <min_length> <output_file> <replace_by>"""

import sys
import re

try:
    from Bio import SeqIO
    from Bio.Seq import Seq as BioSeq
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

try:
    replace_by = sys.argv[4]      # String to replace with
except:
    replace_by = "A"
    print "No replace string entered, using 'A'"

fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')

with open(result_file, "w") as f:
    for seq in fasta_sequences:
        if len(str(seq.seq)) >= min_length:
            SeqIO.write([seq], f, "fasta")
        else:
            seq.seq = BioSeq(replace_by)
            SeqIO.write([seq], f, "fasta")

           














