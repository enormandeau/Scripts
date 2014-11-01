#!/usr/bin/env python
"""Remove genotypes of individuals in populations with few genotyped individuals.

Usage:
    vcf_remove_genotypes.py input_vcf threshold output_vcf

input_vcf = batch_1.vcf (output from Stacks)
threshold = min number of individuals (0 to 100)
#### threshold = max percent of missing individuals (0 to 100)
output_vcf = filename for output vcf
"""

# Version 1.0

# Importing modules
from collections import defaultdict
import sys
import re

# Defining functions
def population_indexes(pops):
    """From list of population names, return dictionary with each population
    name containing the index of the populations.
    """
    d = defaultdict(list)
    for i, p in enumerate(pops):
        d[p].append(i + 9)
    return d

def treat_line(line, popind, threshold):
    repladement_geno = "./.:0:.,.,."
    null_geno = re.compile("\./\.:[0-9]+:\.,\.,\.")
    line_split = line.split("\t")
    for p in popind:
        results = []
        for i in popind[p]:
            results.append(line_split[i])
        num_ok = len([x for x in results if not null_geno.match(x)])
        percent = 100. * num_ok / len(results)
        if num_ok < threshold: ### Integer version
        # if percent < threshold: ### Percent version
            for i in popind[p]:
                line_split[i] = repladement_geno
    return "\t".join(line_split)

# Main
if __name__ == '__main__':

    # Parsing user input
    try:
        input_vcf = sys.argv[1]
        threshold = float(sys.argv[2])
        output_vcf = sys.argv[3]
    except:
        print __doc__
        sys.exit(1)

    if not (0 <= threshold <= 100):
        print "  **  Threshold must be between 0 and 100  **"
        sys.exit(1)

    # Reading input_vcf
    with open(output_vcf, "w") as fout:
        with open(input_vcf) as f:
            for line in f:
                line = line.strip()
                if line.startswith("#CHROM"):
                    header = line.strip().split("\t")[9:]
                    pops = [x.split("_")[0] for x in header]
                    popind = population_indexes(pops)
                    fout.write(line + "\n")
                elif line.startswith("#"):
                    fout.write(line + "\n")
                else:
                    new_line = treat_line(line, popind, threshold)
                    fout.write(new_line + "\n")

