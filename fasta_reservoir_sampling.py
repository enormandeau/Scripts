#!/usr/bin/env python
"""Extract n random sequences from a fasta file.

Usage:
    %program <input_file> n <output_file>"""

# Importing modules
import sys
import re
import random

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)

# Parsing user input
try:
    fasta_file = sys.argv[1]  # Input fasta file
    number_wanted = int(sys.argv[2]) # Number of sequences wanted
    result_file = sys.argv[3] # Output fasta file
except:
    print __doc__
    sys.exit(0)

# Main
if __name__ == '__main__':
    fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')
    index = 0
    retained = []
    for fasta in fasta_sequences:
        index += 1
        if index <= number_wanted:
            retained.append(fasta)
        else:
            rand = random.randrange(index)
            if rand < number_wanted:
                retained[random.randrange(number_wanted)] = fasta
    
    SeqIO.write(retained, open(result_file, "w"), "fasta")

