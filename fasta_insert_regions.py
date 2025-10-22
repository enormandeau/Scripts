#!/usr/bin/env python3
"""Insert regions into sequences at specific positions

Usage:
    <program> input_fasta regions_fasta regions_info output_fasta [number_Ns]

Where the regions_info file contains 3 columns:
    - Name of sequence to be inserted
    - Name of the sequence where to insert it
    - Position

Where number_Ns (optional) is the number of Ns to insert in place of the region
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
    regions_fasta = sys.argv[2]
    regions_info = sys.argv[3]
    output_fasta = sys.argv[4]
except:
    print(__doc__)
    sys.exit(1)

try:
    number_Ns = int(sys.argv[5])
except:
    number_Ns = 0

# Read region sequences
regions_sequences = {x.name: x.sequence for x in fasta_iterator(regions_fasta)}

# Read insertion_info
regions = [x.strip().split("\t") for x in open(regions_info).read().strip().split("\n")]
regions_info_dict = defaultdict(list)

for r in regions:
    regions_info_dict[r[1]].append((int(r[2]), r[0]))

# Load sequences
sequences = fasta_iterator(input_fasta)

with myopen(output_fasta, "wt") as outfile:
    for s in sequences:

        if s.name in regions_info_dict:
            print(s.name, len(s.sequence), "-> The following regions will be inserted")

            for r in sorted(regions_info_dict[s.name], reverse=True):

                if r[0] > len(s.sequence):
                    print(f"  >> WARNING region {r[1]} not inserted - Position outside sequence")

                else:
                    print(f"  {r[1]}, pos: {r[0]}")

                    # Insert region
                    region_seq = regions_sequences[r[1]]

                    s.sequence = "".join([
                        s.sequence[: r[0]],
                        number_Ns * "N",
                        region_seq,
                        number_Ns * "N",
                        s.sequence[r[0]: ]
                        ])

        #else:
        #    print(s.name, len(s.sequence), "-> Nothing to do")

        s.write_to_file(outfile)
