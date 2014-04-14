#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Preparing a file for codeml in PAML from a fasta alignment file

__authors__ = "Eric Normandeau"
__program_name__ = "fasta2paml"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-04-20"


# Importing modules

import os
import sys
import getopt
import platform

from Bio import SeqIO


# Function definitions

def help():
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)                  User Commands                %s(1)

\033[1mNAME\033[0m
\t%s - prepare file for PAML (codeml) from a fasta file

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s \033[0m[\033[4mOPTION\033[0m]... [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tCreate a PAML (codeml) allele file from a fasta alignment file.

\t%s uses the Biopython library to parse a fasta file
\tcontaining multiple alignements, each with the same number of
\tsequences, and create the allele file needed by codeml from PAML.
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-i, --input\033[0m
\t\tInput file in fasta format

\t\033[1m-o, --output\033[0m
\t\tOutput file name

\t\033[1m-n, --numseq\033[0m
\t\tNumber of sequences per group

\033[1mAUTHORS\033[0m
\t%s

%s %s                  %s                %s(1)
"""%(name, name, name, name, name, __authors__, name, __version__, __revision_date__, name)
    
    if _plateform != 'Windows' and "this is cool":
        print text
    else:
        remove = ["\033[1m","\033[0m","\033[4m"]
        for i in remove:
            text = text.replace(i, "")
        print text

def create_paml_files(in_file, out_file, numseq):
    """Create groups of N sequences and write them to a file in fasta format"""
    fasta_sequences = SeqIO.parse(open(in_file),'fasta')
    out_folder = "paml_ready_files"
    out_path = os.path.join(out_folder, out_file)
    end = 0
    try:
        with open (out_path, "w") as test:
            pass
    except:
        print "Created", "'"+ out_folder +"'", "folder to put result files in"
        os.mkdir(out_folder)
    with open(out_path, "w") as f:
        while end == 0:
            sequences = []
            for i in xrange(numseq):
                try:
                    sequences.append(fasta_sequences.next())
                except:
                    end = 1
                    if i == 0:
                        print "All sequences have been treated successfully."
                    else:
                        print "WARNING! Last group does not contain", \
                              numseq, "sequences."
                    break
            if end == 0:
                f.write(str(len(sequences)) + "\t" +
                        str(len(sequences[0].seq.tostring())) + "\n")
                for i, seq in enumerate(sequences):
                    f.write("allele" + str(i + 1) + "\n")
                    f.write(seq.seq.tostring() + "\n")


# Main function

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:n:", ["help", "input=",
            "output=", "numseq="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    output_file = None
    numseq = "zero"
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_file = value
        elif option in ('-o', '--output'):
            output_file = value
        elif option in ('-n', '--numseq'):
            numseq = value
    try:
        with open(input_file) as test:
            pass
    except:
        print "Input Error: No input file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    if output_file == None:
        print "Input Error: No output file specified."
        print "Use -h for help."
        sys.exit(0)
    try:
        numseq = int(numseq)
    except:
        print "Input Error: Enter number of sequences as a positive integer."
        sys.exit(0)
    print "Using version:", __version__, "of", sys.argv[0]
    print "Last revision:", __revision_date__
    
    print
    create_paml_files(input_file, output_file, numseq)
    print

if __name__ == "__main__":
    main()
