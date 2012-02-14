#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Reformat Blast2GO GO results for the perch microarray.

Usage:
    %program <microarray_info_file> <blast2go_results> <output_file>"""

import sys

try:
    microarray_file = sys.argv[1] # Microarray information file
    blast2go_file = sys.argv[2]   # Blast2Go result file
    output_file = sys.argv[3]     # Output file
except:
    print __doc__
    sys.exit(0)

array_dict = {}
with open(microarray_file) as f:
    array_header = f.readline().strip().split("\t")

with open(microarray_file) as f:
    for line in f:
        if not line.startswith("Num") and line.strip() != "":
            l = line.strip()
            array_dict[l.split("\t")[14]] = l.split("\t")

with open(blast2go_file) as f:
    go_header = f.readline().strip().split("\t")[0:10]

with open(output_file, "w") as out_f:
    out_f.write("\t".join(go_header + array_header) + "\n")
    with open(blast2go_file) as f:
        for line in f:
            if not line.startswith("GO-ID") and line.strip() != "":
                l = line.strip().split("\t")
                go_info = l[0:10]
                probe_ids = [p.strip() for p in l[10].split(",")]
                out_f.write("\n")
                for probe in probe_ids:
                    out_f.write("\t".join(go_info + array_dict[probe]) + "\n")

