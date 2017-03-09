#!/usr/bin/env python
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

# Defining functions
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
        yield Fasta(name, sequence)

# Parsing user input
try:
    fasta_file = sys.argv[1]  # Input fasta file
    remove_file = sys.argv[2] # Input remove file, one gene name per line
    result_file = sys.argv[3] # Output fasta file
except:
    print __doc__
    sys.exit(0)

remove = set()
with open(remove_file) as f:
    for line in f:
        line = line.strip()
        if line != "":
            remove.add(line)


# Iterate through sequences and write to files
fasta_sequences = fasta_iterator(fasta_file)

with myopen(result_file, "w") as outf:
    for seq in fasta_sequences:
        name = seq.name
        if name not in remove and len(str(seq.sequence)) > 0:
            seq.write_to_file(outf)
