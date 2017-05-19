#!/usr/bin/env python
"""Split long sequences in fasta file

Usage:
    fasta_split_long_sequences.py input_file max_len output_file

input_file = fasta input file name
max_len = maximum length of sequence
output_file = fasta output file name
"""

# Modules
import copy
import sys
import re

# Classes
class Fasta(object):
    """Fasta object with name and sequence
    """
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence
    def write_to_file(self, handle):
        handle.write(">" + self.name + "\n")
        handle.write(self.sequence + "\n")
    def __repr__(self):
        return(self.name + ": " + self.sequence[0:31])

# Functions
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

def split_sequence(sequence, max_len):
    """Takes a Fasta object and split on N repeats of max_len or more

    Returns a list of Fasta objects
    """
    seq = sequence.sequence
    name = sequence.name

    n_stretches = sorted(list(re.findall("N{" + str(max_len) + ",}", seq)),
            cmp = lambda x,y: cmp(len(x), len(y)), reverse=True)

    for s in n_stretches:
        seq = seq.replace(s, "_SPLIT-HERE_")

    sequences = []
    sections = seq.split("_SPLIT-HERE_")

    counter = 1
    for s in sections:
        sequences.append(Fasta(name + "_split_" + str(counter), s))
        counter += 1

    return sequences

# Main
try:
    input_file = sys.argv[1]
    max_len = int(sys.argv[2])
    output_file = sys.argv[3]
except:
    print __doc__
    sys.exit(1)

fasta_sequences = fasta_iterator(input_file)

with open(output_file, "w") as outfile:
    for seq in fasta_sequences:
        if len(seq.sequence) > max_len:
            counter = 0
            while len(seq.sequence) > 0:
                left = copy.deepcopy(seq)
                left.sequence = seq.sequence[0:max_len]
                print len(seq.sequence)
                seq.sequence = seq.sequence[max_len:]
                print len(seq.sequence)
                counter += 1
                chunk_name = "chunk_" + str(counter)
                left.name += chunk_name
                left.write_to_file(outfile)
        else:
            seq.write_to_file(outfile)
