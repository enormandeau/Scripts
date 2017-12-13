#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Find stop codons and longuest ORF from blastx results
__authors__ = "Eric Normandeau"
__program_name__ = "stop_codons_find"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2011-01-14"

# Importing modules
import os
import sys
import getopt
import platform
from Bio import SeqIO

# Class definitions
# !!! This program REALLY needs a class definition for each sequence !!!

# Function definitions
def help():
    """Help attained by typing './program_name.py -h'
    """
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)            User Commands         %s(1)

\033[1mNAME\033[0m
\t%s - Find stop codons in nucleotide sequences

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]    [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tReport the presence and position of stop codons in a fasta file

\t%s used Biopython to pass through a fasta file and report
\tthe presence of stop codons in the sequences.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-i, --input\033[0m
\t\tInput fasta file. This file is expected to contain
\t\tsequences that have been trimmed to start in a reading frame.

\t\033[1m-o, --output\033[0m
\t\tOutput result file containing the name of the sequences and
\t\tthe positions of the stop codons, if they contain some.

\033[1mAUTHORS\033[0m
\t%s

%s %s           %s          %s(1)
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

def find_stop_codons(fasta_sequences):
    """Find stop codons in the sequences of a fasta file
    """
    aa_chains = [] # Amino acid chains
    for seq in fasta_sequences:
        aa_chains.append(translate_sequence(seq))
    return get_stop_positions(aa_chains)

def translate_sequence(sequence):
    """Translate a nucleotide sequence into an amino acid chain
    
    Return it's name and sequence in a list
    """
    codon_length = 3
    chain = ""
    name, seq = sequence.id, sequence.seq.tostring()
    if len(seq) % 3 != 0: # Use assert instead
        print "All sequence lengths must be factors of 3"
        sys.exit(0)
    for codon_start in xrange(0, len(seq), 3):
        codon_end = codon_start + 3
        codon = seq[codon_start:codon_end]
        chain += translate(codon)
    return [name, seq, "good_seq", chain]

def translate(codon): # VERIFY translation matrix!!!
    """Translate codons in amino acids using the XXXX code
    """
    code = {     'ttt': 'F', 'tct': 'S', 'tat': 'Y', 'tgt': 'C',
                 'ttc': 'F', 'tcc': 'S', 'tac': 'Y', 'tgc': 'C',
                 'tta': 'L', 'tca': 'S', 'taa': '*', 'tga': '*',
                 'ttg': 'L', 'tcg': 'S', 'tag': '*', 'tgg': 'W',
                 'ctt': 'L', 'cct': 'P', 'cat': 'H', 'cgt': 'R',
                 'ctc': 'L', 'ccc': 'P', 'cac': 'H', 'cgc': 'R',
                 'cta': 'L', 'cca': 'P', 'caa': 'Q', 'cga': 'R',
                 'ctg': 'L', 'ccg': 'P', 'cag': 'Q', 'cgg': 'R',
                 'att': 'I', 'act': 'T', 'aat': 'N', 'agt': 'S',
                 'atc': 'I', 'acc': 'T', 'aac': 'N', 'agc': 'S',
                 'ata': 'I', 'aca': 'T', 'aaa': 'K', 'aga': 'R',
                 'atg': 'M', 'acg': 'T', 'aag': 'K', 'agg': 'R',
                 'gtt': 'V', 'gct': 'A', 'gat': 'D', 'ggt': 'G',
                 'gtc': 'V', 'gcc': 'A', 'gac': 'D', 'ggc': 'G',
                 'gta': 'V', 'gca': 'A', 'gaa': 'E', 'gga': 'G',
                 'gtg': 'V', 'gcg': 'A', 'gag': 'E', 'ggg': 'G'
            }
    assert len(codon) == 3, "Codon of wrong length"
    assert codon.isalpha(), "Codon contains non alphabetic characters"
    codon = codon.lower().replace("u", "t")
    standard_nuc = ["a", "c", "t", "g"]
    for n in codon:
        assert n in standard_nuc, "Unknown nucleotide found in codon"
    try:
        aa = code[codon]
    except:
        aa = "!"
        print "Warning! Found an inexistant codon, translating as '!'"
    return aa

def get_stop_positions(aa_chains):
    """Get stop codon position from a list of proteins
    """
    stops = []
    for chain in aa_chains:
        stops.append([chain[0],
                     "_".join(["0"] + [str(x) for x in multi_find("*", chain[3])]),
                     "", "", chain[1], chain[2],str(len(chain[3])), chain[3]])
    return stops

def multi_find(search,text,start=0):
    positions = []
    while start > -1:
        pos = text.find(search, start)
        if pos > -1:
            positions.append(pos)
            start = pos + 1
        else:
            return positions

def trim(sequences):
    """Trim sequences to the longuest stretch of uninterrupted amino acids
    """
    for seq in sequences:
        longuest = longuest_stretch(seq[1], seq[6])
        seq[2] = "_".join([str(x) for x in longuest])
        start_aa, stop_aa = seq[2].split("_")
        seq[3] = "_".join([str(int(start_aa) * 3), str(int(stop_aa) * 3)])
        start, stop = [int(x) for x in seq[3].split("_")]
        seq[5] = seq[4][start:stop]
    return sequences

def longuest_stretch(positions, length):
    """Find the longuest stretch of amino acids in a sequence
    
    Known limitation: Will keep one longuest stretch randomly in case of ties
    """
    stretches = {}
    positions = positions.split("_") + [length]
    for i in xrange(len(positions) - 1):
        start = int(positions[i])
        stop = int(positions[i + 1])
        l = stop - start
        stretches[l] = [start, stop]
    longuest = list(sorted(stretches.keys()))[-1]
    return stretches[longuest]

def output_results(results, output_file):
    """Print results to output file
    """
    with open(output_file, "w") as f:
        f.write("\t".join(["seq_name", "stops", "longuest_aa", "longuest_nuc",
                "seq_nuc", "seq_good", "len_seq", "seq_aa\n"]))
        for res in results:
            f.write("\t".join(res) + "\n")


# stop_codons_find looks
# for annoying stop codons
# hated by Genbank

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help",
            "input=", "output="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_file = value
        elif option in ('-o', '--output'):
            output_file = value
    try:
        with open(input_file) as test:
            pass
    except:
        print "Input Error: No input file specified or file not found."
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
    print "Authors:", __authors__
    print

    fasta_sequences = SeqIO.parse(open(input_file),'fasta')
    sequences = find_stop_codons(fasta_sequences)
    results = trim(sequences)
    output_results(results, output_file)

