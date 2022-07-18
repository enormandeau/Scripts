#!/usr/bin/env python3
"""Extract genomic regions

Usage:
    <program> input_genome wanted_file flanking_size output_fasta

Where:
    wanted_files contains two tab separated columns with scaffold name and position
    (there may be other columns after, as in a bedfile)
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
    flanking_size = int(sys.argv[3])
    output_fasta = sys.argv[4]
except:
    print(__doc__)
    sys.exit(1)

# Create wanted set
wanted_regions = defaultdict(list)

with open(wanted_file) as wfile:
    for line in wfile:
        l = line.strip().split("\t")
        scaffold = l[0]
        position = l[1]
        wanted_regions[scaffold].append(position)

# Extract regions
sequences = fasta_iterator(input_genome)

with open(output_fasta, "w") as outfile:
    for scaffold in sequences:
        scaffold_id = scaffold.name.split()[0]

        if scaffold_id in wanted_regions:
            seq = scaffold.sequence

            for position in wanted_regions[scaffold_id]:
                pos = int(position)
                assert pos <= len(seq), "Errof: SNP outside the scaffold"

                left = pos - flanking_size

                if left < 0:
                    left = 0

                region = Fasta(scaffold_id + "_" + position,
                        seq[pos - flanking_size: pos + flanking_size].upper())

                region.write_to_file(outfile)
