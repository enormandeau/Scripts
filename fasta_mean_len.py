#!/usr/bin/env python

"""Display mean length of sequences in a fasta file.

Usage:
    %program file.fasta"""

import sys

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)
try:
    handle = open(sys.argv[1], 'rU')
    lengths = map(lambda seq: len(seq.seq), SeqIO.parse(handle, 'fasta'))
    print reduce(lambda x,y: x+y, lengths)/float(len(lengths))
except:
    print __doc__
