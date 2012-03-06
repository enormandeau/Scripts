#!/usr/bin/python
# -*- coding: utf-8 -*-

# gexpress.py
# From ACE format to individual gene expression

__authors__ = "Eric Normandeau"
__program_name__ = "ace2gene_expression"
__version_info__ = ('0', '0', '4')
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

def import_tags(in_tags):
    tags = []
    with open(in_tags) as f:
        for line in f:
            if line.strip() != "":
                tags.append(line.strip())
    return tags

def read_fasta_2list(in_fasta):
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

def gene_expression_2column(in_ace, out_file, tags, min_seq):
    """Count sequences with each tags in all contigs.
    
    """
    print
    print "USING COLUMN OUTPUT FORMAT"
    print
    ace_gen = Ace.parse(open(in_ace, 'r'))
    with open(out_file, "w") as output_file:
        output_file.write("Contig\tTag\tCount\n")
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
            sequences = read_fasta_2list(align.format("fasta"))
            if len(sequences) < min_seq:
                continue
            contig_name = re.findall("(Contig_[0-9]+)", sequences[0][0])[0]
            print "Treating", contig_name
            d = defaultdict(int)
            for tag in tags:
                d[tag] = 0
            d["XX_noTag"] = 0
            fasta_counter = 0
            for fasta in sequences:
                fasta_counter += 1
                found_tag = 0
                for tag in tags:
                    if fasta[0].find(tag) > -1:
                        d[tag] += 1
                        found_tag = 1
                if found_tag == 0 and fasta[0].find("Consensus") < 0:
                    d["XX_noTag"] += 1
            for tag in sorted(d):
                output_file.write(contig_name + "\t" + 
                                  tag + "\t" + str(d[tag]) + "\n")

def gene_expression_2matrix(in_ace, out_file, tags, min_seq):
    """Count sequences with each tags in all contigs.
    
    """
    print
    print "USING MATRIX OUTPUT FORMAT"
    print
    ace_gen = Ace.parse(open(in_ace, 'r'))
    with open(out_file, "w") as output_file:
        output_file.write("gene_name\tgene_length")
        for tag in tags:
            output_file.write("\t" + tag)
        output_file.write("\tXX_noTag")
        output_file.write("\n")
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
            sequences = read_fasta_2list(align.format("fasta"))
            if len(sequences) < min_seq:
                continue
            contig_name = re.findall("(Contig_[0-9]+)", sequences[0][0])[0]
            contig_seq = sequences[0][1].replace("*", "")
            contig_length = str(len(contig_seq))
            output_file.write(contig_name + "\t" + contig_length)
            print "Treating", contig_name
            d = defaultdict(int)
            for tag in tags:
                d[tag] = 0
            d["XX_noTag"] = 0
            fasta_counter = 0
            for fasta in sequences:
                fasta_counter += 1
                found_tag = 0
                for tag in tags:
                    if fasta[0].find(tag) > -1:
                        d[tag] += 1
                        found_tag = 1
                if found_tag == 0 and fasta[0].find("Consensus") < 0:
                    d["XX_noTag"] += 1
            for tag in sorted(d):
                output_file.write("\t" + str(d[tag]))
            output_file.write("\n")

def help():
    _plateform = platform.system()
    name = __program_name__
    text = """
%s(1)                   User Commands                   %s(1)

\033[1mNAME\033[0m
\t%s - From ACE format to individual gene expression

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]... [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tCount the number of sequences for each tag in each contig.

\t%s uses the Biopython library to parse an ACE file containing
\tNext Generation Sequencing contig alignments with sequences tagged
\taccording to the individual from which they originate. It also
\timports a file containing a list of tag names (one tag name per line)
\tin order to count the number of sequences from each individuals
\tcontribute to a contig. It then writes a file containing the sequence
\tcount for each tag in each contig (see output format below).

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the manual of this program

\t\033[1m-i, --input\033[0m
\t\tInput file in .ACE format

\t\033[1m-o, --output\033[0m
\t\tOutput file in tabulated text format

\t\033[1m-t, --tags\033[0m
\t\tInput tags file with one tag name per line

\t\033[1m-m, --minsequences\033[0m
\t\tMinimum number of sequences in order for a contig to be used

\t\033[1m-f, --format\033[0m
\t\tOutput format (use digit):
\t\t1 - Matrix, one line per gene (default)
\t\t2 - Column, n + 2 lines per gene (n is the number of tags)

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

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:t:m:f:", ["help",
                     "input=", "output=", "tags=", 
                     "minsequences=", "format="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_ace = value
            output_snpcount = input_ace.replace(".ace", "") + "_snp_count.txt"
        elif option in ('-t', '--tags'):
            input_tags = value
        elif option in ('-o', '--output'):
            output_snpcount = value
        elif option in ('-m', '--minsequences'):
            min_sequences = value
        elif option in ('-f', '--format'):
            output_format = value
    try:
        with open(input_ace) as test:
            pass
    except:
        print "Input Error: No ACE file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(input_tags) as test:
            pass
    except:
        print "Input Error: No tags file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        min_sequences = int(min_sequences)
    except:
        print "Using all sequences"
        min_sequences = 0
    try:
        output_format = int(output_format)
    except:
        print "Input Error: Format must be specified as an integer."
        print "Use -h for help."
        sys.exit(0)
    
    tags = import_tags(input_tags)
    if output_format == 1:
        gene_expression_2matrix(input_ace, output_snpcount, tags, min_sequences)
    elif output_format == 2:
        gene_expression_2column(input_ace, output_snpcount, tags, min_sequences)
    else:
        print "Input Error: Select from available formats"
        print "Use -h for help."
        sys.exit(0)

if __name__ == "__main__":
    main()
