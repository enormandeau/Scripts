#!/usr/bin/env python3
"""Extract nucleotides at specified positions

Usage:
    <program> input_genome wanted_file output_tsv

Where:
    wanted_files contains two tab separated columns with scaffold name and position
"""

# Modules
from collections import defaultdict
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
        return self.name + " " + self.sequence[0:31]

# Functions
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

def myopen(infile, mode="rt"):
    """Replacement for `open` function to accept gzip files

    Use gzip compression algorithm on files ending with `.gz`

    `myopen` can be used like the `open` function because it has the same
    behaviour. Namely, it returns a file handle (ie: an opened connection
    to a file).
    """

    # If filename ends with .gz, open in gzip mode
    if infile.endswith(".gz"):
        return gzip.open(infile, mode=mode)

    # Else open normally
    else:
        return open(infile, mode=mode)

# Parse user input
try:
    input_genome = sys.argv[1]
    wanted_file = sys.argv[2]
    output_tsv = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Create wanted set
wanted_positions = defaultdict(list)

with open(wanted_file) as wfile:
    for line in wfile:
        l = line.strip().split("\t")
        scaffold = l[0]
        position = l[1]
        wanted_positions[scaffold].append(position)

# Extract regions
sequences = {x.name: x.sequence for x in fasta_iterator(input_genome)}

with open(output_tsv, "wt") as outfile:
    for chrom in wanted_positions:
        for pos in wanted_positions[chrom]:
            outfile.write("\t".join([chrom, pos, sequences[chrom][int(pos)-1]]) + "\n")
