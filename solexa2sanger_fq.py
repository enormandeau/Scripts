import sys
from Bio import SeqIO
SeqIO.convert(sys.stdin, "fastq-solexa", sys.stdout, "fastq")
