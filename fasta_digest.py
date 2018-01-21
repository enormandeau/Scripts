#!/usr/bin/env python

"""Digest sequences from a fasta file in sequences of a specified length.

Usage:
    %program <input_file> <fragment_length> <move> <output_file>

input_file: a fasta file
fragment_length: length of digested fragments
move: number of non-overlapping nucleotides between two consecutive fragments"""


import sys

try:
    from Bio import SeqIO
except:
    print("This program requires the Biopython library")
    sys.exit(0)

try:
    in_file = open(sys.argv[1], "rU")
    nb_nuc = int(sys.argv[2])
    move = int(sys.argv[3])
    out_file = sys.argv[4]
except:
    print(__doc__)
    sys.exit(0)

sequences = ([seq.id, seq.seq.tostring()] 
             for seq in SeqIO.parse(in_file, 'fasta'))

def digest(seq, nb_nuc):
    fragments = []
    n = seq[0]
    n_counter = 0
    s = seq[1]
    start = nb_nuc/2
    while len(s) > nb_nuc/2:
        frag = s[:nb_nuc - start]
        start -= move
        if start < 0:
            start = 0
            s = s[move:]
        n_counter +=1
        fragments.append([n + "_" + str("%06i" % n_counter), frag])
    return fragments

with open(out_file, "w") as out_file:
    for seq in sequences:
        fragments = digest(seq, nb_nuc)
        for frag in fragments:
            out_file.write(">" + frag[0] + "\n" + frag[1] + "\n")

