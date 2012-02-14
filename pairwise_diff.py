#!/usr/bin/python
# -*- coding: utf-8 -*-

# pairwise_diff.py
# Calculate pairwise differentiation indexes

__authors__ = "Eric Normandeau"
__program_name__ = "pairwise_diff"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-05-20"

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

def cut_ends(read, start, end):
    '''Replace residues on either end of a sequence with gaps.
    
    Cut out the sections of each read which the assembler has decided are not
    good enough to include in the contig and replace them with gap
    
    ''' 
    return (start-1) * '-' + read[start-1:end] + (len(read)-end) * '-'

def pad_read(read, start, conlength):
    ''' Pad ends of a read to make it fit into an alignment.
    
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

def read_fasta(in_fasta): # Should be renamed 'parse_fasta_string'
    """Parse a FASTA string with lines delimited by \\n into a list of lists.
    
    Each inner list contains a name and a sequence.
    
    """
    out = []
    line_counter = -1
    for line in in_fasta.split("\n"):
        if line.startswith(">"):
            contig_name = line.split()[0]
            contig_seq = ""
            out.append([contig_name, contig_seq])
        else:
            out[line_counter][1] += line.rstrip()
    return out

def count_diff(seq1, seq2, max_diff):
    """Count nucleotide differences between two sequences.
    
    Ignore difference if one of the 2 nucleotides compared is an "*".
    If the total number of differences is above 'max_diff', does not count.
    Return a list with: [count = 'int', remove = 'True/False']
    
    """
    count = 0
    remove = False
    for i in xrange(len(seq1)):
        if seq1[i] == "*" or seq2[i] == "*":
            continue
        elif seq1[i] != seq2[i]:
            count += 1
    if count > max_diff:
        remove = True
    return list([count, remove])

def pairwise(in_ace, out_file):
    """Calculate pairwise differentiation indexes.
    
    """
    ace_gen = Ace.parse(open(in_ace, 'r'))
    with open(out_file, "w") as output_file:
        while 1:
            try:
                contig = ace_gen.next()
            except:
                print "***All contigs treated***"
                break
            align = Alignment(Gapped(IUPAC.ambiguous_dna, "-"))
            align.add_sequence(contig.name, contig.sequence)
            for readn in xrange(len(contig.reads)):
                clipst = contig.reads[readn].qa.qual_clipping_start
                clipe = contig.reads[readn].qa.qual_clipping_end
                start = contig.af[readn].padded_start
                seq = cut_ends(contig.reads[readn].rd.sequence, clipst, clipe)
                seq = pad_read(seq, start, len(contig.sequence))
                if "pseudo" not in contig.reads[readn].rd.name:
                    align.add_sequence(contig.reads[readn].rd.name, seq)
            sequences = read_fasta(align.format("fasta"))
            contig_name = re.findall("(Contig_[0-9]+)", sequences[0][0])[0]
            print "Treating", contig_name
            window_len = 8 # PARAMETER
            max_diff = 3 # PARAMETER
            len_contig = len(sequences[0][1])
            number_indexes = 0
            total_indexes = 0
            for seq in sequences[1:]:
                try:
                    start = len(re.findall("^-+", seq[1])[0])
                except:
                    start = 0
                len_seq = 0
                min_len_seq = 100 # PARAMETER
                count = 0
                for window in range(start, len_contig, window_len):
                    nuc_contig = sequences[0][1][window:window + window_len]
                    nuc_seq = seq[1][window:window + window_len]
                    if "-" in nuc_seq:
                        len_seq += len(nuc_seq.replace("-", ""))
                    else:
                        diff = count_diff(nuc_contig, nuc_seq, max_diff)
                        if diff[1] == False:
                            count += diff[0]
                            len_seq += window_len
                len_seq -= seq.count("*")
                if len_seq >= min_len_seq:
                    index = float(count) / len_seq
                    if count > 0:
                        number_indexes +=1
                        total_indexes += index
                else:
                    index = "NA"
                #output_file.write(contig_name + "\t" + str(index) + "\n")
            try:
                mean_index = float(total_indexes) / number_indexes
            except:
                mean_index = "NA"
            output_file.write(contig_name + "\t" + str(mean_index) + "\n")


def help():
    _plateform = platform.system()
    name = __program_name__
    text = """
%s(1)            User Commands           %s(1)

\033[1mNAME\033[0m
\t%s - Calculate pairwise differentiation indexes for sequences
\tin an alignment file in ACE format.

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]... [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tCalculate pairwise differentiation indexes

\t%s uses Biopython to parse an ACE file and calculate, for
\teach sequence in each contig, a pairwise differentiation index. The
\tindex (P) is calculated as follows:

\tP = N/L

\twher 'N' is the number of differences between the sequence and the
\tconcensus of the contig to which it belongs and 'L' is the length of
\tthe sequence.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the manual of this program

\t\033[1m-i, --input\033[0m
\t\tInput file in ACE format

\t\033[1m-o, --output\033[0m
\t\tOutput file in tab separated text format

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
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:s:", ["help",
                     "input=", "output="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    window_length = 11
    maximum_indels = 2
    stars = False
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_ace = value
            output_snpcount = input_ace.replace(".ace", "") + "_pwd.txt"
        elif option in ('-o', '--output'):
            output_file = value
    try:
        with open(input_ace) as test:
            pass
    except:
        print "Input Error: No ACE file specified or file not found."
        print "Use -h for help."
        sys.exit(0)

    pairwise(input_ace, output_file)

if __name__ == "__main__":
    main()
