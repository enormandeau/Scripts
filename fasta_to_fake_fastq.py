#!/usr/bin/env python
"""Create a fastq file from a fasta file by adding a fake quality to each
sequence.

Usage:
    ./fasta_to_fake_fastq.py  input.fasta  output.fastq  [quality_symbol]

The quality symbol is optional and defaults to 'I' for compatibility with phred
33 and Illumina phred 33 formats.
"""

# Importing modules
import sys
from Bio import SeqIO

# Main
if __name__ == '__main__':
    # Parsing user input
    try:
        fasta = sys.argv[1]
        fastq = sys.argv[2]
    except:
        print(__doc__)
        sys.exit(1)
    try:
        symbol = sys.argv[3]
    except:
        symbol = 'I'
    
    # Processing fasta file
    with open(fastq, "w") as f:
        for seq in (s for s in SeqIO.parse(open(fasta), 'fasta')):
            f.write("\n".join([
                "@" + seq.name,
                seq.seq.tostring(),
                "+",
                symbol * len(seq.seq.tostring())
            ]) + "\n")

