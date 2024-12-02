#!/usr/bin/env python3
"""Get average sequence complexity by sequence, normalized by 50 bp windows

Sequence complexity is measured as the ratio of the length of a gzip-compressed
50 bp sequence over its non-compressed length. Reported values range between 0
(infinite compression) to 1 (maximum sequence entropy). Lower values thus
represent sequences with lower complexity.

Usage:
    <program> input_file

Where:
    input_file is a fasta or fasta.gz file
"""

# Modules
from random import choice
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

                name = line[1:].split(" ")[0]
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

def compression_ratio(seq, minimum_ratio=0.0, maximum_ratio=1.0):
    ratio = len(gzip.compress(seq.upper().encode())) / len(seq)
    return (ratio - minimum_ratio) / (maximum_ratio - minimum_ratio)

# Parse user input
try:
    input_file = sys.argv[1]
except:
    print(__doc__)
    sys.exit(1)

# Normalize complexity values by maximum for window size
# Generate 20 random sequences of window_size and find maximum_ratio
window_size = 50
#print(f"Calibrating maximum entropy for windows of {window_size}bp")
minimum_ratio = compression_ratio("".join("A" * window_size))
maximum_ratio = 0.0

for i in range(50):
    random_sequence = "".join(choice("ACGT") for _ in range(window_size))
    ratio = compression_ratio(random_sequence)
    #print(ratio, end=" ", flush=True)
    maximum_ratio = max(ratio, maximum_ratio)

# Extract complexity by sliding window
tot_pos = 0
sequences = fasta_iterator(input_file)

for s in sequences:
    seq = s.sequence
    complexities = []
    pos = 0

    while len(s.sequence) > (1.0 * window_size):

        # Get next window
        window, s.sequence = s.sequence[: window_size], s.sequence[window_size: ]

        # Compute compression ratio
        comp = compression_ratio(window, minimum_ratio, maximum_ratio)
        complexities.append(comp)

        # Upgrade positions
        pos += window_size
        tot_pos += window_size

    # Report stats for sequence
    avg_comp = sum(complexities) / len(complexities)
    line = "\t".join([s.name, str(round(avg_comp, 6)), seq])
    print(line)
