#!/usr/bin/env python3
"""Strip names and introduce fake quality string [GGGGG...] to improve fastq compressibility

WARNING: DO NOT USE IN PRODUCTION
    Sequence names and qualities are lost or modified in the process. This may
    be fine for some applications but potentially catastrophic for others.

Usage:
    <program> input_fastq output_fastq

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
        return self.name + " " + self.sequence[:31] + " " + self.quality[:31]

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

    def quality_level_encode(qual, num_levels, offset):
        """Recode quality string into num_levels levels
        """
        divisor = int(40 / num_levels)
        new_qual = []
        for q in qual:
            new_qual.append(
                    chr(divisor * int((ord(q) - offset) / divisor) + offset)
                    )
        return("".join(new_qual))
    
    with myopen(infile) as f:
        while True:
            name = f.readline().strip()

            if not name:
                break

            sequence = f.readline().strip()
            name2 = f.readline().strip()
            quality = quality_level_encode(f.readline().strip(), num_levels=8, offset=33)
            yield Fastq("@", sequence, "+", quality)

# Parse user input
try:
    input_fastq = sys.argv[1]
    output_fastq = sys.argv[2]
except:
    print(__doc__)
    sys.exit()

# Treat sequences
sequences = fastq_iterator(input_fastq)

with myopen(output_fastq, "wt") as outfile:
    for s in sequences:
        s.write_to_file(outfile)
