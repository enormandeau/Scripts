#!/usr/bin/env python3
"""Exract portions of scaffolds from a fasta file

Usage:
    <program> input_fasta input_info output_fasta

Where input_info has 3 tab-separated columns:
    - Scaffold or sequence FULL name line
    - Start position
    - End position
"""

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

# Module
from collections import defaultdict
import gzip
import sys

# Parse user input
try:
    input_fasta = sys.argv[1]
    input_info = sys.argv[2]
    output_fasta = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Parse info file
wanted = defaultdict(list)

with myopen(input_info) as infile:
    for line in infile:
        name, start, end = line.strip().split()

        wanted[name].append(
                (int(start), int(end))
                )

# Read fasta file and extract needed regions
sequences = fasta_iterator(input_fasta)

with myopen(output_fasta, "wt") as outfile:
    for s in sequences:
        if s.name in wanted:
            print(s.name)

            for region in wanted[s.name]:
                start, end = region
                region_name = s.name + "_" + str(start) + "-" + str(end)
                region_seq = s.sequence[start: end]
                fasta = Fasta(region_name, region_seq)
                fasta.write_to_file(outfile)
