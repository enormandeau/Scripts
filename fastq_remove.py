#!/usr/bin/env python
"""Remove unwanted sequences from a Fastq file

Usage:
    python fastq_remove.py  input_file  unwanted_file  output_file

input_file = input Fastq file
unwanted_file = file containing one unwanted sequence ID per line
output_file = output Fastq file
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
        unwanted_file = sys.argv[2]
        output_file = sys.argv[3]
    except:
        print __doc__
        exit(1)

    # Build unwanted set
    unwanted = set()
    with open(unwanted_file) as f:
        for line in f:
            l = line.strip()
            if l != "":
                unwanted.add(l)

    # Filter sequences
    sequences = fastq_parser(input_file)
    with open(output_file, "w") as out_f:
        for s in sequences:
            if s.name not in unwanted and s.name.split(" ")[0] not in unwanted:
                s.write_to_file(out_f)

