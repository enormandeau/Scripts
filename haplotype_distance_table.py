#!/usr/bin/python
# -*- coding: utf-8 -*-

# First, run the following terminal command:
# awk -F"\t" '{print $1, $NF}' haplotype_finder_output.txt |
#    grep Marker | uniq >markers_for_distance_table.txt

import sys

in_file = sys.argv[1]
out_file = sys.argv[2]

def distance(h1, h2):
    """Find number of differing nucleotides between two haplotypes
    
    """
    d = 0
    for i, n in enumerate(h1):
        if n != h2[i]:
            d += 1
    return d

with open(in_file) as f:
    with open(out_file, "w") as out_f:
        for line in f:
            l = line.strip()
            if l != "":
                marker, haplotypes = l.split()
                out_f.write(marker + "\n")
#                out_f.write(" ".join(haplotypes.split(":")) + "\n")
                for i in haplotypes.split(":"):
                    temp_dist = []
                    for j in haplotypes.split(":"):
                        print i, j
                        temp_dist.append(distance(i, j))
                    out_f.write(" ".join([str(x) for x in temp_dist]) + "\n")

