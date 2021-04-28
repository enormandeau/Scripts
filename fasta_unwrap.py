#!/usr/bin/env python3
"""
Unwrap fasta file so that each sequence takes up only one line.

Usage:
    <program> input_file output_file
"""

# Modules
import gzip
import sys

# Classes
class Fasta(object):
    """Fasta object with name and sequence
    """

    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence

    def write_to_file(self, handle):
        handle.write(">" + self.name + "\n")
        handle.write(self.sequence + "\n")

    def __repr__(self):
        return self.name + " " + self.sequence[:31]

# Defining functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

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

                name = line[1:]
                sequence = ""
                begun = True

            else:
                sequence += line

        if name != "":
            yield Fasta(name, sequence)

# Parse user input
try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except:
    print(__doc__)
    sys.exit(0)

# Treat sequences
sequences = fasta_iterator(input_file)

with myopen(sys.argv[2], "wt") as outfile:
    for seq in sequences:
        seq.write_to_file(outfile)
