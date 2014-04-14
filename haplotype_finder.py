#!/usr/bin/env python
# -*- coding: utf-8 -*-

# snpcount.py
# From ACE format to haplotypes

__authors__ = "Eric Normandeau"
__program_name__ = "haplotype_finder"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2011-03-07"


# Module imports

import getopt
import sys
import platform
import re
from math import sqrt
from collections import defaultdict
from itertools import islice
from itertools import groupby

from Bio.Sequencing import Ace
from Bio.Align.Generic import Alignment
from Bio.Alphabet import IUPAC, Gapped


# Function definitions

def help():
    _plateform = platform.system()
    name = __program_name__
    text = """
%s(1)             User Commands            %s(1)

\033[1mNAME\033[0m
\t%s - From ACE format to haplotypes

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]... [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tExtract haplotypes from an ACE file.

\t%s uses the Biopython library to parse an ACE file
\tcontaining Next Generation Sequencing contig alignments. It scans the
\tcontigs to find windows of a defined length with a minimal sequence
\tcoverage. For the contigs where such a window is found, it returns the
\tpossible haplotypes for that window.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the manual of this program

\t\033[1m-i, --input\033[0m
\t\tInput file in .ACE format

\t\033[1m-o, --output\033[0m
\t\tOutput file in tabulated text format

\t\033[1m-w, --windowlength\033[0m
\t\tCoverage evaluation window length
\t\tDefault value: 100

\t\033[1m-s, --step\033[0m
\t\tWindow step distance
\t\tDefault value: 10

\t\033[1m-c, --coverage\033[0m
\t\tMinimum coverage over window for haplotype extraction
\t\tDefault value: 10

\t\033[1m-S, --stars\033[0m
\t\tWhether insertions ('*') are present in the contig sequence.
\t\tDefaulted to no.
\t\tUse yes or no

\t\033[1m-g, --groups\033[0m
\t\tMinimum number of groups with haplotype information
\t\tContigs with less than this value will be discarted
\t\tDefaulted to 2

\t\033[1m-n, --num_haplotypes\033[0m
\t\tMinimum number of haplotypes per group
\t\tContigs with less than this value will be discarted
\t\tDefaulted to 8


\033[1mAUTHORS\033[0m
\t%s

%s %s              %s            %s(1)
"""%(name, name, name, name, name, __authors__, name, __version__, __revision_date__, name)
    if _plateform != 'Windows' and "this is cool":
        print text
    else:
        remove = ["\033[1m","\033[0m","\033[4m"]
        for i in remove:
            text = text.replace(i, "")
        print text

def cut_ends(read, start, end):
    """Replace residues on either end of a sequence with gaps.
    
    Cut out the sections of each read which the assembler has decided are not
    good enough to include in the contig and replace them with gap
    
    """ 
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

def multi_find(search,text,start=0):
    """Find positions for a multiple search
    
    """
    positions = []
    while start > -1:
        pos = text.find(search, start)
        if pos > -1:
            positions.append(pos)
            start = pos + 1
        else:
            return positions

def sliding_window(seq, win, step=1):
    """Sliding window over seq by step distance
    
    """
    n = 1 + (len(seq) - win) / step
    for i in range(0, n * step, step):
        yield [i,i + win]

def correct_sequence(concensus, seq):
    """Correct sequencing deletions according to concensus sequence
    
    """
    corrected_seq = ""
    for i, cn in enumerate(concensus):
        sn = seq[i] # consensus nucleotide and sequence nucleotide
        if sn == "*":
            corrected_seq += cn
        else:
            corrected_seq += sn
    return corrected_seq

