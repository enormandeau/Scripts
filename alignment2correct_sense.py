#!/usr/bin/env python

"""Warning! For test purposes only! Should not be used."""

print __doc__


# Eric Normandeau
# Last revision 2010-12-14

from Bio import SeqIO
import re
import math

# Put all the sequences in a file in the same orientation, based on the first
# sequence in the file. Sequences MUST have an overlap with the first sequence
# in order to be correctly orientated.

# Correct sense is determined by the score from matching kmers of length 11
# from the first sequence of the file on each other sequence and its reverse
# complement. The score is simply the number of matches on the sequence or its
# reverse complement. If the score ratio (score_sense/score_anti) is greater
# than 2, then the sequence is retro transcribed.

fasta_file = sys.argv[1] # Input fasta file
result_file = sys.argv[2] # Output fasta file

def complement(seq):
    """Return the complement of a sequenc *NOT* it's reverse complement
    
    WARNING! This function will NOT treat sequences containing lowcaps letters
    """
    if not seq.isalpha():
        print "The sequence contained non-alphabetic characters"
        print seq
    if not seq.isupper():
        print "The sequence contained non capital-letter characters"
        print "THIS WILL RESULT IN BAD COMPLEMENTATION!"
        seq = seq.upper()
    return seq.replace("A","t").replace("T","a").replace("C","g").replace("G","c").upper()

def reverse_complement(seq):
    return complement(seq)[::-1]

def correct_sense(s1, s2):
    """Insure s2 is in the same sense as s1 for alignment"""
    len_word = 11
    min_ratio = 2
    s2_rev = reverse_complement(s2)
    score_sense = 1
    score_anti = 1
    for i in range(len(s1) - len_word + 1):
        word = s1[i:i + len_word]
        if s2.find(word) > -1:
            score_sense +=1
        if s2_rev.find(word) > -1:
            score_anti +=1
    ratio = math.log(float(score_sense) / score_anti, 10)
    correct_seq = s2
    if ratio < - math.log(min_ratio, 10):
        correct_seq = s2_rev
    return correct_seq

fasta_sequences = [[re.findall("Contig_[0-9]+", x.id)[0], x.seq.tostring()] 
                   for x in SeqIO.parse(open(fasta_file),'fasta')]

print len(fasta_sequences)

seq1 = fasta_sequences[0]
good_sequences = []
for seq in fasta_sequences:
    temp_seq = correct_sense(seq1[1], seq[1])
    good_sequences.append([seq[0], temp_seq])

with open(result_file, "w") as f:
    for seq in good_sequences:
        f.write(str(">%s\n" % seq[0]))
        f.write(str("%s\n" % seq[1]))

