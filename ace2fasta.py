#!/usr/bin/python
# -*- coding: utf-8 -*-

# ace2fasta.py
# From ACE format to FASTA format

# Eric Normandeau
# 2010 04 15

# Create an output_file.fasta containing contig sequences alignements from
# an input_file.ace
# Clean each contig by removing insertions '*' in the contig consensus and
# all the sequences in the contig alignment

__version_info__ = ('0', '0', '2')
__version__ = '.'.join(__version_info__)

# Module imports

import getopt
import sys
import platform

from Bio.Sequencing import Ace
from Bio.Align.Generic import Alignment
from Bio.Alphabet import IUPAC, Gapped


# Function definitions

def cut_ends(read, start, end):
    '''Replace residues on either end of a sequence with gaps.
    
    Cut out the sections of each read which the assembler has decided are not
    good enough to include in the contig and replace them with gap
    ''' 
    return (start-1) * '-' + read[start-1:end] + (len(read)-end) * '-'

def pad_read(read, start, conlength):
    ''' Pad out either end of a read so it fits into an alignment.
    
    The start argument is the position of the first base of the reads sequence 
    in the contig it is part of. If the start value is lower than 1 (since 
    ACE files count from 1, not 0) we take part of the sequence off the start,
    otherwise each end is padded to the length of the consensus with gaps.
    '''
    if start < 1:
        seq = read[-1*start+1:]
    else:
        seq = (start-1) * '-' + read
    seq = seq + (conlength-len(seq)) * '-'
    return seq

def ace2fasta(in_file, out_file):
    ace_gen = Ace.parse(open(in_file, 'r'))
    with open(out_file, "w") as output_file:
        while 1:
            try:
                contig = ace_gen.next()
            except:
                print "All contigs treated"
                break
            align = Alignment(Gapped(IUPAC.ambiguous_dna, "-"))
            
            # Now we have started our alignment we can add sequences to it 
            # Add concensus sequence to alignment
            align.add_sequence(contig.name, contig.sequence)
            
            for readn in xrange(len(contig.reads)):
                clipst = contig.reads[readn].qa.qual_clipping_start
                clipe = contig.reads[readn].qa.qual_clipping_end
                start = contig.af[readn].padded_start
                seq = cut_ends(contig.reads[readn].rd.sequence, clipst, clipe)
                seq = pad_read(seq, start, len(contig.sequence))
                if "pseudo" not in contig.reads[readn].rd.name:
                    align.add_sequence(contig.reads[readn].rd.name, seq)
            
            output_file.write(align.format("fasta"))

def help():
    _plateform = platform.system()
    name = sys.argv[0]
    text =  """
%s(1)                   User Commands                 %s(1)

\033[1mNAME\033[0m
\t%s - From ACE format to FASTA format

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s \033[0m[\033[4mOPTION\033[0m]... [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tCreate FASTA alignment file from an ACE file containing contigs.

\t%s uses the Biopython library to parse an ACE file containing
\tNext Generation Sequencing contig alignments. It then writes a FASTA
\tfile containing all the contigs, with both the consensus sequence
\tand the aligned sequences for each contig.

\t\033[1m-h, --help\033[0m
\t\tDisplay the manual of this program

\t\033[1m-i, --input\033[0m
\t\tInput file in .ACE format

\t\033[1m-o, --output\033[0m
\t\tOutput file in .FASTA format

\033[1mAUTHORS\033[0m
\tWritten by Eric Normandeau and Nicolas Maillet.
""" % (name, name, name, name, name)
    
    if _plateform != 'Windows' and "this is cool":
        print text
    else:
        remove = ["\033[1m","\033[0m","\033[4m"]
        for i in remove:
            text = text.replace(i, "")
        print text

def main():
    # parse command line options
    # opts, args = None, None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "input=",
            "output="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    # Process command lines options
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_ace = value
            output_fasta = input_ace.replace(".ace", "") + ".fasta"
        elif option in ('-o', '--output'):
            output_fasta = value
    try:
        with open(input_ace) as test:
            pass
    except:
        print "Input Error: No input file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    
    ace2fasta(input_ace, output_fasta)

if __name__ == "__main__":
    main()
