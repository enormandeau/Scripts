#!/usr/bin/env python
"""Convert fastq to fasta

Usage:
    python fastq_to_fastq.py inputFile outputFile
"""

import sys
from Bio import SeqIO
try:
    infile = sys.argv[1]
    outfile = sys.argv[2]
except:
    print __doc__
    sys.exit(1)

SeqIO.write(SeqIO.parse(open(infile), "fastq"), open(outfile, "w"), "fasta")
