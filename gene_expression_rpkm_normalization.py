#!/usr/bin/env python
# -*- coding: utf-8 -*-

# normalize.py
# RPKM normalization of gene expression matrix

__authors__ = "Eric Normandeau"
__program_name__ = "normalize"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-04-27"


# Module imports

import getopt
import sys
import platform
import re
from collections import defaultdict

from Bio.Sequencing import Ace
from Bio.Align.Generic import Alignment
from Bio.Alphabet import IUPAC, Gapped


# Function definitions

def normalize(in_file, out_file, min_gene_count):
    lines = []
    with open(in_file) as f:
        for line in f:
            lines.append(line)
    title_line = lines[0]
    num_individuals = len(title_line.strip().split()) - 2
    total_counts = [0] * num_individuals
    for line in lines[1:]:
        splited = line.strip().split()
        counts = splited[2:]
        for i, count in enumerate(counts):
            total_counts[i] += int(count)
    with open(out_file, "w") as f:
        f.write(title_line.strip() + "\t" + "total" + "\n")
        for line in lines[1:]:
            splited = line.strip().split()
            counts = splited[2:]
            total_gene_count = 0
            for count in counts:
                total_gene_count += int(count)
            f.write(splited[0] + "\t" + splited[1])
            for i, count in enumerate(counts):
                try:
                    norm = float(int(count) * 1000000000) / \
                           (int(total_counts[i]) * int(splited[1]))
                except:
                    norm = 0
                f.write("\t" + str(norm))
            f.write("\t" + str(total_gene_count))
            f.write("\n")

def help():
    _plateform = platform.system()
    name = __program_name__
    text = """
%s(1)                     User Commands                     %s(1)

\033[1mNAME\033[0m
\t%s - RPKM normalization of gene expression matrix

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]... [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tCreate a RPKM normalized gene expression matrix from read counts

\t%s takes a matrix of next generation sequencing gene expression
\tcounts, as outputed by gexpress.py with format number 1. It returns
\ta similar matrix where the read counts have been normalized for each
\tindividual by using the RPKM approach
\t(Reads Per Kilobase of exon model per Million mapped reads).
\tFor each individual, in each gene:

\tR = 10e9 x C / (N x L)

\twhere:
\tC = number of sequences from that individual in that gene
\tN = total number of sequences from that individual
\tL = length of combined exons

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the manual of this program

\t\033[1m-i, --input\033[0m
\t\tInput file in matrix format from genexpress.py

\t\033[1m-o, --output\033[0m
\t\tOutput file in tabulated text format

\033[1mAUTHORS\033[0m
\t%s

%s %s                     %s                     %s(1)
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
        print "Input Error: No input file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(output_file, "w") as test:
            pass
    except:
        output_file = input_file + ".normalized"
    
    min_gene_count = 200
    normalize(input_file, output_file, min_gene_count)

if __name__ == "__main__":
    main()
