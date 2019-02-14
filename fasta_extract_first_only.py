#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract sequences from a fasta file if their name is in a 'wanted' file.

Wanted file contains one sequence name per line.

Usage:
    %program <input_file> <wanted_file> <output_file>"""

import gzip
import sys

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
    fasta_file = sys.argv[1]  # Input fasta file
    wanted_file = sys.argv[2] # Input wanted file, one gene name per line
    result_file = sys.argv[3] # Output fasta file
except:
    print(__doc__)
    sys.exit(0)

wanted = set()
with open(wanted_file) as f:
    for line in f:
        line = line.strip()
        if line != "":
            wanted.add(line)

if not wanted:
    sys.exit()

fasta_sequences = fasta_iterator(fasta_file)

with open(result_file, "w") as f:
    for seq in fasta_sequences:
        name = seq.name.split(" ")[0]
        if name in wanted and len(seq.sequence) > 0:
            wanted.remove(name) # Output only the first appearance for a name
            seq.write_to_file(f)
