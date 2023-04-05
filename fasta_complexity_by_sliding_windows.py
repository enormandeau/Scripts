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

# Parse user input
try:
    input_file = sys.argv[1]
    window_size = int(sys.argv[2])
    output_file = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Extract complexity by sliding window
tot_pos = 0
sequences = fasta_iterator(input_file)

with myopen(output_file, "wt") as outfile:

    # If scaffold doesn't have at least 2 full windows, skip
    for s in sequences:
        if len(s.sequence) < (2 * window_size):
            continue

        pos = 0
        while len(s.sequence) > (1.5 * window_size):

            # Get next window
            window, s.sequence = s.sequence[: window_size], s.sequence[window_size: ]

            # Write stats to output
            compression_ratio = len(gzip.compress(window.upper().encode())) / len(window)
            line = "\t".join([s.name, str(pos), str(tot_pos), str(round(compression_ratio, 6))])

            outfile.write(line + "\n")
            outfile.flush()

            # Upgrade positions
            pos += window_size
            tot_pos += window_size

            # Report result on stdin
            print(line)
        
        # Delimiter between chromosomes
        # Twix, definition:
        #(a) With ref. to position or location in space: among (several
        #animals); in among (surrounding objects); ~ hondes, in (one's) hands;
        #(b) with ref. to association or relationship: between two
        #(parties); also, among (parties) [quot. a1400, last]; ben born
        tot_pos -= window_size
        outfile.write(f"Twix\t{pos}\t{tot_pos}\t0\n")
        tot_pos += window_size * 5
        outfile.write(f"Twix\t{pos}\t{tot_pos}\t0\n")

        print("#####")
