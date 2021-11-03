#!/usr/bin/env python3

"""Extract sequences from a fastq file if their name is in a 'wanted' file.

Wanted file contains one sequence name per line.

Usage:
    %program <input_file> <wanted_file> <output_file>"""

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
    wanted_file = sys.argv[2] # Input wanted file, one gene name per line
    result_file = sys.argv[3] # Output fasta file
except:
    print(__doc__)
    sys.exit(0)

wanted = set()
with open(wanted_file) as f:
    for line in f:
        line = line.strip()
        if line != "":
            wanted.add(line)

if not wanted:
    sys.exit()

fastq_sequences = fastq_parser(fasta_file)

with open(result_file, "wt") as f:
    for seq in fastq_sequences:
        name = seq.name.split(" ")[0]
        if name in wanted and len(seq.seq) > 0:
            wanted.remove(name) # Output only the first appearance for a name
            seq.write_fastq(f)
