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

added = set()
clusters = []
count = 0

with open(in_file) as f:
    for line in f:
        if line.strip() != "":
            count += 1
            a, b = line.strip().split()
        if not a in added and not b in added:
            clusters.append(set([a,b]))
            added.update([a,b])
        else:
            for c in xrange(len(clusters)):
                if a in clusters[c] or b in clusters[c]:
                    clusters[c].update([a,b])
        added.update([a,b])

print "There are", len(added), "unique identifiers"

for i in list(sorted(range(len(clusters)), reverse=True)):
    for j in range(i):
        if len(clusters[i].intersection(clusters[j])) > 0:
            clusters[j].update(clusters[i])
            clusters[i] = set()

clusters = [x for x in sorted(clusters) if len(x) != 0]
clusters.sort(key=len, reverse=True)
    
print "which regroup into", len(clusters), "clusters"
with open(out_file, "w") as f:
    for c in sorted(clusters):
        f.write("\t".join(c) + "\n")














