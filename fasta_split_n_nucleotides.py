#!/usr/bin/env python
"""Split a fasta file into chuncks of at least n nucleotides

Usage:
    python fasta_split_n_nucleotides.py input_file n output_stub

input_file = fasta file to split (string)
n = minimal number of nucleotides in each split files (integer > 0)
output_stub = name stub for ouptut files (string, defaults to input_file)
"""

# Importing modules
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

# Defining functions
def fasta_iterator(input_file):
    """Takes a fasta file input_file and returns a fasta iterator
    """
    with open(input_file) as f:
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

# Main
if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
        n = int(sys.argv[2])
    except:
        print __doc__
        sys.exit(1)

    try:
        output_stub = sys.argv[3]
    except:
        output_stub = input_file

    sequences = fasta_iterator(input_file)

    output_number = 1
    output_file = output_stub + "_{:06n}".format(output_number)
    outf = open(output_file, "w")

    nucleotide_count = 0
    for s in sequences:
        if nucleotide_count > n:
            outf.close()
            nucleotide_count = 0
            output_number += 1
            output_file = output_stub + "_{:06n}".format(output_number)
            outf = open(output_file, "w")

        nucleotide_count += len(s.sequence)
        outf.write(">" + s.name + "\n" + s.sequence + "\n")

