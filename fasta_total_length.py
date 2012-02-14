#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Display total length of sequences in a fasta file.

Usage:
    %program file.fasta"""

import sys
import re

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)

try
    fasta_file = sys.argv[1]  # Input fasta file
except:
    print __doc__
    sys.exit(0)

fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')
total_length = 0
for seq in fasta_sequences:
    total_length += len(seq.seq.tostring())
print "The total sequence length in %s is %i bases" % (fasta_file, total_length)

