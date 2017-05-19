#!/usr/bin/env python
"""kmer_find_unique.py

Find kmers that are unique to a genome and found in no other genomes

Usage:
    python virtual_rapd.py  wanted_file  unwanted_file  kmer_length

wanted_file =   genome of interest in fasta format
unwanted_file = all other genomes in one fasta file
kmer_length =   length of kmer to compare (positive integer)
"""

# Importing modules
import sys
from collections import defaultdict

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

def kmer_iterator(seq, kmer_length):
    """Takes a Fasta object and returns a kmer iterator
    """
    for k in xrange(len(seq.sequence) - kmer_length + 1):
        yield seq.sequence[k: k + kmer_length].upper()

def complement(seq):
    """Return the complement of a sequence, *NOT* it's reverse complement"""
    if not seq.isalpha():
        print "The sequence contained non-alphabetic characters"
        print seq
    if not seq.isupper():
        #print "The sequence contained non capital-letter characters"
        seq = seq.upper()
    seq = seq.replace("A","1").replace("T","2").replace("C","3").replace("G","4")
    seq = seq.replace("a","5").replace("t","6").replace("c","7").replace("t","8")
    seq = seq.replace("1","T").replace("2","A").replace("3","G").replace("4","C")
    seq = seq.replace("5","t").replace("6","a").replace("7","g").replace("8","c")
    return seq

def reverse_complement(seq):
    return complement(seq)[::-1]

def lowest_kmer(k1, k2):
    """Given 2 kmers, return the one that sorts first
    """
    return sorted([k1, k2])[0]

# main
if __name__ == '__main__':
    # Parsing user input
    try:
        wanted_file = sys.argv[1]
        unwanted_file = sys.argv[2]
        kmer_length = int(sys.argv[3])
    except:
        print __doc__
        sys.exit(1)
    assert 6 <= kmer_length <= 30, "kmer_length must be a positive integer in range 6-30"

    # Create iterators and kmer dictionaries
    good_sequences = fasta_iterator(wanted_file)
    bad_sequences = fasta_iterator(unwanted_file)

    good_kmers = defaultdict(int)
    bad_kmers = defaultdict(int) # TODO Could be a set (would save memory)

    # Iterate through sequences
    #print "Treating wanted file..."
    for s in good_sequences:
        for k in kmer_iterator(s, kmer_length):
            if "N" not in k:
                good_kmers[lowest_kmer(k, reverse_complement(k))] += 1

    #print "Treating unwanted file..."
    for s in bad_sequences:
        for k in kmer_iterator(s, kmer_length):
            if "N" not in k:
                bad_kmers[lowest_kmer(k, reverse_complement(k))] += 1

    # Keep only interesting kmers
    #print "Removing kmers that are in bad_kmers..."
    interesting_kmers = dict((k, good_kmers[k]) for k in good_kmers if k not in bad_kmers)

    for i in interesting_kmers:
        print i

    #print len(interesting_kmers), "retained kmers"

