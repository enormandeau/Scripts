#!/usr/bin/python
# -*- coding: utf-8 -*-

# ngs_prepare_sequences.py
# A suite of utilities for preparing tagged 454 or NGS data for assembly:
# - Identify tag sequences at the begining of 454 sequences
# - Rename sequences according to the tag found
# - Find CAP sequences (and their reverse complements)
# - Remove tag and CAP sequences and corresponding base quality scores

# Note: Once the tag and cap sequences have been removed, it is recommended to
# use another tool to get rid of low complexity regions like microsatellites
# and remaining poly-A or poly-T sequences.

# Code by:
# Eric Normandeau
# from: 2010-03-08
# to:   2010-05-26


# Version history

__version_info__ = ('0', '0', '6')
__version__ = '.'.join(__version_info__)

# From version 0.0.2
# - Revised code form

# From version 0.0.3
# - Revised code for form
# - Annotated CAP sequences in a recursive manner (4h)
# - Annotate tags with 1 bad nucleotides in tag if no tag found

# From version 0.0.4
# - 'Version history' replaces 'New in this version'
# - Improved CAP searching algorithm (sliding window over tag sequence)

# From version 0.0.5
# - Replaced SOME 'open' with 'with open("file") as f
# - Replaced SOME 'for line in f.readlines()' with 'for line in f'

# Todo

# - Replace .setdefault methods for collections.setdefault (see S.Lott on SO)

# - Replace 'for i in d.items()' with 'for k, v in d.items()'
# - Remove global variables from function calls if not appropriate (1h)
# - Fill 'tag_utils_MANUAL.txt' (1h)
# - Add error catching (3h) (try/except and assert)
# - Add main() function for calls from the console (2h)
# - Add GUI (4h, Nicolas Maillet) ???
# - Put on the lab's website (15 min)

# - Approximate remaining work time: 7h Eric, 4h Nicolas


# Bugs and limitation

# Fasta and qual files must match LINE FOR LINE perfectly!
# CAP sequences are searched with a crude algorithm (See MANUAL for more info)
# CAP sequence names in the input CAP fasta file must contain 'Rev' if the CAP
#   to be found on the right side.
# CAP sequences are removed SEQUENCIALLY. Put the ones to be removed first
#   earlier in the INPUT_CAPS file


#   How to use

# - See tag_utils_MANUAL.txt for more information
# - Modify GLOBAL VARIABLES (Section below)
# - Open Python console
# - type 'import tag_utils'
#   (alternatively, from Linux, from the Bash console
#   'time python tag_utils')
# - "Et voila"


# Global variables (to be modified by user)

PROJECT_NAME = "LD"  # To be included in each sequence name
INPUT_FASTA = r"LD.fasta"     # Input fasta file
INPUT_QUAL = r"LD.fasta.qual" # Input qual file
INPUT_TAGS = r"LDtags.fa" # File containing tag sequences to remove (FASTA)
INPUT_CAPS = r"caps.fa" # File containing CAP sequences to remove (FASTA)
TAGS_TO_USE = range(1, 9)
CAPS_TO_USE = "all" # range(1, 5) # Put numbers of tags to be used in a list
# Ex: [1,2,3,4] or range(1, 5) for 1 through 4. Use "all" to use everything.
OUTPUT_FASTA = "noTag_" + INPUT_FASTA  # Output fasta file
OUTPUT_QUAL = "noTag_" + INPUT_QUAL    # Output qual file


# Importing modules

import sys
import platform

                           
# Function definitions

def read_fasta(path): # Should be renamed 'parse_fasta_file'
    # Should use Biopython fasta parser
    """
    Read FASTA file into a list of lists.
    Each inner list contains a name and a sequence.
    
    """
    out = []
    line_counter = -1
    with open(path) as file_:
        for line in file_:
            if line.startswith(">"):
                contig_name = line.split()[0]
                contig_seq = ""
                out.append([contig_name, contig_seq])
            else:
                out[line_counter][1] += line.rstrip()
    return out

def append_fasta(name, sequence, output_file):
    """
    Append fasta or fasta.qual sequence information at the end of a file.
    Output is in FASTA format (>name, sequence).
    
    """
    output_file.write(name + "\n" + sequence + "\n")

