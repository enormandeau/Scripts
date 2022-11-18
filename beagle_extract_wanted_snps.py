#!/usr/bin/env python3
"""Extract wanted SNPs from beagle file

Usage
    <program> input_beagle wanted_file output_beagle

wanted_file has two tabulation-separated columns with chrom and pos
"""

# Modules
import gzip
import sys

# Functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)
    else:
        return open(_file, mode=mode)

# Parsing user input
try:
    input_beagle = sys.argv[1]
    wanted_file  = sys.argv[2]
    output_beagle = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Load wanted SNP infos in set
with myopen(wanted_file) as snpfile:
    wanted_snps = set(["_".join(x.strip().split()) for x in snpfile.readlines()])

# Read beagle and filter
with myopen(input_beagle) as infile:
    with myopen(output_beagle,"wt") as outfile:

        # Keep header
        outfile.write(infile.readline())

        for line in infile:
            l = line.strip().split("\t")

            if l[0] in wanted_snps:
                outfile.write(line)
