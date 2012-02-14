#!/usr/bin/env python
import sys
from Bio import SeqIO
infile = sys.argv[1]
outfile = sys.argv[2]
SeqIO.write(SeqIO.parse(open(infile), "fastq"), open(outfile, "w"), "fasta")
