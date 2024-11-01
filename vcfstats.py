#!/usr/bin/env python3
"""Report statistics about STACKS VCF

Usage:
    <program> input_vcf
"""

# Modules
import statistics
import gzip
import sys

# Functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

# Parse user input
try:
    input_vcf = sys.argv[1]
except:
    print(__doc__)
    sys.exit(1)

# Report on:
# --
# VCF name (input_vcf)
# STACKS version (version)
# File date (date)
# Number of samples (num_samples)
# Number of SNPs
# Proportion of missing
# Median coverage

# Extract stats
num_geno = 0
num_miss = 0
num_snps = 0
coverages = []

print(f"{input_vcf.split('/')[-1]}")
print("--")

with myopen(input_vcf, "rt") as infile:
    for line in infile:
        l = line.strip().split("\t")

        if not line.startswith("#"):
            data = l[9:]
            num_snps += 1
            num_geno += num_samples
            num_miss += len([x for x in data if "./." in x])
            coverages += [int(x.split(":")[1]) for x in data if x != "./." and x.split(":")[1] != "0"]

        elif "##fileDate=" in line:
            date = l[0].split("=")[1]
            date = date[:4] + "-" + date[4: 6] + "-" + date[6:]
            print(f"Date: {date}")

        elif "##source=" in line:
            version = l[0].split("=")[1].replace('"', '')
            print(f"Version: {version}")
        
        elif l[0] == "#CHROM":
            num_samples = len(l[9:])

print(f"Samples: {num_samples}")
print(f"SNPs: {num_snps}")
print(f"Missing: {round(100 * num_miss / num_geno, 2)}%")
print(f"Coverage mean: {round(statistics.mean(coverages), 2)}")
print(f"Coverage median: {statistics.median(coverages)}")
print(f"Coverage mode: {statistics.mode(coverages)}")
print()
