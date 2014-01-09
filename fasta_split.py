#!/usr/bin/python
"""Split a fasta file in n files of approximately the same number of sequences

WARNING: This will create 'n' files in your present directory

USAGE:
    python fasta_split.py input_file num_files

input_file: fasta file
num_files: number of files to split into
"""

# Importing modules
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
def fasta_iterator(object):
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
        yield Fasta(name, sequence)

if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
        num_files = int(sys.argv[2])
    except:
        print __doc__
        sys.exit(1)

    # Open output files for writting
    output_files = {}
    for n in xrange(1, num_files + 1):
        output_files[n] = open(input_file + str(n) + ".fasta", "w")

    # Iterate through sequences and write to files
    file_number = 0
    for sequence in fasta_iterator(input_file):
        current_file = file_number % num_files
        sequence.write_to_file(output_files[current_file])
        file_number += 1

    # Close output file handles
    for n in xrange(1, num_files + 1):
        output_files[n].close()

