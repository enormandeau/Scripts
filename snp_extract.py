#!/usr/bin/env python

"""Extract wanted SNPs from a file containing information about many SNPs.

Input file:
Tab separated, the 2 first columns are 'contig_name' and 'snp_position'

Unwanted SNPs file:
Tab separated, 2 columns: 'contig_name' and 'snp_position' in the same
format as the input file

Usage:
    %program <input_file> <remove_file> <output_file>"""

import sys

try:
    in_snps = open(sys.argv[1], "rU")
    in_wanted = open(sys.argv[2], "rU")
except:
    print __doc__
    sys.exit(0)

wanted = set(["_".join(x.strip().split("\t")[0:2]) for x in in_wanted])
snps = (x for x in in_snps)

with open(sys.argv[3], "w") as out_file:
    for snp in snps:
        if "_".join(snp.strip().split("\t")[0:2]) in wanted:
            out_file.write(snp)

