#!/usr/bin/python
# -*- coding: utf-8 -*-

# Correlating gene expression measures from two experiments
# Example, comparing NGS vs microarray data

__authors__ = "Eric Normandeau"
__program_name__ = "gene_expression_correlation"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-12-14"


# Importing modules

import os
import sys
import getopt
import platform


# Function definitions

def find_ratios(r1, r2, c1, c2):
    """Desctiption
    """
    return avg_ratios(c1, c2, import_ratios(r1, r2))

def import_ratios(r1, r2):
    """Create dictionary of sequence IDs and ratios from two files
    """
    ratios = dict()
    with open(r1) as f:
        for l in f:
            line = l.strip()
            if line != "":
                info = line.split("\t")
                ratios[info[0]] = info[1]
    with open(r2) as f:
        for l in f:
            line = l.strip()
            if line != "":
                info = line.split("\t")
                ratios[info[0]] = info[1]
    return ratios

def avg_ratios(c1, c2, ratios):
    """Create dictionary of cluster IDs and average ratios
    """
    avg_ratios = dict()
    with open(c1) as f:
        for l in f:
            line = l.strip()
            if line != "":
                info = line.split("\t")
                ids = info[1:]
                data = []
                for i in ids:
                    data.append(float(ratios[i]))
            avg_ratios[info[0]] = sum(data)/len(data)
    with open(c2) as f:
        for l in f:
            line = l.strip()
            if line != "":
                info = line.split("\t")
                ids = info[1:]
                data = []
                for i in ids:
                    data.append(float(ratios[i]))
            avg_ratios[info[0]] = sum(data)/len(data)
    return avg_ratios

def correlation(ratios, corr, output):
    """Desctiption
    """
    with open(output, "w") as out_f:
        with open(corr) as f:
            for l in f:
                line = l.strip()
                if line != "":
                    data = line.split("\t")
                    out = "\t".join([data[0], data[1],
                                    str(ratios[data[0]]), str(ratios[data[1]])])
                    out_f.write(out + "\n")

def help():
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)                 User Commands              %s(1)

\033[1mNAME\033[0m
\t%s - NGS versus Microarray expression ratios

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]    [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tGet corresponding expression ratios from NGS and Microarray data

\t%s uses expression ratios from two experiments (NGS and Microarray)
\tand returns the corresponding ratios in order to make plots of
\texpression correlation between the two experiments.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-r, --ratios_1\033[0m
\t\tInput file for ratios of the first experiment

\t\033[1m-R, --ratios_2\033[0m
\t\tInput file for ratios of the second experiment

\t\033[1m-c, --clusters_1\033[0m
\t\tInput file for sequence clusters of the first experiment

\t\033[1m-C, --clusters_2\033[0m
\t\tInput file for sequence clusters of the second experiment

\t\033[1m-k, --correspondance\033[0m
\t\tInput file for cluster correspondance between the experiments

\t\033[1m-o, --output\033[0m
\t\tOutput text file, in tab separated format.

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


# Expression correlation
# Pray you confirm results
# From many techniques

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr:R:c:C:k:o:", ["help",
            "ratios_1", "ratios_2", "clusters_1", "clusters_2"
            "correspondance", "output="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    output_file = None
    header = True
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-r', '--ratios_1'):
            ratios_1_file = value
        elif option in ('-R', '--ratios_2'):
            ratios_2_file = value
        elif option in ('-c', '--clusters_1'):
            clusters_1_file = value
        elif option in ('-C', '--clusters_2'):
            clusters_2_file = value
        elif option in ('-k', '--correspondance'):
            correspondance_file = value
        elif option in ('-o', '--output'):
            output_file = value
    try:
        with open(ratios_1_file) as test:
            pass
    except:
        print "Input Error: No ratios_1 file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(ratios_2_file) as test:
            pass
    except:
        print "Input Error: No ratios_2 file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(clusters_1_file) as test:
            pass
    except:
        print "Input Error: No clusters_1 file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(clusters_2_file) as test:
            pass
    except:
        print "Input Error: No clusters_2 file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(correspondance_file) as test:
            pass
    except:
        print "Input Error: No correspondance file specified or file not found."
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
        
    # Return dict of cluster names and average ratios for both groups
    cluster_ratios = find_ratios(ratios_1_file, ratios_2_file,
                                    clusters_1_file, clusters_2_file)
    
    # Put corresponding ratios together (with their IDs) and print to file
    correlation(cluster_ratios, correspondance_file, output_file)

if __name__ == "__main__":
    main()
