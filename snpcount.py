#!/usr/bin/env python
# -*- coding: utf-8 -*-

# snpcount.py
# From ACE format to SNP individual genotype table

# Eric Normandeau
# 2009 04 07

# Create a snp_genotype.txt file containing snp genotypes from an
# input_file.ace, a snp table file, and a tag list file

__authors__ = "Eric Normandeau and Nicolas Maillet"
__program_name__ = "snpcount"
__version_info__ = ('0', '0', '5')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-06-08"


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

def build_snp_dict(in_snp):
    d = defaultdict(list)
    with open(in_snp) as f:
        for line in f:
            if line.strip() != "":
                temp = line.strip().split("\t")
                contig = temp[0]
                snp = int(temp[1])
                d[contig].append(snp)
    return d

def import_tags(in_tags):
    tags = []
    with open(in_tags) as f:
        for line in f:
            if line.strip() != "":
                tags.append(line.strip())
    return tags

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

def correct_position(pos, seq):
    current_pos = 0
    correct_pos = 0
    while current_pos < pos:
        if seq[correct_pos] != "*":
            current_pos +=1
        correct_pos += 1
    return(correct_pos)

def snp_count(in_ace, out_file, snp_dict, tags, win_len, max_del, stars):
    """Genotype individuals at SNPs loci.
    
    """
    win_buffer = (win_len - 1) / 2
    ace_gen = Ace.parse(open(in_ace, 'r'))
    with open(out_file, "w") as output_file:
        output_file.write("Contig_nb\tPos\ttag_name\tA\tC\tG\tT\tN\t*\t-\n")
        while 1:
            try:
                contig = ace_gen.next()
            except:
                print "***All contigs treated***"
                break
            align = Alignment(Gapped(IUPAC.ambiguous_dna, "-"))
            align.add_sequence(contig.name, contig.sequence)
            for readn in xrange(len(contig.reads)):
                clipst = contig.reads[readn].qa.qual_clipping_start # GOOD
                clipe = contig.reads[readn].qa.qual_clipping_end # GOOD
                clipst2 = contig.reads[readn].qa.align_clipping_start # Added
                clipe2 = contig.reads[readn].qa.align_clipping_end # Added
                if clipst2 > clipst: # Added
                    clipst = clipst2 # Added
                if clipe2 < clipe2: # Added
                    clipe = clipe2 # Added
                start = contig.af[readn].padded_start
                seq = cut_ends(contig.reads[readn].rd.sequence, clipst, clipe)
                seq = pad_read(seq, start, len(contig.sequence))
                if "pseudo" not in contig.reads[readn].rd.name:
                    align.add_sequence(contig.reads[readn].rd.name, seq)
            sequences = read_fasta(align.format("fasta"))
            contig_name = re.findall("(Contig_[0-9]+)", sequences[0][0])[0]
            print "Treating", contig_name
            positions = []
            try:
                positions = snp_dict[contig_name]
            except:
                continue
            d = {}
            for pos in positions:
                if stars == True:
                    pos_ok = correct_position(pos, sequences[0][1])
                else:
                    pos_ok = pos
                left = pos_ok - 5
                if left < 0:
                    left = 0
                right = pos_ok + 1 + 5 # takes into account the middle nucleotide
                ref_window = sequences[0][1][left:right]
                d.setdefault(pos, {})
                d[pos].setdefault("XX_noTag", {})
                for nuc in list("ACGTN*-"):
                    d[pos]["XX_noTag"].setdefault(nuc, 0)
                for tag in tags:
                    d[pos].setdefault(tag, {})
                    for nuc in list("ACGTN*-"):
                        d[pos][tag].setdefault(nuc, 0)
                for fasta in sequences:
                    window = fasta[1][left:right]
                    del_count = 0
                    if window.count("-") > win_buffer - 3:
                        continue # Need at least 3 nucleotides on each side
                    for tag in tags:
                        if tag in fasta[0]:
                            t = tag
                            break
                        else:
                            t = "XX_noTag"
                    if len(ref_window) == len(window):
                        for i in xrange(len(window)):
                            if ref_window[i].isalpha() and window[i] == "*" or \
                               window[i].isalpha() and ref_window[i] == "*":
                                del_count += 1
                    if del_count > max_del:
                        continue
                    p = pos
                    s = fasta[1] # Sequence
                    n = s[pos_ok - 1].upper()
                    d[p][t][n] += 1
            for p in sorted(d):
                for t in sorted(d[p]):
                    output_file.write(contig_name + "\t" + str(p) + "\t" + 
                                      str(t))
                    for n in list("ACGTN*-"):
                        output_file.write("\t" + str(d[p][t][n]))
                    output_file.write("\n")

