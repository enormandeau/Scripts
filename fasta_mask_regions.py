#!/usr/bin/env python3
"""Mask regions from fasta file given in bedfile

Usage:
    <program> input_fasta input_bed flank_size output_fasta

beddfile format:

sequence_name<TAB>from<TAB>to<NEWLINE>
"""


# Modules
from collections import defaultdict
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

def overlap(r1, r2):
    """Return True if ranges overlap, even by only one position
    """
    return (r1[0] <= r2[1]) and (r1[1] >= r2[0])

# Parsing user input
try:
    input_fasta = sys.argv[1]
    input_bed = sys.argv[2]
    flank_size = int(sys.argv[3])
    output_fasta = sys.argv[4]
except:
    print(__doc__)
    sys.exit(1)

# Get regions
regions = defaultdict(set)
count = 0

with open(input_bed) as infile:
    for line in infile:
        count += 1
        l = line.strip().split("\t")
        chrom = l[0]
        start = int(l[1])
        stop = int(l[2])

        regions[chrom].update(range(start-flank_size, stop+flank_size+1))

# Read, mask, write fasta sequences
sequences = fasta_iterator(input_fasta)

with open(output_fasta, "wt") as outfile:
    for s in sequences:
        print(s, s.name in regions)
        print(f"masking {len(regions[s.name])} positions")
        seq = list(s.sequence)

        for p in regions[s.name]:
            seq[p] = "N"

        s.sequence = "".join(seq)

        s.write_to_file(outfile)
