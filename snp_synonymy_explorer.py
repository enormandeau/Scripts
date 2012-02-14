#!/usr/bin/python
# -*- coding: utf-8 -*-

# Find synonymous and non-synonymous SNP variants in fasta alignments

__authors__ = "Eric Normandeau"
__program_name__ = "synonym_storm"
__version_info__ = ('0', '0', '3')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-06-14"


# Importing modules

import os
import sys
import getopt
import platform

from Bio import SeqIO


# Class definitions

class AutoDict(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


# Function definitions

def help():
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)                  User Commands                %s(1)

\033[1mNAME\033[0m
\t%s - Synonymous vs. non-synonymous SNPs in fasta alignments

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]    [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tCount SNP variants in a fasta alignment file.

\t%s uses the Biopython library to parse a fasta file
\tcontaining aligned sequences all trimmed to the same length
\t(including missing nucleotides, represented by "-") and
\tstarting at the +1 nucleotide of the proper reading frame.

\tIt then counts possible SNP variants for each position in the aligned
\tsequences and determines whether the substitution is synonymous or
\tnon-synonymous. Optionally, the variant count can be done separatly
\tfor user specified groups. The output is redirected to a file
\tcontaining the name of the input file plus one variant per line with
\tthe position, count for the frequent and rare variants, either total
\tor separated per group, and the impact of the substitution (synonymous
\tor not). To use more than one group, specify a group text file
\tcontaining one group identifier per line. These names must be found
\tin the names of the sequences in the alignment input file. See the
\toutput format below.

\033[1mOUTPUT FORMAT\033[0m
\tInput_filename.txt
\tPos   Freq  Rare  Syn
\t34    A:22  T:3   Yes
\t62    T:8   G:4   No
\t88    C:32  G:6   Yes
\t107   A:22  C:3   Yes
\t131   G:12  T:11  No

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-i, --input\033[0m
\t\tInput file, in fasta format

\t\033[1m-o, --output\033[0m
\t\tOutput file, in fasta format

\t\033[1m-g, --group\033[0m
\t\tOptional group file

\033[1mAUTHORS\033[0m
\t%s

%s %s                  %s                %s(1)
"""%(name, name, name, name, name, __authors__, name, __version__, __revision_date__, name)
    
    if _plateform != 'Windows' and "this is great news":
        print text
    else:
        __Windows__ = "This is an abomination"
        remove = ["\033[1m","\033[0m","\033[4m"]
        for i in remove:
            text = text.replace(i, "")
        print text
        del(__Windows__) # If only we could...

def import_groups(group_file):
    groups = []
    try:
        with open(group_file) as test:
            pass
    except:
        print "Input Error: Group file not found."
        print "Use -h for help."
        sys.exit(0)
    with open(group_file) as f:
        for line in f:
            if line.strip() != "":
                groups.append(line.strip())
    return groups

def good_positions(in_file, out_folder, out_file, groups, min_count=2):
    """Count SNP variants in a fasta alignment file"""
    fasta_sequences = SeqIO.parse(open(in_file),'fasta')
    output_path = os.path.join(out_folder, out_file)
    try:
        with open (output_path, "w") as test:
            pass
    except:
        print "Created", "'"+ out_folder +"'", "folder to put result files in"
        os.mkdir(out_folder)
    end = 0
    names = []
    sequences = []
    mega_dict = AutoDict()
    codon_length = 3
    while end == 0:
        try:
            temp_fasta = fasta_sequences.next()
            temp_name, temp_sequence = temp_fasta.id, temp_fasta.seq.tostring()
            names.append(temp_name)
            if len(temp_sequence) % 3 != 0:
                print "All sequence lengths must be factors of 3"
                sys.exit(0)
            sequences.append(temp_sequence)
        except:
            print "All sequences treated"
            end = 1
    try:
        len_seqs = len(sequences[0])
    except:
        print "No sequences were found"
        sys.exit(0)
    num_seqs = len(names)
    all_groups = "all"
    for i in xrange(0, len_seqs, 3):
        codon_start = i
        codon_end = codon_start + 3
        codons = [seq[codon_start:codon_end] for seq in sequences]
        for j in xrange(codon_length):
            pos = str(i) + "-" + str(j)
            for k in xrange(num_seqs):
                codon = codons[k]
                if "-" not in codon:
                    name = names[k]
                    group = "No_group"
                    variant = codon[j]
                    for g in groups:
                        if name.startswith(g):
                            group = g
                    try:
                        mega_dict[pos][codon][group] += 1
                    except:
                        mega_dict[pos][codon][group] = 1
    snp_dict = AutoDict()
    with open(output_path, "w") as f:
        many_variants = set()
        for p in sorted(mega_dict):
            if len(mega_dict[p]) > 2:
                many_variants.add(p.split("-")[0])
            good_pos = True
            for v in sorted(mega_dict[p]):
                count = 0
                for g in sorted(mega_dict[p][v]):
                    count += mega_dict[p][v][g]
                if count < min_count:
                    good_pos = False
            if good_pos == True and len(mega_dict[p]) == 2:
                snp_dict[p] = mega_dict[p]
        for i in sorted([int(x) for x in many_variants]):
            f.write(str(i + 1) + "  has more than 2 variants\n")
        f.write("\nBegining of data:\n-----------------\n")
    good_snps = AutoDict()
    for p in sorted(snp_dict):
        pos_codon, pos_nuc = [int(x) for x in p.split("-")]
        c1 = sorted(snp_dict[p])[0]
        c2 = sorted(snp_dict[p])[1]
        if c1[pos_nuc] != c2[pos_nuc]:
            good_snps[pos_codon + pos_nuc] = snp_dict[p]
    print len(good_snps), "interesting positions found"
    return good_snps

def synonym_output(good_snps, output_path, groups):
    """Output synonym results to file.
    """
    with open(output_path, "a") as f:
        if len(good_snps.keys()) == 0:
            f.write("No interesting snps found for this contig")
            sys.exit(0)
        for p in sorted(good_snps):
            c1 = sorted(good_snps[p])[0]
            c2 = sorted(good_snps[p])[1]
            n1 = good_snps[p][c1]
            n2 = good_snps[p][c2]
            s = are_synonym(c1, c2)
            line_begin = str(p + 1)
            line_c1 = c1
            line_c2 = c2
            for g in groups:
                line_c1 +=  "\t" + g + "\t" + str(n1[g]).replace("{}", "0")
                line_c2 +=  "\t" + g + "\t" + str(n2[g]).replace("{}", "0")
            line = line_begin + "\t" + line_c1 + "\t" + line_c2 + "\t" + s + "\n"
            f.write(line)
        #f.write("And a merry Christmas to you tiny Tim!\n\n")

def are_synonym(c1, c2):
    """Determine if two codons are synonymous
    """
    if translate(c1) == translate(c2):
        synonym = "synonymous"
    else:
        synonym = "non-synonymous"
    return synonym

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


# Main function
# (This is the heart of the program
# Without it, nothing will happen...)

# Synonymous storm
# From sequence jumbo-mumbo
# Brings Truth and Order

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:g:", ["help", "input=",
            "output=", "group="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    output_file = None
    group_file = None
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_file = value
        elif option in ('-o', '--output'):
            output_file = value
        elif option in ('-g', '--group'):
            group_file = value
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
    
    output_folder = "synonym_results"
    output_path = os.path.join(output_folder, output_file)

    print "Using version:", __version__, "of", __program_name__
    print "Last revision:", __revision_date__
    print "By:", __authors__

    if group_file == None:
        groups = []
    else:
        groups = import_groups(group_file)
    
    print
    min_count = 2 # Implement in input options
    good_snps = good_positions(input_file, output_folder, output_file, groups, min_count)
    synonym_output(good_snps, output_path, groups)

if __name__ == "__main__":
    main()
