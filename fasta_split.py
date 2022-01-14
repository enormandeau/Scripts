#!/usr/bin/env python2
"""Split a fasta file in n files of approximately the same number of sequences

WARNING: This will create 'n' files in your present directory

USAGE:
    python fasta_split.py input_file num_files

input_file: fasta file
num_files: number of files to split into
"""

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

# parse user input
try:
    input_file = sys.argv[1]
    num_files = int(sys.argv[2])
except:
    print(__doc__)
    sys.exit(1)

# Iterate through sequences and write to files
file_number = 0
for sequence in fasta_iterator(input_file):
    n = file_number % num_files + 1
    print(n)
    current_file = input_file + str(n) + ".fasta"
    with open(current_file, "a") as f:
        sequence.write_to_file(f)
    file_number += 1
