#!/usr/bin/env python
"""Simulate depth of coverage on a per nucleotide basis given a genome size, a
read length, and an average depth

USAGE:
    python simulate_depth.py genome_size read_length average_coverage

genome_size: length of the genome in nucleotides
read_length: length of the reads in nucleotide
average_coverage: average sequencing coverage on the genome

"""

# Importing libraries
import sys
import random

# Main
if __name__ == '__main__':
    try:
        genome_size = int(sys.argv[1])
        read_length = int(sys.argv[2])
        average_coverage = int(sys.argv[3])
    except:
        print __doc__
        sys.exit(1)

    genome = [0] * genome_size
    num_reads = int(float(genome_size) * average_coverage / read_length)
    for read in range(num_reads):
        start = random.randint(0, genome_size - read_length)
        for position in range(start, start + read_length):
            genome[position] += 1
    print genome

