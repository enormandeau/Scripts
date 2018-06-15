#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract fasta sequences that are below a maximal length.

Usage:
    %program <input_file> <max_length> <output_file>"""

import gzip
import sys
import re

class Fasta(object):
    """Fasta object with name and sequence
    """
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence
    def write_to_file(self, handle):
        handle.write(">" + self.name + "\n")
        handle.write(self.sequence + "\n")

# Functions
def myopen(infile, mode="r"):
    if infile.endswith(".gz"):
        return gzip.open(infile, mode=mode)
    else:
        return open(infile, mode=mode)

def fasta_iterator(input_file):
    """Takes a fasta file input_file and returns a fasta iterator
    """
    with myopen(input_file) as f:
        sequence = ""
        name = ""
        begun = False
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if begun:
                    yield Fasta(name, sequence)
                name = line.replace(">", "")
                sequence = ""
                begun = True
            else:
                sequence += line

        if name != "":
            yield Fasta(name, sequence)

try:
    fasta_file = sys.argv[1]      # Input fasta file
    max_length = int(sys.argv[2]) # Maximum length of sequence
    result_file = sys.argv[3]     # Output fasta file
except:
    print(__doc__)
    sys.exit(0)

fasta_sequences = fasta_iterator(fasta_file)

with myopen(result_file, "w") as outfile:
    for seq in fasta_sequences:
        if len(seq.sequence) <= max_length:
            seq.write_to_file(outfile)

