#!/usr/bin/env python3
"""Remove specific regions from sequences in a fasta file

Usage:
    <program> input_fasta regions_file output_fasta [n_size]

Where the regions_file contains 3 columns:
    - Name of the sequence
    - Start of region
    - End of region

Where n_size (optional) is the number of Ns to insert in place of the region
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

# Parse user input
try:
    input_fasta = sys.argv[1]
    regions_file = sys.argv[2]
    output_fasta = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

try:
    n_size = int(sys.argv[4])
except:
    n_size = 0

# Read regions
regions = [x.strip().split("\t") for x in open(regions_file).read().strip().split("\n")]

regions_dict = defaultdict(list)

for r in regions:
    regions_dict[r[0]].append((int(r[1]), int(r[2])))

# Load sequences
sequences = fasta_iterator(input_fasta)

with myopen(output_fasta, "wt") as outfile:
    for s in sequences:
        print(s.name, len(s.sequence), end=": ")

        if s.name in regions_dict:
            print("yes", s.name, regions_dict[s.name])

            for r in sorted(regions_dict[s.name], reverse=True):
                print("", r)

                # Avoid adding Ns at ends of sequences
                if r[1] >= len(s.sequence) or r[0] == 0:
                    n = 0
                else:
                    n = n_size

                # Remove region
                s.sequence = s.sequence[:r[0]] + n * "N" + s.sequence[r[1]: ]

        s.write_to_file(outfile)
