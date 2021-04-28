#!/usr/bin/env python
"""Calculate N50 from an assembled genome fasta file

Usage:
    python fasta_n50.py genome_file [min_length]
"""

# Importing modules
from signal import signal, SIGPIPE, SIG_DFL
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

# Defining functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

def fasta_iterator(genome_file):
    """Takes a fasta file genome_file and returns a fasta iterator
    """
    with myopen(genome_file) as f:
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

if __name__ == '__main__':
    # Prevent broken pipe error
    signal(SIGPIPE, SIG_DFL)

    # Parse user input
    try:
        genome_file = sys.argv[1]
    except:
        print(__doc__)
        sys.exit(1)

    try:
        min_length = int(sys.argv[2])
    except:
        min_length = 1

    # Cound kmers
    sequence_lengths = []
    num_seq = 0

    for seq in fasta_iterator(genome_file):
        length = len(seq.sequence)
        if length >= min_length:
            num_seq += 1
            sequence_lengths.append(len(seq.sequence))

    sequence_lengths = sorted(sequence_lengths, reverse=True)
    total_length = sum(sequence_lengths)
    half_length = float(total_length) / 2.0

    print(genome_file)
    print("  " + str(total_length) + " bp in " + str(num_seq) +
            " sequences of " + str(min_length) + "+ bp")

    cumulative_length = 0
    cumulative_seq = 0
    nstats = []

    for percent in range(10, 91, 10):
        nstats.append((percent, int(percent * float(total_length) / 100)))

    for seq_len in sequence_lengths:
        cumulative_length += seq_len
        cumulative_seq += 1

        while cumulative_length >= nstats[0][1]:
            print("  L" + str(nstats[0]) +": " + str(cumulative_seq) +
                    ";\tN" + str(nstats[0]) + ": " + str(seq_len))
            nstats.pop(0)
            if not nstats:
                sys.exit(0)