def import_sequences(input_seqs, seqs_to_use = "all"):
    """
    Import a list of sequences from a fasta file.
    Used to import tag and CAP sequences.
    User may import only specific sequences (See GLOBAL VARIABLES).
    
    """
    seqs = []
    list_seqs = read_fasta(input_seqs)
    if seqs_to_use != "all":
        for i in seqs_to_use:
            seqs.append(list_seqs[i - 1])
    else:
        seqs = list_seqs
    seqs = [[seq[0][1:], seq[1]] for seq in seqs]
    return seqs

def find_tag(seq_number, fasta_name, fasta_seq, qual_seq, tags, project_name):
    """
    Try to find a tag sequence at the beginning of a fasta sequence.
    Delete tag, modify sequence name, write fasta and fasta.qual.
        
    """
    if fasta_name.find("_Tag") > -1:
        return [fasta_name, fasta_seq, " ".join(qual_seq)]
    new_name = ">" + project_name + "_"
    for tag in tags:
        tag_name = tag[0]
        tag_seq = tag[1]
        tag_length = len(tag[1])
        min_similarity = tag_length - 1
        if fasta_seq.startswith(tag_seq):
            fasta_seq = fasta_seq[tag_length:]
            qual_seq = qual_seq[tag_length:]
            tag_no = tag_name + "_"
            break
        else:
            similarity = 0
            if len(fasta_seq) >= tag_length:
                for i in xrange(tag_length):
                    if tag_seq[i] == fasta_seq[i]:
                        similarity += 1
            if similarity >= min_similarity:
                fasta_seq = fasta_seq[tag_length:]
                qual_seq = qual_seq[tag_length:]
                if len(fasta_seq) == 0:
                    fasta_seq = "N"
                    qual_seq = "0"
                tag_no = tag_name + "_"
            else:
                tag_no = "noTag_"
    new_name += tag_no
    new_name += str("%09i" % seq_number)
    return [new_name, fasta_seq, " ".join(qual_seq)]

def find_cap(seq_number, fasta_name, fasta_seq, qual_seq, caps, project_name):
    """
    Try to find CAP sequences in a fasta sequence.
    Shorten CAP recursively and try to find again.
    Replace left-hand CAPs with 'X' and right-hand ones with 'Y'.
    Delete CAP, DO NOT modify sequence name, write fasta and fasta.qual.
    
    """
    min_percent = 60
    min_length = 9 # Length of minimal CAP portion to search for
    for cap in caps:
        cap_name = cap[0]
        cap_seq = cap[1]
        cap_length = len(cap_seq)
        length = cap_length
        min_percent_length = min_percent * len(cap_seq) / 100
        while length >= min_length and length >= min_percent_length:
            diff = cap_length - length
            for i in xrange(diff + 1):
                if cap_name.find("Rev") == -1:
                    cap_temp = cap_seq[diff - i:]
                    if i > 0:
                        cap_temp = cap_temp[:-i]
                    pos = fasta_seq.rfind(cap_temp)
                    if pos > -1:
                        X = "X" * length
                        fasta_seq = fasta_seq[:pos] + X + \
                            fasta_seq[pos + length:]
                        cap_dict[length] = cap_dict.setdefault(length,0)+1
                else:
                    cap_temp = cap_seq[i:]
                    if diff - i > 0:
                        cap_temp = cap_temp[:-(diff - i)]
                    pos = fasta_seq.find(cap_temp)
                    if pos > -1:
                        Y = "Y" * length
                        fasta_seq = fasta_seq[:pos] + Y + \
                            fasta_seq[pos + length:]
                        cap_dict[length] = cap_dict.setdefault(length,0)+1
            length -= 1
    last_x = fasta_seq.rfind("X")
    if last_x > -1:
        fasta_seq = fasta_seq[last_x + 1 : ]
        qual_seq = qual_seq[last_x + 1 : ]
    first_y = fasta_seq.find("Y")
    if first_y > -1:
        fasta_seq = fasta_seq[ : first_y]
        qual_seq = qual_seq[ : first_y]
    qual_seq = " ".join(qual_seq)
    if len(fasta_seq) == 0:
        fasta_seq = "N"
        qual_seq = "0"
    return [fasta_name, fasta_seq, qual_seq]

