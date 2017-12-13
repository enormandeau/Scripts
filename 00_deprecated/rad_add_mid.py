#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Adding MID information to RAD data

__authors__ = "Eric Normandeau"
__program_name__ = "rad_add_mid"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-09-30"


# Importing modules

import os
import sys
import getopt
import platform


# Function definitions

def treat_file(in_file, mid, out_file):
    """Add MIDs to sequences and quality values to quality string
    One line at a time.
    """
    qual = "B" * len(mid)
    print mid, qual
    in_f = open(in_file)
    with open(out_file, "w") as out_f:
        for line in in_f:
            if line != "":
                l = line.strip().split("\t")
                l[-3] = mid + l[-3]
                l[-2] = qual + l[-2]
                l_out = "\t".join(l) + "\n"
                out_f.write(l_out)
    in_f.close()
    print "Pfff! Work done!"

def help():
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)                 User Commands              %s(1)

\033[1mNAME\033[0m
\t%s - Adding MID information to RAD data

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]    [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tAdding MID information to RAD sequencing Fastq files

\t%s uses a Fastq file obtained from RAD sequencing and adds a
\tMID tag to each sequence, as well as a corresponding number of
\tquality values to the quality string describing the sequence.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-i, --input\033[0m
\t\tInput Fastq file

\t\033[1m-m, --mid\033[0m
\t\tMID tag sequence to be added

\t\033[1m-o, --output\033[0m
\t\tOutput Fastq file

\033[1mAUTHORS\033[0m
\t%s

%s %s                %s               %s(1)
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


# RAD add MID
# Albeit small is mighty
# Tags Gigs of data

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:m:o:", ["help",
            "input", "mid" , "output="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    output_file = None
    header = True
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_file = value
        elif option in ('-m', '--mid'):
            mid = value
        elif option in ('-o', '--output'):
            output_file = value
    try:
        with open(input_file) as test:
            pass
    except:
        print "Input Error: No input file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(output_file, "w") as test:
            pass
    except:
        print "Output Error: No output file specified or incorect path."
        print "Use -h for help."
        sys.exit(0)

    print "Using version:", __version__, "of", __program_name__
    print "Last revision:", __revision_date__
    print "By:", __authors__
    print
    
    treat_file(input_file, mid, output_file)

if __name__ == "__main__":
    main()
