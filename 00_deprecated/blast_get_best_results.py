#!/usr/bin/env python
# -*- coding: utf-8 -*-

# best_blast_results.py
# Finding the best blast result

__authors__ = "Eric Normandeau"
__program_name__ = "best_blast_results"
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

def best_blast_results(in_file, out_file):
    output = ""
    penalty = dict([
                ("unnamed", 200),
                ("unknown", 30),
                ("uncharacterized", 30),
                ("hypothetical", 20),
                ("predicted", 10),
                ("similar to", 5),
                ("novel protein", 5)
                ])
    with open(in_file) as f:
        line_counter = 1
        for line in f:
            line_counter += 1
            if line.strip() == "":
                continue
            data = line.strip().split("\t")
            name = data.pop(0)
            results = itertools.izip(*[itertools.islice(data, i, None, 3)
                                     for i in range(3)])
            best_result = ["NoID", "No hits found", 1]
            for result in results:
                if result[0].find("No hits found") >= 0:# or result[0] == "":
                    print("#####" + result[0])
                    continue
                print(result[2], float(result[2]))
                evalue = float(result[2])
                best_evalue = float(best_result[2])
                result = list(result)
                if evalue == 0:
                    evalue = 1e-200
                for k in penalty:
                    if k in result[1].lower():
                        evalue = evalue * math.pow(10, penalty[k])
                    if k in best_result[1].lower():
                        best_evalue = best_evalue * math.pow(10, penalty[k])
                if evalue > 1:
                    evalue = 1
                if evalue < best_evalue:
                    best_result = result
            best_result[2] = str(best_result[2])
            output += name + "\t" + "\t".join(best_result) + "\n"
    with open(out_file, "w") as f:
        f.write(output)

def help():
    _plateform = platform.system()
    name = __program_name__
    text = """
%s(1)            User Commands           %s(1)

\033[1mNAME\033[0m
\t%s - Keep the best blast result for many contigs

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]... [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tKeep best blast result based on evalue.

\t%s takes a file with blast results and returns the best
\tblast result for each contig, based on the blast evalue and
\tmeaningfullness of the gene name. (eg: rejects gene names containing
\t"Unnamed", "Unknown"...)

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the manual of this program

\t\033[1m-i, --input\033[0m
\t\tInput file in tabulated text format
\t\tNote: There can be an indeterminate number of blast results
\t\tfor one contig, as long as they are presented in the following
\t\tformat:

\t\tInput format:
\t\tContigName  GeneID   GeneName  Evalue    ...  [groups of 3 col.]
\t\tContig_1    NA6524.1 ACo-A     9.00E-042
\t\tContig_2    PG4412.1 Putative  3.20E-012
\t\t...
\t\tContig_134  XF0893.1 Zinc fing 1.50E-035

\t\033[1m-o, --output\033[0m
\t\tOutput file in tabulated text format

\033[1mAUTHORS\033[0m
\t%s

%s %s           %s         %s(1)
"""%(name, name, name, name, name, __authors__, name, __version__, __revision_date__, name)    
    if _plateform != 'Windows' and "this is cool":
        print(text)
    else:
        remove = ["\033[1m","\033[0m","\033[4m"]
        for i in remove:
            text = text.replace(i, "")
        print(text)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help",
                     "input=", "output="])
    except getopt.GetoptError, e:
        print("Input error. Use -h for help")
        sys.exit(0)
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_file = value
            output_file = input_file.replace(".txt", "") + "_results.txt"
        elif option in ('-o', '--output'):
            output_file = value
    try:
        with open(input_file) as test:
            pass
    except:
        print("Input Error: No ACE file specified or file not found.")
        print("Use -h for help.")
        sys.exit(0)
    
    best_blast_results(input_file, output_file)

if __name__ == "__main__":
    main()
