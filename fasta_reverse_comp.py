#!/usr/bin/env python

"""Extract all lines of a file found between a 'start' and a 'stop' markers.

Usage:
    %program <input_file> <start_marker> <stop_marker> <output_file>"""

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

def complement(seq):
    """Return the complement of a sequence, *NOT* it's reverse complement"""
    if not seq.isalpha():
        print "The sequence contained non-alphabetic characters"
        print seq
    if not seq.isupper():
        print "The sequence contained non capital-letter characters"
        #seq = seq.upper()
    seq = seq.replace("A","1").replace("T","2").replace("C","3").replace("G","4")
    seq = seq.replace("a","5").replace("t","6").replace("c","7").replace("t","8")
    seq = seq.replace("1","T").replace("2","A").replace("3","G").replace("4","C")
    seq = seq.replace("5","t").replace("6","a").replace("7","g").replace("8","c")
    return seq

def reverse_complement(seq):
    return complement(seq)[::-1]

sequences = ([seq.id, seq.seq.tostring()] for seq in SeqIO.parse(in_file, 'fasta'))
with open(sys.argv[2], "w") as out_file:
    for seq in sequences:
        out_file.write(">" + seq[0] + "\n" + reverse_complement(seq[1]) + "\n")

