#!/usr/bin/env python
"""Keep only sequences that reach a minimal length threshold in a fastq.gz file

Usage:
    python fastq_min_length.py  input_file  length_threshold  output_file

input_file = input compressed Fastq file
length_threshold = minimal acceptable length (positive integer)
output_file = output Fastq file
"""

# Importing modules
import gzip
import sys

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
def fastq_parser(input_file):
    """Takes a fastq file infile and returns a fastq object iterator
    """
    with gzip.open(input_file, "rt") as f:
        while True:
            name = f.readline().strip()[1:]
            if not name:
                break
            seq = f.readline().strip()
            name2 = f.readline().strip()[1:]
            qual = f.readline().strip()
            yield Fastq(name, seq, name2, qual)

# Main
if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
        length_threshold = int(sys.argv[2])
        output_file = sys.argv[3]
    except:
        print(__doc__)
        exit(1)

    assert length_threshold >= 1, "length threshold must be a positive integer"

    # Filter sequences
    sequences = fastq_parser(input_file)
    with gzip.open(output_file, "wt") as out_f:
        for s in sequences:
            if len(s.seq) >= length_threshold:
                s.write_to_file(out_f)

