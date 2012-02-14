#!/usr/bin/python
# -*- coding: utf-8 -*-

# find_score.py
# Finding the average score for identifiers with multiple scores

__authors__ = "Eric Normandeau"
__program_name__ = "find_score"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-05-18"


# Module imports

import getopt
import sys
import platform
import itertools
import math
from collections import defaultdict


# Function definitions

def mean(a_list):
    """Return the mean of a list of numbers
    
    """
    try:
        mean = float(sum(a_list)) / len(a_list)
    except:
        print "Could not compute mean"
        sys.exit(0)
    return mean

def find_score(in_file, out_file):
    scores = defaultdict(list)
    with open(in_file) as f:
        for line in f:
            try:
                line_list = line.split()
                name = line_list[0]
                score = int(line_list[1])
                scores[name].append(score)
            except:
                continue
    output = ""
    for name in sorted(scores.keys()):
        score = mean(scores[name])
        output += name + "\t" + str(score) + "\n"
    with open(out_file, "w") as f:
        f.write(output)

def help():
    _plateform = platform.system()
    name = __program_name__
    text = """
%s(1)            User Commands           %s(1)

\033[1mNAME\033[0m
\t%s - Find the average score of identifiers in a list

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]... [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tCalculate and return the average score of different identifiers

\t%s takes a file with one identifier and one score per line,
\tin a tabulated text file, and returns a file with the average score
\tfor each unique identifier.

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
        print "Input input file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    
    find_score(input_file, output_file)

if __name__ == "__main__":
    main()
