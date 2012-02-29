#!/usr/bin/python
# -*- coding: utf-8 -*-

# Clean fasta DNA sequence alignment for sequencing errors

__authors__ = "Eric Normandeau"
__program_name__ = "alignment_clean"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__copyright__ = "Copyright (c) 2011 Eric Normandeau"
__license__ = "GPLv3"
__revision_date__ = "2011-06-10"


# Importing modules

import os
import sys
import re
import getopt
import platform

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)


# Function definitions

def help():
    """Help attained by typing './program_name.py -h'
    """
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)            User Commands         %s(1)

\033[1mNAME\033[0m
\t%s - Clean fasta DNA sequence alignment for sequencing errors

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTIONS\033[0m]

\033[1mDESCRIPTION\033[0m
\tRemove bad regions/nucleotides from a fasta sequence alignment

\t%s takes a fasta alignment file for input and cleans it.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-i, --input\033[0m
\t\tInput file

\t\033[1m-o, --output\033[0m
\t\tOutput file

\t\033[1m-l, --lefttrim\033[0m
\t\tNumber of nucleotides to trim on the left

\t\033[1m-r, --righttrim\033[0m
\t\tNumber of nucleotides to trim on the right

\t\033[1m-I, --inserts\033[0m
\t\tRemove inserts found at less than a minimum frequency
\t\tNumber between 0 and 1 (eg: 0.01)

\t\033[1m-s, --snps\033[0m
\t\tRemove snp variants found at less than a minimum frequency
\t\tNumber between 0 and 1 (eg: 0.01)

\t\033[1m-p, --partial\033[0m
\t\tRemove partial duplicates
\t\tPatial duplicates are sequences that begin or end with '-'
\t\tcharacters but are otherwise identical to a sequence that
\t\tdoes not start or end with '-' characters

\t\033[1m-d, --duplicates\033[0m
\t\tRemove exact duplicates

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

def short_help(msg):
    """Print short help in case of bad user input
    """
    print msg
    print "Use -h for help"
    sys.exit(0)

def trim_left(names, sequences, lefttrim):
#    print "Trimming left"
    assert lefttrim < len(sequences[0]), "Left trimming by longer than the sequences"
    return names, [s[lefttrim:] for s in sequences]

def trim_right(names, sequences, righttrim):
#    print "Trimming right"
    assert righttrim < len(sequences[0]), "Left trimming by longer than the sequences"
    return names, [s[:-righttrim] for s in sequences]

def remove_inserts(names, sequences, inserts):
#    print "Removing low frequency inserts"
    for i in sorted(range(len(sequences[0])), reverse=True):
        nuc = dict()
        nuc["A"] = nuc["C"] = nuc["G"] = nuc["T"] = nuc["-"] = 0
        for j in range(len(sequences)):
            nuc[sequences[j][i]] += 1
        nonuc = nuc["-"]
        nucs = [nuc["A"], nuc["C"], nuc["G"], nuc["T"]]
        if nonuc > max(nucs) and float(sum(nucs)) / (nonuc + sum(nucs)) < inserts:
            sequences = [s[:i] + s[i+1:] for s in sequences]
    return names, sequences

def remove_snps(names, sequences, snps):
#    print "Removing low frequency snps"
    for i in sorted(range(len(sequences[0])), reverse=True):
        nuc = dict()
        nuc["A"] = nuc["C"] = nuc["G"] = nuc["T"] = nuc["-"] = 0
        for j in range(len(sequences)):
            nuc[sequences[j][i]] += 1
        nuc.pop("-")
        most_frequent = "none"
        maximum = 0
        for n in nuc:
            if nuc[n] > maximum:
                maximum = nuc[n]
                most_frequent = n
        nucs = list(sorted([nuc["A"], nuc["C"], nuc["G"], nuc["T"]], reverse = True))
        if nucs[0] > nucs[1] and float((sum(nucs) - nucs[0])) / sum(nucs) < snps:
            sequences = [s[:i] + most_frequent + s[i+1:] 
                         if s[i] != "-" else s for s in sequences]
    return names, sequences

def remove_partial(names, sequences, partial):
#    print "Removing redundant partial sequences"
    for i in sorted(range(len(sequences)), reverse=True):
        left_pad = len(re.findall("^-*", sequences[i])[0])
        right_pad = len(re.findall("-*$", sequences[i])[0])
        if left_pad > 0:
            temp_sequences = [s[left_pad:] for s in sequences]
            set_sequences = set(temp_sequences[:i] + temp_sequences[i+1:])
            if temp_sequences[i] in set_sequences:
                names = names[:i] + names[i+1:]
                sequences = sequences[:i] + sequences[i+1:]
        if right_pad > 0:
            temp_sequences = [s[:right_pad] for s in sequences]
            set_sequences = set(temp_sequences[:i] + temp_sequences[i+1:])
            if temp_sequences[i] in set_sequences:
                names = names[:i] + names[i+1:]
                sequences = sequences[:i] + sequences[i+1:]
    return names, sequences

def remove_duplicates(names, sequences):
#    print "Removing duplicate sequences"
    unique_sequences = set()
    for i in sorted(xrange(len(sequences)), reverse=True):
        seq = sequences[i]
        name = names[i]
        if seq not in unique_sequences:
            unique_sequences.add(seq)
        else:
            names = names[:i] + names[i+1:]
            sequences = sequences[:i] + sequences[i+1:]
    return names, sequences

def output_sequences(names, sequences, output_file):
    with open(output_file, "w") as f:
        for i, name in enumerate(names):
            f.write(">" + name + "\n" + sequences[i] + "\n")


# Does alignment_clean
# neatify your sequences
# up to your standards?


# The program itself

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:l:r:I:s:pd", ["help",
            "input=", "output=", "lefttrim=", "righttrim=", "inserts=",
            "snps=", "partial", "duplicate"])
    except getopt.GetoptError, e:
        short_help("Input error. Use -h for help")
    lefttrim = 0
    righttrim = 0
    inserts = 0
    snps = 0
    partial = False
    duplicate = False
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_file = value
            try:
                with open(input_file) as test:
                    pass
            except:
                short_help("Input Error: No input file specified or file not found.")
        elif option in ('-o', '--output'):
            output_file = value
            try:
                with open(output_file, "w") as test:
                    pass
            except:
                short_help("Output Error: No output file specified or incorect path.")
        elif option in ('-l', '--lefttrim'):
            try:
                lefttrim = int(value)
                assert lefttrim >= 0
            except:
                short_help("Positive integer needed for 'lefttrim' option")
        elif option in ('-r', '--righttrim'):
            try:
                righttrim = int(value)
                assert righttrim >= 0
            except:
                short_help("Positive integer needed for 'righttrim' option")
        elif option in ('-I', '--inserts'):
            try:
                inserts = float(value)
                assert 0 <= inserts <= 1
            except:
                short_help("Number between 0 and 1 needed for 'inserts' option")
        elif option in ('-s', '--snps'):
            try:
                snps = float(value)
                assert 0 <= snps <= 1
            except:
                short_help("Number between 0 and 1 needed for 'snps' option")
        elif option in ('-p', '--partial'):
            partial = True
        elif option in ('-d', '--duplicates'):
            duplicate = True

#    print __program_name__, __version__
#    print __copyright__
#    print

 
    fasta_sequences = SeqIO.parse(open(input_file),'fasta')
    names = []
    sequences = []
    
    for seq in fasta_sequences:
        names.append(seq.id)
        sequences.append(seq.seq.tostring())
    
#    print "  -", len(sequences[0]), len(sequences)
    if lefttrim > 0:
        names, sequences = trim_left(names, sequences, lefttrim)
    
#    print "  -", len(sequences[0]), len(sequences)
    if righttrim > 0:
        names, sequences = trim_right(names, sequences, righttrim)

#    print "  -", len(sequences[0]), len(sequences)
    names, sequences = remove_inserts(names, sequences, inserts)
    
#    print "  -", len(sequences[0]), len(sequences)
    names, sequences = remove_snps(names, sequences, snps)
    
#    print "  -", len(sequences[0]), len(sequences)
    if partial == True:
        names, sequences = remove_partial(names, sequences, partial)
    
#    print "  -", len(sequences[0]), len(sequences)
    if duplicate == True:
        names, sequences = remove_duplicates(names, sequences)

#    print "  -", len(sequences[0]), len(sequences)
    output_sequences(names, sequences, output_file)
    
#    print "Done"
    

