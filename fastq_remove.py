#!/usr/bin/env python3
"""Remove unwanted sequences from a Fastq file

Usage:
    python fastq_remove.py  input_file  unwanted_file  output_file

input_file = input Fastq file
unwanted_file = file containing one unwanted sequence ID per line
output_file = output Fastq file
"""

# Modules
import gzip
import sys

# Defining classes
class Fastq(object):
    """Fastq object with name and sequence
    """

    def __init__(self, name, seq, name2, qual):
        self.name = name[1:]
        self.seq = seq
        self.name2 = name2
        self.qual = qual

    def getShortname(self, separator):
        self.temp = self.name.split(separator)
        del(self.temp[-1])
        return separator.join(self.temp)

    def write_fastq(self, handle):
        handle.write(">" + self.name + "\n")
        handle.write(self.seq + "\n")

# Defining functions
def myopen(infile, mode="rt"):
    if infile.endswith(".gz"):
        return gzip.open(infile, mode=mode)
    else:
        return open(infile, mode=mode)

def fastq_parser(infile):
    """Takes a fastq file infile and returns a fastq object iterator
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

try:
    fasta_file = sys.argv[1]  # Input fasta file
    unwanted_file = sys.argv[2] # Input wanted file, one gene name per line
    result_file = sys.argv[3] # Output fasta file
except:
    print(__doc__)
    sys.exit(0)

unwanted = set()
with open(unwanted_file) as f:
    for line in f:
        line = line.strip()
        if line != "":
            unwanted.add(line)

if not unwanted:
    sys.exit()

fastq_sequences = fastq_parser(fasta_file)

with open(result_file, "wt") as f:
    for seq in fastq_sequences:
        name = seq.name.split(" ")[0]
        if name not in unwanted and len(seq.seq) > 0:
            seq.write_fastq(f)
