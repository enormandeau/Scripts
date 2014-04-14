#!/usr/bin/env python

"""Display information about the content of a bamova file.

Usage:
    %program <input_file>"""

import sys

try:
    in_file = sys.argv[1]
except:
    print __doc__
    sys.exit(0)

nmarkers = 0
marker_data = []

with open(in_file) as f:
    for line in f:
        l = line.strip()
        if l.startswith("Marker"):
            nmarkers += 1
            marker_data.append([])
        elif l.startswith("Population"):
            marker_data[-1] += l.split("\t")[2:]

for m in marker_data:
    print len(m)/2, sum([int(x) for x in m])
