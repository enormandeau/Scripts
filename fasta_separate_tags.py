#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Separate sequences of a fasta file by MID into different files

__authors__ = "Eric Normandeau"
__program_name__ = "fasta_separate_tags"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__copyright__ = "Copyright (c) 2011 Eric Normandeau"
__license__ = "GPLv3"
__revision_date__ = "2011-06-16"


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
\t%s - Separate sequences of a fasta file by MID

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTIONS\033[0m]

\033[1mDESCRIPTION\033[0m
\tSplit fasta file by MID into multiple files

\t%s takes a fasta file in which the sequence names
\tbegin by a given MID and puts each sequence in a file
\tcontaining only sequences with the same MID. The 
\toutput files have the form: MID001.fasta, where
\t'MID001' stands for one particular MID name, as
\tspecified in the MID file.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-i, --input\033[0m
\t\tInput file

\t\033[1m-m, --mid\033[0m
\t\tFile containing the list of MIDs to use

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


def split_fasta(input_file, mid_file):
    pass


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:m:",
                                   ["help", "input=", "mid="])
    except getopt.GetoptError, e:
        short_help("Input error. Use -h for help")
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
        elif option in ('-m', '--mid'):
            mid_file = value
            try:
                with open(mid_file) as test:
                    pass
            except:
                short_help("Input Error: No MID file specified or incorect path.")

    print __program_name__, __version__
    print __copyright__
    print
    
    fasta_sequences = SeqIO.parse(open(input_file),'fasta')
    mids = [x.strip() for x in open(mid_file, "r").readlines()]
    files = {}
    
    for m in mids:
        files[m] = open(m + ".fasta", "w")
    
    for s in fasta_sequences:
        name = s.id.split(":")[0]
        seq = s.seq.tostring()
        try:
            files[name].write(">" + s.id + "\n" + seq + "\n")
        except:
            print "Output error"
    
    for m in files:
        files[m].close()
    
