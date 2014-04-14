#!/usr/bin/env python

"""Convert a FASTA and a QUAL file from Roche 454 sequencing in a FASTQ file.

Usage:
    %program <input_file> <start_marker> <stop_marker> <output_file>"""

import sys
import re

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)

try:
    quality_file = sys.argv[1] # 454 output quality file <filename>.qual
    fasta_file = sys.argv[2]   # 454 output fasta file : <filename>.fna
    output_file = sys.argv[3]  # Out-put file with FASTQ format
except:
    print __doc__
    sys.exit(0)

reads = SeqIO.to_dict(SeqIO.parse(open(fasta_file), "fasta"))

with open(output_file, "w") as f:
    for rec in SeqIO.parse(open(quality_file), "qual"):
        reads[rec.id].letter_annotations["phred_quality"] = \
            rec.letter_annotations["phred_quality"]
        f.write(reads[rec.id].format("fastq"))

