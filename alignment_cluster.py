#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Cluster aligned sequences based on the number of mismatches

__authors__ = "Eric Normandeau"
__program_name__ = "alignment_cluster"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__copyright__ = "Copyright (c) 2011 Eric Normandeau"
__license__ = "GPLv3"
__revision_date__ = "2011-06-13"


# Importing modules

import os
import sys
import re
import getopt
import platform

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)


# Function definitions

def help():
    """Help attained by typing './program_name.py -h'
    """
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)            User Commands         %s(1)

\033[1mNAME\033[0m
\t%s - Cluster aligned sequences

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTIONS\033[0m]

\033[1mDESCRIPTION\033[0m
\tRegroup aligned sequences based on similarity

\t%s takes a fasta alignment file for input and clusters the sequences.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-i, --input\033[0m
\t\tInput file

\t\033[1m-o, --output\033[0m
\t\tOutput file

\t\033[1m-m, --mismatch\033[0m
\t\tCost of mismatches (integer, default=1)

\t\033[1m-d, --indel\033[0m
\t\tCost of insertions or deletions (integer, default=1)

\t\033[1m-c, --cutoff\033[0m
\t\tMaximum score accepted to cluster sequences (integer, default=3)

\033[1mAUTHORS\033[0m
\t%s

%s %s           %s          %s(1)
"""%(name, name, name, name, name, __authors__, name, __version__, \
    __revision_date__, name)
    
    if _plateform != 'Windows' and "this is great news":
        print text
    else:
        __Windows__ = "This is an abomination"
        remove = ["\033[1m","\033[0m","\033[4m"]
        for i in remove:
            text = text.replace(i, "")
        print text
        del(__Windows__) # If only we could...

def short_help(msg):
    """Print short help in case of bad user input
    """
    print msg
    print "Use -h for help"
    sys.exit(0)

def score_sequences(s1, s2, m, d):
    score = 0
    for i in xrange(len(s1)):
        n1 = s1[i]
        n2 = s2[i]
        if n1 != n2:
            if n1 == "-" or n2 == "-":
                score += d
            else:
                score += m
    return score

# Does alignment_clean
# neatify your sequences
# up to your standards?


# The program itself

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:m:d:c:", ["help",
            "input=", "output=", "mismatch=", "indel=", "cutoff="])
    except getopt.GetoptError, e:
        short_help("Input error. Use -h for help")
    mismatch = 1
    indel = 1
    cutoff = 3
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_file = value
            try:
                with open(input_file) as test:
                    pass
            except:
                short_help("Input Error: No input file specified or file not found.")
        elif option in ('-o', '--output'):
            output_file = value
            try:
                with open(output_file, "w") as test:
                    pass
            except:
                short_help("Output Error: No output file specified or incorect path.")
        elif option in ('-m', '--mismatch'):
            try:
                mismatch = int(value)
                assert mismatch >= 0
            except:
                short_help("Positive integer needed for 'mismatch' option")
        elif option in ('-d', '--indel'):
            try:
                indel = int(value)
                assert indel >= 0
            except:
                short_help("Positive integer needed for 'indel' option")
        elif option in ('-c', '--cutoff'):
            try:
                cutoff = int(value)
                assert cutoff >= 0
            except:
                short_help("Positive integer needed for 'cutoff' option")

    print __program_name__, __version__
    print __copyright__
    print

 
    fasta_sequences = list(SeqIO.parse(open(input_file),'fasta'))
    
    nseq = len(fasta_sequences)
    
    with open(output_file, "w") as f:
        for i in xrange(nseq):
            for j in xrange(i - 1):
                s1 = fasta_sequences[i]
                s2 = fasta_sequences[j + 1]
                if score_sequences(s1.seq.tostring(), s2.seq.tostring(),
                    mismatch, indel) <= cutoff:
                    f.write(s1.id + " " + s2.id + "\n")
    
    print "Done"
    












