#!/usr/bin/env python3

"""Extract sequences from a fastq file if their name is in a 'unwanted' file.

Unwanted file contains one sequence name per line.

Usage:
    %program <input_file> <unwanted_file> <output_file>"""

# Modules
import gzip
import sys

# Defining classes
class Fastq(object):
    """Fastq object with name, sequence, name2, and quality string
    """

    def __init__(self, name, sequence, name2, quality):
        self.name = name
        self.sequence = sequence
        self.name2 = name2
        self.quality = quality

    def getShortname(self, separator):
        if separator:
            self.temp = self.name.split(separator)
            del(self.temp[-1])
            return separator.join(self.temp)

        else:
            return self.name

    def write_to_file(self, handle):
        handle.write("@" + self.name + "\n")
        handle.write(self.sequence + "\n")
        handle.write("+" + self.name2 + "\n")
        handle.write(self.quality + "\n")

    def __repr__(self):
        return self.name + " " + self.sequence[:31]

# Defining functions
def myopen(infile, mode="rt"):
    if infile.endswith(".gz"):
        return gzip.open(infile, mode=mode)
    else:
        return open(infile, mode=mode)

def fastq_iterator(infile):
    """Takes a fastq file infile and returns a fastq object iterator

    Requires fastq file with four lines per sequence and no blank lines.
    """
    
    with myopen(infile) as f:
        while True:
            name = f.readline().strip()[1:]

            if not name:
                break

            seq = f.readline().strip()
            name2 = f.readline().strip()[1:]
            qual = f.readline().strip()
            yield Fastq(name, seq, name2, qual)

# Parse user input
try:
    fasta_file = sys.argv[1]  # Input fasta file
    unwanted_file = sys.argv[2] # Input unwanted file, one gene name per line
    result_file = sys.argv[3] # Output fasta file
except:
    print(__doc__)
    sys.exit(0)

unwanted = set()
with open(unwanted_file) as f:
    for line in f:
        line = line.strip().split("\t")[0]
        if line != "":
            unwanted.add(line)

if not unwanted:
    sys.exit()

fastq_sequences = fastq_iterator(fasta_file)

with myopen(result_file, "wt") as f:
    for seq in fastq_sequences:
        name = seq.name.split(" ")[0]

        if name not in unwanted and len(seq.sequence) > 0:
            seq.write_to_file(f)