def help():
    _plateform = platform.system()
    name = __program_name__
    text = """
%s(1)                   User Commands                   %s(1)

\033[1mNAME\033[0m
\t%s - From ACE format to SNP individual genotype table

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]... [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tExtract SNP genotypes from an ACE file and a SNP table file.

\t%s uses the Biopython library to parse an ACE file containing
\tNext Generation Sequencing contig alignments with sequences tagged
\taccording to the individual from which they originate. It also
\timports a table of SNPs (see SNP table format below) and a file
\tcontaining a list of tag names (one tag name per line) in order to
\tgenotype the individuals for each SNP and then writes a file
\tcontaining the genotypes (see output format below).

\t\033[1mSNP table format\033[0m (tabulated, two columns. \
Do not include line for column names):

\tContig\tSNP_position
\tContig_1\t134
\tContig_3\t27
\t...
\tContig_2538\t45

\t\033[1mOutput format\033[0m (tabulated, nine columns. \
One line for column names):

\tContig   Pos   tag_name  A   C   G   T   N   *   -
\tCont_1   236   Tag02     33  22  0   1   0   3   87
\tCont_3   23    Tag13     2   28  0   84  2   0   125
\t...
\tCont_N   331   Tag04     14  0   0   0   0   0   67

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the manual of this program

\t\033[1m-i, --input\033[0m
\t\tInput file in .ACE format

\t\033[1m-o, --output\033[0m
\t\tOutput file in tabulated text format

\t\033[1m-s, --snptable\033[0m
\t\tInput SNP table file (see format above)

\t\033[1m-t, --tags\033[0m
\t\tInput tags file with one tag name per line

\t\033[1m-w, --windowlength\033[0m
\t\tSNP evaluation window length used for quality criterion
\t\tMust be an odd number, defaulted to 11

\t\033[1m-d, --maxindel\033[0m
\t\tMaximum number of indels acceptable in the SNP evaluation
\t\twindow. Defaulted to 2.
\t\tindels should be represented by the '*' character

\t\033[1m-S, --stars\033[0m
\t\tWhether insertions ('*') are present in the contig sequence.
\t\tDefaulted to no.
\t\tUse yes or no

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
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:s:t:w:d:S:", ["help",
                     "input=", "output=", "snptable=", "tags=",
                     "windowlength=", "maxindel=", "stars="])
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
            output_snpcount = input_ace.replace(".ace", "") + "_snp_count.txt"
        elif option in ('-s', '--snptable'):
            input_snptable = value
        elif option in ('-t', '--tags'):
            input_tags = value
        elif option in ('-o', '--output'):
            output_snpcount = value
        elif option in ('-w', '--windowlength'):
            window_length = value
        elif option in ('-d', '--maxindel'):
            maximum_indels = value
        elif option in ('-S', '--stars'):
            if value in ('yes', 'Yes', 'y', 'Y', '1'):
                stars = True
            elif value in ('no', 'No', 'n', 'N', '0'):
                stars = False
            else:
                print "Input Error: -S option parameter not recognized"
                print "Use -h for help"
                sys.exit(0)
    try:
        with open(input_ace) as test:
            pass
    except:
        print "Input Error: No ACE file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(input_snptable) as test:
            pass
    except:
        print "Input Error: No SNP table file specified or file not found."
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
        window_length = int(window_length)
    except:
        print "SNP evaluation window must be an integer"
    if int(window_length)%2 != True:
        print "SNP evaluation window length must be an odd number."
        sys.exit(0)
    try:
        maximum_indels = int(maximum_indels)
    except:
        print "Maximum number of indels must be an integer"
        sys.exit(0)
    
    tags = import_tags(input_tags)
    snps = build_snp_dict(input_snptable)
    snp_count(input_ace, output_snpcount, snps, tags,
              window_length, maximum_indels, stars)

if __name__ == "__main__":
    main()
