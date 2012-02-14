#!/usr/bin/python

"""Wrap fasta sequences to a given length (60 characters by default).

Usage:
    %program <input_file> <output_file> [line_length]"""

import sys

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)

try:
    in_file = open(sys.argv[1], "rU")
    out_file = open(sys.argv[2], "w")
except:
    print __doc__
    sys.exit(0)

try:
    nb_char = int(sys.argv[3])
except:
    print "No line lenght or bad lenght specified, using 60 pb per line"
    nb_char = 60

sequences = ([seq.id, seq.seq.tostring()] for seq in SeqIO.parse(in_file, 'fasta'))
with open(sys.argv[2], "w") as out_file:
    for s in sequences:
        name = s[0]
        seq = s[1]
        out_file.write(">" + name + "\n")
        while len(seq) > 0:
            out_file.write(seq[0:nb_char] + "\n")
            seq = seq[nb_char:]

