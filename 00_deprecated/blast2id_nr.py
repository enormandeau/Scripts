#!/usr/bin/env python
# -*- coding: utf-8 -*-

__info__ = "Parse Blast+ result to extract gene names"
__authors__ = "Eric Normandeau and Nicolas Maillet"
__program_name__ = "Blast2id_nr"
__version_info__ = ('0', '0', '2')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-05-06"


# Module imports

import os
import sys
import getopt
import re
import string
import math
from copy import copy


# Globals var

# Usage of this program
USAGE = "\n\033[1mUsage\033[0m : %s [--help, --file, --output, --format]\n\
" % sys.argv[0]
# The output of blast+
FILE = ""
# Result file
OUT = "id_sp.txt"
# Separator between two hits
FORMAT = 6


# Function definitions

def help():
    print "\nBlast2id(1)                      User Commands                  \
    Blast2id(1)\n\n\033[1mNAME\033[0m\n\t%s - Format Blast+ results for \
Gene Ontology\n\n\033[1mSYNOPSIS\033[0m\n\t\033[1mpython %s \033[0m[\033[4mO\
PTION\033[0m]... [\033[4mFILE\033[0m]...\n\n\033[1mDESCRIPTION\033[0m\n\tForma\
t a result file of Blast+ (two differents formats accepted) and c-\n\treate a \
file tab separate which can be used by sp2b2g.py to find GO te-\n\trms.\n\n\tT\
his output file contains per line the sequence id of the blast+ reque-\n\tst a\
nd the id of the best match.\n\n\033[1m-f, --file\033[0m\n\tThe file to proces\
s.\n\n\033[1m-h, --help\033[0m\n\tDisplay the manual of this program.\n\n\
\033[1m-o, --output\033[0m\n\tThe results file\n\n\033[1m-r, --format\033[0m\n\
\tThe format of the input file. 0 for standard option and 6 (default) for\n\to\
ption 6 in Blast+ with 'qseqid sseqid bitscore length pident evalue'\n\n\
\033[1mAUTHOR\033[0m\n\tWritten by Eric Normandeau & Nicolas Maillet.\n\
" % (sys.argv[0],sys.argv[0])

def readfile(path):
    """Read file and return a list containing the file lines"""
    out = []
    try:
        bpfile = open(FILE, "r")
    except:
        print "\n\033[1mError :\033[0m file '%s' can't be open.\n" % FILE
        sys.exit(0)
    else:
        for line in bpfile:
            out.append(line)
        bpfile.close()
    return out

def writefile(var, path):
    """Write lines from the first dimension of structuring of an object"""
    outfile = open(path, "w")
    for line in var:
        outfile.write(line)
    outfile.close()


#########################
## Parsing blast result
## After blast+
## format #6

def formatSix():
    blast = readfile(FILE)
    blast_dict = {}

    for line in blast:
        id_ = line.split("\t")[0]
        if id_ not in blast_dict:
            line = re.split("[a-zA-Z]{2}[a-zA-Z]?(?<!gi)\|", 
            line)[1].split("|")[0]
            # Write the id {TAB} the db id {LF}
            blast_dict[id_] = id_ + "\t" + line + "\n"

    blast_list = sorted([item for item in blast_dict.values()])
    writefile(blast_list, OUT)


#########################
## Parsing blast result
## After blast+
## No format (format zero)

def formatZero():
    input_file = open(FILE, "r")
    output_file = open(OUT, "w")
    res = ""
    complete = False
    new_contig = False
    started = False
    blast_count = 0
    max_blasts = 5
    evalue_found = False

    for line in input_file:
        if line.startswith("Query="):
            if new_contig == True:
                res += "\n"
            blast_count = 0
            current_blast = line.strip().split("  ")[-1]
            new_contig = True
            complete = False
        elif line.startswith(">") and complete == False and blast_count <= max_blasts:
            blast_count += 1
            evalue_found = False
            started = True
            current_blast += "\t" + re.split("[a-zA-Z]{2}[a-zA-Z]?(?<!gi)\|", 
            line)[1].split("|")[0] + "\t" + re.split("\|", line)[2].strip()
        elif line.startswith(">") and started == True:
            "BANG!"
        elif line.startswith("Length=") and started == True:
            started = False
            res += current_blast
            current_blast = ""
        elif line.startswith("***** No hits found *****") and complete == False:
            res += current_blast + "\t" + "No hits found"
            complete = True
            blast_count = -99
            started = False
        elif "Expect" in line and complete == False and evalue_found == False:
            res += "\t" + line.split(" ")[-1].strip()
            evalue_found = True
        elif started == True:
            current_blast += " " + line.strip()
        if blast_count > max_blasts:
            complete = True
            started = False
    res += "\n"
    output_file.write(res)


###############
## Program


# Command line parsing

opts, args = None, None
try:
    opts, args = getopt.getopt(sys.argv[1:], "hf:o:r:", ["help", "file=",
    "output=", "format="])
except getopt.GetoptError, e:
    print USAGE;
    sys.exit(0)


# Process command lines options

for option, value in opts:
    if option in ('-h', '--help'):
        help()
        sys.exit(0)
    elif option in ('-f', '--file'):
        FILE = value
        OUT = value + ".res"
    elif option in ('-o', '--output'):
        OUT = value
    elif option in ('-r', '--format'):
        try:
            FORMAT = int(value)
        except:
            print "\n\033[1mError :\033[0m format '%s' must be integer.\n\
            " % value
            sys.exit(0)

        
# Test the existence of the input file

if FILE == "":
    print "\n\033[1mError :\033[0m you must specify a file with -f option.\n"
    sys.exit(0)

# Run the correct function
if(FORMAT == 6):
    formatSix()
    print "\n\033[1mDone !\033[0m File '%s' created.\n" % OUT
elif(FORMAT == 0):
    formatZero()
    print "\n\033[1mDone !\033[0m File '%s' created.\n" % OUT
else:
    print "\n\033[1mError :\033[0m format '%s' not recognize.\n" % FORMAT
    sys.exit(0)
