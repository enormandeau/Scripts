#!/usr/bin/env python3
"""Create a simple AGP file from a fasta file for chromonomer

Usage:
    <program> input_fasta output_agp
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

# user input
try:
    input_fasta = sys.argv[1]
    output_agp = sys.argv[2]
except:
    print(__doc__)
    sys.exit(1)

# Treat fasta
sequences = fasta_iterator(input_fasta)

with myopen(output_agp, "wt") as outfile:
    n = 1
    for s in sequences:
        line = [
                s.name,
                "1",
                str(len(s.sequence)),
                "1",
                "W",
                str(n),
                "1",
                str(len(s.sequence)),
                "+"
                ]
        line = "\t".join(line) + "\n"
        outfile.write(line)

        n += 1
