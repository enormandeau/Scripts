#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Longest fasta sequence for each cluster of contigs

__authors__ = "Eric Normandeau"
__program_name__ = "fasta_cluster_longest"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-09-24"


# Importing modules

import os
import sys
import getopt
import platform
from Bio import SeqIO


# Function definitions

def get_longest(cluster, fasta, output):
    """Output the longest sequence of a set of sequences representing a gene
    """
    seqs = dict()
    clusters = dict()
    fasta_sequences = SeqIO.parse(open(fasta),'fasta')
    with open(cluster) as f:
        for l in f:
            line = l.strip()
            if line != "":
                info = line.split("\t")
                cluster_id = info[0]
                clusters[cluster_id] = ["", "", 0]
                seq_ids = info[1:]
                for i in seq_ids:
                    seqs[i] = cluster_id
    end = False
    while end != True:
        try:
            name = ""
            seq = fasta_sequences.next()
        except:
            end = True
        try:
            name = seq.id
        except:
            print(name, "no info")
        sequence = str(seq.seq)
        seq_length = len(sequence)
        if name in seqs:
            if seq_length > clusters[seqs[name]][2]:
                clusters[seqs[name]] = [seq.id, sequence, seq_length]
    with open(output, "w") as f:
        for c in clusters:
            out = "\n".join([">" + c, clusters[c][1]]) + "\n"
            f.write(out)        

def help():
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)                 User Commands              %s(1)

\033[1mNAME\033[0m
\t%s - Longest fasta sequence for each cluster of contigs

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]    [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tGet the longest sequence of a set of sequences representing a gene

\t%s uses a cluster file. Each line contains the name
\tof the cluster and then the name(s) of the sequence(s) forming that
\tcluster. It also uses a fasta file from which to get the sequences.
\tIt returns a file containing, for each contig, the longest fasta
\tsequence corresponding to one of the sequence names.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-c, --cluster\033[0m
\t\tInput file for cluster sequences info

\t\033[1m-f, --fasta\033[0m
\t\tInput file for fasta sequences

\t\033[1m-o, --output\033[0m
\t\tOutput text file, in tab separated format.

\033[1mAUTHORS\033[0m
\t%s

%s %s                %s               %s(1)
"""%(name, name, name, name, name, __authors__, name, __version__, \
    __revision_date__, name)
    
    if _plateform != 'Windows' and "this is great news":
        print(text)
    else:
        __Windows__ = "This is an abomination"
        remove = ["\033[1m","\033[0m","\033[4m"]
        for i in remove:
            text = text.replace(i, "")
        print(text)
        del(__Windows__) # If only we could...


# fasta_cluster_longest
# With such a clumsy name
# Can you be useful?

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:f:o:", ["help",
            "cluster=", "fasta=", "output="])
    except getopt.GetoptError, e:
        print("Input error. Use -h for help")
        sys.exit(0)
    output_file = None
    header = True
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-c', '--cluster'):
            cluster_file = value
        elif option in ('-f', '--fasta'):
            fasta_file = value
            correspondance_file = value
        elif option in ('-o', '--output'):
            output_file = value
    try:
        with open(cluster_file) as test:
            pass
    except:
        print("Input Error: No cluster file specified or file not found.")
        print("Use -h for help.")
        sys.exit(0)
    try:
        with open(fasta_file) as test:
            pass
    except:
        print("Input Error: No fasta file specified or file not found.")
        print("Use -h for help.")
        sys.exit(0)
    try:
        with open(output_file, "w") as test:
            pass
    except:
        print("Output Error: No output file specified or incorect path.")
        print("Use -h for help.")
        sys.exit(0)

    print("Using version:", __version__, "of", __program_name__)
    print("Last revision:", __revision_date__)
    print("By:", __authors__)
    print
        
    get_longest(cluster_file, fasta_file, output_file)

if __name__ == "__main__":
    main()
