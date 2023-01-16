#!/usr/bin/env python2
"""Wrap fasta sequences to a given length (60 characters by default).

Usage:
    <program> input_file output_file [line_length]
"""

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
try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except:
    print(__doc__)
    sys.exit(0)

try:
    nb_char = int(sys.argv[3])
except:
    print("No line length or bad length specified, using 60 pb per line")
    nb_char = 60

sequences = fasta_iterator(input_file)

with open(sys.argv[2], "w") as out_file:
    for s in sequences:
        pos = 0
        out_file.write(">" + s.name + "\n")

        while pos < len(s.sequence):
            out_file.write(s.sequence[pos: pos+nb_char] + "\n")
            pos += nb_char
