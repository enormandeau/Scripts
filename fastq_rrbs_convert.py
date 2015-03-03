#!/usr/bin/env python
"""Convert fastq to fasta

Usage:
    python fastq_to_fastq.py inputfile outputfile proportion

Where:
    inputfile is a fastq or fastq.gz file
    outputfile is a fastq or fastq.gz file to output to
    proportion is the proportion of converted Ts
"""

# Modules
import sys
import gzip
import random

from Bio import SeqIO
try:
    infile = sys.argv[1]
    outfile = sys.argv[2]
    proportion = float(sys.argv[3])
except:
    print __doc__
    sys.exit(1)

# Functions
def myopen(infile, mode="r"):
    if infile.endswith(".gz"):
        return gzip.open(infile, mode=mode)
    else:
        return open(infile, mode=mode)

# Main
sequences = (s for s in (SeqIO.parse(myopen(infile), "fastq")))

with myopen(outfile, "w") as outf:
    for s in sequences:
        fastq = s.format("fastq").strip().split("\n")
        converted = list(fastq[1])

        end = len(converted)
        if "".join(converted[-3:]) == "CCG":
            end = len(converted) - 3

        for i in xrange(3, end):
            if converted[i] == "T" and proportion > random.random():
                converted[i] = "C"

        fastq[1] = "".join(converted)

        outf.write("\n".join(fastq) + "\n")

