#!/usr/bin/env python
"""Return frequency of kmers present in a fasta file

Usage:
    python fasta_count_kmer.py genome_file kmer_length
"""

# Importing modules
from signal import signal, SIGPIPE, SIG_DFL
from collections import defaultdict
import sys

# Defining classes
class Fasta(object):
    """Fasta object with name and sequence
    """
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence
    def write_to_file(self, handle):
        handle.write(">" + self.name + "\n")
        handle.write(self.sequence + "\n")

# Defining functions
def fasta_iterator(input_file):
    """Takes a fasta file input_file and returns a fasta iterator
    """
    with open(input_file) as f:
        sequence = ""
        name = ""
        begun = False
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if begun:
                    yield Fasta(name, sequence)
                name = line.replace(">", "")
                sequence = ""
                begun = True
            else:
                sequence += line

        if name != "":
            yield Fasta(name, sequence)

if __name__ == '__main__':
    # Prevent broken pipe error
    signal(SIGPIPE, SIG_DFL)

    # Parse user input
    try:
        input_file = sys.argv[1]
        kmer_length = int(sys.argv[2])
    except:
        print(__doc__)
        sys.exit(1)

    # Cound kmers
    kmer_dict = defaultdict(int)

    for seq in fasta_iterator(input_file):
        for start in range(0, len(seq.sequence) - kmer_length):
            stop = start + kmer_length
            kmer_dict[seq.sequence[start: stop]] += 1

    kmer_list = sorted([(kmer_dict[k], k) for k in kmer_dict], reverse=True)

    # Print results
    for kmer in kmer_list:
        print(kmer[1], kmer[0])

