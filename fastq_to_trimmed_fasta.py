#!/usr/bin/env python
"""Take a .fastq file and return a .fasta file where the sequences have been
trimmed to a specified length.

Usage:
    python fastq_to_trimmed_fasta.py  inputFile  length

inputFile = fastq file ** WARNING** Sequeces must NOT be wrapped
length = lenght to which all the sequences will be trimmed

The output is printed to the standard output (ie: terminal)
"""

# Importing modules
import sys

# Defining classes

# Defining function

# Main
if __name__ == '__main__':
    try:
        infile = sys.argv[1]
        length = int(sys.argv[2])
    except:
        print __doc__
        sys.exit(1)
    blackhole = "something"
    with open(infile) as f:
        while True:
            l1 = f.readline().strip()
            l2 = f.readline().strip()
            blackhole = f.readline().strip()
            blackhole = f.readline().strip()
            if blackhole != "":
                print l1.replace("@", ">")
                print l2[0:length]
            else:
                break
                print "Done"

