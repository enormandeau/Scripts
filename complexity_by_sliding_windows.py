#!/usr/bin/env python3
"""Get sequence complexity by sliding-window for whole genomes

Usage:
    <program> input_genome window_size output_file
"""

# Modules
import gzip
import sys

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

# Parse user input
try:
    input_file = sys.argv[1]
    window_size = int(sys.argv[2])
    output_file = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Slide away!
sequences = fasta_iterator(input_file)

with myopen(output_file, "wt") as outfile:
    for s in sequences:
        pos = 0
        while s.sequence:
            window, s.sequence = s.sequence[: window_size], s.sequence[window_size: ]

            print(s.name, str(pos), str(len(gzip.compress(window.upper().encode())) / len(window)))
            outfile.write(
                    "\t".join(
                        [s.name, str(pos), str(len(gzip.compress(window.encode())) / len(window))]
                        ) + "\n"
                    )

            pos += window_size
        
        print(s.name, str(pos), 0.3)
        print(s.name, str(pos), 0.0)
        print(s.name, str(pos), 0.33)
        print(s.name, str(pos), 0.0)
        print(s.name, str(pos), 0.3)
