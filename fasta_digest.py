#!/usr/bin/python

"""Digest sequences from a fasta file in sequences of a specified length.

Usage:
    %program <input_file> <length> <output_file>"""

import sys

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)

try:
    in_file = open(sys.argv[1], "rU")
    nb_nuc = int(sys.argv[2])
    out_file = sys.argv[3]
except:
    print __doc__
    sys.exit(0)

sequences = ([seq.id, seq.seq.tostring()] 
             for seq in SeqIO.parse(in_file, 'fasta'))

def digest(seq, nb_nuc):
    fragments = []
    n = seq[0]
    n_counter = 0
    s = seq[1]
    while len(s) > nb_nuc/2:
        frag = s[0:nb_nuc]
        s = s[nb_nuc/4:]
        n_counter +=1
        fragments.append([n + "_" + str("%06i" % n_counter), frag])
    return fragments

with open(out_file, "w") as out_file:
    for seq in sequences:
        fragments = digest(seq, nb_nuc)
        for frag in fragments:
            out_file.write(">" + frag[0] + "\n" + frag[1] + "\n")

