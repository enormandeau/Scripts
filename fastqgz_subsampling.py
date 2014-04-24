#!/usr/bin/env python
"""Extract n random sequences from a fastq file.

Usage:
    %program input_file proportion output_file

input_file: name of the gzip compressed fastq file to treat
    eg: sequences.fastq.gz
proportion: between 0 and 1, the proportion of reads to randomly keep
output_file: name of the gzip compressed fastq file to output to
"""

# Importing modules
import random
import gzip
import sys
import re

# Defining classes
class Fastq(object):
    """Fastq object with name and sequence
    """
    def __init__(self, name, seq, name2, qual):
        self.name = name
        self.seq = seq
        self.name2 = name2
        self.qual = qual
    def write_to_file(self, handle):
        handle.write("@" + self.name + "\n")
        handle.write(self.seq + "\n")
        handle.write("+" + self.name2 + "\n")
        handle.write(self.qual + "\n")

# Defining functions
def fastq_iterator(input_file):
    """Takes a fastq file infile and returns a fastq object iterator
    """
    with gzip.open(input_file) as f:
        while True:
            name = f.readline().strip()[1:]
            if not name:
                break
            seq = f.readline().strip()
            name2 = f.readline().strip()[1:]
            qual = f.readline().strip()
            yield Fastq(name, seq, name2, qual)

# Parsing user input
try:
    fastq_file = sys.argv[1]  # Input fastq file
    proportion = float(sys.argv[2]) # Number of sequences wanted
    result_file = sys.argv[3] # Output fastq file
except:
    print __doc__
    sys.exit(0)

# Main
if __name__ == '__main__':
    fastq_sequences = fastq_iterator(fastq_file)
    with gzip.open(result_file, "w") as outf:
        for seq in fastq_sequences:
            if random.random() < proportion:
                seq.write_to_file(outf)

