#!/usr/bin/env python2
"""Split a fastq file in n files of approximately the same number of sequences

Usage:
    python fastq_remove.py  input_file  num_seq_per_file

input_file = input Fastq file
num_seq_per_file = number of sequences to put in each output files
"""

# Importing modules
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
    with open(input_file) as f:
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
        num_seq_per_file = int(sys.argv[2])
    except:
        print __doc__
        exit(1)

    # Test input parameters
    assert num_seq_per_file >= 1, "num_seq_per_file must be a non-zero positive integer"

    # Write sequences to ouptut files
    sequences = fastq_parser(input_file)
    output_file_number = 1
    seq_num = 0
    output_file_name = input_file + "_split_" + str(output_file_number)
    # TODO open first file
    output_file = open(output_file_name, "w")

    for s in sequences:
        seq_num += 1
        if seq_num > num_seq_per_file:
            output_file_number += 1 
            seq_num = 1
            output_file.close()
            output_file_name = input_file + "_split_" + str(output_file_number)
            output_file = open(output_file_name, "w")
        s.write_to_file(output_file)
