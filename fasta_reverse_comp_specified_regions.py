#!/usr/bin/env python3
"""Invert specified regions of sequences in a fasta file

Usage:
    <program> input_fasta regions_info output_fasta

Where the regions_info file contains 3 columns:
    - Name of sequence in which a region must be inverted
    - Start position
    - Stop position 
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

def reverse(s):
    return(s[::-1])

def complement(s):
    """Return the complement of a sequence, *NOT* it's reverse complement
    """

    if not s.isalpha():
        print("The sequence contained non-alphabetic characters")

    s = s.replace("A","1").replace("T","2").replace("C","3").replace("G","4")
    s = s.replace("a","5").replace("t","6").replace("c","7").replace("t","8")
    s = s.replace("1","T").replace("2","A").replace("3","G").replace("4","C")
    s = s.replace("5","t").replace("6","a").replace("7","g").replace("8","c")

    return(s)

def revcomp(s):
    return(reverse(complement(s)))

# Parse user input
try:
    input_fasta = sys.argv[1]
    regions_info = sys.argv[2]
    output_fasta = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Read invertion_info
regions = [x.strip().split("\t") for x in open(regions_info).read().strip().split("\n")]
regions_info_dict = defaultdict(list)

for r in regions:
    regions_info_dict[r[0]].append((int(r[1]), int(r[2])))

# Load sequences
sequences = fasta_iterator(input_fasta)

with myopen(output_fasta, "wt") as outfile:
    for s in sequences:

        if s.name in regions_info_dict:
            print(s.name, len(s.sequence), "-> The following regions will be inverted")

            for r in sorted(regions_info_dict[s.name], reverse=True):

                if r[0] > len(s.sequence) or r[1] > len(s.sequence):
                    print(f"  >> WARNING region {(r[0], r[1])} outside sequence")

                else:
                    print(f"  region {(r[0], r[1])}")

                    # Invert region
                    region_seq = s.sequence[r[0]: r[1]]

                    s.sequence = "".join([
                        s.sequence[: r[0]],
                        revcomp(region_seq).lower(),
                        s.sequence[r[1]: ]
                        ])

        else:
            print(s.name, "-> Nothing to do")

        s.write_to_file(outfile)
