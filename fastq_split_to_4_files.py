#!/usr/bin/env python3
"""Split fastq(.gz) file into 4 files for further compression

Usage:
    <program> input_fastq_file
"""

# Modules
import gzip
import sys

# Classes
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
        handle.write(self.name + "\n")
        handle.write(self.sequence + "\n")
        handle.write(self.name2 + "\n")
        handle.write(self.quality + "\n")

    def __repr__(self):
        return self.name + " " + self.sequence[:31]

# Defining functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

def fastq_iterator(infile):
    """Takes a fastq file infile and returns a fastq object iterator

    Requires fastq file with four lines per sequence and no blank lines.
    """
    
    with myopen(infile) as f:
        while True:
            name = f.readline().strip()

            if not name:
                break

            seq = f.readline().strip()
            name2 = f.readline().strip()
            qual = f.readline().strip()
            yield Fastq(name, seq, name2, qual)

# Parse user input
try:
    input_fastq_file = sys.argv[1]
except:
    print(__doc__)
    sys.exit(1)

# Open output file handles
out1 = gzip.open(input_fastq_file + ".1.gz", "wt")
out2 = gzip.open(input_fastq_file + ".2.gz", "wt")
out3 = gzip.open(input_fastq_file + ".3.gz", "wt")
out4 = gzip.open(input_fastq_file + ".4.gz", "wt")

# Read and split file
sequences = fastq_iterator(input_fastq_file)

for s in sequences:
    out1.write(s.name[1:] + "\n")
    out2.write(s.sequence + "\n")
    out3.write(s.name2[1:] + "\n")
    out4.write(s.quality + "\n")

# Close output file handles
out1.close()
out2.close()
out3.close()
out4.close()
