#!/usr/bin/env python
"""Keep only sequences that reach a minimal length and trim the other to that
length in a fastq.gz file

Usage:
    python fastq_trim.py  input_file  min_length  max_length  output_file

input_file = input compressed Fastq file
min_length = minimal acceptable length (positive integer)
max_length = maximal acceptable length (positive integer)
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
    with gzip.open(input_file, "rb") as f:
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
        min_length = int(sys.argv[2])
        max_length = int(sys.argv[3])
        output_file = sys.argv[4]
    except:
        print __doc__
        exit(1)

    assert min_length >= 1, "length threshold must be a positive integer"

    # Filter sequences
    sequences = fastq_parser(input_file)
    with gzip.open(output_file, "wb") as out_f:
        for s in sequences:
            if len(s.seq) >= min_length:
                s.seq = s.seq[0:max_length]
                s.qual = s.qual[0:max_length]
                s.write_to_file(out_f)

