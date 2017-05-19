#!/usr/bin/env python
"""Split scaffolds by cutting in long stretches of Ns

Usage:
    fasta_split_scaffold.py infile min_len outfile

infile = fasta input file name
min_len = minimum length of N stretch to cut
outfile = fasta output file name
"""

# Modules
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

def split_sequence(sequence, min_len):
    """Takes a Fasta object and split on N repeats of min_len or more

    Returns a list of Fasta objects
    """
    seq = sequence.sequence
    name = sequence.name

    n_stretches = sorted(list(re.findall("N{" + str(min_len) + ",}", seq)),
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
if __name__ == '__main__':
    try:
        infile = sys.argv[1]
        min_len = str(sys.argv[2])
        outfile = sys.argv[3]
    except:
        print __doc__
        sys.exit(1)

    fasta_sequences = fasta_iterator(infile)
    output = []

    for seq in fasta_sequences:
        output.extend(split_sequence(seq, min_len))
    
    with open(outfile, "w") as outf:
        for seq in output:
            seq.write_to_file(outf)

