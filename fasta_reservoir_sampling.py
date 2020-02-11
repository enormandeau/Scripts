#!/usr/bin/env python
"""Extract n random sequences from a fasta file.

Usage:
    %program <input_file> n <output_file>"""

# Importing modules
import random
import gzip
import sys
import re

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
                name = line.replace(">", "")
                sequence = ""
                begun = True
            else:
                sequence += line

        if name != "":
            yield Fasta(name, sequence)

# Parsing user input
try:
    fasta_file = sys.argv[1]  # Input fasta file
    number_wanted = int(sys.argv[2]) # Number of sequences wanted
    result_file = sys.argv[3] # Output fasta file
except:
    print(__doc__)
    sys.exit(0)

# Main
if __name__ == '__main__':
    fasta_sequences = fasta_iterator(fasta_file)
    index = 0
    retained = []
    for fasta in fasta_sequences:
        index += 1
        if index <= number_wanted:
            retained.append(fasta)
        else:
            rand = random.randrange(index)
            if rand < number_wanted:
                retained[random.randrange(number_wanted)] = fasta
    
    with myopen(result_file, "wt") as outf:
        for s in retained:
            outf.write(">" + s.name + "\n")
            outf.write(s.sequence + "\n")

