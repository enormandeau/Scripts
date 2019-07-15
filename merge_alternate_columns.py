#!/usr/bin/env python3
"""Merger two files by alternating columns from file 1 and 2

Usage:
    <program> file1 file2 output_file
"""

# Modules
import sys

# Parse user input
try:
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Open both files
f1 = open(file1)
f2 = open(file2)

# Write columns to output file
with open(output_file, "w") as outfile:
    while True:
        l1 = f1.readline()
        l2 = f2.readline()

        if not l1:
            sys.exit()

        columns1 = l1.strip().split("\t")
        columns2 = l2.strip().split("\t")

        # Create new line
        new_line = []

        for i, v1 in enumerate(columns1):
            v2 = columns2[i]
            new_line.append(v1)
            new_line.append(v2)
        
        # Write to file
        outfile.write("\t".join(new_line) + "\n")
