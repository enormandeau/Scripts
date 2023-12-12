#!/usr/bin/env python3
"""Split sequences in fasta file in shorter overlapping sequences

Usage:
    <program> input_fasta max_len overlap output_fasta
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

# Functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

def fasta_iterator(input_file):
    """Takes a fasta file input_file and returns a fasta iterator
    """
    with myopen(input_file) as f:
        sequence = []
        name = ""
        begun = False

        for line in f:
            line = line.strip()

            if line.startswith(">"):
                if begun:
                    yield Fasta(name, "".join(sequence))

                name = line[1:]
                sequence = ""
                begun = True

            else:
                sequence += line

        if name != "":
            yield Fasta(name, "".join(sequence))

# Parsing user input
try:
    input_fasta = sys.argv[1]
    max_len = int(sys.argv[2])
    overlap = int(sys.argv[3])
    output_fasta = sys.argv[4]
except:
    print(__doc__)
    sys.exit(1)

# Fasta iterator
sequences = fasta_iterator(input_fasta)

# Split
with myopen(output_fasta, "wt") as outfile:
    for s in sequences:
        chunk = 0
        while s.sequence:
            pos = chunk * overlap
            chunk += 1

            name = s.name + "_chunk" + str(chunk) + "_pos" + str(pos)
            seq = s.sequence[: max_len]
            s.sequence = s.sequence[overlap: ]

            outfile.write(">" + name + "\n" + seq + "\n")
