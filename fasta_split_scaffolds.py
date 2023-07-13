#!/usr/bin/env python3
"""Split scaffolds at occurences of one or more Ns

Usage:
    fasta_split_scaffold.py input_file min_Ns min_len output_file

input_file = fasta input file name
min_Ns = minimum number of Ns to cut
min_len = minimum sequence length to keep
output_file = fasta output file name
"""

# Modules
import sys
import re

# Modules
import gzip

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
        return self.name + " (len: " + str(len(self.sequence)) + ") " + self.sequence[:31]

# Functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

def fasta_iterator(input_file):
    """Takes a fasta file input_file and returns a fasta iterator
    """
    with myopen(input_file) as f:
        sequence = []
        name = ""
        begun = False

        for line in f:
            line = line.strip()

            if line.startswith(">"):
                if begun:
                    yield Fasta(name, "".join(sequence))

                name = line[1:]
                sequence = ""
                begun = True

            else:
                sequence += line

        if name != "":
            yield Fasta(name, "".join(sequence))

def split_and_write_sequences(seq, min_Ns, min_len, output_file):
    short_name = seq.name.split(" ")[0]
    seq.name = short_name
    fragments = list(re.finditer("[^nN]{" + str(min_len) + ",}", seq.sequence))
    n = 0

    for f in fragments:
        n += 1
        nstr = str(n).rjust(8, "0")
        _from, _to = f.span()
        print(short_name, _from, _to)

        if (_to - _from) > min_len:
            Fasta("_".join(
                [short_name, nstr, str(_from), str(_to)]), seq.sequence[_from: _to]
                ).write_to_file(outfile)

# Main
if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
        min_Ns = int(sys.argv[2])
        min_len = int(sys.argv[3])
        output_file = sys.argv[4]
    except:
        print(__doc__)
        sys.exit(1)

    fasta_sequences = fasta_iterator(input_file)
    output = []

    with open(output_file, "w") as outfile:
        for seq in fasta_sequences:
            split_and_write_sequences(seq, min_Ns, min_len, outfile)
