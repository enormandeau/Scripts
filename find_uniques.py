#!/usr/bin/env python
# -*- coding: utf-8 -*-

# find_uniques.py
# Finding unique identifiers

__authors__ = "Eric Normandeau"
__program_name__ = "find_uniques"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-05-18"


# Module imports

import getopt
import sys
import platform
import re
import itertools
import math


# Function definitions

def find_uniques(in_file, out_file):
    with open(in_file) as f:
        initial_list = list(f)
    initial_list = [x for x in initial_list if x != "\n"]
    unique_list = list(set(initial_list))
    number_uniques = len(unique_list)
    print "There were:", number_uniques, "unique identifiers"
    with open(out_file, "w") as f:
        f.writelines(sorted(unique_list))

def help():
    _plateform = platform.system()
    name = __program_name__
    text = """
%s(1)            User Commands           %s(1)

\033[1mNAME\033[0m
\t%s - Find uniques in a list

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]... [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tFind the number and identity of uniques in a list

\t%s takes a file with one identifier per line and returns the
\tnumber of unique identifiers as well as a file containing only the
\tunique identifiers, one per line.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the manual of this program

\t\033[1m-i, --input\033[0m
\t\tInput file in text format

\t\033[1m-o, --output\033[0m
\t\tOutput file in text format

\033[1mAUTHORS\033[0m
\t%s

%s %s           %s         %s(1)
"""%(name, name, name, name, name, __authors__, name, __version__, __revision_date__, name)    
    if _plateform != 'Windows' and "this is cool":
        print text
    else:
        remove = ["\033[1m","\033[0m","\033[4m"]
        for i in remove:
            text = text.replace(i, "")
        print text

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help",
                     "input=", "output="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    output_file = "uniques_output.txt"
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_file = value
        elif option in ('-o', '--output'):
            output_file = value
    try:
        with open(input_file) as test:
            pass
    except:
        print "No input file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    
    find_uniques(input_file, output_file)

if __name__ == "__main__":
    main()
