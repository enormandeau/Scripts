#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Search sequences that represent the same gene in a blastn result file.

Input file is the result file (outfmt 6) of fasta file blasted against itself.

Usage:
    %program <input_file> <wanted_file> <output_file>"""

import sys
import re

try:
    in_file = sys.argv[1]
    out_file = sys.argv[2]
except:
    print __doc__
    sys.exit(0)

def blast_generator(in_file):
    """Yield one blastplus result at a time
    """
    with open(in_file) as f:
        begin = False
        while begin == False:
            l = f.readline().rstrip()
            if l.find("Query=") > -1:
                query = [l]
                begin = True
        for line in f:
            l = line.rstrip()
            if l.find("Query=") > -1:
                yield query
                query = []
            query.append(l)
        yield query

def find_name(text):
    """Use regex to find the name of the sequence being treated
    """
    contig_search = re.compile("Contig_[0-9]+")
    est_search = re.compile("gi\|[0-9]+")
    geneFP_search = re.compile("geneFP_[0-9]+")
    array_search = re.compile("[a-zA-Z]+[0-9]+")
    name = re.findall(contig_search, text)
    name += re.findall(est_search, text)
    name += re.findall(geneFP_search, text)
    name += re.findall(array_search, text)
    try:
        name = name[0]
    except:
        name = "No_name"
    return name

blast_results = blast_generator(in_file)
my_sum = 0

with open(out_file, "w") as f:
    for res in blast_results:
        name = find_name(res[0])
        results = [x.strip().split()[0] for x in res[1:] if 
                   find_name(x) != "No_name" and not x.startswith(">")
                   and not x.strip().split()[0] == name]
        line = name
        if len(results) == 0:
            my_sum += 1
            line += "\n"
        elif len(results) == 1:
            my_sum += 0
            line += "\t" + "\t".join(results) + "\n"
        else:
            line += "\t" + "\t".join(results) + "\n"
        f.write(line)
print "There are", my_sum, "non-repeated sequences"