def most_common(L):
    """Get the most common element from a list
    
    """
    return max(groupby(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]


def snp_positions(sequences, min_cov=20, min_freq=0.05, min_count=3):
    """Find position of SNP variants from a contig alignment
    
    """
    again = True
    nuc_counts = []
    problematic = False
    while again == True:
        positions = []
        seqs = [s[1] for s in sequences] # Keep only the sequences
        seq_len = len(seqs[0])
        removed = False
        nsnps = 0
        for i in range(seq_len):
            nucs = [s[i] for s in seqs if s[i] != "-" and s[i] != "N"]
            set_nucs = set()
            try:
                most_freq = most_common(nucs)
            except:
                most_freq = []
            if len(nucs) >= min_cov and len(most_freq) == 1:
                set_nucs.update(nucs)
                nuc_counts = sorted([["".join(nucs).count(n), n]
                                     for n in list(sorted(set_nucs))],
                                     reverse=True)
                if len(nuc_counts) == 2: # Treating biallelic SNPs
                    if nuc_counts[-1][0] >= min_count and \
                        float(nuc_counts[-1][0]) / sum([c[0] for c in nuc_counts]) >= min_freq:
                        nsnps += 1
                        positions.append(i)
                if len(nuc_counts) == 3: # Treating triallelic SNPs
                    if nuc_counts[-1][0] >= min_count and \
                        float(nuc_counts[-1][0]) / (sum([c[0] for c in nuc_counts]) +
                              nuc_counts[1][0]) >= min_freq:
                        nsnps += 1
                        positions.append(i)
                    elif nuc_counts[-2][0] >= min_count and \
                        float(nuc_counts[-2][0]) / sum([c[0] for c in nuc_counts]) >= min_freq:
                        sequences = [[s[0], s[1][:i] +
                                      s[1][i].replace(nuc_counts[-1][1],
                                      nuc_counts[0][1])+ s[1][i+1:]] 
                                      for s in sequences]
                        removed = True
                if len(nuc_counts) == 4: # Treating quadriallelic SNPs
                    if nuc_counts[-1][0] >= min_count and \
                        float(nuc_counts[-1][0]) / (sum([c[0] for c in nuc_counts]) +
                              nuc_counts[1][0] + nuc_counts[2][0]) >= min_freq:
                        nsnps += 1
                        positions.append(i)
                    elif nuc_counts[-3][0] >= min_count and \
                        float(nuc_counts[-3][0]) / sum([c[0] for c in nuc_counts]) >= min_freq:
                        sequences = [[s[0], s[1][:i] +
                                      s[1][i].replace(nuc_counts[-1][1],
                                      nuc_counts[0][1])+ s[1][i+1:]] 
                                      for s in sequences]
                        removed = True
        if removed == False:
            again = False
    if len(positions) >= 2:
        ratio = float(len(positions)) / (positions[-1] - positions[0])
        if ratio >= 1. / 20: # Number of SNPs found per bases
            problematic = True
    if problematic:
        positions = []
    return sequences, positions

def best_snps(sequences, positions, coverage):
    """Find the longuest consecutive SNP postions with the good coverage
    
    """
    best_hap_info = "Empty"
    haplotypes = {}
    scores = []
    for i in xrange(3, 9):
        for w in sliding_window(positions, i):
            list_pos = positions[w[0]: w[1]]
            pos = "_".join([str(x) for x in list_pos])
            haplotypes[pos] = []
            for s in sequences:
                name = s[0]
                seq = s[1]
                haplotypes[pos].append([name, list_pos, seq[list_pos[0]:list_pos[-1]+1], ""])
                for p in list_pos:
                    haplotypes[pos][-1][-1] += seq[p]
            haplotypes[pos] = [h for h in haplotypes[pos] if "-" not in h[-1]]
            if len(haplotypes[pos]) >= coverage:
                nvar = len(list_pos)
                cov = len(haplotypes[pos])
                ratio = (len(list_pos) -1) / float(list_pos[-1] - list_pos[0] + 1)
                index = (cov + 5 * nvar) / sqrt(ratio)
                varies = True
                for p in xrange(len(list_pos)):
                    if len(list(set([h[-1][p] for h in haplotypes[pos]]))) == 1:
                        varies = False
                info = [index, nvar, cov, ratio, list_pos, varies]
                if ratio <= 0.05:
                    scores.append(info)
    if len(scores) > 0:
        scores = [s[:-1] for s in scores if s[-1] == True]
        scores = list(sorted(scores, reverse=True))
        try:
            best_score = scores[0]
            best_hap = haplotypes["_".join([str(x) for x in best_score[-1]])]
            best_hap_info = [int(scores[0][0]), len(scores[0][-1]), best_hap]
        except:
            pass # Will return "Empty"
    return best_hap_info

def get_haplotypes(in_ace, out_file, out_bamova, win_len, step,
                   coverage, stars, ngroups, nhaplo):
    """Get haplotypes from contigs in an ace file
    
    """
    marker_number = 0
    min_freq = 0.05
    ace_gen = Ace.parse(open(in_ace, 'r'))
    with open(out_file, "w") as output_file:
        with open(out_bamova, "w") as bamova_file:
            output_file.write("Contig_nb\tWindow\tHaplotype\n")
            contig_counter = 0
            ntreated = 0
            for contig in ace_gen:
                pass_haplo = False
                contig_counter += 1
                align = Alignment(Gapped(IUPAC.ambiguous_dna, "X"))
                align.add_sequence(contig.name, contig.sequence)
                if len(contig.reads) -1 < coverage:
                    continue
                ntreated += 1
                for readn in xrange(len(contig.reads)):
                    clipst = contig.reads[readn].qa.qual_clipping_start
                    clipe = contig.reads[readn].qa.qual_clipping_end
                    clipst2 = contig.reads[readn].qa.align_clipping_start
                    clipe2 = contig.reads[readn].qa.align_clipping_end
                    if clipst2 > clipst:
                        clipst = clipst2
                    if clipe2 < clipe2:
                        clipe = clipe2
                    start = contig.af[readn].padded_start
                    seq = cut_ends(contig.reads[readn].rd.sequence, clipst, clipe)
                    seq = pad_read(seq, start, len(contig.sequence))
                    if "pseudo" not in contig.reads[readn].rd.name:
                        align.add_sequence(contig.reads[readn].rd.name, seq)
                sequences = read_fasta(align.format("fasta"))
                sequences = [[s[0].replace(">", ""), s[1]] for s in sequences]
                contig_name = sequences[0][0]
                concensus = sequences[0][1]
                error_positions = multi_find("*", concensus)[::-1]
                for p in error_positions:
                    sequences = [[s[0], s[1][0:p] + s[1][p+1:]] for s in sequences]
                concensus = sequences[0][1]
                sequences = [[s[0], correct_sequence(concensus, s[1])]
                             for s in sequences[1:]]
                sequences, snp_pos = snp_positions(sequences)
                haplotypes = best_snps(sequences, snp_pos, coverage)
                if haplotypes != "Empty":
                    bamova = []
                    variants = list(sorted(list(set([h[-1] for h in haplotypes[-1]]))))
                    groups = list(sorted(set([h[0][:3] for h in haplotypes[-1]])))
                    if len(groups) >= ngroups:
                        pass_haplo = True
                        for g in groups:
                            if len([h[0] for h in haplotypes[-1] if h[0].startswith(g)]) < nhaplo:
                                pass_haplo = False
                    if pass_haplo:
                        print contig.name
                        bamova_file.write("Marker" + str(marker_number) + "\n")
                        group_number = 0
                        for g in groups:
                            bamova_file.write("Population\t" + str(group_number))
                            group_number += 1
                            for v in variants:
                                bamova_file.write("\t" + str(len([h for h in haplotypes[-1]
                                                  if h[-1] == v and h[0].startswith(g)])))
                            bamova_file.write("\n")
                        with open ("fasta_output/" + contig.name + ".fasta", "w") as f:
                            output_file.write(contig.name + "\n")
                            for h in haplotypes[-1]:
                                f.write(">" + h[0] + str(marker_number) + "\n" + h[2] + "\n")
                                h[1] = [x - h[1][0] + 1 for x in h[1]]
                                output_file.write("Marker" + str(marker_number) + "\t" +
                                                  "\t".join([str(x) for x in h]) + "\t" +
                                                  ":".join(variants) + "\n")
                        marker_number += 1
                output_file.flush()
                bamova_file.flush()
                cutoff = 100000
                if contig_counter > cutoff:
                    break
        print "\n", str(ntreated), "contigs out of", str(contig_counter), "were treated"


# Haplotype finder
# Was born on a stormy day
# From a composed mind

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:b:w:s:c:S:g:n:", ["help",
                     "input=", "output=", "bamova=", "windowlength=", "step=",
                     "coverage=", "stars=", "groups=", "num_haplotypes="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    window_length = 100
    step = 10
    coverage = 10
    stars = False
    ngroups = 2
    nhaplo = 8
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_ace = value
            output_snpcount = input_ace.replace(".ace", "") + "_snp_count.txt"
        elif option in ('-o', '--output'):
            output_file = value
        elif option in ('-b', '--bamova'):
            output_bamova = value
        elif option in ('-w', '--windowlength'):
            window_length = value
        elif option in ('-c', '--coverage'):
            coverage = value
        elif option in ('-s', '--step'):
            step = value
        elif option in ('-S', '--stars'):
            if value in ('yes', 'Yes', 'y', 'Y', '1'):
                stars = True
            elif value in ('no', 'No', 'n', 'N', '0'):
                stars = False
            else:
                print "Input Error: Wrong value for option of -s"
                print "Use -h for help"
                sys.exit(0)
        elif option in ('-g', '--group'):
            ngroups = value
        elif option in ('-n', '--num_haplotypes'):
            nhaplo = value
            
    try:
        with open(input_ace) as test:
            pass
    except:
        print "Input Error: No ACE file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(output_file, "w") as test:
            pass
    except:
        print "No output file specified."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(output_bamova, "w") as test:
            pass
    except:
        print "No bamova file specified."
        print "Use -h for help."
        sys.exit(0)
    try:
        window_length = int(window_length)
    except:
        print "Window length must be an integer"
        print "Use -h for help."
        sys.exit(0)
    try:
        step = int(step)
    except:
        print "Step length must be an integer"
        print "Use -h for help."
        sys.exit(0)
    try:
        coverage = int(coverage)
    except:
        print "Coverage must be an integer"
        print "Use -h for help."
        sys.exit(0)
    if step > window_length:
        print "Warning: Steps are longer than window size!"
    try:
        ngroups = int(ngroups)
    except:
        print "Minimum number of groups (-g) must be an integer"
        print "Use -h for help."
        sys.exit(0)
    try:
        nhaplo = int(nhaplo)
    except:
        print "Minimum number of haplotypes (-n) must be an integer"
        print "Use -h for help."
        sys.exit(0)
    
    get_haplotypes(input_ace, output_file, output_bamova, window_length, step, coverage, stars, ngroups, nhaplo)

if __name__ == "__main__":
    main()

