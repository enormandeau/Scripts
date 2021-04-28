#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Extract sequences from a fasta file if their name is not in a 'remove' file.

Remove file contains one sequence name per line.

Usage:
    %program <input_file> <remove_file> <output_file>"""

# Importing modules
import gzip
import sys

# Defining classes
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
    fasta_file = sys.argv[1]  # Input fasta file
    remove_file = sys.argv[2] # Input remove file, one gene name per line
    result_file = sys.argv[3] # Output fasta file
except:
    print(__doc__)
    sys.exit(0)

remove = set()
with open(remove_file) as f:
    for line in f:
        line = line.strip()
        if line != "":
            remove.add(line)


# Iterate through sequences and write to files
fasta_sequences = fasta_iterator(fasta_file)

with myopen(result_file, "wt") as outf:
    for seq in fasta_sequences:
        name = seq.name
        if name.split(" ")[0] not in remove and len(str(seq.sequence)) > 0:
            seq.write_to_file(outf)
