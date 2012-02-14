#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Cluster sequence IDs into groups of IDs whose sequences blast together.

Input file is the result file (outfmt 0) of fasta file blasted against itself.

Usage:
    %program <input_file> <output_file>"""

import sys
from collections import defaultdict
from copy import deepcopy

try:
    in_file = sys.argv[1]
    out_file = sys.argv[2]
except:
    print __doc__
    sys.exit(0)

in_dict = defaultdict(set)
all_ids = set()
clusters = []
MAX_DEPTH = 100

with open(in_file) as f:
    for line in f:
        all_ids.update(line.strip().split())
        k = line.strip().split()[0]
        in_dict[k].update(line.strip().split())

print "There are", len(all_ids), "unique identifiers"

while len(in_dict.items()) > 0:
    temp = in_dict.popitem()
    items = set(temp[1])
    for d in range(MAX_DEPTH):
        temp_items = deepcopy(items)
        for i in items:
            temp_items.update(in_dict[i])
            in_dict.pop(i)
        items = deepcopy(temp_items)
    clusters.append(items)

clusters.sort(key=len, reverse=True)
    
print "which regroup into", len(clusters), "clusters"
with open(out_file, "w") as f:
    for c in sorted(clusters):
        f.write("\t".join(c) + "\n")

