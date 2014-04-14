#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Preparing a file for codeml in PAML from a fasta alignment file

__authors__ = "Eric Normandeau"
__program_name__ = "alignment2paml"
__version_info__ = ('0', '0', '2')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-05-20"


# Importing modules

import os
import sys
import getopt
import platform
import re

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
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]... [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tClean alignments so that no more '-' characters are found in the
\tmain sequences, thus maintaining integrity of the reading frame.
\tAlso replaces any '-' character in the non-main sequences by the
\tcorresponding nucleotide in the main sequence.

\t%s uses the Biopython library to parse a fasta file
\tcontaining multiple alignements, each with the same number of
\tsequences, clean them by removing nucleotides in all sequences
\tif a '-' character is found in the main sequence, thus restoring
\tthe correct reading frame for the main sequence.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-i, --input\033[0m
\t\tInput file, in fasta format

\t\033[1m-o, --output\033[0m
\t\tOutput file, in fasta format

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

def clean_alignment(in_file, out_file, numseq):
    """Create groups of N sequences and write them to a file in fasta format"""
    fasta_sequences = SeqIO.parse(open(in_file),'fasta')
    out_folder = "cleaned_alignments"
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
                    temp_fasta = fasta_sequences.next()
                    name, sequence = temp_fasta.id, temp_fasta.seq.tostring()
                    sequences.append([name, sequence])
                except:
                    end = 1
                    if i == 0:
                        print "All sequences have been treated successfully."
                    else:
                        print "WARNING! Last group does not contain", \
                              numseq, "sequences."
                    break
            if end == 0:
                positions = []
                # Defining which is the main sequence!!!
# original line                main_seq = sequences[0][1]
                main_seq = sequences[5][1]
                for i, nuc in enumerate(main_seq):
                    if nuc == "-":
                        positions.append(i)
                temp_sequences = []
                # Remove '-' positions from the main sequence
                for seq in sequences:
                    name = seq[0]
                    the_seq = seq[1]
                    for i in reversed(positions):
                        the_seq = the_seq[:i] + the_seq[i + 1:]
                    temp_sequences.append([name, the_seq])
                # Trim all sequences to codon length
                sequences = temp_sequences
                temp_sequences = []
                for seq in sequences:
                    name = seq[0]
                    the_seq = seq[1][0:3 * len(seq[1])/3]
                    temp_sequences.append([name, the_seq])
                # Verify that only full codons are present, if not remove
                # Also confirm absence of stop codons, cut if present
                sequences = temp_sequences
                temp_sequences = []
                for seq in sequences:
                    name = seq[0]
                    the_seq = seq[1]
                    for i in xrange(0, len(the_seq), 3):
                        codon = the_seq[i:i+3]
                        if "-" in codon and "---" not in codon:
                            the_seq = the_seq[:i] + "---" + the_seq[i + 3:]
                        elif codon in ["TAG", "TAA", "TGA"]:
                            the_seq = the_seq[:i] + "DEL" + "-" * len(the_seq[i + 3:])
                    temp_sequences.append([name, the_seq])
                # Removing sequences that have a 'DEL' codon tag
                sequences = temp_sequences
                temp_sequences = []
                for seq in sequences:
                    name = seq[0]
                    the_seq = seq[1]
                    if 'DEL' in the_seq:
                        the_seq = "ATG" + "-" * (len(the_seq) - 3)
                    temp_sequences.append([name, the_seq])
                # Removing "-" characters from secondary sequences
                # Replace by nucleotides from the main sequence
                sequences = temp_sequences
                temp_sequences = []
                main_seq = sequences[5][1]
                for seq in sequences:
                    name = seq[0]
                    the_seq = seq[1]
                    for i in xrange(len(the_seq)):
                        if the_seq[i] == "-":
                            the_seq = the_seq[:i] + main_seq[i] + the_seq[i+1:]
                    temp_sequences.append([name, the_seq])
                # Printing result to file
                for output in temp_sequences:
                    name = output[0]
                    temp_seq = output[1]
                    f.write(">" + name + "\n")
                    line_return = 60 # fasta with 60 characters per line
                    while len(temp_seq) > 0:
                        f.write(temp_seq[:line_return] + "\n")
                        temp_seq = temp_seq[line_return:]


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
    clean_alignment(input_file, output_file, numseq)
    print

if __name__ == "__main__":
    main()
