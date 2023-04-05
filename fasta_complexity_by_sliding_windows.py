#!/usr/bin/env python3
"""Get sequence complexity by sliding-window for whole genomes

Sequence complexity is measured as the ratio of the length of a gzip-compressed
sequence of window_size over its non-compressed length. Reported values range
between 0 (infinite compression) to 1 (maximum sequence entropy). Lower values
thus represent regions of low complexity.

Results are written to the output_file and a different version is also printed
on screen. Namely, the delimitations between chromosomes or scaffolds are
reported with "#####" on the screen but with lines starting by "Twix" in the
output_file.

Usage:
    <program> input_genome window_size min_scaf_size output_file

Where:
    input_genome is a fasta or fasta.gz file with chromosomes or scaffolds
    window_size is the size of the windows to evaluate complexity in
    min_scaf_size is the minimum size of scaffold to be considered
    output_file is the name of a file for the tabulation-separated output
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

def compression_ratio(seq, maximum_ratio=1.0):
    return len(gzip.compress(seq.upper().encode())) / (len(seq) * maximum_ratio)

# Parse user input
try:
    input_file = sys.argv[1]
    window_size = int(sys.argv[2])
    min_scaf_size = int(sys.argv[3])
    output_file = sys.argv[4]
except:
    print(__doc__)
    sys.exit(1)

# Normalize output by maximum
# Generate 20 random sequences of window_size and find maximum_ratio
print(f"Calibrating maximum entropy for windows of {window_size}bp")
maximum_ratio = 0.0

for i in range(20):
    random_sequence = "".join(choice("ACGT") for _ in range(window_size))
    ratio = compression_ratio(random_sequence)
    print(ratio, end=" ", flush=True)
    maximum_ratio = max(ratio, maximum_ratio)

print()

# Extract complexity by sliding window
tot_pos = 0
sequences = fasta_iterator(input_file)

with myopen(output_file, "wt") as outfile:

    # If scaffold doesn't have at least 2 full windows, skip
    for s in sequences:
        if len(s.sequence) < (2 * window_size) or len(s.sequence) < min_scaf_size:
            continue

        pos = 0
        while len(s.sequence) > (1.5 * window_size):

            # Get next window
            window, s.sequence = s.sequence[: window_size], s.sequence[window_size: ]

            # Write stats to output
            line = "\t".join([s.name, str(pos), str(tot_pos),
                str(round(compression_ratio(window, maximum_ratio), 6))])

            outfile.write(line + "\n")
            outfile.flush()

            # Upgrade positions
            pos += window_size
            tot_pos += window_size

            # Report result on stdin
            print(line)
        
        # Delimiter between chromosomes
        # Twix, definition:
        #     (a) With ref. to position or location in space: among (several
        #         animals); in among (surrounding objects); ~ hondes, in (one's) hands;
        #     (b) with ref. to association or relationship: between two
        #         (parties); also, among (parties) [quot. a1400, last];
        tot_pos -= window_size
        outfile.write(f"Twix\t{pos}\t{tot_pos}\t0\n")
        tot_pos += window_size * 5
        outfile.write(f"Twix\t{pos}\t{tot_pos}\t0\n")

        print("#####")
