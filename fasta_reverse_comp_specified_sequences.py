#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Reverse complement sequences from a fasta file if their name is in a 'reverse_file' file

reverse_file contains one sequence name per line

Usage:
    %program <input_file> <reverse_file> <output_file>"""

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

def reverse(s):
    s.sequence = s.sequence[::-1]

def complement(s):
    """Return the complement of a sequence, *NOT* it's reverse complement
    """

    if not s.sequence.isalpha():
        print("The sequence contained non-alphabetic characters")

    s.sequence = s.sequence.replace("A","1").replace("T","2").replace("C","3").replace("G","4")
    s.sequence = s.sequence.replace("a","5").replace("t","6").replace("c","7").replace("t","8")
    s.sequence = s.sequence.replace("1","T").replace("2","A").replace("3","G").replace("4","C")
    s.sequence = s.sequence.replace("5","t").replace("6","a").replace("7","g").replace("8","c")

# Parsing user input
try:
    fasta_file = sys.argv[1]  # Input fasta file
    reverse_file = sys.argv[2]  # Input reverse_file, one sequence name per line
    result_file = sys.argv[3] # Output fasta file
except:
    print(__doc__)
    sys.exit(0)

to_reverse = set()
with open(reverse_file) as f:
    for line in f:
        line = line.strip()
        if line != "":
            to_reverse.add(line)

# Iterate through sequences and write to files
fasta_sequences = fasta_iterator(fasta_file)

with myopen(result_file, "wt") as outfile:
    for seq in fasta_sequences:
        name = seq.name
        print(seq)

        if name.split(" ")[0] in to_reverse:
            print("reversed")
            reverse(seq)
            complement(seq)
            seq.write_to_file(outfile)

        else:
            seq.write_to_file(outfile)
