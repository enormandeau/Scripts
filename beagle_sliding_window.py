#!/usr/bin/env python3
"""Divide a beagle file in non-overlaping windows of N snps within each chromosome

Usage:
    <program> input_beagle num_snps output_folder

WARNING:
    Writes multiple files in output_folder
"""

# Modules
import gzip
import sys
import os

# Classes
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

def write_to_file(header, snps):

    if len(snps):
        scaffold = snps[0].split()[0].split("_")[0]
        first_pos = snps[0].split()[0].split("_")[1]
        last_pos = snps[-1].split()[0].split("_")[1]
        filename = os.path.join(
                output_folder,
                "window_" + scaffold + "_" + first_pos + "-" + last_pos + "_" + str(len(snps)) + "_snps.beagle.gz"
                )

        with myopen(filename, "wt") as outfile:
            outfile.write(header)

            for snp in snps:
                outfile.write(snp)

# Parse user input
try:
    input_beagle = sys.argv[1]
    num_snps = int(sys.argv[2])
    output_folder = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Variables
snp_bag = []
current_locus = None

# Read and split beagle file
with myopen(input_beagle) as infile:
    for line in infile:

        # Store header line
        if line.startswith("marker"):
            header = line
            continue

        locus = line.strip().split()[0].split("_")[0]

        # Write to file if new snp started
        if locus != current_locus:
            current_locus = locus
            write_to_file(header, snp_bag)
            snp_bag = []

        snp_bag.append(line)

        # Write to file if num_snps
        if len(snp_bag) == num_snps:
            write_to_file(header, snp_bag)
            snp_bag = []

    # Write to file at end of beagle file
    write_to_file(header, snp_bag)
