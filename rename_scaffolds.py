#!/usr/bin/env python3
"""Rename scaffolds using a correspondence file

Rename chromosomes to wanted names and then automatically rename shorter
contigs numerically by decreasing size.

Usage:
    <program> input_fasta correspondence min_length output_fasta

The correspondence file has two tab-separated columns with the prsent name on
the left and the wanted name on the right.

Scaffolds below min_length will be removed
"""

# Modules
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

# Parsing user input
try:
    input_fasta = sys.argv[1]
    correspondence = sys.argv[2]
    min_length = int(sys.argv[3])
    output_fasta = sys.argv[4]
except:
    print(__doc__)
    sys.exit(1)

# Read renaming info
corr = dict()
with open(correspondence) as corr_file:
    for line in corr_file:
        _from, _to = line.strip().split()
        if _to.startswith("Un"):
            _to = f"Un{int(_to[2:]):04d}"
        corr[_from] = _to

# Rename sequences (keep in memory)
sequences = fasta_iterator(input_fasta)
chroms = []
others = []

for s in sequences:

    if s.name in corr:
        new_name = corr[s.name]
        s.name = new_name
        chroms.append((new_name, s))

    else:
        others.append((len(s.sequence), s))

# Write sequences to file
scaff_num = 1
with myopen(output_fasta, "wt") as outfile:

    # Sort LGs by name
    for s in sorted(chroms):

        # Stop if scaffold is too short
        if len(s[1].sequence) < min_length:
            continue

        s[1].write_to_file(outfile)

    # Sort other contigs/scaffols per length
    for s in sorted(others, reverse=True, key=lambda x: x[0]):

        seq = s[1]

        # Stop if scaffold is too short
        if len(seq.sequence) < min_length:
            break

        seq.name = "scaf" + str(scaff_num).zfill(4)
        scaff_num += 1
        seq.write_to_file(outfile)