def print_tags(input_file):
    """
    Print table of tag names and their count in the data.
    
    """
    tag_dict = {}
    num_seqs = 0
    with  open(input_file, "r") as fasta_file:
        print "Counting tag representation."
        for line in fasta_file.readlines():
            if line.startswith(">"):
                num_seqs += 1
                tag_name = line.split("_")[1]
                tag_dict[tag_name] = tag_dict.setdefault(tag_name, 0) + 1
        tag_list = [x for x in tag_dict.items()]
        tag_list.sort()
        print "Name\tcount"
        for tag in tag_list:
            print tag[0] + "\t" + str("%7i" % tag[1])
        num_noTag = tag_dict["noTag"]
        print "Sequences without tags: %5.2f %%\n" \
              % (100 * float(num_noTag) / num_seqs)

def prepare_sequences(project_name, input_fasta, input_qual,
                output_fasta, output_qual, input_seqs,
                seqs_to_use, find_function):
    """
    Read through a couple of fasta AND fasta.qual files to find tags or caps.
    
    """
    counter = 0
    missing_sequences = 0
    _plateform = platform.system()
    in_fasta = open(input_fasta)
    in_qual = open(input_qual)
    out_fasta = open(output_fasta, "w")
    out_qual = open(output_qual, "w")
    seqs = import_sequences(input_seqs, seqs_to_use)
    seq_number = 0
    fasta_line = in_fasta.readline().strip()
    qual_line = in_qual.readline().strip()
    if fasta_line.startswith(">") and qual_line.startswith(">"):
        fasta_next_name = fasta_line
        fasta_seq = ""
        qual_next_name = qual_line
        qual_seq = []
        seq_number += 1
    while fasta_line != "" and qual_line != "":
        fasta_line = in_fasta.readline().strip()
        qual_line = in_qual.readline().strip()    
        if fasta_line.startswith(">") and qual_line.startswith(">"):
            fasta_name = fasta_next_name
            fasta_next_name = fasta_line
            qual_name = qual_next_name
            qual_next_name = qual_line
            if qual_name == fasta_name and len(qual_seq) == len(fasta_seq):
                if counter % 10 == 0:
                    if _plateform == 'Linux':
                        print "\x0d\033[K" + "%s, treating line: %7i" % \
                              (find_function.__name__, counter),
                        sys.stdout.flush()
                    else:
                        print "%s, treating line: %7i" % \
                              (find_function.__name__, counter)
                counter += 1
                output = find_function(seq_number, fasta_name,
                fasta_seq, qual_seq, seqs, PROJECT_NAME)
                append_fasta(output[0], output[1], out_fasta)
                append_fasta(output[0], output[2], out_qual)
                seq_number += 1
            else:
                print "Error: fasta and qual names and lengths different"
                break
            fasta_seq = ""
            qual_seq = []
        else:
            fasta_seq += fasta_line
            qual_seq += qual_line.split(" ")
    fasta_name = fasta_next_name
    qual_name = qual_next_name
    if qual_name == fasta_name:
        output = find_tag(seq_number, fasta_name,
        fasta_seq, qual_seq, seqs, PROJECT_NAME)
        append_fasta(output[0], output[1], out_fasta)
        append_fasta(output[0], output[2], out_qual)
    else:
        print "Error: fasta and qual names and lengths different"
    in_fasta.close()
    in_qual.close()
    out_fasta.close()
    out_qual.close()
    if _plateform == 'Linux':
        print
    if missing_sequences > 0:
        print missing_sequences, "had a length of zero after treatment"


# Running the program

print "You are using version %s of tag_utils.py\n" % (__version__)
remove_tags = False


# Removing tags and renaming sequences

prepare_sequences(PROJECT_NAME, INPUT_FASTA, INPUT_QUAL,
            OUTPUT_FASTA, OUTPUT_QUAL, INPUT_TAGS,
            TAGS_TO_USE, find_tag); remove_tags = True

if remove_tags == True:
    print_tags(OUTPUT_FASTA)

# Annotating and removing CAP sequences

INPUT_FASTA = "noTag_" + INPUT_FASTA   # Input fasta file
INPUT_QUAL = "noTag_" + INPUT_QUAL     # Input qual file
OUTPUT_FASTA = "noCAP_" + INPUT_FASTA  # Output fasta file
OUTPUT_QUAL = "noCAP_" + INPUT_QUAL    # Output qual file

cap_dict = {}

prepare_sequences(PROJECT_NAME, INPUT_FASTA, INPUT_QUAL,
            OUTPUT_FASTA, OUTPUT_QUAL, INPUT_CAPS,
            CAPS_TO_USE, find_cap)


# Printing diverse informations

for k, v in sorted(cap_dict.iteritems()):
    print k, v


